import bcrypt
import secrets
import hashlib
from fastapi import Request, Response
from backend.db.profile_store import ProfileRecord, read_profile_by_id
from backend.db.session_store import read_session

SESSION_COOKIE_NAME = "nhlrecs_session"
SESSION_MAX_AGE_SECONDS = 30 * 24 * 60 * 60


def hash_password(
    password: str
) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    return password_hash.decode("utf-8")

def verify_password(
    password: str,
    password_hash: str
) -> bool:
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def create_session_token() -> str:
    return secrets.token_urlsafe(32)

def hash_session_token(
    token: str
) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def set_session_cookie(
    response: Response,
    token: str
) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=SESSION_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/"
    )

def clear_session_cookie(
    response: Response,
) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        path="/"
    )

def get_current_profile_for_cookie(
    request: Request
) -> ProfileRecord | None:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token is None:
        return None

    token_hash = hash_session_token(token)
    session = read_session(token_hash)
    if session is None:
        return None

    return read_profile_by_id(session.profile_id)
