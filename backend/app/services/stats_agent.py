from typing import Dict, List, Any
import pandas as pd
from app.services.vertex_client import VertexAIClient
from app.services.gemini_client import GeminiClient

class StatsAgent:
    def __init__(self):
        self.vertex_client = VertexAIClient()
        self.gemini_client = GeminiClient()
        self.csv_path = "SeasonsData.csv"
    
    def _load_csv_data(self) -> pd.DataFrame:
        """Load CSV data"""
        return pd.read_csv(self.csv_path)
    
    async def get_team_stats(self, team_name: str) -> Dict[str, Any]:
        """AI agent extracts and analyzes team stats from CSV"""
        try:
            df = self._load_csv_data()
            
            # Get team data
            home_games = df[df['HomeTeam'] == team_name]
            away_games = df[df['AwayTeam'] == team_name]
            
            # Basic stats
            stats = {
                "team": team_name,
                "total_matches": len(home_games) + len(away_games),
                "home_wins": len(home_games[home_games['FTR'] == 'H']),
                "home_draws": len(home_games[home_games['FTR'] == 'D']),
                "home_losses": len(home_games[home_games['FTR'] == 'A']),
                "away_wins": len(away_games[away_games['FTR'] == 'A']),
                "away_draws": len(away_games[away_games['FTR'] == 'D']),
                "away_losses": len(away_games[away_games['FTR'] == 'H']),
                "recent_form": self._get_recent_form(df, team_name, 5)
            }
            
            # Use AI to analyze the stats
            analysis_prompt = f"""
            Analyze these team statistics for {team_name}:
            {stats}
            
            Provide analysis in JSON format:
            {{
                "form_rating": "EXCELLENT/GOOD/AVERAGE/POOR",
                "home_strength": "STRONG/MODERATE/WEAK",
                "away_strength": "STRONG/MODERATE/WEAK",
                "key_insights": ["insight1", "insight2"],
                "trend": "IMPROVING/STABLE/DECLINING"
            }}
            """
            
            ai_analysis = await self.vertex_client.generate_json(analysis_prompt)
            
            return {
                "raw_stats": stats,
                "ai_analysis": ai_analysis
            }
            
        except Exception as e:
            return {"error": f"Failed to get team stats: {str(e)}"}
    
    def _get_recent_form(self, df: pd.DataFrame, team_name: str, last_n: int) -> List[str]:
        """Get recent form for a team"""
        home_games = df[df['HomeTeam'] == team_name].tail(last_n)
        away_games = df[df['AwayTeam'] == team_name].tail(last_n)
        
        form = []
        for _, game in home_games.iterrows():
            if game['FTR'] == 'H':
                form.append('W')
            elif game['FTR'] == 'D':
                form.append('D')
            else:
                form.append('L')
        
        for _, game in away_games.iterrows():
            if game['FTR'] == 'A':
                form.append('W')
            elif game['FTR'] == 'D':
                form.append('D')
            else:
                form.append('L')
        
        return form[-last_n:]
    
    async def compare_teams(self, team1: str, team2: str) -> Dict[str, Any]:
        """AI agent compares two teams using CSV data"""
        team1_stats = await self.get_team_stats(team1)
        team2_stats = await self.get_team_stats(team2)
        
        if "error" in team1_stats or "error" in team2_stats:
            return {"error": "Failed to get team stats"}
        
        comparison_prompt = f"""
        Compare these two teams:
        
        {team1}: {team1_stats['raw_stats']}
        {team2}: {team2_stats['raw_stats']}
        
        Provide comparison in JSON format:
        {{
            "stronger_team": "team_name",
            "key_differences": ["difference1", "difference2"],
            "head_to_head_advantage": "team_name",
            "prediction_factors": ["factor1", "factor2"]
        }}
        """
        
        try:
            comparison = await self.gemini_client.generate_json(comparison_prompt)
            return {
                "team1_stats": team1_stats,
                "team2_stats": team2_stats,
                "comparison": comparison
            }
        except Exception as e:
            return {"error": str(e)} 