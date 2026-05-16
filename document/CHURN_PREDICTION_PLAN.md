# Kế hoạch Phân tích & Xây dựng Mô hình Dự đoán Churn (Gym)

## 1. Mục tiêu cốt lõi
Xây dựng mô hình Machine Learning có khả năng dự báo sớm những học viên có nguy cơ bỏ tập để hệ thống có thể đưa ra các biện pháp giữ chân kịp thời.

## 2. Định nghĩa Biến mục tiêu (Target)
Vì dữ liệu thô chưa có cột Churn, chúng ta sẽ định nghĩa:
*   **Churn (1):** Học viên không đi tập trong vòng > 30 ngày (dựa trên cột `time_lag`).
*   **Active (0):** Học viên vẫn duy trì đi tập đều đặn.

## 3. Các đặc trưng dự báo (Key Features)
Để mô hình đạt độ chính xác cao, chúng ta sẽ tập trung vào 3 nhóm dữ liệu:

### A. Nhóm Hành vi (Behavioral - Quan trọng nhất)
*   **Recency:** Số ngày kể từ lần tập cuối (`time_lag`).
*   **Frequency:** Tần suất đi tập trung bình mỗi tuần/tháng (`att_rate`, `visits`).
*   **Trend:** Tần suất đi tập đang tăng hay giảm so với tháng trước.

### B. Nhóm Nhân khẩu học (Demographic)
*   **Cá nhân:** Độ tuổi, Giới tính.
*   **Kinh tế:** Thu nhập hộ gia đình trung bình (từ dữ liệu Census).
*   **Vị trí:** Loại khu vực sinh sống (Trung tâm, Ngoại ô, Nông thôn).

### C. Nhóm Tác động (Experimental)
*   **Treatment:** Học viên có tham gia các chương trình cam kết hay khuyến mãi không (`exp_condition`).

## 4. Lộ trình thực hiện (Roadmap)
1.  **Giai đoạn 1: Tiền xử lý & Hợp nhất**
    *   Kết nối dữ liệu hành vi (`pptdata.csv`) với dữ liệu nhân khẩu học (`gym_demo_auc.csv`) và Census.
2.  **Giai đoạn 2: Phân tích đặc tính (EDA)**
    *   Tìm "điểm gãy" của thời gian vắng mặt (Khi nào thì một người thực sự sẽ bỏ tập luôn?).
    *   So sánh sự khác biệt giữa nhóm Active và nhóm Churn.
3.  **Giai đoạn 3: Feature Engineering (Trích xuất đặc trưng)**
    *   Tạo các biến số mới như: "Tỷ lệ đi tập trong 2 tuần gần nhất", "Khoảng cách từ nhà đến phòng tập".
4.  **Giai đoạn 4: Training & Validation**
    *   Thử nghiệm các thuật toán (Random Forest, XGBoost) để dự đoán nhãn Churn.

---
**Ghi chú:** Kế hoạch này được thiết kế để có thể triển khai vào các hệ thống quản lý phòng gym thực tế bằng cách sử dụng API để gửi cảnh báo khi một học viên rơi vào vùng "Nguy cơ cao".
