import gradio as gr

from core.metrics import TotalGoalsMetric
from core.scorer import Scorer
from data.game_loader import load_season_games, load_watched, toggle_watched


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


def on_row_select(event: gr.SelectData) -> int:
    return event.index[0]


def on_toggle_watched(table, selected_row):
    if selected_row is None:
        return table # nothing selected
    
    game_id = table.iloc[selected_row, 0]
    toggle_watched(SEASON_STR, game_id)
    
    return load_ranked_games()


with gr.Blocks(title="NHL Game Recommender") as demo:
    gr.Markdown("## NHL Game Recommender")

    selected_row: int = gr.State(None)

    games_table = gr.DataFrame(
        headers=["Game ID", "Date", "Away", "Home", "Watched"],
        datatype=["str", "str", "str", "str", "str"],
        interactive=False
    )

    toggle_watched_button = gr.Button("Toggle Watched")

    games_table.select(
        fn=on_row_select,
        inputs=[],
        outputs=[selected_row]
    )

    toggle_watched_button.click(
        fn=on_toggle_watched,
        inputs=[games_table, selected_row],
        outputs=[games_table]
    )

    demo.load(
        fn=load_ranked_games,
        inputs=[],
        outputs=[games_table]
    )


if __name__ == "__main__":
    demo.launch()