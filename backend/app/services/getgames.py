import csv
from typing import Dict, Any, List
import json
import os
from datetime import datetime
from .nfl_api_service import nfl_api

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
                    "competition": "NFL 2025",  # Since all games are NFL
                    "season": row.get("season", "")
                })
    return games

async def enhance_games_data(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enhance games data with team info from NFL API"""
    enhanced_matches = []
    
    for game in games:
        # Get team information from NFL API
        home_team_info = await nfl_api.get_team_info(game["home_team"])
        away_team_info = await nfl_api.get_team_info(game["away_team"])
        
        # Get team stats
        home_team_stats = await nfl_api.get_team_stats(game["home_team"])
        away_team_stats = await nfl_api.get_team_stats(game["away_team"])
        
        # Create enhanced match data
        enhanced_match = {
            "original_data": game,
            "home_team_logo": home_team_info.get('logo_url'),
            "away_team_logo": away_team_info.get('logo_url'),
            "match_description": generate_match_description(
                home_team_info,
                away_team_info,
                game["date"],
                game["time"]
            ),
            "key_players": ["Star players to be announced"],
            "rivalry_history": generate_rivalry_description(home_team_stats, away_team_stats),
            "home_team_info": {
                **home_team_info,
                **home_team_stats
            },
            "away_team_info": {
                **away_team_info,
                **away_team_stats
            }
        }
        enhanced_matches.append(enhanced_match)
    
    return enhanced_matches

def generate_match_description(home_info: Dict[str, Any], away_info: Dict[str, Any], date: str, time: str) -> str:
    """Generate a description for the match"""
    home_name = home_info.get('name', 'Unknown Team')
    away_name = away_info.get('name', 'Unknown Team')
    home_location = home_info.get('location', '')
    stadium = home_info.get('stadium', 'Unknown Stadium')
    
    return f"{home_name} hosts {away_name} at {stadium} on {date} at {time}. A matchup between NFL teams, featuring {home_location} against the visiting {away_name}."

def generate_rivalry_description(home_info: Dict[str, Any], away_info: Dict[str, Any]) -> str:
    """Generate a description of the rivalry between the teams"""
    home_name = home_info.get('name', 'Unknown Team')
    away_name = away_info.get('name', 'Unknown Team')
    home_division = home_info.get('division', 'Unknown')
    away_division = away_info.get('division', 'Unknown')
    
    if home_division == away_division and home_division != 'Unknown':
        return f"Divisional rivalry matchup between {home_name} and {away_name} in the {home_division} division."
    else:
        return f"NFL matchup between {home_name} and {away_name}."

def get_team_logo(team_name: str) -> str:
    """Get the team logo URL based on team name"""
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
    
    # Get team code
    team_code = "NFL"  # Default fallback
    for key, value in team_logos.items():
        if key in team_name:
            team_code = value
            break
    
    return f"https://static.www.nfl.com/t_headshot_desktop/f_auto/league/api/clubs/logos/{team_code}"

def create_default_enhanced_data(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create default enhanced data when Gemini fails"""
    default_descriptions = {
        "Eagles": "Known for their strong offensive line and passionate fanbase",
        "Cowboys": "America's Team with a rich history of success",
        "Chiefs": "High-powered offense led by Patrick Mahomes",
        "Chargers": "Dynamic team with explosive playmakers",
        "Falcons": "Looking to rebuild and return to playoff contention",
        "Buccaneers": "Strong defensive unit with playoff aspirations",
        "Browns": "Built around a strong running game and defense",
        "Bengals": "Young and talented team with explosive offense",
        "Colts": "Team in transition with promising young talent",
        "Dolphins": "Fast-paced offense with dynamic playmakers"
    }
    
    def get_team_description(team_name: str) -> str:
        for key, desc in default_descriptions.items():
            if key in team_name:
                return desc
        return "Looking to make their mark in the NFL"
    
    return [
        {
            "original_data": game,
            "home_team_logo": get_team_logo(game["home_team"]),
            "away_team_logo": get_team_logo(game["away_team"]),
            "match_description": f"Week 1 matchup: {get_team_description(game['home_team'])} hosting {get_team_description(game['away_team'])}",
            "key_players": ["Star players to be announced"],
            "rivalry_history": f"Historic NFL matchup between {game['home_team']} and {game['away_team']}"
        }
        for game in games
    ]

async def getnextgames() -> Dict[str, Any]:
    """Get next 5 games with enhanced data"""
    try:
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
            
        enhanced_matches = await enhance_games_data(next_games)

        return {
            "raw_games": games_json,
            "enhanced_matches": enhanced_matches,
            "source": "CSV + RapidAPI NFL Data"
        }
        
    except Exception as e:
        print(f"Error in getnextgames: {str(e)}")
        raise
