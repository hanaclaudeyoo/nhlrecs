from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

SQLITE_DATA_PATH = REPO_ROOT / "data" / "nhlrecs.sqlite3"