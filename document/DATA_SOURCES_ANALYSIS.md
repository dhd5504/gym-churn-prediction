# Phân tích Nguồn Dữ liệu - Dự án Dự đoán Churn (Gym)

## Tóm tắt nhanh

| File | Loại | Kích thước | Mức độ phù hợp | Dùng cho |
|---|---|---|---|---|
| `weather.RData` (→ `gym_data`) | Hành vi theo ngày | ~26MB | ⭐⭐⭐⭐⭐ | Feature chính |
| `gym_demo_auc.csv` | Hồ sơ cá nhân | ~6MB | ⭐⭐⭐⭐⭐ | Feature phụ |
| `pptdata.csv` | Hành vi theo tuần | ~596MB | ⭐⭐⭐⭐ | Feature phụ |
| `gym_participant_id.csv` | Bảng tra cứu | ~5.6MB | ⭐⭐⭐ | Lookup/Join key |
| `Census_Data.csv` | Khu vực sống | ~11MB | ⭐⭐⭐ | Feature bổ sung |
| `gym_coef.RData` | Hệ số mô hình cũ | ~4.4MB | ⭐⭐ | Tham khảo |
| `hand_data.RData` | Dữ liệu rửa tay BV | ~596MB | ❌ | KHÔNG dùng |
| `hand_coef.RData` | Hệ số rửa tay BV | ~468KB | ❌ | KHÔNG dùng |
| `gym_lasso*.RData` | Mô hình Lasso cũ | ~580-723MB | ❌ | KHÔNG dùng |

---

## Nhận xét chi tiết từng file

### ✅ 1. `weather.RData` → `sample_R_weather.RData_weather.csv`
**Đây là file quan trọng nhất cho bài toán Churn.**

**Các cột quan trọng:**
- `short_p_id`: ID người tập (khóa nối với các bảng khác)
- `date`: Ngày quan sát
- `attended` (0/1): **Đây chính là biến mục tiêu cần tổng hợp!**
- `time_lag`: Số ngày kể từ lần tập cuối → **Feature Recency quan trọng nhất**
- `streak`: Số ngày tập liên tiếp hiện tại → **Feature quan trọng thứ 2**
- `last7days_attendance`: Tần suất 7 ngày gần nhất → **Feature Frequency**
- `good_weather` / `bad_weather`: Yếu tố ngoại cảnh
- `pre_habit` / `post_habit`: Thói quen trước/sau → gợi ý hành vi dài hạn
- `tstar`: Ngưỡng thời gian dự đoán

**Lưu ý:** File `weather.RData` mặc dù tên là "thời tiết" nhưng thực chất là **bảng dữ liệu hành vi đi tập theo từng ngày** kết hợp với yếu tố thời tiết. Đây là cấu trúc lý tưởng nhất để xây dựng target Churn.

---

### ✅ 2. `gym_demo_auc.csv` → `sample_gym_demo_auc.csv`
**Bảng hồ sơ cá nhân của học viên.**

**Các cột quan trọng:**
- `short_p_id` / `participant_id`: Khóa nối
- `att_rate`: Tỷ lệ đi tập tổng thể → Feature tổng quan
- `N_obs`: Số ngày quan sát → Biết được thâm niên
- `gender`: Giới tính
- `age` / `birthyear`: Độ tuổi
- `main_density_class`: Loại khu vực (1st Tier Suburban, Rural...) → Quan trọng
- `customer_postal`: Mã bưu điện → Dùng để join với Census
- `first_att_year`: Năm bắt đầu tập → Tính thâm niên
- `auc_holdout` / `auc_train`: Độ chính xác mô hình cũ trên từng người

---

### ✅ 3. `pptdata.csv` → `sample_pptdata.csv`
**Bảng hành vi theo tuần của học viên (cấu trúc dạng panel data).**

**Các cột quan trọng:**
- `week`: Số tuần (âm = trước khi đăng ký, dương = sau khi đăng ký)
- `visits`: Số buổi tập trong tuần đó
- `any_visit` (0/1): Có đi tập tuần đó không
- `age`, `gender`, `customer_state`: Thông tin cá nhân
- `exp_condition`: Nhóm thí nghiệm (Có cam kết tập luyện hay không)
- `new_member`: Hội viên mới hay cũ

**Lưu ý:** File này sẽ cần xử lý nặng (596MB) vì mỗi người có nhiều hàng (nhiều tuần). Cần group by `participant_id` để tổng hợp trước khi dùng.

---

### ⚠️ 4. `gym_participant_id.csv`
**Bảng tra cứu thuần túy.** Chỉ chứa `att_rate` và `N_obs` tổng hợp. Thông tin này đã có đầy đủ hơn trong `gym_demo_auc.csv`. Dùng để join key khi cần.

---

### ⚠️ 5. `Census_Data.csv`
Cung cấp thông tin kinh tế khu vực (Thu nhập, Mật độ dân cư) theo mã bưu điện `customer_postal`. Bổ sung cho `gym_demo_auc.csv`.

---

### ❌ 6. `hand_data.RData` / `hand_coef.RData`
**KHÔNG liên quan đến bài toán Gym.**
Đây là dữ liệu về **việc rửa tay trong bệnh viện** (`hospital_tag`, `shift7id`, `compliant`, `dispense_count`). Cấu trúc dữ liệu tương tự nhưng hoàn toàn khác domain. Bỏ qua hoàn toàn.

---

### ❌ 7. `gym_lasso0.RData` / `gym_lasso1.RData` / `gym_lasso.RData`
Đây là các mô hình Lasso đã train sẵn từ nghiên cứu trước. Không phải dữ liệu thô. Bỏ qua trong giai đoạn phân tích, có thể tham khảo sau.

---

## Kết luận: Bộ dữ liệu cần sử dụng

### Nguồn dữ liệu chính để train model:
```
weather.RData (gym_data)   →  Biến mục tiêu (attended, time_lag) + Features hành vi
gym_demo_auc.csv           →  Features nhân khẩu học (tuổi, giới tính, khu vực)
Census_Data.csv            →  Features kinh tế khu vực (thu nhập)
pptdata.csv                →  Features thí nghiệm (treatment group) - xử lý sau
```

### Khóa nối giữa các bảng:
```
weather.RData.short_p_id  ←→  gym_demo_auc.short_p_id  ←→  Census qua customer_postal
```

### Định nghĩa Biến mục tiêu (Target):
Dựa trên cột `time_lag` từ `weather.RData`:
- **Churn = 1**: Nếu `time_lag > 30` tại thời điểm quan sát cuối cùng
- **Active = 0**: Ngược lại
