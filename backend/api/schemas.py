from pydantic import BaseModel
from backend.core.teams import Team


class GameRecommendation(BaseModel):
    rank: int
    season: str
    season_type: str
    game_id: str
    date: str
    away_team: Team
    home_team: Team
    watched: bool
