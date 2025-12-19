import json
from pathlib import Path
from core.models import Game


DEFAULT_GAME_DIR = "data/game_objects"


def load_season_games(
    season_str: str, # e.g. "20252026",
    input_dir: Path = Path(DEFAULT_GAME_DIR)
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


def load_watched(season_str: str) -> set[str]:
    watched_file = Path(f"data/watched/{season_str}/watched.json")
    if not watched_file.exists():
        return set()
    
    with open(watched_file, "r") as f:
        return set(json.load(f))


def save_watched(season_str: str, watched: set[str]) -> None:
    watched_file = Path(f"data/watched/{season_str}/watched.json")
    watched_file.parent.mkdir(parents=True, exist_ok=True)

    with open(watched_file, "w") as f:
        json.dump(sorted(watched), f, indent=2)


def toggle_watched(season_str: str, game_id: str) -> None:
    watched = load_watched(season_str)
    if game_id in watched:
        watched.remove(game_id)
    else:
        watched.add(game_id)
    save_watched(season_str, watched)