from pydantic import BaseModel
from backend.core.teams import Team


class GameRecommendation(BaseModel):
    rank: int
    season: str
    season_phase: str
    game_id: str
    date: str
    away_team: Team
    home_team: Team
    watched: bool

class GameRecommendationsPage(BaseModel):
    games: list[GameRecommendation]
    page: int
    page_size: int
    total: int
    total_pages: int

class LoginRequest(BaseModel):
    username: str
    password: str

class ProfileResponse(BaseModel):
    id: int
    username: str
    