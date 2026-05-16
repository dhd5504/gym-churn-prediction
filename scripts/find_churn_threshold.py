import pyreadr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Config
DATA_PATH = "Data/weather.RData"
CUTOFF_DATE = pd.to_datetime("2019-01-01")
OUTPUT_PLOT = "reports/figures/return_probability_curve.png"
OUTPUT_DIR = "reports/figures"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("Reading weather.RData...")
result = pyreadr.read_r(DATA_PATH)
# The object name in RData might be 'gym_data' or 'weather'
df = result[list(result.keys())[0]]

print(f"Total rows: {len(df):,}")

# Keep only necessary columns to save RAM and filter for 2016-2019
df = df[['short_p_id', 'date', 'attended']]
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= '2016-01-01']

# Filter only days where they attended
visits = df[df['attended'] == 1].sort_values(['short_p_id', 'date'])

print(f"Total visits: {len(visits):,}")

# Calculate gaps between visits for each user
visits['prev_date'] = visits.groupby('short_p_id')['date'].shift(1)
visits['gap'] = (visits['date'] - visits['prev_date']).dt.days

# Identify the last visit for each user
last_visits = visits.groupby('short_p_id').tail(1).copy()
last_visits['gap_to_cutoff'] = (CUTOFF_DATE - last_visits['date']).dt.days

# Analysis: Probability of eventual return given N days of absence
# We want to know: Among all instances where a user has been away for >= N days,
# what percentage eventually came back?

max_days = 180
prob_data = []

# All "closed" gaps (user returned)
all_gaps = visits['gap'].dropna().values

# All "open" gaps (user hasn't returned as of cutoff)
open_gaps = last_visits['gap_to_cutoff'].values

for n in range(1, max_days + 1):
    # Total instances where someone was away for >= n days:
    # 1. Any closed gap that was >= n
    # 2. Any open gap that is >= n
    num_away_n = (all_gaps >= n).sum() + (open_gaps >= n).sum()
    
    # Among those, how many eventually returned?
    # Only the ones in 'all_gaps' returned.
    num_returned = (all_gaps >= n).sum()
    
    if num_away_n > 0:
        prob = num_returned / num_away_n
    else:
        prob = 0
        
    prob_data.append({'days_absent': n, 'return_prob': prob})

prob_df = pd.DataFrame(prob_data)

# Print results
print("\nReturn Probability by Days Absent:")
print(prob_df.head(10))
print("...")
print(prob_df.tail(10))

# Identify "Point of No Return" (where prob < 50%)
threshold_50 = prob_df[prob_df['return_prob'] < 0.50]
if not threshold_50.empty:
    suggested_threshold = threshold_50.iloc[0]['days_absent']
    print(f"\n[INSIGHT] Return probability drops below 50% at day: {suggested_threshold}")
else:
    suggested_threshold = "Not reached in 180 days"
    print("\n[INSIGHT] Return probability stays above 50% even after 180 days.")

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(prob_df['days_absent'], prob_df['return_prob'], marker='o', linestyle='-', color='b')
plt.axhline(y=0.50, color='r', linestyle='--', label='50% Threshold')
plt.title('Probability of Eventual Return by Days of Absence')
plt.xlabel('Days Absent (N)')
plt.ylabel('Probability of Return')
plt.grid(True)
plt.legend()
plt.savefig(OUTPUT_PLOT)
print(f"Plot saved to: {OUTPUT_PLOT}")

# Save results to CSV for later use in report
prob_df.to_csv("data_analysis/return_probability_stats.csv", index=False)
print("Stats saved to: data_analysis/return_probability_stats.csv")
