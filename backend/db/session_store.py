from dataclasses import dataclass
from datetime import datetime, timezone
from backend.db.connection import get_connection

@dataclass(frozen=True)
class SessionRecord:
    token_hash: str
    profile_id: int
    created_at: str
    expires_at: str


def create_session(
    token_hash: str,
    profile_id: int,
    created_at: datetime,
    expires_at: datetime
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO sessions (token_hash, profile_id, created_at, expires_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                token_hash,
                profile_id,
                created_at.isoformat(),
                expires_at.isoformat()
            )
        )

        conn.commit()

def read_session(
    token_hash: str
) -> SessionRecord | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT token_hash, profile_id, created_at, expires_at
            FROM sessions
            WHERE token_hash = ?;
            """,
            (token_hash,)
        ).fetchone()

        if row is None:
            return None

        expires_at = datetime.fromisoformat(row["expires_at"])
        if expires_at <= datetime.now(timezone.utc):
            conn.execute(
                """
                DELETE FROM sessions
                WHERE token_hash = ?;
                """,
                (token_hash,)
            )
            conn.commit()
            return None
        
        return SessionRecord(
            token_hash=row["token_hash"],
            profile_id=row["profile_id"],
            created_at=row["created_at"],
            expires_at=row["expires_at"]
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
