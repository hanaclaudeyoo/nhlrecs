from backend.db.connection import get_connection


DEFAULT_GUEST_ID = 0


def read_profile(
    username: str
) -> int | None:
    with get_connection() as conn:
        profile_row = conn.execute(
            """
            SELECT id
            FROM profiles
            WHERE username = ?;
            """,
            (username,)
        ).fetchone()

        if profile_row is None:
            return None

        return profile_row["id"]
