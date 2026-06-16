from pydantic import BaseModel, Field, field_validator
from backend.core.teams import Team


MIN_PASSWORD_LENGTH = 5
MAX_USERNAME_LENGTH = 32
MAX_PASSWORD_LENGTH = 128


class AuthRequest(BaseModel):
    username: str = Field(min_length=1, max_length=MAX_USERNAME_LENGTH)
    password: str = Field(
        min_length=MIN_PASSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH
    )

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()

        return value


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

class ProfileResponse(BaseModel):
    id: int
    username: str
    
