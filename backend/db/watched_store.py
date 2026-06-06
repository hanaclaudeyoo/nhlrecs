from backend.db.connection import get_connection


def read_watched_game_ids(
    season: str,
    season_phase: str
) -> set[str]:
    with get_connection() as conn:
        watched_rows = conn.execute(
            """
            SELECT games.game_id
            FROM watched
            JOIN games ON games.id = watched.game_db_id
            WHERE games.season = ? AND games.season_phase = ?;
            """,
            (season, season_phase)
        ).fetchall()

        watched = set([row["game_id"] for row in watched_rows])

        return watched


def insert_watched_game(
    season: str,
    season_phase: str,
    game_id: str
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO watched (game_db_id)
            SELECT id
            FROM games
            WHERE season = ? AND season_phase = ? AND game_id = ?;
            """,
            (season, season_phase, game_id)
        )
        conn.commit()

def remove_watched_game(
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
            );
            """,
            (season, season_phase, game_id)
        )
        conn.commit()
