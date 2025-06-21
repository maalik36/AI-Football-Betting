import aiohttp
from typing import Dict, Any, List
import json
from app.config.settings import settings

class NFLApiService:
    def __init__(self):
        self.base_url = "https://nfl-api-data.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": "13c102ca59msh5fbfaa62e3be4fap1c10d8jsn35245a387509",
            "X-RapidAPI-Host": "nfl-api-data.p.rapidapi.com"
        }
        self._teams_cache = None
        
    async def _get_all_teams(self) -> List[Dict[str, Any]]:
        """Get all teams data and cache it"""
        if self._teams_cache is None:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.base_url}/nfl-team-listing/v1/data",
                        headers=self.headers
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            self._teams_cache = data
                            return data
                        else:
                            print(f"Error fetching teams: {response.status}")
                            return []
            except Exception as e:
                print(f"Error in _get_all_teams: {str(e)}")
                return []
        return self._teams_cache

    async def get_team_info(self, team_name: str) -> Dict[str, Any]:
        """Get team information from NFL API"""
        try:
            teams = await self._get_all_teams()
            for team_data in teams:
                team = team_data.get('team', {})
                if team.get('displayName', '').lower() == team_name.lower() or \
                   team.get('name', '').lower() == team_name.lower():
                    # Get the default logo URL
                    logo_url = None
                    for logo in team.get('logos', []):
                        if 'default' in logo.get('rel', []):
                            logo_url = logo.get('href')
                            break
                    
                    return {
                        'name': team.get('displayName'),
                        'abbreviation': team.get('abbreviation'),
                        'logo_url': logo_url,
                        'location': team.get('location'),
                        'color': f"#{team.get('color')}" if team.get('color') else None,
                        'alternate_color': f"#{team.get('alternateColor')}" if team.get('alternateColor') else None
                    }
            
            print(f"Team not found: {team_name}")
            return {
                'name': team_name,
                'abbreviation': '',
                'logo_url': None,
                'location': '',
                'color': None,
                'alternate_color': None
            }
            
        except Exception as e:
            print(f"Error in get_team_info: {str(e)}")
            return {
                'name': team_name,
                'abbreviation': '',
                'logo_url': None,
                'location': '',
                'color': None,
                'alternate_color': None
            }

    async def get_team_stats(self, team_name: str) -> Dict[str, Any]:
        """Get team statistics from NFL API"""
        try:
            teams = await self._get_all_teams()
            for team_data in teams:
                team = team_data.get('team', {})
                if team.get('displayName', '').lower() == team_name.lower() or \
                   team.get('name', '').lower() == team_name.lower():
                    return {
                        'name': team.get('displayName'),
                        'location': team.get('location'),
                        'division': team.get('division', 'Unknown'),
                        'conference': team.get('conference', 'Unknown'),
                        'stadium': team.get('venue', {}).get('fullName', 'Unknown Stadium')
                    }
            return {}
        except Exception as e:
            print(f"Error in get_team_stats: {str(e)}")
            return {}

    async def get_team_roster(self, team_key: str) -> List[Dict[str, Any]]:
        """Get team roster from NFL API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/nfl-team-roster/v1/data",
                    headers=self.headers,
                    params={"team_key": team_key}
                ) as response:
                    if response.status == 200:
                        players = await response.json()
                        return [
                            {
                                'name': player.get('player_name'),
                                'position': player.get('player_position'),
                                'jersey_number': player.get('player_jersey_number'),
                                'experience': player.get('player_experience'),
                                'college': player.get('player_college'),
                                'photo_url': player.get('player_photo_url'),
                                'status': player.get('player_status')
                            }
                            for player in players
                            if player.get('player_status') == 'Active'  # Only active players
                        ][:5]  # Return top 5 players
        except Exception as e:
            print(f"Error fetching team roster: {str(e)}")
        return []

# Create a singleton instance
nfl_api = NFLApiService() 