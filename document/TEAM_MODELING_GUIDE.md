# 👥 HƯỚNG DẪN PHÂN CÔNG & HUẤN LUYỆN MÔ HÌNH (Dành cho Thành viên Nhóm)

Chào các thành viên nhóm dự án **Gym Churn Prediction**! 

Để chuẩn bị cho phần thực hành code và báo cáo cuối kỳ đạt kết quả tốt nhất, Trưởng nhóm đã thiết lập một file Notebook gốc mang tên **`notebooks/05_Modeling_Template.ipynb`** và chạy thử nghiệm thành công mô hình Baseline (Logistic Regression) với điểm số **Macro F1-Score đạt ~0.56**.

Nhiệm vụ của 4 thành viên còn lại là tải file Template này về, sao chép ra thành file riêng và thực hiện xây dựng mô hình của mình ở **Mục 4** của Notebook theo đúng phân công dưới đây.

---

## 🚨 3 QUY TẮC BẮT BUỘC CHO CẢ NHÓM (Không được làm sai)

1.  **KHÔNG sửa Phần 1 và Phần 2 của Notebook:** Đây là phần tải dữ liệu Master sạch (6,327 dòng) và chia Train/Test (`random_state=42`). Việc giữ nguyên phần này đảm bảo 5 người chúng ta cùng giải một đề thi giống hệt nhau, kết quả mang ra so sánh mới công bằng.
2.  **Dùng biến chuẩn hóa `scaled` khi cần thiết:** 
    *   *Người 4 (SVM) và Người 5 (MLP):* **Bắt buộc** phải dùng tập dữ liệu đã chuẩn hóa: `X_train_scaled` và `X_test_scaled`.
    *   *Người 2 (Random Forest) và Người 3 (XGBoost):* Có thể dùng tập dữ liệu thô `X_train` và `X_test` (dòng cây không nhạy cảm với scale).
3.  **Đánh giá bằng hàm chung:** Tất cả mọi người sau khi train xong mô hình của mình phải gọi hàm `evaluate_model` ở Phần 3 để vẽ Confusion Matrix và in ra chỉ số. **Chỉ số quyết định để so sánh giữa 5 người là Macro F1-Score**.

---

## 🛠️ HƯỚNG DẪN CHI TIẾT CHO TỪNG THÀNH VIÊN

### 👤 Người 2: Mô hình Random Forest
*   **Mục tiêu:** Cải thiện độ phủ (Recall) của nhóm Churn và tìm ra các thuộc tính quan trọng nhất bằng phương pháp Bagging.
*   **Thư viện sử dụng:**
    ```python
    from sklearn.ensemble import RandomForestClassifier
    ```
*   **Các siêu tham số cần tinh chỉnh (GridSearchCV):**
    ```python
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [2, 5, 10],
        'class_weight': ['balanced'] # Cực kỳ quan trọng do dữ liệu mất cân bằng
    }
    ```
*   **Nhiệm vụ đặc biệt:** Trích xuất biến quan trọng (`feature_importances_`) và vẽ biểu đồ cột Top 10 đặc trưng ảnh hưởng nhiều nhất đến Random Forest để so sánh với biểu đồ của trưởng nhóm.

---

### 👤 Người 3: Mô hình Gradient Boosting / XGBoost
*   **Mục tiêu:** Sử dụng thuật toán Boosting mạnh mẽ nhất hiện nay để sửa sai cho các ca dự đoán nhầm của mô hình Baseline, nâng F1-Score tổng thể lên tối đa.
*   **Thư viện sử dụng:** (Đảm bảo đã chạy `pip install xgboost`)
    ```python
    from xgboost import XGBClassifier
    ```
*   **Các siêu tham số cần tinh chỉnh (GridSearchCV):**
    ```python
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 6, 9],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 1.0],
        'scale_pos_weight': [3.5] # Tỷ lệ giữa nhãn 1 và nhãn 0 để phạt nặng khi đoán sai nhóm Churn
    }
    ```
*   **Lưu ý:** XGBoost yêu cầu nhãn phải là số (đã được xử lý sẵn ở Phần 2). Hãy cố gắng điều chỉnh `scale_pos_weight` để tối ưu hóa F1-Score.

---

### 👤 Người 4: Mô hình Support Vector Machine (SVM)
*   **Mục tiêu:** Tìm ra ranh giới phân loại tối ưu (Margin) trong không gian nhiều chiều.
*   **Thư viện sử dụng:**
    ```python
    from sklearn.svm import SVC
    ```
*   **Các siêu tham số cần tinh chỉnh (GridSearchCV):**
    ```python
    param_grid = {
        'C': [0.1, 1, 10],
        'gamma': ['scale', 'auto', 0.01, 0.1],
        'kernel': ['linear', 'rbf'], # rbf để học các quan hệ phi tuyến tính
        'class_weight': ['balanced']
    }
    ```
*   **Lưu ý cực kỳ quan trọng:** **Bắt buộc** phải truyền dữ liệu đã được chuẩn hóa `X_train_scaled` và `X_test_scaled` vào hàm `fit()`. SVM chạy trên dữ liệu chưa chuẩn hóa sẽ cho kết quả rất tệ và chạy cực kỳ lâu.

---

### 👤 Người 5: Mô hình MLP / Artificial Neural Network
*   **Mục tiêu:** Xây dựng mạng Nơ-ron nhân tạo cơ bản (Deep Learning đơn giản) để tự động học các đặc trưng phức tạp.
*   **Thư viện sử dụng:**
    ```python
    from sklearn.neural_network import MLPClassifier
    ```
*   **Các siêu tham số cần tinh chỉnh (GridSearchCV):**
    ```python
    param_grid = {
        'hidden_layer_sizes': [(64, 32), (100,), (50, 25)],
        'activation': ['relu', 'tanh'],
        'solver': ['adam'],
        'alpha': [0.0001, 0.001, 0.01], # Hệ số phạt L2 chống Overfitting
        'learning_rate_init': [0.001, 0.01]
    }
    ```
*   **Nhiệm vụ đặc biệt:** Theo dõi và vẽ biểu đồ tổn thất (Loss Curve) trong quá trình huấn luyện bằng thuộc tính `mlp.loss_curve_` để giải thích hiện tượng hội tụ (Convergence) và kiểm soát Overfitting trong slide thuyết trình. **Bắt buộc dùng dữ liệu đã chuẩn hóa (Scaled)**.

---

## 📈 ĐÍCH ĐẾN CỦA CẢ NHÓM (KPI)

*   **Điểm số cần vượt qua (Baseline):** **`0.5519` (Macro F1-Score)**.
*   **Sản phẩm cần bàn giao cho Trưởng nhóm trước ngày [Điền ngày]:**
    1.  File Notebook cá nhân đã chạy hoàn chỉnh (Ví dụ: `05B_RandomForest_NguyenVanA.ipynb`).
    2.  Bộ tham số tốt nhất (`best_params_`) tìm được qua Grid Search.
    3.  Bảng báo cáo phân loại (Classification Report) và ảnh chụp Confusion Matrix sạch đẹp.
    4.  Nhận xét ngắn gọn (3-4 dòng) về mô hình của mình.

Chúc cả nhóm chúng ta hoàn thành xuất sắc đồ án này! Có khó khăn gì về mặt kỹ thuật, hãy liên hệ ngay với Trưởng nhóm để được hỗ trợ kịp thời.
