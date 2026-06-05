from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DATASETS_DIR = REPO_ROOT / "datasets"
RAW_SCORESHEET_DIR = DATASETS_DIR / "scoresheet_htm_raw"
PARSED_GAMES_DIR = DATASETS_DIR / "game_objects"
WATCHED_DIR = DATASETS_DIR / "watched"

SQLITE_DATA_PATH = REPO_ROOT / "data" / "nhlrecs.sqlite3"