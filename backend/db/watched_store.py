from backend.db.connection import get_connection


def read_watched_game_ids(
    season: str,
    season_type: str
) -> set[str]:
    with get_connection() as conn:
        watched_rows = conn.execute(
            """
            SELECT games.game_id
            FROM watched
            JOIN games ON games.id = watched.game_db_id
            WHERE games.season = ? AND games.season_type = ?;
            """,
            (season, season_type)
        ).fetchall()

        watched = set([row["game_id"] for row in watched_rows])

        return watched


def insert_watched_game(
    season: str,
    season_type: str,
    game_id: str
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO watched (game_db_id)
            SELECT id
            FROM games
            WHERE season = ? AND season_type = ? AND game_id = ?;
            """,
            (season, season_type, game_id)
        )
        conn.commit()

def remove_watched_game(
    season: str,
    season_type: str,
    game_id: str
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM watched
            WHERE game_db_id = (
                SELECT id
                FROM games
                WHERE season = ? AND season_type = ? AND game_id = ?
            );
            """,
            (season, season_type, game_id)
        )
        conn.commit()
