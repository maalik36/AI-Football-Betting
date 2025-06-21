import csv
from google import genai
from typing import Dict, Any, List
import json
import os

async def enhance_games_data(client: genai.Client, games_json: str) -> List[Dict[str, Any]]:
    """Enhance games data with team logos and descriptions"""
    try:
        games = json.loads(games_json)
        
        # Get team logos and descriptions
        prompt = f"""
        For these football matches: {json.dumps(games)}
        
        For each match, I need:
        1. Team logos (use official team website URLs if possible)
        2. A brief, exciting description of the matchup
        3. Key players to watch
        4. Historical context of the rivalry (if any)
        
        Return the data in this exact JSON format:
        {{
            "matches": [
                {{
                    "original_data": <original match object>,
                    "home_team_logo": "url",
                    "away_team_logo": "url",
                    "match_description": "exciting description",
                    "key_players": ["player1", "player2"],
                    "rivalry_history": "brief history or null if no significant rivalry"
                }}
            ]
        }}
        
        Make sure all URLs are real and accessible. If you can't find an official logo URL, use a placeholder like 'https://via.placeholder.com/150?text=TEAM_NAME'.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        enhanced_data = json.loads(response.text.strip())
        return enhanced_data["matches"]
        
    except Exception as e:
        print(f"Error enhancing games data: {str(e)}")
        return []

async def getnextgames(key: str) -> Dict[str, Any]:
    """Get next 5 games using Gemini AI"""
    try:
        if not key:
            raise ValueError("GEMINI_API_KEY is not set in environment variables")
            
        client = genai.Client(api_key=key)
        
        csv_path = "games.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Required file {csv_path} not found")
            
        with open(csv_path, "r") as f:
            csv_data = f.read()

        if not csv_data.strip():
            raise ValueError(f"File {csv_path} is empty")

        prompt = f"""
        {csv_data}

        Please output the next 5 games, based on the current date, and assuming that all these games are in the year 2025.
        Format each game with home team, away team, date, time, and competition/league.
        Return as a JSON array of objects with these exact fields: home_team, away_team, date, time, competition
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        games_json = response.text.strip()
        if not games_json:
            raise ValueError("Gemini API returned empty response")
            
        enhanced_matches = await enhance_games_data(client, games_json)

        return {
            "raw_games": games_json,  # Keep the original JSON
            "enhanced_matches": enhanced_matches,  # Add enhanced data
            "count": 5,
            "source": "CSV + Gemini AI"
        }
        
    except Exception as e:
        error_msg = str(e)
        if "API key not valid" in error_msg.lower():
            error_msg = "Invalid Gemini API key"
        elif "quota exceeded" in error_msg.lower():
            error_msg = "Gemini API quota exceeded"
        return {"error": f"Failed to get next games: {error_msg}"}
