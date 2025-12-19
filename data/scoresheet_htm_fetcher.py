import requests
from pathlib import Path
import time


BASE_URL = "https://www.nhl.com/scores/htmlreports"
REQUEST_DELAY = 0.5 # seconds
DEFAULT_OUTPUT_DIR = "data/scoresheet_htm_raw"
PARSED_DIR = "data/game_objects"


def is_parsed(season_str, filename: str) -> bool:
    parsed_filepath = Path(PARSED_DIR) / season_str / f"{filename}.json"
    if parsed_filepath.exists():
        return True
    return False


def fetch_season(
    season_str: str, # i.e. "20252026"
    season_type: str = "02",
    output_dir: Path = Path(DEFAULT_OUTPUT_DIR),
    redownload: bool = False,
    start_game_num: int = 1
):
    out_season_dir = output_dir / season_str

    game_num = start_game_num

    session = requests.Session()

    while True:
        req_url = f"{BASE_URL}/{season_str}/PL{season_type}{game_num:04d}.HTM"
        out_filename = f"{season_str}_{season_type}_{game_num:04d}.HTM"
        out_path = out_season_dir / out_filename

        if not redownload and is_parsed(season_str, out_filename[:-4]):
            print(f"Already parsed {out_filename}, skipping.")
            game_num += 1
            continue
            
        response = session.get(req_url)
        
        if response.status_code == 404:
            print(f"No game available for {req_url}")
            print("Ending fetch.")
            break
        if response.status_code != 200:
            raise RuntimeError(f"Unexpected response status {response.status_code} for {req_url}")

        out_path.write_bytes(response.content)
        print(f"Downloaded {game_num} to {out_filename}")

        game_num += 1
        time.sleep(REQUEST_DELAY)