import pyreadr
import pandas as pd
import numpy as np
import os

# Config
WEATHER_PATH = "Data/weather.RData"
DEMO_PATH = "Data/gym_demo_auc.csv"
CENSUS_PATH = "Data/Census_Data.csv"
OUTPUT_PATH = "dataMaster/gym_churn_master_final.csv" # Changed to CSV for user viewing convenience
CUTOFF_DATE = pd.to_datetime("2019-02-01")
CHURN_THRESHOLD = 78  # Days of absence to be labeled as Churn (based on 50% return prob)

print("--- STARTING ETL PIPELINE ---")

# 1. Process Weather Data (Behavior)
print("Loading and Aggregating Weather data (Filtered 2016-2019)...")
result = pyreadr.read_r(WEATHER_PATH)
weather = result[list(result.keys())[0]]
weather['date'] = pd.to_datetime(weather['date'])
weather = weather[weather['date'] >= '2016-01-01']

# Feature Engineering: Weekend Ratio
weather['is_weekend'] = weather['date'].dt.dayofweek >= 5

# Feature Engineering: Recent Momentum (Last 30 days vs Previous 30 days)
# Using CUTOFF_DATE as 'Today'
m_end = CUTOFF_DATE
m_mid = CUTOFF_DATE - pd.Timedelta(days=30)
m_start = CUTOFF_DATE - pd.Timedelta(days=60)

weather['in_last_30'] = (weather['date'] > m_mid) & (weather['attended'] == 1)
weather['in_prev_30'] = (weather['date'] > m_start) & (weather['date'] <= m_mid) & (weather['attended'] == 1)

print("Aggregating detailed behavior features...")
behavior = weather.groupby('short_p_id').agg(
    total_days_obs=('date', 'count'),
    first_visit=('date', 'min'),
    last_visit=('date', 'max'),
    total_visits=('attended', 'sum'),
    max_streak=('streak', 'max'),
    avg_time_lag=('time_lag', 'mean'),
    std_time_lag=('time_lag', 'std'),
    weekend_visits=('is_weekend', lambda x: (x & weather.loc[x.index, 'attended']).sum()),
    visits_last_30=('in_last_30', 'sum'),
    visits_prev_30=('in_prev_30', 'sum')
).reset_index()

# Calculate derived behavior features
behavior['seniority_days'] = (behavior['last_visit'] - behavior['first_visit']).dt.days
behavior['visits_per_month'] = behavior['total_visits'] / (behavior['total_days_obs'] / 30)
behavior['recency'] = (CUTOFF_DATE - behavior['last_visit']).dt.days

# New "Premium" Features
behavior['weekend_ratio'] = behavior['weekend_visits'] / (behavior['total_visits'] + 1e-5)
behavior['attendance_momentum'] = (behavior['visits_last_30'] + 1) / (behavior['visits_prev_30'] + 1)
behavior['attendance_variance'] = behavior['std_time_lag'].fillna(0)

# Labeling Churn
behavior['is_churn'] = (behavior['recency'] > CHURN_THRESHOLD).astype(int)

# 2. Process Demo Data
print("Loading Demographics...")
demo = pd.read_csv(DEMO_PATH)
demo = demo[['short_p_id', 'age', 'gender', 'main_density_class', 'customer_postal', 'att_rate']]

# 3. Process Census Data
print("Loading and Cleaning Census data...")
census = pd.read_csv(CENSUS_PATH)
# Clean average_household_income (remove $ and ,)
if census['average_household_income'].dtype == 'object':
    census['income'] = census['average_household_income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
else:
    census['income'] = census['average_household_income']

# CRITICAL FIX: Aggregate census by ZipCode to avoid duplication
print("Aggregating census by ZipCode...")
census = census.groupby('ZipCode').agg({
    'income': 'mean',
    'population_density_sq_mi': 'mean'
}).reset_index()

# 4. Final Merging
print("Merging all tables...")
master = pd.merge(behavior, demo, on='short_p_id', how='left')
master = pd.merge(master, census, left_on='customer_postal', right_on='ZipCode', how='left')

# Drop redundant or intermediate columns
cols_to_drop = ['ZipCode', 'first_visit', 'last_visit', 'total_days_obs', 'weekend_visits', 'visits_last_30', 'visits_prev_30', 'std_time_lag']
master = master.drop(columns=cols_to_drop)

# Final Safety Check: Drop any remaining duplicates
master = master.drop_duplicates(subset=['short_p_id'])

# Handling missing values (Simple Imputation)
master['income'] = master['income'].fillna(master['income'].median())
master['age'] = master['age'].fillna(master['age'].median())
master['gender'] = master['gender'].fillna('U') # Unknown
master['main_density_class'] = master['main_density_class'].fillna('U') # Unknown
master['population_density_sq_mi'] = master['population_density_sq_mi'].fillna(master['population_density_sq_mi'].median())

# 5. Export
print(f"Exporting Master Dataset to {OUTPUT_PATH}...")
try:
    master.to_csv(OUTPUT_PATH, index=False)
    print("Export successful!")
except Exception as e:
    print(f"Export failed ({e}).")

print("\n--- MASTER DATASET SUMMARY ---")
print(f"Total Members: {len(master):,}")
print(f"Churn Rate: {master['is_churn'].mean():.2%}")
print(f"Final Features: {master.columns.tolist()}")
print("Pipeline Completed.")
