from backend.core.models import Game, Goal
from backend.core.teams import Team
from backend.db.connection import get_connection


def read_season_games(
    season: str,
    season_phase: str
) -> list[Game]:
    with get_connection() as conn:
        # get all games for the season
        game_rows = conn.execute(
            """
            SELECT id, game_id, season, season_phase, date, home_team, away_team
            FROM games
            WHERE season = ? AND season_phase = ?
            ORDER BY date, game_id;
            """, 
            (season, season_phase)
        ).fetchall()

        games: list[Game] = []

        # for each game, get all the goals
        for game_row in game_rows:
            goal_rows = conn.execute(
                """
                SELECT time_elapsed_seconds, team
                FROM goals
                WHERE game_db_id = ?
                ORDER BY goal_index;
                """, 
                (game_row["id"],)
            ).fetchall()

            goals: list[Goal] = [
                Goal(
                    time_elapsed_seconds=goal_row["time_elapsed_seconds"],
                    team=Team(goal_row["team"])
                )
                for goal_row in goal_rows
            ]

            games.append(
                Game(
                    game_id=game_row["game_id"],
                    season=game_row["season"],
                    season_phase=game_row["season_phase"],
                    date=game_row["date"],
                    home_team=Team(game_row["home_team"]),
                    away_team=Team(game_row["away_team"]),
                    goals=goals
                )
            )

        return games
