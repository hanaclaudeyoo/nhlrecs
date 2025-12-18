import gradio as gr

from core.metrics import TotalGoalsMetric
from core.scorer import Scorer
from data.game_loader import load_season_games


SEASON_STR = "20252026"


def load_ranked_games() -> list[list[str]]:
    games = load_season_games(SEASON_STR)

    scorer = Scorer([TotalGoalsMetric()])

    ranked_games = scorer.rank_games(games)

    rows = []
    for game in ranked_games:
        rows.append([
            game.game_id,
            game.date,
            game.away_team,
            game.home_team
        ])
    return rows


with gr.Blocks(title="NHL Game Recommender") as demo:
    gr.Markdown("## NHL Game Recommender")

    games_table = gr.DataFrame(
        headers=["Game ID", "Date", "Away", "Home"],
        datatype=["str", "str", "str", "str"],
        interactive=False
    )

    demo.load(
        fn=load_ranked_games,
        inputs=[],
        outputs=[games_table]
    )


if __name__ == "__main__":
    demo.launch()