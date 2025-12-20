from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass
import re
from datetime import datetime
from pathlib import Path
import json

from core.models import Goal, Game
from core.teams import Team, FULL_NAME_TO_TEAM


PERIOD_LENGTH_SECONDS = 20 * 60
TEAM_TABLE_TYPES = ("Home", "Visitor")
DEFAULT_INPUT_DIR = "data/scoresheet_htm_raw"
DEFAULT_OUTPUT_DIR = "data/game_objects"


@dataclass
class PlayRow:
    time_elapsed_seconds: int
    event: str
    description: str


def get_time_elapsed(cell_text: str, period: int) -> int:
    # cell text i.e. "1:0019:00"
    times = re.findall(r"\d{1,2}:\d{2}", cell_text)
    if not times:
        raise ValueError(f"Could not parse elapsed time from '{cell_text}'")

    minutes_str, seconds_str = times[0].split(":")
    return (period - 1) * PERIOD_LENGTH_SECONDS + int(minutes_str) * 60 + int(seconds_str)


def get_team_from_desc(description: str) -> Team:
    # e.g. "TOR #74 MCMANN..."
    team_name = description.split()[0]
    return Team(team_name)


def extract_htm_play_rows(soup: BeautifulSoup) -> list[PlayRow]:
    play_rows: list[PlayRow] = []

    for tr in soup.find_all("tr", id=re.compile(r"^PL-\d+")):
        tds = tr.find_all("td")
        if len(tds) < 6:
            continue

        period = int(tds[1].get_text(strip=True))
        time_elapsed = get_time_elapsed(tds[3].get_text(), period)
        event = tds[4].get_text(strip=True)
        description = tds[5].get_text(" ", strip=True)

        play_rows.append(PlayRow(
            time_elapsed_seconds=time_elapsed,
            event=event,
            description=description
        ))

    return play_rows


def extract_game_info(soup: BeautifulSoup) -> Tag:
    return soup.find("table", id="GameInfo")


def is_final_game(game_info: Tag) -> bool:
    for td in game_info.find_all("td"):
        text = td.get_text(strip=True)
        if text == "Final":
            return True
    return False


def parse_goals(play_rows: list[PlayRow]) -> list[Goal]:
    goals: list[Goal] = []

    for row in play_rows:
        if row.event != "GOAL":
            continue

        if row.time_elapsed_seconds >= PERIOD_LENGTH_SECONDS * 4:
            continue # skip shootout goals

        team = get_team_from_desc(row.description)

        goals.append(Goal(
            time_elapsed_seconds=row.time_elapsed_seconds,
            team=team
        ))

    return goals


def parse_team_names(soup: BeautifulSoup, team_type: str) -> str:
    if team_type not in TEAM_TABLE_TYPES:
        raise ValueError(f"Invalid team type {team_type}, should be one of {TEAM_TABLE_TYPES}")
    
    table = soup.find("table", id=team_type)
    if table is None:
        raise ValueError(f"Could not find table {team_type}")
    
    text = table.find_all("td")[-1].get_text(strip=True)
    # e.g. "FLORIDA PANTHERSGame 1 Home Game 1"
    team_name = text.split("Game")[0].strip().upper()

    if team_name not in FULL_NAME_TO_TEAM:
        raise ValueError(f"Unknown team: {team_name}")
    return FULL_NAME_TO_TEAM[team_name]


def parse_game_id(game_info: Tag) -> str:
    for td in game_info.find_all("td"):
        text = td.get_text(strip=True)

        if text.startswith("Game "):
            # e.g. "Game 0001"
            return text.split("Game ")[1]
        
    raise ValueError("Could not find game id in GameInfo.")


def parse_game_date(game_info: Tag) -> str:
    for td in game_info.find_all("td"):
        text = td.get_text(strip=True)

        if "," in text and "Attendance" not in text:
            # e.g. "Tuesday, October 7, 2025"
            date = datetime.strptime(text, "%A, %B %d, %Y")
            return date.date().isoformat()
        
    raise ValueError("Could not find game date in GameInfo.")


def parse_game_htm(htm: str) -> Game:
    soup = BeautifulSoup(htm, "html.parser")

    game_info = extract_game_info(soup)
    if game_info is None:
        return None
    if not is_final_game(game_info):
        return None
    
    game_id = parse_game_id(game_info)
    game_date = parse_game_date(game_info)

    home_team = parse_team_names(soup, "Home")
    away_team = parse_team_names(soup, "Visitor")

    play_rows = extract_htm_play_rows(soup)
    goals = parse_goals(play_rows)

    return Game(
        game_id=game_id,
        date=game_date,
        home_team=home_team,
        away_team=away_team,
        goals=goals
    )

def parse_season(
    season_str: str, # i.e. "20252026",
    season_type: str = "02",
    input_dir: Path = Path(DEFAULT_INPUT_DIR),
    output_dir: Path = Path(DEFAULT_OUTPUT_DIR),
    overwrite: bool = False
):
    in_season_dir = input_dir / season_str
    out_season_dir = output_dir / season_str
    out_season_dir.mkdir(parents=True, exist_ok=True)

    for htm_file in sorted(in_season_dir.glob(f"{season_str}_{season_type}*.HTM")):
        out_file = out_season_dir / (htm_file.stem + ".json")
        if not overwrite and out_file.exists():
            continue

        with open(htm_file, "r", encoding="utf-8") as f:
            htm_str = f.read()

        game = parse_game_htm(htm_str)
        if game is None:
            print(f"Game {out_file.stem} is invalid or unfinished, skipping.")
            continue

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(game.to_json(indent=2), f, indent=2)
        
        print(f"Parsed {out_file.stem}")
    print(f"Completed parsing season {season_str}")