from dataclasses import dataclass
from backend.db.connection import get_connection

@dataclass(frozen=True)
class SessionRecord:
    token_hash: str
    profile_id: int


def create_session(
    token_hash: str,
    profile_id: int
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO sessions (token_hash, profile_id)
            VALUES (?, ?)
            """,
            (token_hash, profile_id)
        )

        conn.commit()

def read_session(
    token_hash: str
) -> SessionRecord | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT token_hash, profile_id
            FROM sessions
            WHERE token_hash = ?;
            """,
            (token_hash,)
        ).fetchone()

        if row is None:
            return None
        
        return SessionRecord(
            token_hash=row["token_hash"],
            profile_id=row["profile_id"]
        )

def delete_session(
    token_hash: str
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM sessions
            WHERE token_hash = ?;
            """,
            (token_hash,)
        )

        conn.commit()
