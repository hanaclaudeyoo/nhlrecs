from pathlib import Path
from backend.data.scoresheet_htm_fetcher import fetch_season
from backend.data.scoresheet_htm_parser import parse_season
from backend.core.paths import PARSED_GAMES_DIR


def count_parsed_games(season: str) -> int:
    parsed_dir = Path(PARSED_GAMES_DIR) / season
    if not parsed_dir.exists():
        return 0
    return len(list(parsed_dir.glob("*.json")))


def update_season(
    season: str, # e.g. "20252026"
    refetch: bool = False,
    reparse: bool = False
) -> int:
    fetch_season(season, redownload=refetch)

    before = count_parsed_games(season)
    parse_season(season, overwrite=reparse)
    after = count_parsed_games(season)

    return after - before # returns number of new games added


if __name__ == "__main__":
    update_season("20252026", reparse=True)