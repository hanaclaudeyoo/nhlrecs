import gradio as gr

from core.metrics import TotalGoalsMetric
from core.scorer import Scorer
from data.game_loader import load_season_games, load_watched


SEASON_STR = "20252026"


def load_ranked_games() -> list[list[str]]:
    games = load_season_games(SEASON_STR)
    watched = load_watched(SEASON_STR)

    scorer = Scorer([TotalGoalsMetric()])

    ranked_games = scorer.rank_games(games)

    rows = []
    for game in ranked_games:
        watched_flag = "✓" if game.game_id in watched else ""
        rows.append([
            game.game_id,
            game.date,
            game.away_team,
            game.home_team,
            watched_flag
        ])
    return rows


with gr.Blocks(title="NHL Game Recommender") as demo:
    gr.Markdown("## NHL Game Recommender")

    games_table = gr.DataFrame(
        headers=["Game ID", "Date", "Away", "Home", "Watched"],
        datatype=["str", "str", "str", "str", "str"],
        interactive=False
    )

    demo.load(
        fn=load_ranked_games,
        inputs=[],
        outputs=[games_table]
    )


if __name__ == "__main__":
    demo.launch()