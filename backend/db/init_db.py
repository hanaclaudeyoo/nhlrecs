from backend.db.connection import get_connection


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
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
            username TEXT NOT NULL UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS watched (
            game_db_id INTEGER NOT NULL,
            profile_id INTEGER NOT NULL,
            PRIMARY KEY (game_db_id, profile_id),
            FOREIGN KEY (game_db_id) REFERENCES games(id) ON DELETE CASCADE,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
        );
                           
        INSERT OR IGNORE INTO profiles (id, username)
        VALUES (0, "Guest");
                           
        INSERT OR IGNORE INTO profiles (username)
        VALUES ("Test1");
        INSERT OR IGNORE INTO profiles (username)
        VALUES ("Test2");
        """)

        conn.commit()
        print("Database initialized.")


if __name__ == "__main__":
    init_db()
