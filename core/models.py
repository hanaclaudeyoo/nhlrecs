from dataclasses import dataclass, field
from teams import Team


@dataclass
class Goal:
    time_elapsed_seconds: int
    team: Team


@dataclass
class Game:
    game_id: str
    date: str
    home_team: Team
    away_team: Team
    goals: list[Goal]
    
    summary: dict[str, float] = field(default_factory=dict)
    watched: bool