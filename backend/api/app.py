from fastapi import FastAPI, Query, HTTPException
from backend.api.services import list_game_recommendations, toggle_game_watched, load_new_games


app = FastAPI(title="NHL Game Recommender API")

@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/api/games")
def get_games(
    show_watched: bool = Query(True),
    show_unwatched: bool = Query(True)
):
    return list_game_recommendations(show_watched, show_unwatched)

@app.post("/api/games/{game_id}/watched/toggle")
def post_toggle_game_watched(
    game_id: str
):
    watched = toggle_game_watched(game_id)

    if watched is None:
        raise HTTPException(status_code=404, detail="Game ID not found")
    
    return {
        "game_id": game_id,
        "watched": watched
    }

@app.post("/api/seasons/current/update")
def post_update_current_season():
    return {
        "num_games_added": load_new_games()
    }