import gradio as gr
from ui.controller import load_ranked_games, toggle_watched, load_new_games


def refresh(show_watched: bool, show_unwatched: bool) -> gr.DataFrame | list[list[str]]:
    return load_ranked_games(show_watched, show_unwatched)


def on_row_select(event: gr.SelectData, table: gr.DataFrame | list[list[str]]) -> int:
    row, _ = event.index

    if hasattr(table, "iloc"):
        return table.iloc[row,0]
    return table[row][0]


def on_toggle_watched(selected_game_id: str, show_watched: bool, show_unwatched: bool) -> gr.DataFrame | list[list[str]]:
    toggle_watched(selected_game_id)
    return load_ranked_games(show_watched, show_unwatched)


def on_update_click(show_watched: bool, show_unwatched: bool) -> tuple[gr.DataFrame | list[list[str]], str]:
    num_new_rows = load_new_games()
    status = f"Added {num_new_rows} new games"
    table = load_ranked_games(show_watched, show_unwatched)
    return table, status