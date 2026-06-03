from backend.data.game_store import load_season_games, load_watched, save_watched
from backend.data.update_pipeline import update_season
from backend.core.metrics import TotalGoalsMetric, LeadChangesMetric, MaxLeadMetric, MaxTimeBetweenGoalsMetric
from backend.core.scorer import Scorer
from backend.api.schemas import GameRecommendation


SEASON_STR = "20252026"


def list_game_recommendations(
    show_watched: bool,
    show_unwatched: bool
) -> list[GameRecommendation]:
    games = load_season_games(SEASON_STR)
    watched = load_watched(SEASON_STR)

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
            game_id=game.game_id,
            date=game.date,
            away_team=game.away_team,
            home_team=game.home_team,
            watched=is_watched
        ))

    return game_recommendations


def toggle_game_watched(game_id: str) -> bool:
    # check if valid game_id
    if game_id is None:
        return None
    
    games = load_season_games(SEASON_STR)
    game_ids = {game.game_id for game in games}
    if game_id not in game_ids:
        return None
    
    # toggle watched
    watched = load_watched(SEASON_STR)

    if game_id in watched:
        watched.remove(game_id)
        is_watched = False
    else:
        watched.add(game_id)
        is_watched = True

    save_watched(SEASON_STR, watched)
    return is_watched


def load_new_games() -> int:
    return update_season(SEASON_STR)