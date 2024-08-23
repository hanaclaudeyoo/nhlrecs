import pandas as pd
import numpy as np


pbp = pd.read_csv("play_by_play_2023_24_lite.csv")
goals = pbp[pbp["event_type"] == "GOAL"]

def streak_analysis(game_id):
    game_goals = goals[goals["game_id"] == game_id]

    streaks = []
    current_team = ""
    for row in game_goals.itertuples(index=False, name="Pandas"):
        print(row.event_team_type)
        if row.event_team_type == current_team:
            streaks[-1] += 1
        else:
            streaks.append(1)
            current_team = row.event_team_type

    print(streaks)
    print(f"# streak changes: {len(streaks) - 1}")
    print(f"longest streak: {max(streaks)}")
    print(f"last streak: {streaks[-1]}")

    mask = np.mod(np.arange(len(streaks)), 2) * 2 - 1
    signed_streaks = mask * streaks
    shift = np.cumsum(signed_streaks)
    print(shift)
    lead_changes = 0
    tied_not_led = 0
    for i in range(len(shift) - 1):
        print(f"{shift[i]} —> {shift[i+1]}")
        if shift[i] * shift[i+1] < 0:
            print("lead change")
            lead_changes += 1
        elif shift[i+1] == 0:
            print("tied")
            tied_not_led += 1
    print(f"# of lead changes: {lead_changes}")
    print(f"# of times tied (w/o changing lead): {tied_not_led}")

    print(current_team)
    print(f"max goal differential: {max(shift)}")
    print(f"min goal differential: {min(shift)}")

    goal_diffs = [0]
    for row in game_goals.itertuples(index=False, name="Pandas"):
        if row.event_team_type == "home":
            goal_diffs.append(goal_diffs[-1] + 1)
        else:
            goal_diffs.append(goal_diffs[-1] - 1)
    print(goal_diffs)
    print(f"max home goal differential: {max(goal_diffs)}")
    print(f"max away goal differential: {min(goal_diffs)}")
    print(f"max winner goal differential: {max(goal_diffs) if goal_diffs[-1] > 0 else min(goal_diffs)}")
    print(f"max loser goal differential: {min(goal_diffs) if goal_diffs[-1] > 0 else max(goal_diffs)}")
    
    print("-----")

# streak_analysis(2023020002)
# streak_analysis(2023020001)
# streak_analysis(2023020003)
# streak_analysis(2023020006)
# streak_analysis(2023020007)


def lead_analysis(game_id):
    game_goals = goals[goals["game_id"] == game_id]

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
    
    lead_changes = 0
    tied_not_led = 0
    print(goal_diffs)
    for i in range(len(goal_diffs) - 1):
        if goal_diffs[i] * goal_diffs[i+1] < 0:
            lead_changes += 1
        if goal_diffs[i+1] == 0:
            tied_not_led += 1
    print(lead_changes)
lead_analysis(2023020002)
lead_analysis(2023020001)
lead_analysis(2023020003)
lead_analysis(2023020006)
lead_analysis(2023020007)
