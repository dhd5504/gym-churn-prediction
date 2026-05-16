# Nhật ký Nghiên cứu & Thử nghiệm (Research Log)

File này dùng để ghi lại các kết quả, quyết định và nhận định quan trọng trong quá trình xử lý dữ liệu lớn. Đây là tài liệu gốc để viết báo cáo bài tập lớn sau này.

---

## [2026-05-16] Khám phá dữ liệu gốc (Raw Data Discovery)

*   **Hành động:** Kiểm tra phạm vi ngày tháng trên toàn bộ dữ liệu Weather.
*   **Phát hiện:** 
    *   Ngày bắt đầu: **02/01/2007** (Dữ liệu kéo dài 12 năm)
    *   Ngày kết thúc (Cut-off date): **01/02/2019**
*   **Quyết định:** Sử dụng ngày 01/02/2019 làm mốc thời gian "Hôm nay". Lưu ý rằng dữ liệu kéo dài 12 năm giải thích tại sao tỷ lệ Churn tích lũy lại cao (78%).

---

## [2026-05-16] Bước 1: Phân tích xác suất quay lại (Giai đoạn 2016-2019)

*   **Hành động:** Thu hẹp phạm vi phân tích từ năm 2016 để loại bỏ nhiễu từ quá khứ. 
*   **Lý do lọc thời gian:** 
    1. Dữ liệu từ 2016-2019 chiếm 50% tổng số quan sát (4.4 triệu/8.7 triệu dòng) dù chỉ kéo dài 3 năm.
    2. Hành vi học viên thay đổi theo thời gian; dữ liệu từ 2007 không còn phản ánh đúng thói quen hiện tại.
    3. Giảm tải cho bộ nhớ (RAM) khi thực hiện các lệnh Join phức tạp.
*   **Phát hiện mới:**
    *   Tại ngày thứ **78**, xác suất học viên quay lại phòng tập rơi xuống dưới **50%**.
    *   Đây là mốc "Điểm gãy" lý tưởng để dán nhãn Churn (Xác suất vắng mặt vĩnh viễn cao hơn xác suất quay lại).
*   **Quyết định chiến thuật:** Chốt mốc Churn = **78 ngày**.
*   **Hình ảnh minh họa:** `reports/figures/return_probability_curve.png`

---

## [2026-05-17] Bước 2: Tối ưu Master Dataset & Sửa lỗi Duplicate
*   **Hành động:** 
    1.  Phát hiện lỗi nhân bản dữ liệu (Data Duplication) do quan hệ 1-N trong bảng `Census_Data.csv` (một mã ZipCode có nhiều bản ghi census nhỏ).
    2.  Thực hiện **Gom nhóm (Aggregate)** dữ liệu Census theo mã ZipCode trước khi gộp để đảm bảo tính duy nhất.
    3.  Cập nhật ngày chốt dữ liệu chính xác là **01/02/2019** để đảm bảo biến `recency` luôn dương và phản ánh đúng thực tế.
*   **Thông số kỹ thuật sau cập nhật:**
    *   Phạm vi: Filter `date >= 2016-01-01`.
    *   Số lượng học viên (Unique): **6,327 người**. (Đây là con số chính xác sau khi loại bỏ 160k dòng trùng lặp ảo).
    *   Tỷ lệ Churn: **78.14%**.
    *   Định dạng lưu trữ: **CSV** (để dễ dàng kiểm tra bằng mắt thường).
*   **Các Features cao cấp bổ sung:**
    *   `attendance_momentum`: Tỷ lệ đi tập 30 ngày gần nhất so với 30 ngày trước đó (phát hiện dấu hiệu "chán tập").
    *   `weekend_ratio`: Tỷ lệ tập vào cuối tuần (phân loại nhóm khách hàng đi làm vs nhóm tự do).
    *   `attendance_variance`: Độ biến động của thời gian giữa các buổi tập (đo lường tính kỷ luật).
*   **Nhận định chuyên gia:** Bộ dữ liệu 6,327 dòng này là "vàng ròng" vì đã được làm sạch 100%. Việc phát hiện lỗi nhân bản từ 170k dòng xuống 6k dòng là một bước đột phá về tính trung thực của dữ liệu (Data Integrity).
*   **Đường dẫn file:** `dataMaster/gym_churn_master_final.csv`
