# BÁO CÁO DỰ ÁN: DỰ ĐOÁN KHÁCH HÀNG RỜI BỎ PHÒNG GYM (CHURN PREDICTION)

**Môn học:** Khoa học Dữ liệu  
**Trường:** Đại học Bách Khoa Hà Nội (HUST)

---

## 1. GIỚI THIỆU ĐỀ TÀI

### 1.1 Bài toán Churn là gì?

Churn (hay còn gọi là "rời bỏ khách hàng") là hiện tượng khách hàng ngừng sử dụng dịch vụ trong một khoảng thời gian nhất định. Trong lĩnh vực phòng tập thể dục (Gym/Fitness), một học viên được xác định là đã "churn" khi họ không quay lại tập luyện sau **78 ngày** kể từ buổi tập cuối cùng.

### 1.2 Vì sao cần dự đoán Churn?

Giữ chân khách hàng cũ luôn là bài toán kinh doanh cốt lõi trong mọi ngành dịch vụ. Nghiên cứu cho thấy chi phí để thu hút một khách hàng mới cao hơn **5–7 lần** so với chi phí giữ chân một khách hàng hiện có. Với một phòng gym, việc phát hiện sớm những học viên có nguy cơ nghỉ tập giúp:

- **Triển khai chiến dịch retention kịp thời** (gọi điện chăm sóc, tặng ưu đãi, mời buổi tập thử miễn phí).
- **Tối ưu hóa doanh thu** và dự báo được lượng khách hàng ổn định.
- **Cá nhân hóa dịch vụ** dựa trên hành vi tập luyện của từng học viên.

### 1.3 Mục tiêu đề tài

Xây dựng và so sánh các mô hình Machine Learning để **dự đoán học viên có khả năng nghỉ tập**, từ đó hỗ trợ ban quản lý phòng gym đưa ra quyết định can thiệp kịp thời.

**Metric đánh giá chính:** **Macro F1-Score** — được chọn thay cho Accuracy vì dữ liệu có sự mất cân bằng nghiêm trọng (khoảng 78% học viên trong dataset là đã churn).

---

## 2. MÔ TẢ DỮ LIỆU (DATASET)

### 2.1 Nguồn dữ liệu

Tập dữ liệu sử dụng là `gym_churn_master_final.csv` — dữ liệu log thực tế từ hệ thống quản lý thành viên của một chuỗi phòng gym.

- **Số lượng bản ghi (sau làm sạch):** 6,322 học viên  
- **Số lượng đặc trưng:** 18 cột

### 2.2 Mô tả các đặc trưng (Feature Description)

| Feature | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `short_p_id` | int | ID định danh học viên |
| `total_visits` | float | Tổng số buổi tập |
| `max_streak` | float | Chuỗi ngày tập liên tiếp dài nhất |
| `avg_time_lag` | float | Khoảng cách trung bình giữa các buổi tập (ngày) |
| `seniority_days` | int | Thâm niên thành viên (ngày) |
| `visits_per_month` | float | Số buổi tập trung bình mỗi tháng |
| `recency` | int | Số ngày kể từ lần tập cuối (**bị loại — Data Leakage**) |
| `weekend_ratio` | float | Tỷ lệ buổi tập vào cuối tuần |
| `attendance_momentum` | float | Động lực tập luyện (tỷ số gần đây/lịch sử) |
| `attendance_variance` | float | Độ biến thiên tần suất tập |
| `age` | float | Tuổi học viên |
| `gender` | string | Giới tính (F/M/I) |
| `main_density_class` | string | Loại khu vực dân cư |
| `customer_postal` | int | Mã bưu điện |
| `att_rate` | float | Tỷ lệ chuyên cần (buổi tham dự / tổng buổi) |
| `income` | float | Thu nhập ước tính của khu vực |
| `population_density_sq_mi` | float | Mật độ dân số khu vực |
| **`is_churn`** | **int** | **Nhãn mục tiêu (0 = Ở lại, 1 = Nghỉ tập)** |

### 2.3 Biến mục tiêu (Target Variable)

| Nhãn | Ý nghĩa | Tỷ lệ |
|---|---|---|
| 0 | Học viên đang hoạt động (Ở lại) | ~22% |
| 1 | Học viên đã nghỉ tập (Churn) | ~78% |

> ⚠️ **Mất cân bằng dữ liệu (Class Imbalance):** ~78% là Churn. Đây là thách thức chính yêu cầu xử lý đặc biệt trong quá trình huấn luyện mô hình.

---

## 3. TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING)

### 3.1 Kiểm tra Missing Values

Sau khi kiểm tra, **không có giá trị bị thiếu (null)** trong dataset. Đây là dữ liệu log hệ thống được thu thập tự động nên có tính toàn vẹn cao.

### 3.2 Xử lý Outliers

Phát hiện các bản ghi có `avg_time_lag` cực kỳ lớn (lên tới 1,696 ngày). Sau khi điều tra, các bản ghi này là "tài khoản bóng ma" — không phản ánh hành vi tập luyện thực tế. Nhóm đã **xóa 2 bản ghi ngoại lai** này.

### 3.3 Xử lý Data Leakage — Loại bỏ cột `recency`

> 🚨 **Quan trọng nhất trong toàn bộ quá trình tiền xử lý.**

Nhãn `is_churn = 1` được định nghĩa khi `recency > 78` ngày. Đưa `recency` vào đặc trưng huấn luyện sẽ gây **Data Leakage** — mô hình sẽ "gian lận" bằng cách dùng thông tin của nhãn để đoán nhãn. Quyết định: **loại bỏ hoàn toàn cột `recency`**.

### 3.4 Encoding và Chuẩn hóa

- **One-Hot Encoding** cho biến phân loại: `gender`, `main_density_class`.
- **StandardScaler** cho LR, SVM, MLP (fit trên Train, transform trên cả Train và Test).

### 3.5 Chia tập Train/Test

| Tham số | Giá trị |
|---|---|
| Tỷ lệ | 80% Train / 20% Test |
| `random_state` | 42 |
| `stratify=y` | Giữ nguyên tỷ lệ nhãn |
| Số mẫu Train | 5,057 |
| Số mẫu Test | 1,264 |

### 3.6 Xử lý Class Imbalance

- **LR, SVM, MLP:** `class_weight='balanced'`
- **XGBoost:** `scale_pos_weight = n_negative / n_positive`
- **Random Forest:** `class_weight='balanced'`

---

## 4. PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA)

### 4.1 Thống kê mô tả

| Đặc trưng | Mean | Std | Min | Max |
|---|---|---|---|---|
| `total_visits` | 158.21 | 132.30 | 1 | 841 |
| `avg_time_lag` | 26.10 | 52.77 | 1.03 | 891 |
| `seniority_days` | 689 | 249 | 0 | 1,126 |
| `att_rate` | 0.24 | 0.16 | 0.02 | 0.93 |
| `age` | 35.76 | 12.68 | 12 | 81 |

### 4.2 Key Insights từ EDA

1. **`att_rate` thấp → Churn cao:** Học viên có tỷ lệ chuyên cần dưới 15% có xác suất nghỉ tập gần như tuyệt đối.
2. **`avg_time_lag` lớn → Dấu hiệu chán nản:** Khoảng cách giữa các buổi tập càng dài, học viên càng dễ bỏ cuộc.
3. **`attendance_momentum`:** Tỷ số "gần đây so với lịch sử" là chỉ báo hành vi mạnh nhất.
4. **Tuổi trung bình 35.7 tuổi:** Khách hàng chủ yếu là dân văn phòng trong độ tuổi lao động.

---

## 5. XÂY DỰNG MÔ HÌNH

### 5.1 Các mô hình sử dụng

| STT | Mô hình | Lý do lựa chọn |
|---|---|---|
| 1 | **Logistic Regression** | Baseline tuyến tính, dễ diễn giải |
| 2 | **Support Vector Machine** | Mạnh với dữ liệu nhiều chiều |
| 3 | **MLP (Neural Network)** | Học đặc trưng phi tuyến |
| 4 | **XGBoost** | Gradient boosting mạnh, phổ biến |
| 5 | **Random Forest** | Ensemble ổn định, miễn nhiễm outliers |

### 5.2 Tối ưu tham số (GridSearchCV)

- **Logistic Regression:** `C=0.01`, `penalty='l2'`
- **XGBoost:** `learning_rate=0.01`, `max_depth=3`, `n_estimators=100`

---

## 6. ĐÁNH GIÁ VÀ SO SÁNH MÔ HÌNH

### 6.1 Bảng kết quả tổng hợp

| Mô hình | Accuracy | Macro F1 | ROC-AUC | Recall (Churn) |
|---|---|---|---|---|
| Logistic Regression | 0.62 | 0.5710 | 0.6926 | 0.61 |
| SVM | 0.92 | 0.8694 | 0.9017 | 0.98 |
| MLP | 0.94 | 0.9128 | 0.9411 | 0.98 |
| XGBoost | 0.96 | 0.9438 | 0.9236 | 1.00 |
| **Random Forest ⭐** | **0.97** | **0.9484** | **0.9419** | **1.00** |

### 6.2 Phân tích từng mô hình

**Logistic Regression (Baseline):**
- Macro F1 = 0.5710 — thất bại vì LR giả định quan hệ tuyến tính, không phù hợp với hành vi churn phi tuyến phức tạp.
- Vai trò: làm mốc so sánh (baseline) cho các mô hình phức tạp hơn.

**SVM:**
- Macro F1 = 0.8694 — cải thiện đáng kể, Recall Churn = 0.98.

**MLP (Neural Network):**
- Macro F1 = 0.9128, ROC-AUC = 0.9411. Mạng nơ-ron `(64, 32)` học được đặc trưng phi tuyến hiệu quả.

**XGBoost:**
- Macro F1 = 0.9438, Recall Churn = 1.00 (không bỏ sót học viên nào).
- `attendance_momentum` là feature quan trọng nhất (importance ≈ 0.78).

**Random Forest ⭐ (Mô hình tốt nhất):**
- **Macro F1 = 0.9484** — cao nhất trong tất cả.
- **Recall Churn = 1.00** — không bỏ sót bất kỳ học viên churn nào.
- Ổn định, ít overfitting, miễn nhiễm với outliers trong dữ liệu.

---

## 7. BUSINESS INSIGHTS

### 7.1 Mô hình khuyến nghị: Random Forest

Với Macro F1 = 0.9484 và Recall = 100%, mô hình đảm bảo **không bỏ sót bất kỳ học viên nào** có nguy cơ nghỉ tập.

### 7.2 Top yếu tố ảnh hưởng đến Churn

1. **`attendance_momentum`** (~78% importance trong XGBoost): Học viên giảm tần suất tập gần đây so với lịch sử = nhóm rủi ro cao nhất.
2. **`seniority_days`** (~22%): Thâm niên thành viên ảnh hưởng đến mức độ gắn kết.
3. **`att_rate`, `avg_time_lag`, `max_streak`**: Các chỉ số hành vi phản ánh sự đều đặn.

### 7.3 Chiến lược Retention cho Gym Manager

**① Hệ thống cảnh báo tự động:**
- Khi `P(Churn) > 0.75` → tạo task CSKH tự động.
- Theo dõi hàng tuần: `att_rate < 15%` và `avg_time_lag > 14 ngày`.

**② Gamification:**
- Thưởng điểm/badge cho chuỗi tập liên tiếp (`max_streak`).
- Voucher khi đạt mốc 30 ngày liên tiếp.

**③ Chăm sóc cá nhân hóa theo mức rủi ro:**
- **Rủi ro cao** (P > 0.75): Gọi điện trực tiếp, tặng 1 buổi PT miễn phí.
- **Rủi ro trung bình** (0.5 < P < 0.75): Email động viên, ưu đãi gia hạn.
- **Đang gắn kết tốt** (P < 0.3): Chương trình referral.

---

## 8. KẾT LUẬN

Dự án đã thành công xây dựng hệ thống dự đoán churn cho phòng gym với pipeline hoàn chỉnh. **Random Forest là mô hình tốt nhất** với Macro F1 = 0.9484 và Recall Churn = 100%, vượt trội hoàn toàn so với baseline (F1 = 0.5710).

**Đóng góp chính:**
- Pipeline chuẩn, chống Data Leakage.
- Xử lý class imbalance hiệu quả.
- So sánh hệ thống 5 mô hình từ tuyến tính đến phi tuyến.
- Business Insights có giá trị thực tiễn.

**Hướng phát triển:**
- Thử nghiệm TimeSeriesSplit để xác minh temporal leakage.
- Thu thập thêm dữ liệu hành vi (loại bài tập, giờ tập).
- Triển khai mô hình thành REST API tích hợp vào CRM.

---

*Báo cáo được thực hiện trong khuôn khổ bài tập lớn môn Khoa học Dữ liệu — HUST.*
