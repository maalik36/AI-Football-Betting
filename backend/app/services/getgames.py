import csv
from google import genai
from typing import Dict, Any, List
import json
import os
from datetime import datetime

def parse_csv_games(csv_data: str) -> List[Dict[str, Any]]:
    """Parse CSV data into a list of games"""
    games = []
    reader = csv.DictReader(csv_data.splitlines())
    for row in reader:
        if row.get('Game'):  # Make sure it's a game row
            # Parse the game string which is in format "Team1 at Team2" or "Team1 vs Team2"
            game_parts = row['Game'].replace(' at ', ' vs ').split(' vs ')
            if len(game_parts) == 2:
                home_team = game_parts[1]  # The team after "at" or "vs" is home
                away_team = game_parts[0]  # The team before is away
                
                # Clean up the time format
                time = row.get('Local Time', '').replace('p', ' PM').replace('a', ' AM')
                if '(' in time:  # Remove timezone info for simplicity
                    time = time.split('(')[0].strip()
                
                games.append({
                    "home_team": home_team,
                    "away_team": away_team,
                    "date": row.get('Date', ''),
                    "time": time,
                    "competition": "NFL 2025"  # Since all games are NFL
                })
    return games

async def enhance_games_data(client: genai.Client, games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enhance games data with team logos and descriptions"""
    try:
        # Create a more structured prompt for better results
        prompt = """
        You are a sports data enhancer. Given these NFL matches:
        {}
        
        Generate enhanced data for each match including:
        1. Team logos (using NFL's CDN)
        2. A brief description
        3. Key players
        4. Rivalry history
        
        Format your response EXACTLY as a JSON object with this structure:
        {{
            "matches": [
                {{
                    "original_data": <input match object>,
                    "home_team_logo": "https://static.www.nfl.com/t_headshot_desktop/f_auto/league/api/clubs/logos/<team>",
                    "away_team_logo": "https://static.www.nfl.com/t_headshot_desktop/f_auto/league/api/clubs/logos/<team>",
                    "match_description": "string",
                    "key_players": ["string"],
                    "rivalry_history": "string"
                }}
            ]
        }}
        
        ONLY respond with the JSON. No other text.
        """.format(json.dumps(games, indent=2))

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            generation_config={
                "temperature": 0.3,
                "candidate_count": 1,
                "stop_sequences": ["}}}"],
                "max_output_tokens": 2048,
            }
        )
        
        response_text = response.text.strip()
        print("Gemini raw response:", response_text)  # Debug log
        
        try:
            enhanced_data = json.loads(response_text)
            if "matches" in enhanced_data and len(enhanced_data["matches"]) > 0:
                return enhanced_data["matches"]
        except json.JSONDecodeError as e:
            print(f"Failed to parse Gemini response: {e}")
        
        # If we get here, create default enhanced data
        team_logos = {
            "Eagles": "PHI",
            "Cowboys": "DAL",
            "Chiefs": "KC",
            "Chargers": "LAC",
            "Falcons": "ATL",
            "Buccaneers": "TB",
            "Browns": "CLE",
            "Bengals": "CIN",
            "Colts": "IND",
            "Dolphins": "MIA"
        }
        
        def get_team_code(team_name: str) -> str:
            for key, value in team_logos.items():
                if key in team_name:
                    return value
            return "NFL"  # Default fallback
        
        return [
            {
                "original_data": game,
                "home_team_logo": f"https://static.www.nfl.com/t_headshot_desktop/f_auto/league/api/clubs/logos/{get_team_code(game['home_team'])}",
                "away_team_logo": f"https://static.www.nfl.com/t_headshot_desktop/f_auto/league/api/clubs/logos/{get_team_code(game['away_team'])}",
                "match_description": f"Week 1 NFL matchup between {game['home_team']} and {game['away_team']}. Both teams looking to start their 2025 season with a victory.",
                "key_players": ["Loading team rosters..."],
                "rivalry_history": f"Historic matchup between {game['home_team']} and {game['away_team']} in the NFL."
            }
            for game in games
        ]
        
    except Exception as e:
        print(f"Error in enhance_games_data: {str(e)}")
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

        # Parse CSV data
        games = parse_csv_games(csv_data)
        if not games:
            raise ValueError("No games found in CSV file")
            
        # Get next 5 games
        next_games = games[:5]  # For simplicity, just take first 5
        
        # Convert games to JSON string for raw_games
        games_json = json.dumps(next_games, indent=2)
            
        enhanced_matches = await enhance_games_data(client, next_games)

        return {
            "raw_games": games_json,
            "enhanced_matches": enhanced_matches,
            "count": len(next_games),
            "source": "CSV + Gemini AI"
        }
        
    except Exception as e:
        error_msg = str(e)
        if "API key not valid" in error_msg.lower():
            error_msg = "Invalid Gemini API key"
        elif "quota exceeded" in error_msg.lower():
            error_msg = "Gemini API quota exceeded"
        return {"error": f"Failed to get next games: {error_msg}"}
