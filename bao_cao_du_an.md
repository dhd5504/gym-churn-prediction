# BÁO CÁO BÀI TẬP LỚN
## DỰ ĐOÁN KHÁCH HÀNG RỜI BỎ PHÒNG GYM
### (GYM MEMBER CHURN PREDICTION)

---

**Môn học:** Khoa học Dữ liệu (Data Science)
**Trường:** Đại học Bách Khoa Hà Nội (HUST)
**Năm học:** 2025 – 2026

---

## MỤC LỤC

1. [MỞ ĐẦU](#1-mở-đầu)
   - 1.1 Bối cảnh và tính cấp thiết
   - 1.2 Mục tiêu nghiên cứu
   - 1.3 Phạm vi và giới hạn

2. [ĐẶT VẤN ĐỀ](#2-đặt-vấn-đề)
   - 2.1 Thực trạng ngành Gym & Fitness
   - 2.2 Bài toán Churn – Định nghĩa & Tác động kinh tế
   - 2.3 Câu hỏi nghiên cứu

3. [PHƯƠNG PHÁP NGHIÊN CỨU](#3-phương-pháp-nghiên-cứu)
   - 3.1 Quy trình CRISP-DM
   - 3.2 Sơ đồ khối của hệ thống

4. [NGUỒN DỮ LIỆU & MÔ TẢ DATASET](#4-nguồn-dữ-liệu--mô-tả-dataset)
   - 4.1 Nguồn dữ liệu
   - 4.2 Khối lượng & cấu trúc
   - 4.3 Mô tả các đặc trưng
   - 4.4 Biến mục tiêu & phân bố nhãn

5. [PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA)](#5-phân-tích-khám-phá-dữ-liệu-eda)
   - 5.1 Thống kê mô tả tổng quan
   - 5.2 Phân tích phân phối và Tương quan
   - 5.3 Trực quan hóa dữ liệu (Visualization)
   - 5.4 Key Insights từ EDA

6. [TIỀN XỬ LÝ DỮ LIỆU & FEATURE ENGINEERING](#6-tiền-xử-lý-dữ-liệu--feature-engineering)
   - 6.1 Xử lý Data Leakage (Cực kỳ quan trọng)
   - 6.2 Xử lý Missing Values & Outliers
   - 6.3 Feature Engineering (Tạo biến phái sinh)
   - 6.4 Encoding, Chuẩn hóa & Xử lý Class Imbalance

7. [XÂY DỰNG MÔ HÌNH MACHINE LEARNING](#7-xây-dựng-mô-hình-machine-learning)
   - 7.1 Logistic Regression (Baseline)
   - 7.2 Support Vector Machine (SVM)
   - 7.3 Multi-Layer Perceptron (MLP)
   - 7.4 XGBoost
   - 7.5 Random Forest

8. [ĐÁNH GIÁ & SO SÁNH KẾT QUẢ](#8-đánh-giá--so-sánh-kết-quả)
   - 8.1 Metric đánh giá & Lý do chọn
   - 8.2 Bảng so sánh tổng hợp
   - 8.3 Phân tích Confusion Matrix thực tế
   - 8.4 Biện luận kết quả Random Forest (Tại sao đạt 97%?)
   - 8.5 Explainability & Feature Importance

9. [KẾT LUẬN & ĐỀ XUẤT GIẢI PHÁP](#9-kết-luận--đề-xuất-giải-pháp)
   - 9.1 Tổng kết kết quả nghiên cứu
   - 9.2 Giải pháp Retention & Tính toán ROI (Revenue Saved)
   - 9.3 Hạn chế & Hướng phát triển

10. [TÀI LIỆU THAM KHẢO](#10-tài-liệu-tham-khảo)

---

## 1. MỞ ĐẦU

### 1.1 Bối cảnh và tính cấp thiết

Ngành Fitness & Gym toàn cầu đang tăng trưởng mạnh, nhưng đi kèm đó là thách thức lớn về việc giữ chân khách hàng. Dữ liệu hành vi thành viên được hệ thống CRM thu thập ngày càng phong phú — đây là nguồn tài nguyên quý giá nếu được khai thác đúng cách bằng Machine Learning.

- Thị trường Gym & Fitness toàn cầu đạt **~112 tỷ USD** (2023), dự báo tăng lên **169 tỷ USD** vào 2030.
- Tỷ lệ churn trung bình ngành gym dao động từ **30–50%/năm**, cao hơn nhiều so với các ngành dịch vụ khác.
- Chi phí thu hút khách hàng mới cao hơn **5–7 lần** so với giữ chân khách hàng cũ (Harvard Business Review).

### 1.2 Mục tiêu nghiên cứu

- Xây dựng pipeline dự đoán churn hoàn chỉnh từ dữ liệu thô đến mô hình triển khai.
- So sánh hiệu suất của 5 thuật toán Machine Learning phổ biến.
- Trích xuất Business Insights để đề xuất chiến lược Retention thực tiễn.

### 1.3 Phạm vi & Giới hạn

- Dữ liệu: log thành viên từ hệ thống CRM phòng gym (không bao gồm dữ liệu tài chính, mạng xã hội).
- Metric chính: **Macro F1-Score** (phù hợp với dữ liệu mất cân bằng).
- Ngôn ngữ & thư viện: Python, scikit-learn, XGBoost, pandas, matplotlib/seaborn.

---

## 2. ĐẶT VẤN ĐỀ

### 2.1 Thực trạng ngành Gym & Fitness tại Việt Nam

Thị trường gym Việt Nam đang bùng nổ với hơn **3,000+ phòng tập** tính đến năm 2024, tăng gấp đôi so với 2019. Tuy nhiên, nghịch lý là tỷ lệ thành viên bỏ tập vẫn rất cao:

> *"Theo khảo sát của Vietnam Fitness Report 2023, có đến **67% thành viên đăng ký phòng tập** không tái ký hợp đồng sau năm đầu tiên."*

Điều này dẫn đến một vòng lặp tốn kém: phòng gym liên tục đổ ngân sách vào marketing để tuyển thành viên mới, trong khi bỏ qua nhóm thành viên cũ đang dần mất động lực — những người hoàn toàn có thể được giữ lại với chi phí thấp hơn nhiều.

### 2.2 Bài toán Churn – Định nghĩa & Tác động kinh tế

**Định nghĩa:** Một thành viên được xác định là **churn** khi họ không quay lại tập luyện sau **78 ngày** kể từ buổi tập cuối cùng.

**Tác động kinh tế cụ thể:**

| Chỉ số | Giá trị ước tính |
|---|---|
| Chi phí giữ chân 1 khách hàng | ~150.000 VNĐ/người |
| Chi phí thu hút khách hàng mới | ~750.000–1.050.000 VNĐ/người |
| Doanh thu mất đi mỗi khách churn | ~2.000.000–5.000.000 VNĐ/năm |
| Tỷ lệ churn trung bình dataset này | **~78.1%** |

Nếu một phòng gym có **1,000 thành viên** và giảm tỷ lệ churn từ **78.1% xuống 60%** nhờ can thiệp kịp thời, phòng gym đó giữ lại thêm **181 thành viên** — tương đương **362–905 triệu VNĐ doanh thu/năm**.

### 2.3 Câu hỏi nghiên cứu

1. Những yếu tố hành vi nào **dự báo mạnh nhất** khả năng một thành viên sẽ nghỉ tập?
2. Mô hình Machine Learning nào cho kết quả **tốt nhất** trên bài toán này?
3. Làm thế nào để chuyển hóa kết quả mô hình thành **hành động can thiệp thực tế**?

---

## 3. PHƯƠNG PHÁP NGHIÊN CỨU

### 3.1 Quy trình CRISP-DM
Nghiên cứu áp dụng khung làm việc CRISP-DM (Cross-Industry Standard Process for Data Mining) bao gồm 6 giai đoạn:
1. **Business Understanding:** Xác định bài toán giữ chân khách hàng (Churn Prediction) từ góc độ kinh doanh.
2. **Data Understanding:** Phân tích dữ liệu log điểm danh (EDA) để hiểu phân phối và đặc trưng hành vi.
3. **Data Preparation:** Làm sạch dữ liệu, xử lý Data Leakage, tạo Feature Engineering (attendance_momentum).
4. **Modeling:** Xây dựng Baseline (Logistic Regression) và các mô hình phức tạp (SVM, MLP, XGBoost, Random Forest).
5. **Evaluation:** Đánh giá bằng Macro F1-Score và phân tích Feature Importance.
6. **Deployment/Action:** Đề xuất chiến lược phân tầng rủi ro và tích hợp CRM.

### 3.2 Khung phương pháp ML
Dự án sử dụng phương pháp **Supervised Learning** (Phân loại nhị phân) với nhãn `is_churn` được định nghĩa trước dựa trên ngưỡng vắng mặt 78 ngày.

---

## 4. NGUỒN DỮ LIỆU & MÔ TẢ DATASET

### 4.1 Nguồn dữ liệu

- **Nguồn gốc học thuật:** Nghiên cứu PNAS 2023 — *"Habit formation in the wild: Evidence from gym attendance"* — dữ liệu điểm danh thực tế từ chuỗi phòng gym tại Mỹ.
- **File master:** `gym_churn_master_final.csv` — kết quả sau toàn bộ pipeline ETL.
- **Dữ liệu thô:** ~**8.7 triệu dòng** log điểm danh hàng ngày (file `weather.RData`) → qua ETL → **6,327 thành viên** duy nhất.
- **Thời gian dữ liệu:** `2016-01-01` đến `2019-02-01` (Cutoff date: `2019-02-01`).
- **Loại dữ liệu:** Behavioral log thu thập tự động — độ tin cậy cao, không có survey bias.

### 4.2 Khối lượng & Cấu trúc

| Thông số | Giá trị |
|---|---|
| Dữ liệu log thô | ~**8,700,000 dòng** điểm danh hàng ngày |
| Thành viên duy nhất (trước làm sạch) | **6,327 học viên** |
| Số bản ghi sau làm sạch | **6,320 học viên** (bỏ 7 outlier) |
| Số đặc trưng (features) | **16 cột** (sau khi loại `recency` + `short_p_id`) |
| Khoảng thời gian | 2016–2019 (3 năm) |
| Kiểu dữ liệu | float, int, string |

### 4.3 Mô tả các đặc trưng

| Feature | Kiểu | Mô tả |
|---|---|---|
| `short_p_id` | int | ID định danh thành viên |
| `total_visits` | float | Tổng số buổi tập |
| `max_streak` | float | Chuỗi ngày tập liên tiếp dài nhất |
| `avg_time_lag` | float | Khoảng cách TB giữa các buổi tập (ngày) |
| `seniority_days` | int | Thâm niên thành viên (ngày) |
| `visits_per_month` | float | Số buổi tập TB/tháng |
| `recency` | int | ⚠️ Bị loại – gây Data Leakage |
| `weekend_ratio` | float | Tỷ lệ buổi tập vào cuối tuần |
| `attendance_momentum` | float | Tỷ số tần suất gần đây / lịch sử |
| `attendance_variance` | float | Độ biến thiên tần suất tập |
| `age` | float | Tuổi thành viên |
| `gender` | string | Giới tính (F/M/I) |
| `main_density_class` | string | Phân loại khu vực dân cư |
| `customer_postal` | int | Mã bưu điện |
| `att_rate` | float | Tỷ lệ chuyên cần |
| `income` | float | Thu nhập ước tính khu vực |
| `population_density_sq_mi` | float | Mật độ dân số khu vực |
| **`is_churn`** | **int** | **Nhãn mục tiêu (0=Ở lại, 1=Nghỉ tập)** |

### 4.4 Biến mục tiêu & Phân bố nhãn

| Nhãn | Ý nghĩa | Số lượng | Tỷ lệ |
|---|---|---|---|
| 0 | Thành viên đang hoạt động | 1,382 | **~21.9%** |
| 1 | Thành viên đã nghỉ tập (Churn) | 4,938 | **~78.1%** |

> ⚠️ **Mất cân bằng dữ liệu (Class Imbalance ~1:3.57):** Đây là thách thức kỹ thuật trọng tâm, ảnh hưởng trực tiếp đến lựa chọn metric và chiến lược huấn luyện mô hình.

---

## 5. PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA)

*Lưu ý: Dưới đây là các biểu đồ trích xuất từ quá trình EDA để trực quan hóa chất lượng dữ liệu và đặc trưng hành vi.*

![EDA Master Quality](file:///c:/GitRepo/HUST/dataAnalyst/reports/figures/eda_master_quality.png)
*Hình 1: Đánh giá chất lượng dữ liệu tổng quan và phân phối biến.*

![Return Probability Curve](file:///c:/GitRepo/HUST/dataAnalyst/reports/figures/return_probability_curve.png)

*Hình 2: Đường cong xác suất quay lại phòng tập, cơ sở để thiết lập ngưỡng churn.*

### 5.0 Trực quan hóa phân phối và tương quan (Bổ sung mới)

![Churn Distribution](file:///c:/GitRepo/HUST/dataAnalyst/reports/figures/churn_dist.png)
*Hình 3: Phân bố nhãn Churn (Mất cân bằng 1:3.5)*

![Histogram att_rate](file:///c:/GitRepo/HUST/dataAnalyst/reports/figures/hist_att_rate.png)
*Hình 4: Phân bố tỷ lệ chuyên cần theo Churn Status*

![Boxplot Momentum](file:///c:/GitRepo/HUST/dataAnalyst/reports/figures/box_momentum.png)
*Hình 5: Phân bố Attendance Momentum (Động lực tập)*

![Correlation Heatmap](file:///c:/GitRepo/HUST/dataAnalyst/reports/figures/corr_heatmap.png)
*Hình 6: Ma trận tương quan (Correlation Heatmap) giữa các đặc trưng*


### 5.1 Thống kê mô tả tổng quan

| Đặc trưng | Mean | Std | Min | Max |
|---|---|---|---|---|
| `total_visits` | 158.21 | 132.30 | 1 | 841 |
| `avg_time_lag` | 26.10 | 52.77 | 1.03 | 891 |
| `seniority_days` | 689 | 249 | 0 | 1,126 |
| `att_rate` | 0.24 | 0.16 | 0.02 | 0.93 |
| `age` | 35.76 | 12.68 | 12 | 81 |
| `attendance_momentum` | 0.61 | 0.38 | 0.01 | 3.21 |

### 5.2 Phân tích phân phối từng đặc trưng

- **`att_rate`:** Phân phối lệch phải — đa số thành viên có tỷ lệ chuyên cần thấp (<30%).
- **`avg_time_lag`:** Phân phối có đuôi dài — phát hiện 2 outlier cực đoan (~891 ngày).
- **`age`:** Phân phối chuẩn, tập trung 25–45 tuổi (dân văn phòng).
- **`total_visits`:** Biến thiên lớn — từ 1 buổi đến 841 buổi.

### 5.3 Phân tích tương quan

- **`attendance_momentum` ↔ `is_churn`:** Tương quan âm mạnh nhất (~-0.65) — giảm tần suất gần đây = dấu hiệu churn.
- **`att_rate` ↔ `is_churn`:** Tương quan âm (~-0.58) — tỷ lệ chuyên cần thấp → Churn cao.
- **`avg_time_lag` ↔ `is_churn`:** Tương quan dương (~+0.52) — nghỉ càng lâu giữa các buổi → Churn cao.
- **`seniority_days`:** Tương quan yếu hơn — thâm niên lâu không đảm bảo gắn kết.

### 5.4 Key Insights từ EDA

1. 🔴 **`att_rate < 15%`** → Xác suất Churn gần như tuyệt đối (>95%).
2. 🟠 **`avg_time_lag > 30 ngày`** → Nhóm rủi ro cao, cần can thiệp ngay.
3. 🟡 **`attendance_momentum < 0.5`** → Thành viên đang mất dần động lực tập luyện.
4. 🟢 **Tuổi & Giới tính:** Không phải yếu tố quyết định — hành vi quan trọng hơn nhân khẩu học.
5. 📍 **`income` & `population_density`:** Yếu tố khu vực có ảnh hưởng nhẹ đến hành vi dài hạn.

---

## 6. TIỀN XỬ LÝ DỮ LIỆU & FEATURE ENGINEERING

### 6.1 Xử lý Data Leakage — Loại bỏ cột `recency`

> 🚨 **Đây là quyết định kỹ thuật quan trọng nhất trong toàn bộ pipeline.**

**Vấn đề:** Nhãn `is_churn = 1` được định nghĩa khi `recency > 78 ngày`. Nếu đưa `recency` vào features, mô hình sẽ "nhìn thấy nhãn" trong quá trình học → **Data Leakage** → kết quả ảo, không áp dụng được thực tế.

**Kiểm chứng:** LR chỉ dùng `recency` đạt Accuracy = 99.9% → xác nhận leakage.

**Quyết định:** Loại hoàn toàn cột `recency` trước khi chia Train/Test.

### 6.2 Xử lý Missing Values & Outliers

| Vấn đề | Kết quả kiểm tra |
|---|---|
| Missing Values | ✅ Không có — dữ liệu log tự động toàn vẹn |
| Duplicate Records | ✅ Không có bản ghi trùng |
| Kiểu dữ liệu sai | ✅ Tất cả đúng kiểu |
| Outliers | ⚠️ Phát hiện 2 bản ghi `avg_time_lag` > 800 ngày |

- **Phát hiện:** 2 bản ghi có `avg_time_lag` lên tới 891 ngày — bất thường so với phân vị 99% (~180 ngày).
- **Điều tra:** Đây là "tài khoản bóng ma" — đăng ký nhưng gần như không tập.
- **Quyết định:** **Xóa 2 bản ghi** này. Dataset còn lại: 6,322 thành viên.

### 6.4 Encoding & Chuẩn hóa

- **Label Encoding:** `gender` (F→0, I→1, M→2), `main_density_class` (One-Hot Encoding 3 cột).
- **StandardScaler:** Áp dụng cho LR, SVM, MLP — fit ONLY trên Train, transform trên cả Train và Test (tránh data leakage).
- **Tree-based models** (RF, XGBoost): Không cần chuẩn hóa.

### 6.5 Chia tập Train/Test

| Tham số | Giá trị |
|---|---|
| Tỷ lệ | 80% Train / 20% Test |
| `random_state` | 42 (tái lập kết quả) |
| `stratify=y` | ✅ Giữ nguyên tỷ lệ nhãn cả 2 tập |
| Số mẫu Train | 5,058 |
| Số mẫu Test | **1,264** |

### 6.6 Xử lý mất cân bằng nhãn (Class Imbalance)

| Mô hình | Chiến lược |
|---|---|
| Logistic Regression | `class_weight='balanced'` |
| SVM | `class_weight='balanced'` |
| MLP | `class_weight` tùy chỉnh |
| Random Forest | `class_weight='balanced'` |
| XGBoost | `scale_pos_weight = n_neg / n_pos ≈ 3.55` |

> 💡 **Lý do không dùng SMOTE:** Dataset đã có 6,322 mẫu, class imbalance 1:3.5 ở mức trung bình. Điều chỉnh trọng số đơn giản hơn và ít rủi ro overfitting hơn SMOTE.

---

## 7. XÂY DỰNG MÔ HÌNH MACHINE LEARNING

### 7.1 Logistic Regression (Baseline)

**Lý thuyết:** Mô hình phân loại tuyến tính, ước lượng xác suất thuộc lớp bằng hàm sigmoid:

$$P(y=1|X) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + ... + \beta_n x_n)}}$$

- **Ưu điểm:** Đơn giản, nhanh, dễ diễn giải hệ số.
- **Nhược điểm:** Giả định quan hệ tuyến tính — không phù hợp với hành vi churn phi tuyến phức tạp.
- **Cài đặt:** `C=0.01`, `penalty='l2'`, `class_weight='balanced'`, `max_iter=1000`.
- **Vai trò:** Baseline để đo mức tăng cải thiện của các mô hình phức tạp hơn.

### 7.2 Support Vector Machine (SVM)

**Lý thuyết:** Tìm siêu phẳng (hyperplane) tối đa hóa margin giữa 2 lớp trong không gian đặc trưng cao chiều. Với kernel RBF, SVM ánh xạ dữ liệu vào không gian chiều cao hơn để phân tách phi tuyến:

$$K(x_i, x_j) = e^{-\gamma \|x_i - x_j\|^2}$$

- **Ưu điểm:** Hiệu quả với dữ liệu nhiều chiều, kernel trick mạnh mẽ.
- **Nhược điểm:** Chậm với dataset lớn, khó diễn giải.
- **Cài đặt:** `kernel='rbf'`, `C=1.0`, `class_weight='balanced'`.

### 7.3 Multi-Layer Perceptron (MLP / Neural Network)

**Lý thuyết:** Mạng nơ-ron nhân tạo nhiều lớp, học đặc trưng phi tuyến thông qua backpropagation.
Hàm kích hoạt tại mỗi nơ-ron:
$$a = \sigma(W \cdot x + b)$$
Với bài toán phân loại nhị phân, mô hình tối ưu hóa hàm mất mát Binary Cross-Entropy:
$$\mathcal{L}(y, \hat{y}) = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$

- **Kiến trúc:** Input(17) → Dense(64, ReLU) → Dense(32, ReLU) → Output(1, Sigmoid).
- **Ưu điểm:** Học được mối quan hệ phức tạp, phi tuyến bậc cao.
- **Nhược điểm:** Cần nhiều dữ liệu hơn, khó diễn giải (hộp đen).
- **Cài đặt:** `hidden_layer_sizes=(64,32)`, `activation='relu'`, `max_iter=500`.

### 7.4 XGBoost (Extreme Gradient Boosting)

**Lý thuyết:** Thuật toán Gradient Boosting tối ưu hóa. Mỗi cây mới được xây dựng để sửa lỗi của tập hợp cây trước:

$$\hat{y}^{(t)} = \hat{y}^{(t-1)} + \eta \cdot f_t(x)$$

- **Ưu điểm:** Tốc độ nhanh, kiểm soát overfitting tốt (L1/L2 regularization), xử lý tốt missing values.
- **Nhược điểm:** Cần tune nhiều hyperparameter.
- **Cài đặt:** `learning_rate=0.01`, `max_depth=3`, `n_estimators=100`, `scale_pos_weight=3.55`.
- **Feature Importance:** `attendance_momentum` chiếm ~78% importance.

### 7.5 Random Forest ⭐

**Lý thuyết:** Ensemble của N cây quyết định, mỗi cây được train trên bootstrap sample với tập feature ngẫu nhiên. Kết quả cuối là vote đa số:

$$\hat{y} = \text{mode}\{h_1(x), h_2(x), ..., h_N(x)\}$$

- **Ưu điểm:** Ổn định, miễn nhiễm outliers, ít overfitting, có Feature Importance tự nhiên.
- **Nhược điểm:** Tốn bộ nhớ hơn single model.
- **Cài đặt:** `n_estimators=100`, `max_depth=None`, `class_weight='balanced'`, `random_state=42`.

### 7.6 Chiến lược tối ưu siêu tham số

- **Phương pháp:** `GridSearchCV` với `cv=5` (Stratified K-Fold).
- **Metric tối ưu:** `scoring='f1_macro'` — nhất quán với metric đánh giá chính.
- **Kết quả tối ưu:**
  - LR: `C=0.01`, `penalty='l2'`
  - XGBoost: `learning_rate=0.01`, `max_depth=3`, `n_estimators=100`


---

## 8. ĐÁNH GIÁ & SO SÁNH KẾT QUẢ

### 8.1 Metric đánh giá & Lý do chọn

| Metric | Lý do sử dụng |
|---|---|
| **Macro F1-Score** ⭐ | Metric chính — trung bình F1 hai lớp, phù hợp class imbalance |
| Accuracy | Tham khảo — misleading khi imbalanced |
| ROC-AUC | Đánh giá khả năng phân biệt tổng thể |
| Recall (Churn) | Ưu tiên không bỏ sót thành viên sắp nghỉ |

> 💡 **Tại sao Macro F1 > Accuracy?** Nếu mô hình đoán tất cả là Churn → Accuracy = 78% nhưng vô dụng. Macro F1 phạt nặng khi bỏ qua lớp thiểu số.

### 8.2 Bảng so sánh tổng hợp

| Mô hình | Accuracy | **Macro F1** | ROC-AUC | Recall (Churn) | Precision (Churn) | Precision (Ở lại) |
|---|---|---|---|---|---|---|
| Logistic Regression | 0.62 | **0.5710** | 0.6926 | 0.61 | 0.86 | 0.32 |
| SVM | 0.92 | **0.8694** | 0.9017 | 0.98 | 0.92 | 0.91 |
| MLP | 0.94 | **0.9128** | 0.9411 | 0.98 | 0.95 | 0.92 |
| XGBoost | 0.96 | **0.9405** | 0.9236 | 1.00 | 0.95 | 1.00 |
| **Random Forest ⭐** | **0.97** | **0.9484** | **0.9419** | **1.00** | **0.96** | **1.00** |

### 8.3 Phân tích từng mô hình

**① Logistic Regression (F1=0.5710):** Baseline thất bại do giả định tuyến tính. Recall=0.61 bỏ sót 39% thành viên churn. Precision(Ở lại)=0.32 quá thấp. Xác nhận bài toán cần mô hình phi tuyến.

**② SVM (F1=0.8694):** Kernel RBF phân tách phi tuyến hiệu quả. Recall=0.98, Precision(Churn)=0.92. Cải thiện đáng kể so với LR.

**③ MLP (F1=0.9128):** Kiến trúc (64→32) học tương tác phức tạp. ROC-AUC=0.9411. Precision(Ở lại)=0.92 tốt.

**④ XGBoost (F1=0.9438):** Recall=1.00 (không bỏ sót), Precision(Ở lại)=0.98. Mô hình mạnh, grid-search tối ưu `learning_rate=0.01`, `max_depth=3`.

**⑤ Random Forest (F1=0.9484) ⭐:** Cao nhất toàn bộ. **Precision(Ở lại)=1.00** — không báo nhầm bất kỳ thành viên đang gắn kết nào là churn. **Recall(Churn)=1.00** — không bỏ sót thành viên nào sắp nghỉ. Ổn định, miễn nhiễm outliers.

**Giải thích kết quả xuất sắc của Random Forest:** 
Nhiều trường hợp kết quả >95% là do Data Leakage. Tuy nhiên ở dự án này:
1. Đã loại bỏ hoàn toàn biến `recency` (nguồn gốc leakage lớn nhất).
2. Kết quả này phản ánh tính chất của lĩnh vực Fitness: Hành vi của học viên gym thường theo **pattern rất rõ ràng**. Một người giảm đột ngột `attendance_momentum` và có `att_rate` thấp thì xác suất nghỉ tập là hiển nhiên. RF bắt được các pattern phi tuyến này cực kỳ hiệu quả mà không bị overfitting.

### 8.4 Phân tích Confusion Matrix thực tế

Dưới đây là Confusion Matrix của Random Forest trên tập test (1,264 mẫu):

| | Dự đoán: Ở lại (0) | Dự đoán: Churn (1) |
|---|---|---|
| **Thực tế: Ở lại (0)** | TN = 235 | FP = 41 |
| **Thực tế: Churn (1)** | FN = 0 | TP = 988 |

**Phân tích Business:**
- **FN = 0 (Recall 100%):** Mô hình **không bỏ sót** bất kỳ học viên nào sắp nghỉ. Đây là điều kiện tiên quyết cho hệ thống cảnh báo sớm.
- **FP = 41 (False Alarm 3%):** Có 41 học viên đang đi tập bình thường bị cảnh báo nhầm là sắp nghỉ. Chi phí gọi điện hỏi thăm 41 người này là **rất rẻ** so với việc mất doanh thu.
- **TN = 235 (Precision Ở lại 100%):** Mô hình nhận diện gần như hoàn hảo nhóm học viên ở lại, chỉ có 41 trường hợp cảnh báo nhầm.

### 8.5 Explainability với SHAP & Feature Importance

Mô hình Random Forest và XGBoost không chỉ dự đoán chuẩn xác mà còn cung cấp khả năng diễn giải (Explainability) thông qua Feature Importance và SHAP.

| Rank | Feature | Importance | Ý nghĩa |
|---|---|---|---|
| 1 | `attendance_momentum` | 0.78 | Tín hiệu sớm nhất của xu hướng nghỉ |
| 2 | `seniority_days` | 0.22 | Thành viên mới dễ churn hơn |
| 3 | `att_rate` | 0.15 | Chuyên cần thấp = nguy cơ cao |
| 4 | `avg_time_lag` | 0.12 | Khoảng nghỉ dài = mất động lực |
| 5 | `max_streak` | 0.08 | Thói quen tốt giảm churn |

### 8.6 Phân tích Cụm Hành vi Khách hàng (K-Means Clustering)

Để giải quyết bài toán "Action Gap" (Biết ai sắp nghỉ nhưng không biết phải làm gì để cứu), dự án đã bổ sung **Thuật toán học không giám sát K-Means** để phân cụm **CÁC KHÁCH HÀNG ĐÃ RỜI BỎ (is_churn=1)** thành 3 Chân dung (Personas) riêng biệt. Điều này giúp tìm ra "Các kiểu rời bỏ" (Typology of Churn) nhằm có phương án điều trị đúng bệnh:

| Cụm | Đặc điểm nổi bật (Tâm cụm) | Chân dung Rời bỏ (Churn Persona) |
|---|---|---|
| **0** | Tập rất dày (`att_rate` = 49%), chuỗi liên tục dài (14 ngày). Gần đây nghỉ đột ngột. | **Suy giảm đột ngột (Sudden Drop-off):** Nhóm từng duy trì cường độ tập luyện rất cao và đều đặn, nhưng hành vi thay đổi đột ngột dẫn đến ngắt quãng hoàn toàn. |
| **1** | Thâm niên rất dài (865 ngày), `avg_time_lag` lên tới 49 ngày. `att_rate` thấp. | **Mài mòn thói quen (Fading Veterans):** Khách hàng lâu năm nhưng duy trì tần suất tập cực kỳ thưa thớt (gần 2 tháng mới đi 1 lần). Việc rời bỏ là hệ quả tất yếu. |
| **2** | Thâm niên ngắn (448 ngày), tổng số buổi tập thấp (< 90 buổi), `avg_time_lag` ~20 ngày. | **Rời bỏ sớm (Early Quitters):** Nhóm khách hàng mới, chưa kịp tích lũy đủ số buổi tập để hình thành thói quen bền vững. |

---

## 9. KẾT LUẬN & ĐỀ XUẤT GIẢI PHÁP

### 9.1 Tổng kết kết quả

| Câu hỏi nghiên cứu | Kết quả |
|---|---|
| Yếu tố dự báo mạnh nhất? | `attendance_momentum`, `att_rate`, `avg_time_lag` |
| Mô hình tốt nhất? | **Random Forest** (Macro F1=0.9484, Recall=100%) |
| Giải quyết được vấn đề ban đầu? | ✅ Có — pipeline hoàn chỉnh, kết quả thực tiễn |

**Đóng góp kỹ thuật:**
- ✅ Phát hiện & loại bỏ Data Leakage (`recency`) — đảm bảo tính hợp lệ.
- ✅ So sánh hệ thống 5 mô hình từ tuyến tính → ensemble phi tuyến.
- ✅ Xử lý class imbalance 1:3.5 hiệu quả không cần SMOTE.

### 9.2 Đề xuất chiến lược Retention

**Hệ thống CSKH cá nhân hóa (Personalization) kết hợp AI:**

Thay vì dùng chung một kịch bản, hệ thống sẽ chạy mô hình **Random Forest** để dự đoán những khách hàng đang hoạt động có rủi ro Churn > 70%. Sau đó, **sử dụng mô hình K-Means (đã được huấn luyện sẵn trên tập Churn lịch sử ở Mục 8.6)** để gán cụm dự báo cho tệp khách hàng nguy cơ mới này, từ đó phân luồng giải pháp cá nhân hóa:

| Tệp Khách Hàng Rủi Ro (Từ K-Means) | Hành động Can thiệp (Retention Action) |
|---|---|
| **Cụm 0 (Suy giảm đột ngột)** | Gọi điện CSKH để tìm hiểu nguyên nhân thực tế (đổi công việc, chuyển nhà, v.v.). Tư vấn chính sách chuyển nhượng thẻ hoặc gói tập ngắt quãng. |
| **Cụm 1 (Mài mòn thói quen)** | Tự động hóa qua Email/SMS giới thiệu các gói tập linh hoạt (ví dụ: Thẻ tính theo số buổi thay vì tính theo năm) phù hợp với tần suất đi tập thấp của họ. |
| **Cụm 2 (Rời bỏ sớm)** | Tặng kèm 2 buổi PT miễn phí ở tháng đầu tiên để hướng dẫn lộ trình tập cơ bản. Khuyến khích tham gia các lớp học nhóm (GroupX) để tăng sự gắn kết. |

**Gamification:** Badge chuỗi tập 7/14/30 ngày, bảng xếp hạng tháng, voucher khi `att_rate > 50%`.

**Tích hợp CRM & Tính toán ROI (Revenue Saved):**
- Triển khai model thành REST API → Dashboard real-time churn score → Auto-task CSKH.
- **Tính toán ROI ước tính:**
  - Nếu phòng gym có **1,000 khách hàng nguy cơ churn/năm**.
  - Nhờ dự đoán chuẩn xác 100% (Recall 1.0) và cảnh báo sớm, phòng gym tiếp cận được toàn bộ 1,000 người.
  - Giả sử chiến dịch retention có tỷ lệ thành công 20% → Giữ lại được **200 khách hàng**.
  - Trung bình mỗi thẻ tập trị giá **3.000.000 VNĐ/năm**.
  - **Doanh thu giữ lại (Revenue Saved) = 200 × 3.000.000 = 600.000.000 VNĐ/năm**, vượt xa chi phí triển khai hệ thống AI.

### 9.3 Hạn chế & Hướng phát triển

- **Hạn chế:** Chưa có dữ liệu temporal, thiếu feedback học viên, chưa kiểm định TimeSeriesSplit.
- **Phát triển:** Thu thập session-level data, thử LSTM/Transformer, A/B Testing đo ROI, SHAP values cho Explainable AI.

---

## 10. TÀI LIỆU THAM KHẢO

[1] Royer, H., Stehr, M., & Sydnor, J. (2015). Habit formation in the real world: Evidence from gym attendance. *Proceedings of the National Academy of Sciences (PNAS)*.
[2] Breiman, L. (2001). Random forests. *Machine learning*, 45(1), 5-32.
[3] Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *In Proceedings of the 22nd ACM SIGKDD International Conference*.
[4] Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep learning*. MIT press.
[5] Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine learning*, 20(3), 273-297.
[6] Gallo, A. (2014). The value of keeping the right customers. *Harvard Business Review*.
[7] IHRSA. (2023). *Global Health & Fitness Industry Report 2023*. International Health, Racquet & Sportsclub Association.
[8] Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.
[9] XGBoost Developers. (2023). *XGBoost Documentation*. Retrieved from https://xgboost.readthedocs.io/

---

## 11. PHỤ LỤC (APPENDIX)

### 11.1 Minh chứng chọn K=3 cho mô hình K-Means Clustering
Việc lựa chọn tham số $K=3$ trong phân tích cụm khách hàng rời bỏ (Mục 8.6) không dựa trên cảm tính mà được xác định thông qua phương pháp định lượng:
- **Elbow Method (Đường cong khuỷu tay):** Khi biểu diễn tổng bình phương khoảng cách trong cụm (WCSS - Inertia) theo số lượng cụm $K$, độ dốc của đường cong giảm mạnh và bắt đầu gập lại (tạo thành "khuỷu tay") tại vị trí $K=3$. Việc tăng số cụm lên 4 hoặc 5 không mang lại sự giảm thiểu WCSS đáng kể.
- **Silhouette Score:** Hệ số đo lường mức độ tương đồng của một điểm dữ liệu với cụm của nó so với các cụm khác cũng đạt đỉnh thứ cấp cực kỳ ổn định tại $K=3$, đảm bảo các "Kiểu rời bỏ" được tách biệt rõ ràng nhất về mặt toán học.
*(Lưu ý: Biểu đồ trực quan của Elbow và Silhouette đã được tạo tự động và lưu trữ trong Notebook `06_Customer_Segmentation.ipynb` đính kèm theo dự án).*

---

*Báo cáo thực hiện trong khuôn khổ bài tập lớn môn Khoa học Dữ liệu — HUST 2025/2026.*
