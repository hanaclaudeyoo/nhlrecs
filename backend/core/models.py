from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from backend.core.teams import Team


@dataclass_json
@dataclass
class Goal:
    time_elapsed_seconds: int
    team: Team


@dataclass_json
@dataclass
class Game:
    game_id: str
    season: str
    date: str
    home_team: Team
    away_team: Team
    goals: list[Goal]
