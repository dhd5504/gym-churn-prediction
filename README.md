# 🏋️‍♂️ Gym Churn Prediction & Habit Formation Analysis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![ML Framework](https://img.shields.io/badge/ML-XGBoost%20%7C%20RandomForest-green.svg)](https://xgboost.readthedocs.io/)
[![Dataset](https://img.shields.io/badge/Data-PNAS%202023-orange.svg)](https://www.pnas.org/doi/10.1073/pnas.2216115120)

## 📌 Tổng quan dự án
Dự án này tập trung vào việc dự báo khả năng rời bỏ (Churn) của học viên Gym dựa trên dữ liệu hành vi thực tế kéo dài 12 năm. Mục tiêu là xác định các yếu tố dẫn đến việc hình thành thói quen và đưa ra cảnh báo sớm cho những khách hàng có nguy cơ cao nghỉ tập.

Dự án được thực hiện dựa trên dữ liệu từ nghiên cứu *"Habit formation in the wild: Evidence from gym attendance"* (PNAS 2023).

## 🚀 Các tính năng nổi bật
- **Phân tích ngưỡng Churn thực tế:** Sử dụng phương pháp xác suất quay lại để tìm ra điểm "không thể cứu vãn" (78 ngày vắng mặt).
- **ETL Pipeline mạnh mẽ:** Xử lý và hợp nhất 8.7 triệu dòng dữ liệu hành vi với thông tin nhân khẩu học và kinh tế (Census).
- **Kỹ thuật trích xuất đặc trưng (Feature Engineering):**
    - `attendance_momentum`: Tốc độ thay đổi phong độ đi tập.
    - `weekend_ratio`: Thói quen tập luyện cuối tuần.
    - `attendance_variance`: Độ kỷ luật trong việc duy trì lịch tập.

## 📁 Cấu trúc thư mục
```text
├── dataMaster/          # Chứa dữ liệu Master đã làm sạch (6,327 học viên)
├── Data/                # Dữ liệu thô (.RData, .csv)
├── scripts/             # Các script xử lý dữ liệu (ETL, Analysis)
├── notebooks/           # Jupyter Notebooks phân tích (EDA)
├── document/            # Báo cáo chi tiết và nhật ký nghiên cứu
├── reports/figures/     # Các biểu đồ kết quả phân tích
└── README.md
```

## 📊 Kết quả phân tích chính
- **Ngưỡng Churn tối ưu:** **78 ngày**. Sau thời gian này, xác suất một học viên quay lại phòng tập giảm xuống dưới 50%.
- **Tỷ lệ Churn giai đoạn 2016-2019:** **78.14%**.
- **Yếu tố ảnh hưởng mạnh nhất:** Phong độ đi tập trong 30 ngày gần nhất (`momentum`) và chuỗi ngày đi tập liên tiếp (`streak`).

## 🛠 Hướng dẫn cài đặt
1. Clone repository:
   ```bash
   git clone https://github.com/[your-username]/gym-churn-prediction.git
   ```
2. Cài đặt môi trường:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```
3. Chạy pipeline tạo dữ liệu Master:
   ```bash
   python scripts/build_master_dataset.py
   ```

## 📈 Hướng phát triển tiếp theo
- Xây dựng mô hình dự báo sử dụng XGBoost và Random Forest.
- Triển khai ứng dụng Web đơn giản để dự báo Churn theo thời gian thực.
- Phân tích tác động của các chương trình can thiệp tâm lý (Experimental groups) đến tỷ lệ giữ chân khách hàng.

---
**Tác giả:** [Tên của bạn]
**Học viện:** Đại học Bách Khoa Hà Nội (HUST)
**Liên hệ:** [Email của bạn]
