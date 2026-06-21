"""
Export K-Means Segmentation Models
-----------------------------------
Chạy script này sau khi đã train xong trong notebook 06_Customer_Segmentation.ipynb.

Cách dùng:
    cd C:/GitRepo/HUST/dataAnalyst
    python scripts/export_kmeans_model.py

Output:
    C:/GitRepo/DATN/gym-ai-management-system/ai-service/app/core/churn_model/kmeans_segment_model.pkl
    C:/GitRepo/DATN/gym-ai-management-system/ai-service/app/core/churn_model/kmeans_scaler.pkl
"""

import os
import sys

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

# ── Paths ─────────────────────────────────────────────────────────────────────

DATA_PATH   = os.path.join(os.path.dirname(__file__), '..', 'Data', 'gym_churn_master_final.parquet')
OUTPUT_DIR  = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'DATN',
    'gym-ai-management-system', 'ai-service', 'app', 'core', 'churn_model'
)
KMEANS_OUT  = os.path.join(OUTPUT_DIR, 'kmeans_segment_model.pkl')
SCALER_OUT  = os.path.join(OUTPUT_DIR, 'kmeans_scaler.pkl')

# Features phải khớp với SEGMENT_FEATURES trong segment_predictor.py
FEATURES = [
    'attendance_momentum',
    'avg_time_lag',
    'total_visits',
    'max_streak',
    'seniority_days',
    'att_rate',
]

OPTIMAL_K = 3   # Validated bởi Elbow + Silhouette trong notebook 06

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"[1/5] Loading data from: {DATA_PATH}")
    if not os.path.exists(DATA_PATH):
        # Fallback: thử tìm file CSV
        csv_path = DATA_PATH.replace('.parquet', '.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            print(f"       → Loaded CSV: {csv_path}")
        else:
            print(f"ERROR: Data file not found at {DATA_PATH}")
            sys.exit(1)
    else:
        df = pd.read_parquet(DATA_PATH)

    print(f"       -> Total records: {len(df)}")

    print("[2/5] Filtering churned members (is_churn == 1)...")
    df_churn = df[df['is_churn'] == 1].copy()
    print(f"       -> Churned records: {len(df_churn)}")

    print("[3/5] Preprocessing features...")
    X = df_churn[FEATURES].fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(f"[4/5] Training K-Means with K={OPTIMAL_K}...")
    kmeans = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    sil_score = silhouette_score(X_scaled, labels)
    print(f"       -> Silhouette Score: {sil_score:.4f}")
    print(f"       -> Cluster distribution: {dict(zip(*np.unique(labels, return_counts=True)))}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"[5/5] Exporting models...")
    joblib.dump(kmeans, KMEANS_OUT)
    joblib.dump(scaler, SCALER_OUT)
    print(f"       -> K-Means : {KMEANS_OUT}")
    print(f"       -> Scaler  : {SCALER_OUT}")
    print("\n[OK] Export completed! ai-service will auto-load models on next restart.")



if __name__ == '__main__':
    main()
