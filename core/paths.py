from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DATASETS_DIR = REPO_ROOT / "datasets"
RAW_SCORESHEET_DIR = DATASETS_DIR / "scoresheet_htm_raw"
PARSED_GAMES_DIR = DATASETS_DIR / "game_objects"
WATCHED_DIR = DATASETS_DIR / "watched"