from fastapi import FastAPI, Query, HTTPException, Request, Response
import math
from backend.api.schemas import GameRecommendationsPage, LoginRequest, ProfileResponse, SignupRequest
from backend.api.services import (
    DateWindow,
    get_all_game_recommendations,
    get_current_profile,
    get_current_profile_id,
    load_new_games,
    login_to_profile_with_session,
    logout_current_session,
    signup_to_profile_with_session,
    toggle_game_watched,
)


app = FastAPI(title="NHL Game Recommender API")

@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/api/games")
def get_games(
    request: Request,
    season: str,
    season_phase: str = Query("02"),
    show_watched: bool = Query(True),
    show_unwatched: bool = Query(True),
    team: str = Query(None),
    date_window: DateWindow = Query("all"),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1)
):
    profile_id = get_current_profile_id(request)
    games = get_all_game_recommendations(
        profile_id,
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
    request: Request,
    season: str,
    season_phase: str,
    game_id: str
):
    profile_id = get_current_profile_id(request)
    if profile_id == 0:
        raise HTTPException(
            status_code=403,
            detail="Log in to modify watched games"
        )

    watched = toggle_game_watched(profile_id, season, season_phase, game_id)

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


@app.post("/api/auth/login", response_model=ProfileResponse)
def post_auth_login(
    request: LoginRequest,
    response: Response
):
    profile_response = login_to_profile_with_session(
        request.username,
        request.password,
        response
    )

    if profile_response is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return profile_response


@app.post("/api/auth/signup", response_model=ProfileResponse)
def post_auth_signup(
    request: SignupRequest,
    response: Response
):
    profile_response = signup_to_profile_with_session(
        request.username,
        request.password,
        response
    )

    if profile_response is None:
        raise HTTPException(status_code=409, detail="Username already exists")

    return profile_response


@app.post("/api/auth/logout")
def post_auth_logout(
    request: Request,
    response: Response
):
    logout_current_session(request, response)
    return {
        "status": "ok"
    }


@app.get("/api/auth/me", response_model=ProfileResponse | None)
def get_auth_me(
    request: Request
):
    return get_current_profile(request)
