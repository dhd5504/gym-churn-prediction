# Kế hoạch hành động: Xây dựng Master Dataset & Chốt mốc Churn (Full Data)

Bản kế hoạch này hướng dẫn cách chuyển từ phân tích mẫu (MVP) sang xử lý toàn bộ dữ liệu gốc trong thư mục `/Data` để tạo file thống nhất cho nhóm.

---

## Bước 1: Phân tích ngưỡng Churn thực tế (Threshold Discovery)
*   **Dữ liệu:** Sử dụng bảng `Data/weather.RData` (Sử dụng thư viện `pyreadr` để đọc trực tiếp vào Python).
*   **Mốc thời gian:** Lấy ngày **01/01/2019** làm mốc "Hôm nay" (Cut-off date).
*   **Mục tiêu:** Tìm con số ngày vắng mặt thực tế mà tại đó xác suất quay lại gần bằng 0.
*   **Việc cần làm:**
    *   Tính toán xác suất quay lại của học viên sau $N$ ngày vắng mặt.
    *   Vẽ biểu đồ để xác định "Điểm không thể quay đầu".
*   **Đầu ra:** Chốt con số ngày nghỉ cụ thể để dán nhãn Churn (Ví dụ: 25 ngày).

## Bước 2: Viết Script xây dựng Master Dataset (ETL Pipeline)
*   **Mục tiêu:** Tạo ra một file Master duy nhất cho cả nhóm dùng chung.
*   **Việc cần làm:**
    *   **Aggregation:** Groupby theo `short_p_id` từ 12 triệu dòng để tính: Tỷ lệ đi tập, Chuỗi tập dài nhất, Phong độ 30 ngày gần nhất, Thâm niên (Seniority).
    *   **Cleaning:** Làm sạch cột Thu nhập (Census) và hồ sơ Demo.
    *   **Labeling:** Dán nhãn `Target_Churn` dựa trên ngưỡng đã tìm ở Bước 1 và mốc ngày 01/01/2019.
    *   **Merging:** Hợp nhất (Join) Behavior + Demo + Census + PPTData.

## Bước 3: Lưu trữ và Chia sẻ (Team Handover)
*   **Việc cần làm:**
    *   Lưu file kết quả dưới định dạng **`.parquet`** (Tối ưu cho dữ liệu lớn, nhẹ hơn 10 lần CSV).
    *   Tạo tài liệu mô tả cột (Data Dictionary) để nhóm thống nhất logic.
*   **Đầu ra:** File `dataMaster/gym_churn_master_final.parquet`.

## Bước 4: Huấn luyện & Đánh giá (Modeling)
*   **Việc cần làm:**
    *   Chia dữ liệu Train/Test (Đề xuất 80/20).
    *   Thử nghiệm thuật toán: **XGBoost**, **Random Forest**.
    *   **Chỉ số ưu tiên:** F1-Score và AUC-ROC (Do dữ liệu Churn bị mất cân bằng).

---
**Người lập kế hoạch:** Antigravity AI Expert
**Ngày cập nhật:** 16/05/2026
