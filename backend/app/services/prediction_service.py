from app.services.gemini_client import GeminiClient

class PredictionService:
    def __init__(self):
        self.gemini_client = GeminiClient()
    
    async def get_simple_prediction(self, match_data: str) -> str:
        """Get simple prediction (HOME_WIN/DRAW/AWAY_WIN)"""
        prompt = f"""
        Analyze this football match and provide betting prediction:
        {match_data}
        
        Return only: HOME_WIN, DRAW, or AWAY_WIN
        """
        
        try:
            return await self.gemini_client.generate_content(prompt)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def get_detailed_prediction(self, home_team: str, away_team: str, league: str) -> dict:
        """Get detailed match analysis with probabilities"""
        prompt = f"""
        Analyze this football match:
        Home Team: {home_team}
        Away Team: {away_team}
        League: {league}
        
        Return JSON format:
        {{
            "home_win_prob": 0.XX,
            "draw_prob": 0.XX,
            "away_win_prob": 0.XX,
            "confidence": "HIGH/MEDIUM/LOW",
            "reasoning": "brief explanation"
        }}
        """
        
        return await self.gemini_client.generate_json(prompt)
    
    async def analyze_team_form(self, team_name: str) -> dict:
        """Analyze team's recent form"""
        prompt = f"""
        Analyze the recent form and performance of {team_name}:
        
        Return JSON format:
        {{
            "form_rating": "GOOD/AVERAGE/POOR",
            "recent_results": ["W", "L", "D", ...],
            "key_players": ["player1", "player2"],
            "injuries": ["player1", "player2"],
            "analysis": "brief analysis"
        }}
        """
        
        return await self.gemini_client.generate_json(prompt) 