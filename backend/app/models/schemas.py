from pydantic import BaseModel
from typing import Optional

class Match(BaseModel):
    id: str
    home_team: str
    away_team: str
    date: str
    league: str

class Prediction(BaseModel):
    match_id: str
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    recommended_bet: Optional[str] = None 