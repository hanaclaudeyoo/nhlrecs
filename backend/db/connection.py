import sqlite3
from backend.core.paths import SQLITE_DATA_PATH


def get_connection() -> sqlite3.Connection:
    # make sure parent directories exist
    SQLITE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(SQLITE_DATA_PATH)
    conn.row_factory = sqlite3.Row # allow index by attribute name
    conn.execute("PRAGMA foreign_keys = ON")

    return conn