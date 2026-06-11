from datetime import date, timedelta
from typing import Literal

from backend.db.game_store import read_season_games
from backend.db.watched_store import read_watched_game_ids, insert_watched_game, remove_watched_game
from backend.db.profile_store import read_profile
from backend.scraper.update_pipeline import update_season_games
from backend.core.scorer import Scorer
from backend.api.schemas import GameRecommendation

DateWindow = Literal["all", "last_week", "last_month", "last_two_months"]

DATE_WINDOW_DAYS: dict[DateWindow, int | None] = {
    "all": None,
    "last_week": 7,
    "last_month": 31,
    "last_two_months": 62,
}


def filter_games_by_date_window(games, date_window: DateWindow):
    window_days = DATE_WINDOW_DAYS[date_window]
    if window_days is None or not games:
        return games

    cutoff_date = date.today() - timedelta(days=window_days)

    return [
        game
        for game in games
        if date.fromisoformat(game.date) >= cutoff_date
    ]


def get_all_game_recommendations(
    profile_id: int,
    season: str,
    season_phase: str,
    show_watched: bool,
    show_unwatched: bool,
    team: str | None,
    date_window: DateWindow
) -> list[GameRecommendation]:
    games = read_season_games(season, season_phase, team)
    games = filter_games_by_date_window(games, date_window)
    watched = read_watched_game_ids(profile_id, season, season_phase)

    scorer = Scorer(profile_id)

    ranked_games = scorer.rank_games(games)

    game_recommendations = []

    for i in range(len(ranked_games)):
        game = ranked_games[i]
        is_watched = game.game_id in watched
        if is_watched and not show_watched:
            continue
        if not is_watched and not show_unwatched:
            continue

        game_recommendations.append(GameRecommendation(
            rank=i+1,
            season=season,
            season_phase=season_phase,
            game_id=game.game_id,
            date=game.date,
            away_team=game.away_team,
            home_team=game.home_team,
            watched=is_watched
        ))

    return game_recommendations


def toggle_game_watched(
    profile_id: int, 
    season: str,
    season_phase: str,
    game_id: str
) -> bool | None:
    # check if valid game_id
    if game_id is None:
        return None
    
    games = read_season_games(season, season_phase)
    game_ids = {game.game_id for game in games}
    if game_id not in game_ids:
        return None
    
    # toggle watched
    watched = read_watched_game_ids(profile_id, season, season_phase)

    if game_id in watched:
        remove_watched_game(profile_id, season, season_phase, game_id)
        is_watched = False
    else:
        insert_watched_game(profile_id, season, season_phase, game_id)
        is_watched = True

    return is_watched


def load_new_games(
    season: str,
    season_phase: str
) -> int:
    return update_season_games(season, season_phase)


def get_profile_id_for_username(
    username: str
) -> int | None:
    return read_profile(username)
