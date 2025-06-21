from typing import Dict, Any
from app.services.vertex_client import VertexAIClient

class FootballAgent:
    def __init__(self):
        self.vertex_client = VertexAIClient()
    
    async def analyze_match(self, home_team: str, away_team: str, match_data: str = "") -> Dict[str, Any]:
        """AI agent analyzes a match using Vertex AI"""
        prompt = f"""
        As a football betting expert, analyze this match:
        
        Home Team: {home_team}
        Away Team: {away_team}
        
        {f"Match Data: {match_data}" if match_data else ""}
        
        Provide analysis in JSON format:
        {{
            "prediction": "HOME_WIN/DRAW/AWAY_WIN",
            "confidence": 0.XX,
            "reasoning": "detailed explanation",
            "key_factors": ["factor1", "factor2"],
            "risk_level": "LOW/MEDIUM/HIGH"
        }}
        """
        
        try:
            response = await self.vertex_client.generate_json(prompt)
            return response
        except Exception as e:
            return {"error": str(e)}
    
    async def get_betting_recommendation(self, home_team: str, away_team: str, match_data: str = "") -> Dict[str, Any]:
        """AI agent provides betting recommendations"""
        match_analysis = await self.analyze_match(home_team, away_team, match_data)
        
        if "error" in match_analysis:
            return match_analysis
        
        prompt = f"""
        Based on this match analysis: {match_analysis}
        
        Provide betting recommendations in JSON:
        {{
            "recommended_bet": "HOME_WIN/DRAW/AWAY_WIN/NO_BET",
            "bet_amount": "SMALL/MEDIUM/LARGE",
            "odds_threshold": "minimum odds to bet",
            "explanation": "why this bet is recommended"
        }}
        """
        
        try:
            betting_advice = await self.vertex_client.generate_json(prompt)
            return {
                "match_analysis": match_analysis,
                "betting_advice": betting_advice
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_team_performance(self, team_name: str, performance_data: str = "") -> Dict[str, Any]:
        """AI agent analyzes team performance"""
        prompt = f"""
        Analyze the performance of {team_name}:
        
        {f"Performance Data: {performance_data}" if performance_data else ""}
        
        Provide analysis in JSON format:
        {{
            "form_rating": "EXCELLENT/GOOD/AVERAGE/POOR",
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "key_players": ["player1", "player2"],
            "recent_trend": "IMPROVING/STABLE/DECLINING"
        }}
        """
        
        try:
            return await self.vertex_client.generate_json(prompt)
        except Exception as e:
            return {"error": str(e)} 