from backend.db.game_store import read_season_games
from backend.db.watched_store import read_watched_game_ids, insert_watched_game, remove_watched_game
from backend.scraper.update_pipeline import update_season_games
from backend.core.metrics import TotalGoalsMetric, LeadChangesMetric, MaxLeadMetric, MaxTimeBetweenGoalsMetric
from backend.core.scorer import Scorer
from backend.api.schemas import GameRecommendation


def list_game_recommendations(
    season: str,
    season_phase: str,
    show_watched: bool,
    show_unwatched: bool
) -> list[GameRecommendation]:
    games = read_season_games(season, season_phase)
    watched = read_watched_game_ids(season, season_phase)

    scorer = Scorer([TotalGoalsMetric(), LeadChangesMetric(), MaxLeadMetric(), MaxTimeBetweenGoalsMetric()])

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
    watched = read_watched_game_ids(season, season_phase)

    if game_id in watched:
        remove_watched_game(season, season_phase, game_id)
        is_watched = False
    else:
        insert_watched_game(season, season_phase, game_id)
        is_watched = True

    return is_watched


def load_new_games(
    season: str,
    season_phase: str
) -> int:
    return update_season_games(season, season_phase)
