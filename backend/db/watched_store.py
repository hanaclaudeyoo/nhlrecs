from backend.db.connection import get_connection


def read_watched_game_ids(
    profile_id: int,
    season: str,
    season_phase: str
) -> set[str]:
    with get_connection() as conn:
        watched_rows = conn.execute(
            """
            SELECT games.game_id
            FROM watched
            JOIN games ON games.id = watched.game_db_id
            JOIN profiles ON profiles.id = watched.profile_id
            WHERE profiles.id = ? AND games.season = ? AND games.season_phase = ?;
            """,
            (profile_id, season, season_phase)
        ).fetchall()

        watched = set([row["game_id"] for row in watched_rows])

        return watched


def insert_watched_game(
    profile_id: int,
    season: str,
    season_phase: str,
    game_id: str
) -> None:
    with get_connection() as conn:
        game_row = conn.execute(
            """
            SELECT id
            FROM games
            WHERE season = ? AND season_phase = ? AND game_id = ?;
            """,
            (season, season_phase, game_id)
        ).fetchone()

        if game_row is None:
            return

        conn.execute(
            """
            INSERT OR IGNORE INTO watched (game_db_id, profile_id)
            VALUES (?, ?);
            """,
            (game_row["id"], profile_id)
        )
        conn.commit()


def remove_watched_game(
    profile_id: int, 
    season: str,
    season_phase: str,
    game_id: str
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM watched
            WHERE game_db_id = (
                SELECT id
                FROM games
                WHERE season = ? AND season_phase = ? AND game_id = ?
            ) AND profile_id = ?;
            """,
            (season, season_phase, game_id, profile_id)
        )
        conn.commit()
