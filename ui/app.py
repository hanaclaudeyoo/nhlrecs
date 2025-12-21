import gradio as gr
from ui.hooks import refresh, on_row_select, on_toggle_watched, on_update_click


with gr.Blocks(title="NHL Game Recommender") as demo:

    ### COMPONENTS ###

    gr.Markdown("## NHL Game Recommender - 20252026")

    with gr.Row():
        show_watched_check = gr.Checkbox(value=True, label="Show Watched")
        show_unwatched_check = gr.Checkbox(value=True, label="Show Unwatched")

    table_game_ids: list[str] = gr.State([])
    selected_game_id: str = gr.State(None)

    games_table = gr.DataFrame(
        headers=["Game ID", "Date", "Away", "Home", "Watched"],
        datatype=["str", "str", "str", "str", "str"],
        interactive=False
    )

    toggle_watched_button = gr.Button("Toggle watched")

    update_season_button = gr.Button("Load new games")
    update_season_status = gr.Markdown("")


    ### HOOKS ###

    # Filters
    show_watched_check.change(
        fn=refresh,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table, table_game_ids]
    )
    show_unwatched_check.change(
        fn=refresh,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table, table_game_ids]
    )

    games_table.select(
        fn=on_row_select,
        inputs=[table_game_ids],
        outputs=[selected_game_id]
    )

    # Buttons
    toggle_watched_button.click(
        fn=on_toggle_watched,
        inputs=[games_table, selected_game_id, show_watched_check, show_unwatched_check],
        outputs=[games_table, table_game_ids]
    )

    update_season_button.click(
        fn=on_update_click,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table, table_game_ids, update_season_status]
    )


    ### APP ###

    demo.load(
        fn=refresh,
        inputs=[show_watched_check, show_unwatched_check],
        outputs=[games_table, table_game_ids]
    )


if __name__ == "__main__":
    demo.launch()