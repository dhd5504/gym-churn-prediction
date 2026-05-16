import pandas as pd
import os

# 1. Path Configuration
DATA_DIR = os.path.join('..', 'data_analysis')
GYM_DATA = os.path.join(DATA_DIR, 'gym_data_sample.csv')
CENSUS_DATA = os.path.join(DATA_DIR, 'Census_Data.csv')

def run_pipeline():
    print("--- 1. Loading Data ---")
    gym_df = pd.read_csv(GYM_DATA)
    
    # Keeping only important columns to save RAM and clean the dataset
    census_cols = ['short_p_id', 'gender', 'age', 'average_household_income', 
                   'population_density_sq_mi', 'customer_city']
    census_df = pd.read_csv(CENSUS_DATA, usecols=census_cols)
    
    print("--- 2. Preprocessing & Cleaning ---")
    gym_df['date'] = pd.to_datetime(gym_df['date'])
    gym_df['time_lag'] = pd.to_numeric(gym_df['time_lag'], errors='coerce')

    # Clean Census columns: Remove $ and , then convert to float
    for col in ['average_household_income', 'population_density_sq_mi']:
        if col in census_df.columns:
            census_df[col] = pd.to_numeric(census_df[col].astype(str).str.replace('[\$,]', '', regex=True), errors='coerce')
    
    print("--- 3. Merging Datasets ---")
    combined_df = pd.merge(gym_df, census_df, on='short_p_id', how='inner')
    
    # Analyze Churn Risk
    total_users = combined_df['short_p_id'].nunique()
    churn_risk_users = combined_df[combined_df['time_lag'] > 30]['short_p_id'].nunique()
    
    print(f"\nResults:")
    print(f"- Total records: {len(combined_df)}")
    print(f"- Unique customers: {total_users}")
    print(f"- Avg Income: {combined_df['average_household_income'].mean():.2f}")
    
    print(f"\nChurn Statistics:")
    print(f"- Customers with high risk (break > 30 days): {churn_risk_users}")
    if total_users > 0:
        print(f"- Risk Ratio: {(churn_risk_users/total_users)*100:.2f}%")
    
    # Save cleaned file
    output_path = os.path.join(DATA_DIR, 'final_churn_data.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"\n--- Cleaned data saved to: {output_path} ---")

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
