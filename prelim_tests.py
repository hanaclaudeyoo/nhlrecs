import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)


pbp = pd.read_csv("play_by_play_2023_24_lite.csv")

game_ends = pbp[pbp["event_type"] == "GAME_END"]
games = game_ends[["game_date", "game_id", "home_name", "away_name", "home_score", "away_score"]].copy()

games["total_goals"] = games["home_score"] + games["away_score"]

games["final_goal_diff"] = np.abs(games["home_score"] - games["away_score"])

goals = pbp[pbp["event_type"] == "GOAL"]
def streak_analysis(row):
    game_goals = goals[goals["game_id"] == row["game_id"]]

    streaks = []
    current_team = ""
    for row in game_goals.itertuples(index=False, name="Pandas"):
        if row.event_team_type == current_team:
            streaks[-1] += 1
        else:
            streaks.append(1)
            current_team = row.event_team_type
    
    mask = np.mod(np.arange(len(streaks)), 2) * 2 - 1
    signed_streaks = mask * streaks
    shift = np.cumsum(signed_streaks)
    lead_changes = 0
    tied_not_led = 0
    for i in range(len(shift) - 1):
        if shift[i] * shift[i+1] < 0:
            lead_changes += 1
        elif shift[i+1] == 0:
            tied_not_led += 1

    return len(streaks)-1, max(streaks), streaks[-1], lead_changes, tied_not_led
games[["streak_changes", "max_streak", "last_streak", "lead_changes", "tied_not_led"]] = games.apply(streak_analysis, axis=1, result_type='expand')

def lead_analysis(row):
    game_goals = goals[goals["game_id"] == row["game_id"]]

    goal_diffs = [0]
    for row in game_goals.itertuples(index=False, name="Pandas"):
        if row.event_team_type == "home":
            goal_diffs.append(goal_diffs[-1] + 1)
        else:
            goal_diffs.append(goal_diffs[-1] - 1)
    # max_home_lead = max(goal_diffs)
    # max_away_lead = min(goal_diffs)
    max_winner_lead = abs(max(goal_diffs) if goal_diffs[-1] > 0 else min(goal_diffs))
    max_loser_lead = abs(min(goal_diffs) if goal_diffs[-1] > 0 else max(goal_diffs))
    
    # lead_changes = 0
    # tied_not_led = 0
    # for i in range(len(goal_diffs) - 1):
    #     if goal_diffs[i] * goal_diffs[i+1] < 0:
    #         lead_changes += 1
    #     if goal_diffs[i+1] == 0:
    #         tied_not_led += 1

    return(max_winner_lead, max_loser_lead)
games[["max_winner_lead", "max_loser_lead"]] = games.apply(lead_analysis, axis=1, result_type='expand')

games = games.drop(["home_score", "away_score"], axis=1)

# print(len(games))
# for feature, max_idx in games.idxmax().items():
#     print(f"Maximum {feature} of {games.loc[max_idx][feature]} @ {max_idx}")
#     print(games.loc[max_idx].to_list())

# # games.to_csv("prelim_scores.csv")

stats_columns = ["total_goals", "final_goal_diff", "streak_changes", "max_streak", "last_streak", "lead_changes", "tied_not_led", "max_winner_lead", "max_loser_lead"]
games[stats_columns] = games[stats_columns].rank(pct=True)
games.to_csv("prelim_scores_pct.csv")
print(games.head())