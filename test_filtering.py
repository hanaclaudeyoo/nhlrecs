import pandas as pd

df = pd.read_csv("prelim_scores.csv")
print(f"{len(df)} total games in 2023-24 regular season.")

df = df[df["total_goals"] > 7]
print(f"{len(df)} games w/ 7 or more total goals.")

df = df[df["final_goal_diff"] < 3]
print(f"{len(df)} games w/ 2 or less final goal differential.")

df = df[df["last_streak"] < 3]
print(f"{len(df)} games ending in a team scoring 2 or less in a row.")

df = df[df["max_winner_lead"] < 3]
print(f"{len(df)} games where the winner leads by less than 3.")

df = df[df["lead_changes"] > 2]
print(f"{len(df)} games w/ at least 2 lead changes.")

print(df.to_string())