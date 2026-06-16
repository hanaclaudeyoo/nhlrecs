from collections import defaultdict, deque
from time import monotonic

from fastapi import HTTPException, Request


AUTH_RATE_LIMIT_WINDOW_SECONDS = 5 * 60
AUTH_RATE_LIMIT_MAX_ATTEMPTS = 5

_attempts_by_key: dict[tuple[str, str, str], deque[float]] = defaultdict(deque)


def _client_host(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client is None:
        return "unknown"

    return request.client.host


def check_auth_rate_limit(
    request: Request,
    action: str,
    username: str
) -> None:
    now = monotonic()
    key = (action, _client_host(request), username.strip().lower())
    attempts = _attempts_by_key[key]

    while attempts and now - attempts[0] > AUTH_RATE_LIMIT_WINDOW_SECONDS:
        attempts.popleft()

    if len(attempts) >= AUTH_RATE_LIMIT_MAX_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many attempts. Try again later."
        )

    attempts.append(now)
