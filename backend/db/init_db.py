from backend.db.connection import get_connection
from backend.core.metrics import ALL_METRIC_KEYS
from backend.api.auth import hash_password


def init_db() -> None:
    with get_connection() as conn:
        # create tables
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season TEXT NOT NULL,
                season_phase TEXT NOT NULL,
                game_id TEXT NOT NULL,
                date TEXT NOT NULL,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                UNIQUE (season, season_phase, game_id)
            );
                        
            CREATE TABLE IF NOT EXISTS goals (
                game_db_id INTEGER NOT NULL,
                goal_index INTEGER NOT NULL,
                time_elapsed_seconds INTEGER NOT NULL,
                team TEXT NOT NULL,
                PRIMARY KEY (game_db_id, goal_index),
                FOREIGN KEY (game_db_id) REFERENCES games(id) ON DELETE CASCADE
            );
                            
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT
            );
            
            CREATE TABLE IF NOT EXISTS watched (
                game_db_id INTEGER NOT NULL,
                profile_id INTEGER NOT NULL,
                PRIMARY KEY (game_db_id, profile_id),
                FOREIGN KEY (game_db_id) REFERENCES games(id) ON DELETE CASCADE,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            );
                        
            CREATE TABLE IF NOT EXISTS metric_weights (
                profile_id INTEGER NOT NULL,
                metric_key TEXT NOT NULL,
                weight REAL NOT NULL,
                PRIMARY KEY (profile_id, metric_key),
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                profile_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            );
            """
        )

        # create default guest profile
        conn.execute(
            """                   
            INSERT OR IGNORE INTO profiles (id, username)
            VALUES (0, "Guest");
            """
        )

        conn.commit()
        print("Database initialized.")


if __name__ == "__main__":
    init_db()
