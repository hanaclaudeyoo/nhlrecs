import time
import requests
from backend.db.game_store import game_exists, save_game
from backend.scraper.scoresheet_htm_fetcher import fetch_game
from backend.scraper.scoresheet_htm_parser import parse_game


def update_season_games(
    season: str,
    season_phase: str,
    start_game_id: int = 1,
    end_game_id: int = float('inf'),
    request_delay_seconds: float = 0.2
) -> int:
    game_id = start_game_id
    num_games_updated = 0
    session = requests.Session()

    while game_id <= end_game_id:
        game_id_str = f"{game_id:04d}"

        if not game_exists(season, season_phase, game_id_str):
            htm_str = fetch_game(season, season_phase, game_id_str, session)
            if htm_str is None:
                break
            time.sleep(request_delay_seconds)

            game = parse_game(htm_str, season, season_phase, game_id_str)
            if game is None:
                game_id += 1
                continue

            if save_game(game):
                num_games_updated += 1

        game_id += 1
    
    return num_games_updated
