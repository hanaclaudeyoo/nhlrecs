from fastapi import FastAPI, Query, HTTPException
import math
from backend.api.schemas import GameRecommendationsPage
from backend.api.services import DateWindow, get_all_game_recommendations, toggle_game_watched, load_new_games


app = FastAPI(title="NHL Game Recommender API")

@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/api/games")
def get_games(
    season: str,
    season_phase: str = Query("02"),
    show_watched: bool = Query(True),
    show_unwatched: bool = Query(True),
    team: str = Query(None),
    date_window: DateWindow = Query("all"),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1)
):
    games = get_all_game_recommendations(
        season,
        season_phase,
        show_watched,
        show_unwatched,
        team,
        date_window,
    )

    total_games = len(games)
    total_pages = max(1, math.ceil(total_games/page_size))
    if page > total_pages:
        raise HTTPException(status_code=404, detail=f"Page {page} is out of range ({total_pages} pages total)")

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    return GameRecommendationsPage(
        games=games[start_idx:end_idx],
        page=page,
        page_size=page_size,
        total=total_games,
        total_pages=total_pages
    )


@app.post("/api/games/{season}/{season_phase}/{game_id}/watched/toggle")
def post_toggle_game_watched(
    season: str,
    season_phase: str,
    game_id: str
):
    watched = toggle_game_watched(season, season_phase, game_id)

    if watched is None:
        raise HTTPException(status_code=404, detail="Game ID not found")
    
    return {
        "game_id": game_id,
        "watched": watched
    }


@app.post("/api/seasons/{season}/update")
def post_update_season(
    season: str
):
    return {
        "num_games_added": load_new_games(season, "02") # HOTFIX
    }
