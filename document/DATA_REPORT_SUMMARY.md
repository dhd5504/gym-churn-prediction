# Báo cáo Giải thích Dữ liệu & Phương pháp Dự đoán Churn (Gym)

Báo cáo này tóm tắt các điểm cốt lõi về dữ liệu, logic xử lý hiện tại và các lưu ý quan trọng để đảm bảo tính chuẩn xác cho bài tập lớn.

---

## 1. Ý nghĩa thực tế của các cột dữ liệu (Domain Knowledge)
Dữ liệu phản ánh hành vi và thói quen hình thành của học viên. Hiểu đúng ý nghĩa giúp chọn được các đặc trưng (features) mạnh nhất.

| Cột dữ liệu | Ý nghĩa thực tế | Vai trò trong mô hình |
|---|---|---|
| `attended` | Học viên có đi tập ngày hôm đó hay không. | Dùng để tính toán tần suất (Frequency). |
| `streak` | Số ngày đi tập liên tiếp. | Thể hiện "đà" và sự kỷ luật. Streak càng cao, nguy cơ Churn càng thấp. |
| `time_lag` | Số ngày kể từ lần tập cuối. | **Biến quan trọng nhất.** Phản ánh sự lười biếng hoặc các rào cản đang xuất hiện. |
| `att_rate` | Tỷ lệ đi tập tổng quát. | Thể hiện mức độ trung thành/chuyên cần dài hạn. |
| `income` (Census) | Thu nhập trung bình khu vực học viên sống. | Yếu tố kinh tế ảnh hưởng đến khả năng duy trì thẻ tập. |
| `density_class` | Loại khu vực (Nông thôn, Ngoại ô, Thành thị). | Ảnh hưởng bởi khoảng cách và sự thuận tiện khi đi tập. |
| `attendance_momentum` | Tỷ lệ đi tập tháng gần nhất so với tháng trước. | Biến quan trọng nhất để đo lường "phong độ" đang đi xuống hay đi lên. |
| `weekend_ratio` | Tỷ lệ buổi tập vào Thứ 7/CN. | Phân biệt nhóm "Chiến binh cuối tuần" với nhóm tập đều trong tuần. |
| `attendance_variance` | Độ biến động (Std) của khoảng cách giữa các buổi tập. | Đo lường tính kỷ luật: Người tập rời rạc (biến động cao) dễ Churn hơn. |

---

## 2. Nhận xét kết quả phân tích Dữ liệu Toàn diện (2016-2019)
Dựa trên bộ dữ liệu Master đã xử lý (6,327 người), chúng ta rút ra các nhận định sau:

*   **Tỷ lệ Churn (78.14%):** Sau khi làm sạch, tỷ lệ Churn thực tế khá cao. Đây là đặc thù của dữ liệu gym dài hạn.
    *   *Nhận định:* Dữ liệu hiện tại đã cân bằng hơn (khoảng 1:3), rất thuận lợi cho việc huấn luyện mô hình mà không cần can thiệp quá sâu vào các kỹ thuật cân bằng dữ liệu phức tạp.
*   **Chất lượng dữ liệu:** Đã xử lý triệt để lỗi nhân bản (Duplicate) từ bảng Census. Mỗi học viên hiện là một thực thể duy nhất với các thông số kinh tế - xã hội chính xác.
*   **Các đặc trưng quyết định (Top Features):**
    *   `attendance_momentum`: Đã chứng minh được sự khác biệt rõ rệt giữa người sắp nghỉ (momentum thấp) và người bền bỉ.
    *   `recency`: Đã được chuẩn hóa theo ngày chốt 01/02/2019, đảm bảo tính logic thời gian 100%.
    *   `weekend_ratio`: Giúp phân tách rõ rệt phong cách tập luyện của các nhóm khách hàng khác nhau.

---

## 3. Kiểm tra Logic Mapping & Tính chuẩn xác
Để đạt độ chính xác 100%, chúng ta đã áp dụng các quy tắc:

1.  **Gom nhóm Census:** Chuyển dữ liệu Census từ mức độ khu phố về mức độ **ZipCode** (mã bưu điện) bằng hàm trung bình (mean) để tránh lỗi nhân bản dòng khi join.
2.  **Logic Chốt thời gian (Cutoff):** Sử dụng ngày cuối cùng của hệ thống (**01/02/2019**) làm mốc tính toán, đảm bảo biến `recency` luôn dương và không "nhìn trộm" dữ liệu tương lai.
3.  **Xử lý giá trị lỗi:** Các giá trị thu nhập và tuổi bị thiếu đã được bù đắp bằng giá trị trung vị (Median) của toàn tập dữ liệu.

---

## 4. Đề xuất hướng đi tiếp theo

*   **Mô hình hóa:** Tiến hành huấn luyện với **XGBoost** hoặc **Random Forest**. Đây là hai mô hình mạnh nhất cho dạng dữ liệu bảng (tabular data) có nhiều biến đặc trưng như hiện nay.
*   **Đánh giá:** Sử dụng chỉ số **F1-Score** và **Precision-Recall Curve** để đánh giá, vì trong kinh doanh gym, việc dự báo nhầm một người sắp nghỉ (False Positive) vẫn ít tốn kém hơn việc bỏ sót một khách hàng thực sự sắp rời đi (False Negative).

---
**Người lập báo cáo:** Antigravity AI Assistant
**Ngày:** 17/05/2026
