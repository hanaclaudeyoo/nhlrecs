from backend.db.connection import get_connection
from dataclasses import dataclass
import sqlite3


@dataclass(frozen=True)
class ProfileRecord:
    id: int
    username: str
    password_hash: str | None


def read_profile_by_username(
    username: str
) -> ProfileRecord | None:
    with get_connection() as conn:
        profile_row = conn.execute(
            """
            SELECT id, username, password_hash
            FROM profiles
            WHERE username = ?;
            """,
            (username,)
        ).fetchone()

        if profile_row is None:
            return None

        return ProfileRecord(
            id=profile_row["id"],
            username=profile_row["username"],
            password_hash=profile_row["password_hash"]
        )


def read_profile_by_id(
    profile_id: int
) -> ProfileRecord | None:
    with get_connection() as conn:
        profile_row = conn.execute(
            """
            SELECT id, username, password_hash
            FROM profiles
            WHERE id = ?;
            """,
            (profile_id,)
        ).fetchone()

        if profile_row is None:
            return None

        return ProfileRecord(
            id=profile_row["id"],
            username=profile_row["username"],
            password_hash=profile_row["password_hash"]
        )


def create_profile(
    username: str,
    password_hash: str
) -> ProfileRecord | None:
    with get_connection() as conn:
        try:
            cursor = conn.execute(
                """
                INSERT INTO profiles (username, password_hash)
                VALUES (?, ?);
                """,
                (username, password_hash)
            )
        except sqlite3.IntegrityError:
            return None

        conn.commit()
        return ProfileRecord(
            id=cursor.lastrowid,
            username=username,
            password_hash=password_hash
        )
