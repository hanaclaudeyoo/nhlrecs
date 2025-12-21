import gradio as gr
from ui.controller import load_ranked_games, toggle_watched, load_new_games


def refresh(show_watched: bool, show_unwatched: bool):
    return load_ranked_games(show_watched, show_unwatched)


def on_row_select(event: gr.SelectData, table_game_ids: list[str]) -> int:
    row = event.index[0]
    if row >= len(table_game_ids):
        return None
    return table_game_ids[row]


def on_toggle_watched(
    table: gr.DataFrame,
    selected_game_id: str,
    show_watched: bool,
    show_unwatched: bool
) -> gr.DataFrame | list[list[str]]:
    if selected_game_id is None:
        return table # nothing selected
    
    toggle_watched(selected_game_id)
    
    return load_ranked_games(show_watched, show_unwatched)


def on_update_click(show_watched: bool, show_unwatched: bool):
    num_new_rows = load_new_games()
    status = f"Added {num_new_rows} new games"
    return load_ranked_games(show_watched, show_unwatched), status