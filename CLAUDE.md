# CLAUDE.md — Gym Churn Prediction (HUST)

Tài liệu này cung cấp ngữ cảnh kỹ thuật đầy đủ cho AI assistant khi làm việc trong repo này.
Đọc kỹ trước khi thực hiện bất kỳ thay đổi nào.

---

## 1. Tổng quan Dự án

| Thông tin | Chi tiết |
|---|---|
| **Bài toán** | Binary Classification — Dự đoán học viên gym có Churn hay không |
| **Nguồn dữ liệu** | Nghiên cứu PNAS 2023: *"Habit formation in the wild: Evidence from gym attendance"* |
| **Quy mô** | ~8.7M dòng thô → 6,327 học viên sau ETL |
| **Ngưỡng Churn** | **78 ngày vắng mặt** (xác suất quay lại < 50%) |
| **Tỷ lệ Churn** | ~78.14% (class imbalance nghiêm trọng) |
| **KPI mô hình** | Macro F1-Score > 0.5519 (Baseline: Logistic Regression) |
| **Thời gian dữ liệu** | 2016-01-01 đến 2019-02-01 |
| **Cutoff date** | `2019-02-01` (dùng để tính `recency` và nhãn `is_churn`) |

---

## 2. Cấu trúc thư mục

```
gym-churn-prediction/
├── CLAUDE.md                        ← File này
├── README.md
├── requirements.txt
│
├── Data/                            # Dữ liệu thô — KHÔNG commit
│   ├── weather.RData                # Log điểm danh hàng ngày (~8.7M dòng)
│   ├── gym_demo_auc.csv             # Nhân khẩu học học viên
│   ├── Census_Data.csv              # Kinh tế - xã hội theo ZipCode
│   └── pptdata.csv                  # Dữ liệu thực nghiệm (nhóm can thiệp)
│
├── dataMaster/
│   └── gym_churn_master_final.csv   # ← GOLD STANDARD (6,327 hàng × 15 features)
│
├── scripts/                         # ETL & Analysis pipeline
│   ├── build_master_dataset.py      # Pipeline tổng hợp chính
│   ├── find_churn_threshold.py      # Tính ngưỡng Churn từ xác suất quay lại
│   ├── extract_mvp_data.R           # Đọc và lọc dữ liệu RData
│   └── filter_weather.py            # Lọc dữ liệu thời tiết
│
├── notebooks/
│   ├── 04_final_data_eda.ipynb      # EDA toàn diện
│   ├── 05_Modeling_Template.ipynb   # Template chuẩn — KHÔNG sửa Phần 1,2,3
│   └── 05B_XGBoost_Minh.ipynb      # Notebook cá nhân (branch: Minh-Gradient-Boosting)
│
├── document/                        # Tài liệu kỹ thuật
│   ├── TEAM_MODELING_GUIDE.md       # Hướng dẫn chi tiết cho từng thành viên
│   ├── TEAM_TASK_ASSIGNMENT.txt     # Quy trình làm việc nhóm
│   ├── DATA_AUDIT_REPORT.md         # Phân tích cấu trúc dữ liệu nguồn
│   ├── DATA_REPORT_SUMMARY.md       # Giải thích ý nghĩa từng feature
│   ├── CHURN_PREDICTION_PLAN.md     # Kế hoạch phân tích ban đầu
│   └── PROJECT_CONTEXT_FOR_AGENTS.md
│
├── src/
│   └── analysis.py                  # Helper functions
│
├── data_analysis/                   # Output phân tích (CSV/stats)
├── data_samples/                    # Mẫu dữ liệu nhỏ để test
└── reports/figures/                 # Biểu đồ output
```

---

## 3. Môi trường & Phụ thuộc

### Runtime
- **Python:** 3.9+ (xem `.venv/` — đã có sẵn)
- **R:** Cần thiết chỉ để chạy `extract_mvp_data.R`

### Cài đặt
```bash
# Kích hoạt virtualenv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
pip install xgboost  # Chưa có trong requirements.txt — cần thêm thủ công
```

> **Lưu ý:** `xgboost` hiện chưa có trong `requirements.txt`. Nếu sửa file này, hãy thêm vào.

### Thư viện chính
| Thư viện | Mục đích |
|---|---|
| `pandas`, `numpy` | Xử lý dữ liệu |
| `pyreadr` | Đọc file `.RData` của R |
| `scikit-learn` | ML models (RF, SVM, MLP, Logistic Reg) |
| `xgboost` | XGBoost classifier |
| `matplotlib`, `seaborn` | Visualization |
| `scipy` | Thống kê |

---

## 4. Schema Dữ liệu Master

File: `dataMaster/gym_churn_master_final.csv` — **6,327 hàng, mỗi hàng là 1 học viên duy nhất**

### Features đầu vào (X)
| Tên cột | Kiểu | Mô tả | Ghi chú |
|---|---|---|---|
| `short_p_id` | int | Primary key học viên | **Loại khỏi X khi train** |
| `total_visits` | int | Tổng số buổi tập | Behavioral |
| `max_streak` | int | Chuỗi ngày tập dài nhất | Behavioral |
| `avg_time_lag` | float | Trung bình số ngày giữa các lần tập | Behavioral |
| `visits_per_month` | float | Tần suất tập hàng tháng | Behavioral |
| `recency` | float | Ngày kể từ lần tập cuối đến cutoff | ⚠️ XEM LƯU Ý BÊN DƯỚI |
| `seniority_days` | int | Số ngày từ lần đầu đến lần cuối đi tập | Behavioral |
| `attendance_momentum` | float | Tỷ lệ tập 30 ngày cuối / 30 ngày trước | Feature Engineering |
| `weekend_ratio` | float | Tỷ lệ buổi tập vào cuối tuần | Feature Engineering |
| `attendance_variance` | float | Độ lệch chuẩn của khoảng cách các buổi tập | Feature Engineering |
| `age` | float | Tuổi học viên | Demographic |
| `gender` | str | Giới tính (`M`/`F`/`U`) | Demographic — Encode trước khi train |
| `main_density_class` | str | Loại khu vực sống | Demographic — Encode trước khi train |
| `att_rate` | float | Tỷ lệ chuyên cần tổng quát | Demographic |
| `income` | float | Thu nhập bình quân khu vực (Census) | Economic |
| `population_density_sq_mi` | float | Mật độ dân cư | Economic |

### Target (y)
| Tên cột | Kiểu | Mô tả |
|---|---|---|
| `is_churn` | int (0/1) | `1` = Churn (recency > 78 ngày), `0` = Active |

---

## 5. Quy tắc Quan trọng (CRITICAL RULES)

### ⚠️ Data Leakage — `recency`
> Biến `recency` = `CUTOFF_DATE - last_visit` **trực tiếp xác định** nhãn `is_churn`.  
> `is_churn = 1` khi và chỉ khi `recency > 78`.  
> **PHẢI loại `recency` khỏi feature matrix (X) trước khi train.** Để `recency` trong X là data leakage nghiêm trọng — mô hình sẽ "nhìn thấy câu trả lời".

### 📏 Các biến cần Scale (StandardScaler)
- **BẮT BUỘC scale:** SVM (`SVC`), MLP (`MLPClassifier`)
- **Không cần scale:** Random Forest, XGBoost (tree-based, scale-invariant)
- Dùng biến chuẩn hóa: `X_train_scaled`, `X_test_scaled` (đã có trong Template)

### 🔒 Không sửa Phần 1, 2, 3 của Notebook Template
- **Phần 1:** Load dữ liệu Master
- **Phần 2:** Train/Test split với `random_state=42` + StandardScaler
- **Phần 3:** Hàm `evaluate_model()` — chuẩn đánh giá chung
- Chỉ viết code mô hình riêng ở **Phần 4**

### 🔑 Join keys
- `short_p_id` (numeric): nối Weather ↔ Demo
- `customer_postal` (Demo) ↔ `ZipCode` (Census): **phải group Census theo ZipCode trước khi join**

---

## 6. ETL Pipeline

Chạy theo thứ tự:
```bash
# Bước 1 (nếu cần extract từ RData)
Rscript scripts/extract_mvp_data.R

# Bước 2 (tùy chọn): Tìm ngưỡng Churn
python scripts/find_churn_threshold.py

# Bước 3: Build Master Dataset
python scripts/build_master_dataset.py
```

Output: `dataMaster/gym_churn_master_final.csv`

**Cutoff date:** `2019-02-01` — được hardcode trong cả 2 scripts, thay đổi ở đây nếu cần.

---

## 7. Phân công Mô hình (Nhóm 5 người)

| Branch | Thành viên | Mô hình | Dữ liệu dùng |
|---|---|---|---|
| `main` | Trưởng nhóm | Logistic Regression (Baseline) | `X_train` |
| TBD | Người 2 | Random Forest | `X_train` |
| `Minh-Gradient-Boosting` | Minh | XGBoost | `X_train` |
| TBD | Người 4 | SVM | `X_train_scaled` |
| `Thanh-MLP` | Thanh | MLP | `X_train_scaled` |

### Hyperparameters gợi ý cho XGBoost (Minh)
```python
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'scale_pos_weight': [3.5]  # Xử lý class imbalance
}
```

---

## 8. Metric & Đánh giá

- **Metric chính:** `Macro F1-Score` (do class imbalance)
- **Baseline cần vượt:** `F1 = 0.5519` (Logistic Regression)
- **Hàm đánh giá chuẩn:** `evaluate_model(model, X_test, y_test)` (định nghĩa trong Phần 3 Template)
- **Output bắt buộc:** Classification Report + Confusion Matrix

```python
# Đúng — dùng evaluate_model để đảm bảo đồng nhất
evaluate_model(best_model, X_test, y_test)

# Sai — không tự tính riêng
accuracy_score(y_test, y_pred)
```

---

## 9. Git Workflow

```bash
# Mỗi thành viên làm việc trên branch riêng
git checkout -b TenBan-ModelName      # Tạo branch
git add notebooks/05X_Model_Ten.ipynb
git commit -m "feat: Add XGBoost model with GridSearch results"
git push origin TenBan-ModelName

# Không push trực tiếp lên main
```

**Các branch hiện tại:**
- `main` — baseline + infrastructure
- `Minh-Gradient-Boosting` — XGBoost (đang active)
- `Thanh-MLP` — MLP

---

## 10. Những việc AI KHÔNG nên làm

1. ❌ Đọc hoặc in nội dung file `.env` hay credentials
2. ❌ Sửa **Phần 1, 2, 3** của `05_Modeling_Template.ipynb`
3. ❌ Để biến `recency` trong feature matrix X khi train (data leakage)
4. ❌ Join Census trực tiếp với Demo mà không group by ZipCode trước
5. ❌ Commit dữ liệu thô từ thư mục `Data/` lên Git
6. ❌ Thay đổi `random_state=42` trong train/test split (đảm bảo so sánh công bằng)

---

*Tài liệu này được tạo tự động dựa trên review kỹ thuật toàn diện.*  
*Cập nhật lần cuối: 21/05/2026*
