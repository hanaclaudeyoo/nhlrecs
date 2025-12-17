from dataclasses import dataclass, field


@dataclass
class Goal:
    time_elapsed_seconds: int
    team: str


@dataclass
class Game:
    game_id: str
    date: str
    home_team: str
    away_team: str
    goals: list[Goal]
    
    summary: dict[str, float] = field(default_factory=dict)
    watched: bool