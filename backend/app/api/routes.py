from fastapi import APIRouter, HTTPException
from app.services.prediction_service import PredictionService
from app.models.schemas import Match

router = APIRouter(prefix="/api/v1")
prediction_service = PredictionService()

@router.get("/predictions")
async def get_predictions():
    """Get football match predictions"""
    return {"predictions": []}

@router.get("/matches")
async def get_matches():
    """Get available matches"""
    return {"matches": []}

@router.post("/predict")
async def predict_match(match: Match):
    """Get AI prediction for a specific match"""
    try:
        prediction = await prediction_service.get_detailed_prediction(
            match.home_team, 
            match.away_team, 
            match.league
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-simple")
async def predict_simple(match_data: str):
    """Get simple prediction (HOME_WIN/DRAW/AWAY_WIN)"""
    try:
        result = await prediction_service.get_simple_prediction(match_data)
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/team-form/{team_name}")
async def get_team_form(team_name: str):
    """Get team form analysis"""
    try:
        form_analysis = await prediction_service.analyze_team_form(team_name)
        return form_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 