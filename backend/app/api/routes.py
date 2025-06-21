from fastapi import APIRouter, HTTPException
from app.services.ai_agent import FootballAgent
from app.services.stats_agent import StatsAgent
from app.services.prediction_agent import PredictionAgent
from app.services.getgames import getnextgames
from app.config.settings import settings
from app.models.schemas import Match

router = APIRouter(prefix="/api/v1")

# Lazy initialization of agents
_ai_agent = None
_stats_agent = None
_prediction_agent = None

def get_ai_agent():
    global _ai_agent
    if _ai_agent is None:
        _ai_agent = FootballAgent()
    return _ai_agent

def get_stats_agent():
    global _stats_agent
    if _stats_agent is None:
        _stats_agent = StatsAgent()
    return _stats_agent

def get_prediction_agent():
    global _prediction_agent
    if _prediction_agent is None:
        _prediction_agent = PredictionAgent()
    return _prediction_agent

# Games Routes
@router.get("/games/next")
async def get_next_games():
    """Get next 5 games using Gemini AI"""
    try:
        print("Received request for /games/next")
        games = await getnextgames(settings.GEMINI_API_KEY)
        print("Games response:", games)
        return games
    except Exception as e:
        print("Error in /games/next:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Stats Agent Routes
@router.get("/stats/team/{team_name}")
async def get_team_stats(team_name: str):
    """Get team statistics from CSV with AI analysis"""
    try:
        stats = await get_stats_agent().get_team_stats(team_name)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stats/compare")
async def compare_teams(team1: str, team2: str):
    """Compare two teams using CSV data and AI"""
    try:
        comparison = await get_stats_agent().compare_teams(team1, team2)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Prediction Agent Routes
@router.post("/predict/match")
async def predict_match(home_team: str, away_team: str, match_data: str = ""):
    """Get comprehensive match prediction using multiple AI models"""
    try:
        prediction = await get_prediction_agent().predict_match(home_team, away_team, match_data)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/simple")
async def simple_prediction(home_team: str, away_team: str):
    """Get simple prediction using Gemini"""
    try:
        prediction = await get_prediction_agent().get_simple_prediction(home_team, away_team)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict/form/{team_name}")
async def analyze_team_form(team_name: str):
    """Analyze team form using AI"""
    try:
        form_analysis = await get_prediction_agent().analyze_team_form(team_name)
        return form_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Original AI Agent Routes
@router.post("/agent/analyze")
async def analyze_match_with_agent(home_team: str, away_team: str, match_data: str = ""):
    """AI agent analyzes a match comprehensively"""
    try:
        analysis = await get_ai_agent().analyze_match(home_team, away_team, match_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agent/betting-advice")
async def get_betting_advice(home_team: str, away_team: str, match_data: str = ""):
    """AI agent provides betting recommendations"""
    try:
        advice = await get_ai_agent().get_betting_recommendation(home_team, away_team, match_data)
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agent/team-analysis")
async def analyze_team_performance(team_name: str, performance_data: str = ""):
    """AI agent analyzes team performance"""
    try:
        analysis = await get_ai_agent().analyze_team_performance(team_name, performance_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 