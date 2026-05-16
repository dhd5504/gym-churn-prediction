# Project Context: Gym Churn Prediction & Habit Formation

This document provides a comprehensive overview of the project for future AI agents to understand the context, data structure, and goals.

---

## 1. Project Overview
*   **Topic:** Predicting member churn and analyzing habit formation in a gym environment.
*   **Goal:** Build a Machine Learning model to identify members at high risk of quitting and provide research-based insights.
*   **Source:** Based on the scientific study *"Habit formation in the wild: Evidence from gym attendance"* (PNAS 2023).

## 2. Data Environment & Structure
*   **Raw Data Directory:** `c:/GitRepo/HUST/dataAnalyst/Data/`
*   **Sample/MVP Directory:** `c:/GitRepo/HUST/dataAnalyst/data_samples/`
*   **Core Tables:**
    1.  **Behavioral Log (`weather.RData`):** Daily check-in data (`attended` 0/1). Includes pre-calculated study variables like `streak`, `time_lag`, `last7days_attendance`.
    2.  **Demographics (`gym_demo_auc.csv`):** `age`, `gender`, `att_rate`.
    3.  **Socio-economics (`Census_Data.csv`):** Regional income and density based on `ZipCode`.
    4.  **Experimental (`pptdata.csv`):** Weekly behavior and intervention groups (`exp_condition`).

## 3. Key Technical Metadata
*   **Timeframe:** 2016-01-01 to 2019-02-01 (Optimized period).
*   **Cut-off Date:** **2019-02-01** (Last date in system).
*   **Final Master Dataset:** 
    *   **Location:** `dataMaster/gym_churn_master_final.csv`
    *   **Unique Members:** **6,327** (After deduplication).
    *   **Churn Rate:** **78.14%**.
*   **CRITICAL FIX (Deduplication):** The raw `Census_Data.csv` contains multiple entries per ZipCode. Future agents **MUST** aggregate (mean) census data by ZipCode before merging with demographics to avoid data explosion.
*   **Join Keys:** 
    *   `short_p_id` (Numeric): Primary key for behavior and demo.
    *   `ZipCode` / `customer_postal`: Link to Census data.

## 4. Problem Formulation (Machine Learning)
*   **Target Variable:** `is_churn` (1 = Left, 0 = Active).
*   **Churn Definition:** Last visit > 78 days ago.
*   **High-Value Features:** `attendance_momentum` (velocity of visits), `weekend_ratio`, `attendance_variance`.

## 5. Instructions for Future Agents
*   **Data Integrity:** Always check for `short_p_id` uniqueness in the master dataset.
*   **Mapping:** Ensure `ZipCode` in Census is cleaned (numeric) and aggregated.
*   **Logic:** The current 6,327-row dataset is the "Gold Standard" for training models in this repository.

---
**Last Updated:** 17/05/2026
**Created by:** Antigravity AI Expert
