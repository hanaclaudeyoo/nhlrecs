from data.game_store import load_season_games, load_watched, save_watched
from data.update_pipeline import update_season
from core.metrics import TotalGoalsMetric, LeadChanges, MaxLead
from core.scorer import Scorer


SEASON_STR = "20252026"


def load_ranked_games(
    show_watched: bool,
    show_unwatched: bool
) -> list[list[str]]:
    games = load_season_games(SEASON_STR)
    watched = load_watched(SEASON_STR)

    scorer = Scorer([TotalGoalsMetric(), LeadChanges(), MaxLead()])

    ranked_games = scorer.rank_games(games)

    rows = []
    for game in ranked_games:
        is_watched = game.game_id in watched
        if is_watched and not show_watched:
            continue
        if not is_watched and not show_unwatched:
            continue
        watched_flag = "✓" if is_watched else ""
        rows.append([
            game.game_id,
            game.date,
            game.away_team,
            game.home_team,
            watched_flag
        ])
    return rows


def toggle_watched(game_id: str) -> None:
    watched = load_watched(SEASON_STR)
    if game_id in watched:
        watched.remove(game_id)
    else:
        watched.add(game_id)
    save_watched(SEASON_STR, watched)


def load_new_games() -> int:
    return update_season(SEASON_STR)