from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List
from dataclasses import dataclass
import re
from datetime import datetime

from core.models import Goal, Game
from core.teams import Team, FULL_NAME_TO_TEAM


PERIOD_LENGTH_SECONDS = 20 * 60
TEAM_TABLE_TYPES = ("Home", "Visitor")


@dataclass
class PlayRow:
    time_elapsed_seconds: int
    event: str
    description: str


def get_time_elapsed(cell_text: str, period: int) -> int:
    # cell text e.g: "1:00\n19:00"
    elapsed = cell_text.strip().split("\n")[0]
    minutes, seconds = elapsed.split(":")
    return (period - 1)*PERIOD_LENGTH_SECONDS + int(minutes)*60 + int(seconds)


def get_team_from_desc(description: str) -> Team:
    # e.g. "TOR #74 MCMANN..."
    team_name = description.split()[0]
    return Team(team_name)


def extract_htm_play_rows(soup: BeautifulSoup) -> List[PlayRow]:
    play_rows: List[PlayRow] = []

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
    game_info = soup.find("table", id="GameInfo")
    if game_info is None:
        raise ValueError("Could not find GameInfo table")
    
    return game_info


def parse_goals(play_rows: List[PlayRow]) -> List[Goal]:
    goals: List[Goal] = []

    for row in play_rows:
        if row.event != "GOAL":
            continue

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
        
    raise ValueError("Could not find game id in GameInfo")


def parse_game_date(game_info: Tag) -> str:
    for td in game_info.find_all("td"):
        text = td.get_text(strip=True)

        if "," in text and "Attendance" not in text:
            # e.g. "Tuesday, October 7, 2025"
            date = datetime.strptime(text, "%A, %B %d, %Y")
            return date.date().isoformat()
        
    raise ValueError("Could not find game date in GameInfo")


def parse_game_htm(htm: str) -> Game:
    soup = BeautifulSoup(htm, "html.parser")

    home_team = parse_team_names(soup, "Home")
    away_team = parse_team_names(soup, "Visitor")

    game_info = extract_game_info(soup)
    game_id = parse_game_id(game_info)
    game_date = parse_game_date(game_info)

    play_rows = extract_htm_play_rows(soup)
    goals = parse_goals(play_rows)

    return Game(
        game_id=game_id,
        date=game_date,
        home_team=home_team,
        away_team=away_team,
        goals=goals
    )