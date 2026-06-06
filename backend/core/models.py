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
    season: str         # e.g. 20252026
    season_phase: str    # pre(01)/reg(02)/post(03) season
    game_id: str        # 4 digits
    date: str
    home_team: Team
    away_team: Team
    goals: list[Goal]

    @property
    def uid(self) -> str:
        return f"{self.season}_{self.season_phase}_{self.game_id}"
