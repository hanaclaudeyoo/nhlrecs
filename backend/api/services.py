from datetime import date, datetime, timedelta, timezone
from typing import Literal
from fastapi import Request, Response

from backend.db.game_store import read_season_games
from backend.db.watched_store import read_watched_game_ids, insert_watched_game, remove_watched_game
from backend.db.profile_store import create_profile, read_profile_by_username
from backend.db.session_store import create_session, delete_session
from backend.scraper.update_pipeline import update_season_games
from backend.core.scorer import Scorer
from backend.api.schemas import GameRecommendation, ProfileResponse
from backend.api.auth import (
    SESSION_COOKIE_NAME,
    SESSION_MAX_AGE_SECONDS,
    clear_session_cookie,
    create_session_token,
    get_current_profile_for_cookie,
    hash_password,
    hash_session_token,
    set_session_cookie,
    verify_password,
)

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


def login_to_profile(
    username: str,
    password: str
) -> ProfileResponse | None:
    profile = read_profile_by_username(username)

    # user profile does not exist
    if profile is None:
        return None
    if profile.password_hash is None:
        return None

    # incorrect password
    if not verify_password(password, profile.password_hash):
        return None
    
    return ProfileResponse(
        id=profile.id,
        username=profile.username
    )


def login_to_profile_with_session(
    username: str,
    password: str,
    response: Response
) -> ProfileResponse | None:
    profile_response = login_to_profile(username, password)

    if profile_response is None:
        return None

    token = create_session_token()
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(seconds=SESSION_MAX_AGE_SECONDS)
    create_session(
        hash_session_token(token),
        profile_response.id,
        created_at,
        expires_at
    )
    set_session_cookie(response, token)

    return profile_response


def signup_to_profile_with_session(
    username: str,
    password: str,
    response: Response
) -> ProfileResponse | None:
    profile = create_profile(username, hash_password(password))

    if profile is None:
        return None

    profile_response = ProfileResponse(
        id=profile.id,
        username=profile.username
    )

    token = create_session_token()
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(seconds=SESSION_MAX_AGE_SECONDS)
    create_session(
        hash_session_token(token),
        profile_response.id,
        created_at,
        expires_at
    )
    set_session_cookie(response, token)

    return profile_response


def logout_current_session(
    request: Request,
    response: Response
) -> None:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token is not None:
        delete_session(hash_session_token(token))

    clear_session_cookie(response)


def get_current_profile(
    request: Request
) -> ProfileResponse | None:
    profile = get_current_profile_for_cookie(request)
    if profile is None:
        return None

    return ProfileResponse(
        id=profile.id,
        username=profile.username
    )


def get_current_profile_id(
    request: Request
) -> int:
    profile = get_current_profile(request)
    if profile is None:
        return 0

    return profile.id
