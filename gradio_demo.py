import gradio as gr
import pandas as pd

def filter_games(scoring, closeness, unpredictability, back_and_forth):
    df = pd.read_csv("prelim_scores_pct.csv")

    # filter for Scoring
    df = df[df["total_goals"] >= scoring]
    df["Match"] = df["total_goals"] * 0.23
    print(len(df))

    # filter for Close Game
    df = df[df["final_goal_diff"] <= (1 - closeness)]
    df["Match"] = df["Match"] + (1 - df["final_goal_diff"]) * 0.25
    print(len(df))
    
    # filter for Predictability
    df = df[df["lead_changes"] <= (1 - unpredictability)]
    df["Match"] = df["Match"] + (1 - df["lead_changes"]) * 0.25
    print(len(df))

    # filter for Back and Forth
    df = df[df["max_streak"] <= (1 - back_and_forth)]
    df["Match"] = df["Match"] + (1 - df["max_streak"]) * 0.25
    print(len(df))

    # clean up df for return
    display_df = df[["game_date", "home_name", "away_name", "Match"]]
    display_df["Match"] = round(display_df["Match"], 2)
    display_df = display_df.rename(columns={
        "game_date": "Date",
        "home_name": "Home Team",
        "away_name": "Away Team"
    })
    display_df = display_df.sort_values(by=["Match"], ascending=False)
    return display_df, f"{len(display_df)} total results."

demo = gr.Interface(
    fn=filter_games,
    inputs=[
        gr.Slider(0, 1, value=0, step=0.01, label="Scoring"),
        gr.Slider(0, 1, value=0, step=0.01, label="Close Game"),
        gr.Slider(0, 1, value=0, step=0.01, label="Unpredictability"),
        gr.Slider(0, 1, value=0, step=0.01, label="Back-and-forth")
    ],
    outputs=[
        gr.DataFrame(
            headers=["Date", "Home Team", "Away Team", "Match"]
        ),
        "text"
    ]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
