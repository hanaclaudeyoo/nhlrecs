import json
from pathlib import Path
from core.models import Game

def load_season_games(
    season_str: str, # e.g. "20252026",
    input_dir: Path = Path("data/game_objects")
) -> list[Game]:
    season_dir = input_dir / season_str

    games: list[Game] = []

    for json_file in sorted(season_dir.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, str):
                data = json.loads(data)
            games.append(Game.from_dict(data))
    
    return games
