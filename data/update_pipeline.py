from pathlib import Path
from data.scoresheet_htm_fetcher import fetch_season
from data.scoresheet_htm_parser import parse_season


PARSED_GAME_DIR = "data/game_objects"


def count_parsed_games(season_str: str) -> int:
    parsed_dir = Path(PARSED_GAME_DIR) / season_str
    if not parsed_dir.exists():
        return 0
    return len(list(parsed_dir.glob("*.json")))


def update_season(
    season_str: str, # e.g. "20252026"
) -> int:
    fetch_season(season_str)

    before = count_parsed_games(season_str)
    parse_season(season_str)
    after = count_parsed_games(season_str)

    return after - before # returns number of new games added