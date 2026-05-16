# Báo cáo Rà soát Dữ liệu Nguồn (Raw Data Audit)

Bản rà soát này tập trung vào cấu trúc nguyên bản của Dataset (dựa trên các mẫu dữ liệu thô `data_samples`) để xác định chính xác các thành phần dữ liệu trước khi thực hiện biến đổi.

---

## 1. Hệ thống các bảng dữ liệu nguồn

### 1.1. Nguồn Hành vi: `weather.RData`
Đây là nhật ký quẹt thẻ hàng ngày kết hợp với yếu tố ngoại cảnh.
*   **Dữ liệu thô (Raw):**
    *   `short_p_id`: Khóa định danh học viên (dạng số).
    *   `date`: Ngày ghi nhận.
    *   `attended`: (0/1) Có đi tập hay không.
    *   `good_weather` / `bad_weather`: Chỉ số thời tiết tại địa phương.
*   **Dữ liệu phái sinh (Đã có sẵn từ nghiên cứu gốc):**
    *   `streak`: Chuỗi ngày đi tập liên tiếp tính đến ngày quan sát.
    *   `time_lag`: Số ngày vắng mặt kể từ lần tập cuối.
    *   `last7days_attendance`: Tần suất đi tập trong 7 ngày gần nhất.
    *   `pre_habit` / `post_habit`: Chỉ số thói quen trước và sau can thiệp.

### 1.2. Nguồn Nhân khẩu học: `gym_demo_auc.csv`
Bảng hồ sơ tĩnh của từng học viên tại thời điểm đăng ký.
*   **Các cột quan trọng:**
    *   `short_p_id` / `participant_id`: Hai loại khóa nối (Số và Chuỗi).
    *   `age`, `gender`: Thông tin nhân khẩu học cơ bản.
    *   `main_density_class`: Loại khu vực sinh sống (Urban/Suburban/Rural).
    *   `customer_postal`: Mã bưu điện (Dùng để nối với bảng Census).
    *   `att_rate`: Tỷ lệ chuyên cần tổng quát (Đã tính sẵn).

### 1.3. Nguồn Kinh tế: `Census_Data.csv`
Dữ liệu vĩ mô về khu vực sống theo mã bưu điện.
*   **Các cột quan trọng:**
    *   `ZipCode`: Khóa nối với bảng Demo.
    *   `average_household_income`: Thu nhập bình quân khu vực (Cần làm sạch ký tự tiền tệ).
    *   `population_density_sq_mi`: Mật độ dân cư.
    *   `educational_attainment_*`: Các chỉ số trình độ học vấn.
*   **CẢNH BÁO QUAN TRỌNG:** Một mã `ZipCode` có thể tương ứng với nhiều dòng trong bảng Census (do chia nhỏ theo block/neighborhood). 
    *   *Rủi ro:* Nếu join trực tiếp sẽ gây bùng nổ dữ liệu (nhân bản số lượng học viên).
    *   *Xử lý:* Bắt buộc phải **Gom nhóm (Group by ZipCode)** và lấy giá trị trung bình (`mean`) trước khi thực hiện lệnh Join.

### 1.4. Nguồn Thí nghiệm: `pptdata.csv`
Dữ liệu hành vi theo tuần, chứa thông tin về các nhóm can thiệp tâm lý.
*   **Các cột quan trọng:**
    *   `participant_id`: Khóa nối dạng chuỗi (UUID).
    *   `visits`: Số buổi tập trong tuần.
    *   `exp_condition`: Tên chương trình cam kết học viên tham gia.

### 1.5. Bảng tra cứu: `gym_participant_id.csv`
Bảng trung gian chứa thông tin định danh.
*   **Vai trò:** Dùng để ánh xạ (map) giữa `short_p_id` và `participant_id`. 
*   **Lưu ý:** Có thể thay thế bằng bảng Demo vì bảng Demo đã chứa đủ các ID này.

---

## 2. Sơ đồ mối liên hệ (Entity Relationship)

Dữ liệu được tổ chức theo mô hình hình sao (Star Schema) với trung tâm là học viên:

1.  **Weather ↔ Gym Demo**: Kết nối qua `short_p_id`. (Quan hệ 1-1 sau khi aggregate behavior).
2.  **Gym Demo ↔ PPTData**: Kết nối qua `participant_id`.
3.  **Gym Demo ↔ Census Data**: Kết nối qua `customer_postal` (Demo) và `ZipCode` (Census). (Cần xử lý để đạt quan hệ 1-1).

---

## 3. Tổng kết & Lựa chọn Features

### Danh sách các bảng lựa chọn:
*   Sử dụng cả 4 bảng chính: **Weather, Gym Demo, Census, PPTData**.
*   Bảng `gym_participant_id.csv` có thể bỏ qua nếu đã dùng bảng Demo.

### Tổng hợp Features (Dự kiến 10-15 features):
1.  **Hành vi (5):** `streak`, `time_lag`, `last7days_attendance`, `attended`, `att_rate`.
2.  **Nhân khẩu (3):** `age`, `gender`, `main_density_class`.
3.  **Kinh tế (2):** `income`, `population_density`.
4.  **Ngoại cảnh (2):** `good_weather`, `bad_weather`.
5.  **Tác động (1):** `exp_condition`.

---

## 4. Nhận xét tổng quan
*   **Về xử lý dữ liệu:** Mặc dù các biến quan trọng như `streak`, `time_lag` đã có sẵn, nhưng việc **hợp nhất (Merge)** chúng từ các định dạng khác nhau (RData, CSV lớn) và duy trì tính nhất quán của ID là một công việc kỹ thuật quan trọng.
*   **Về tính ứng dụng:** Dataset này cực kỳ mạnh mẽ để làm bài tập lớn Khoa học dữ liệu vì nó cho phép phân tích hành vi con người dưới tác động của nhiều yếu tố.

---
**Người lập báo cáo:** Antigravity AI Assistant
**Ngày cập nhật:** 16/05/2026
