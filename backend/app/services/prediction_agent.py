from typing import Dict, Any
from app.services.vertex_client import VertexAIClient
from app.services.gemini_client import GeminiClient
from app.services.stats_agent import StatsAgent

class PredictionAgent:
    def __init__(self):
        self.vertex_client = VertexAIClient()
        self.gemini_client = GeminiClient()
        self.stats_agent = StatsAgent()
    
    async def predict_match(self, home_team: str, away_team: str, match_data: str = "") -> Dict[str, Any]:
        """AI agent predicts match outcome using multiple AI models"""
        try:
            # Get team stats from CSV
            home_stats = await self.stats_agent.get_team_stats(home_team)
            away_stats = await self.stats_agent.get_team_stats(away_team)
            
            if "error" in home_stats or "error" in away_stats:
                return {"error": "Failed to get team statistics"}
            
            # Create prediction prompt
            prediction_prompt = f"""
            Predict the outcome of this football match:
            
            HOME TEAM ({home_team}):
            Stats: {home_stats['raw_stats']}
            AI Analysis: {home_stats['ai_analysis']}
            
            AWAY TEAM ({away_team}):
            Stats: {away_stats['raw_stats']}
            AI Analysis: {away_stats['ai_analysis']}
            
            {f"Additional Match Data: {match_data}" if match_data else ""}
            
            Provide prediction in JSON format:
            {{
                "prediction": "HOME_WIN/DRAW/AWAY_WIN",
                "confidence": 0.XX,
                "probability_home_win": 0.XX,
                "probability_draw": 0.XX,
                "probability_away_win": 0.XX,
                "reasoning": "detailed explanation",
                "key_factors": ["factor1", "factor2"],
                "risk_level": "LOW/MEDIUM/HIGH"
            }}
            """
            
            # Use Vertex AI for prediction
            vertex_prediction = await self.vertex_client.generate_json(prediction_prompt)
            
            # Use Gemini for additional analysis
            gemini_prompt = f"""
            Based on this prediction: {vertex_prediction}
            
            Provide betting insights in JSON format:
            {{
                "recommended_bet": "HOME_WIN/DRAW/AWAY_WIN/NO_BET",
                "bet_amount": "SMALL/MEDIUM/LARGE",
                "odds_threshold": "minimum odds to bet",
                "value_bet": true/false,
                "explanation": "why this bet is recommended"
            }}
            """
            
            gemini_analysis = await self.gemini_client.generate_json(gemini_prompt)
            
            return {
                "match": {
                    "home_team": home_team,
                    "away_team": away_team
                },
                "team_stats": {
                    "home": home_stats,
                    "away": away_stats
                },
                "vertex_prediction": vertex_prediction,
                "gemini_betting_advice": gemini_analysis
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def get_simple_prediction(self, home_team: str, away_team: str) -> Dict[str, Any]:
        """Simple prediction using Gemini"""
        prompt = f"""
        Predict the outcome of {home_team} vs {away_team}.
        Return only: HOME_WIN, DRAW, or AWAY_WIN
        """
        
        try:
            prediction = await self.gemini_client.generate_content(prompt)
            return {"prediction": prediction.strip()}
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_team_form(self, team_name: str) -> Dict[str, Any]:
        """Analyze team form using AI"""
        try:
            team_stats = await self.stats_agent.get_team_stats(team_name)
            
            if "error" in team_stats:
                return team_stats
            
            form_prompt = f"""
            Analyze the form and performance of {team_name}:
            
            Stats: {team_stats['raw_stats']}
            AI Analysis: {team_stats['ai_analysis']}
            
            Provide form analysis in JSON format:
            {{
                "current_form": "EXCELLENT/GOOD/AVERAGE/POOR",
                "trend": "IMPROVING/STABLE/DECLINING",
                "strengths": ["strength1", "strength2"],
                "weaknesses": ["weakness1", "weakness2"],
                "next_match_outlook": "POSITIVE/NEUTRAL/NEGATIVE"
            }}
            """
            
            form_analysis = await self.vertex_client.generate_json(form_prompt)
            
            return {
                "team": team_name,
                "stats": team_stats,
                "form_analysis": form_analysis
            }
            
        except Exception as e:
            return {"error": str(e)} 