import pandas as pd
from typing import Dict, List, Optional

class StatsService:
    def __init__(self, csv_path: str = "SeasonsData.csv"):
        self.csv_path = csv_path
    
    def get_team_stats(self, team_name: str) -> Dict:
        """Get basic stats for a team from CSV"""
        try:
            df = pd.read_csv(self.csv_path)
            team_data = df[df['HomeTeam'] == team_name]
            return {
                "team": team_name,
                "total_matches": len(team_data),
                "wins": len(team_data[team_data['FTR'] == 'H']),
                "draws": len(team_data[team_data['FTR'] == 'D']),
                "losses": len(team_data[team_data['FTR'] == 'A'])
            }
        except Exception as e:
            return {"error": f"Failed to get stats: {str(e)}"}
    
    def get_team_form(self, team_name: str, last_n: int = 5) -> List[str]:
        """Get last N results for a team"""
        try:
            df = pd.read_csv(self.csv_path)
            team_data = df[df['HomeTeam'] == team_name].tail(last_n)
            return team_data['FTR'].tolist()
        except Exception as e:
            return [] 