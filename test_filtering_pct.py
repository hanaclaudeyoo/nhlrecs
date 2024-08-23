import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_csv("prelim_scores_pct.csv")
print(f"{len(df)} total games.")

df = df[df["total_goals"] >= 0.7]
print(f"{len(df)} games after filtering for scoring.")

print(df.head())