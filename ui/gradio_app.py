import gradio as gr

from core.metrics import TotalGoalsMetric
from core.scorer import Scorer
from data.game_loader import load_season_games, load_watched, toggle_watched
from data.update_pipeline import update_season


SEASON_STR = "20252026"


def load_ranked_games(
    show_watched: bool,
    show_unwatched: bool
) -> list[list[str]]:
    games = load_season_games(SEASON_STR)
    watched = load_watched(SEASON_STR)

    scorer = Scorer([TotalGoalsMetric()])

    ranked_games = scorer.rank_games(games)

    rows = []
    for game in ranked_games:
        is_watched = game.game_id in watched
        if is_watched and not show_watched:
            continue
        if not is_watched and not show_unwatched:
            continue
        watched_flag = "✓" if is_watched else ""
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


def on_toggle_watched(
    table: gr.DataFrame,
    selected_row: int,
    show_watched: bool,
    show_unwatched: bool
) -> gr.DataFrame | list[list[str]]:
    if selected_row is None:
        return table # nothing selected
    
    game_id = table.iloc[selected_row, 0]
    toggle_watched(SEASON_STR, game_id)
    
    return load_ranked_games(show_watched, show_unwatched)

def on_update_click(show_watched: bool, show_unwatched: bool):
    num_new_rows = update_season(SEASON_STR)
    status = f"Added {num_new_rows} new games"
    return load_ranked_games(show_watched, show_unwatched), status


with gr.Blocks(title="NHL Game Recommender") as demo:
    gr.Markdown("## NHL Game Recommender - 20252026")

    with gr.Row():
        show_watched_check = gr.Checkbox(value=True, label="Show Watched")
        show_unwatched_check = gr.Checkbox(value=True, label="Show Unwatched")

    selected_row: int = gr.State(None)

    games_table = gr.DataFrame(
        headers=["Game ID", "Date", "Away", "Home", "Watched"],
        datatype=["str", "str", "str", "str", "str"],
        interactive=False
    )

    toggle_watched_button = gr.Button("Toggle watched")

    update_season_button = gr.Button("Load new games")
    update_season_status = gr.Markdown("")

    show_watched_check.change(
        fn=load_ranked_games,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table]
    )
    show_unwatched_check.change(
        fn=load_ranked_games,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table]
    )

    games_table.select(
        fn=on_row_select,
        inputs=[],
        outputs=[selected_row]
    )

    toggle_watched_button.click(
        fn=on_toggle_watched,
        inputs=[games_table, selected_row, show_watched_check, show_unwatched_check],
        outputs=[games_table]
    )

    update_season_button.click(
        fn=on_update_click,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table, update_season_status]
    )

    demo.load(
        fn=load_ranked_games,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table]
    )


if __name__ == "__main__":
    demo.launch()
