# ============================================================
# Script: extract_mvp_data.R
# Mục đích: Lấy mẫu MVP từ các bảng dữ liệu chính vào thư mục data_analysis
# Nguyên tắc: Sample theo short_p_id để đảm bảo tính nhất quán khi join
# ============================================================

setwd("C:/GitRepo/dataAnalyst")

# Cấu hình
N_PERSONS <- 2000        # Số người lấy mẫu
SEED      <- 42          # Seed để tái tạo kết quả
OUTPUT_DIR <- "data_analysis"

if (!dir.exists(OUTPUT_DIR)) dir.create(OUTPUT_DIR)

cat("========================================\n")
cat("  Bắt đầu trích xuất dữ liệu MVP\n")
cat("  Sample size:", N_PERSONS, "người\n")
cat("========================================\n\n")

# ============================================================
# BƯỚC 1: Load weather.RData và chọn danh sách short_p_id mẫu
# ============================================================
cat("[1/4] Đang load weather.RData...\n")
load("Data/weather.RData")

# Kiểm tra tên object trong file
weather_obj <- ls()[ls() != "N_PERSONS" & ls() != "SEED" & ls() != "OUTPUT_DIR"]
cat("  -> Các object trong weather.RData:", paste(weather_obj, collapse=", "), "\n")

# Lấy tên bảng thực tế (thường là 'gym_data' hoặc 'weather')
gym_weather <- get(weather_obj[1])
cat("  -> Kích thước bảng gốc:", nrow(gym_weather), "dòng x", ncol(gym_weather), "cột\n")

# Lấy danh sách short_p_id duy nhất và chọn mẫu ngẫu nhiên
set.seed(SEED)
all_ids <- unique(gym_weather$short_p_id)
cat("  -> Tổng số người:", length(all_ids), "\n")

sampled_ids <- sample(all_ids, min(N_PERSONS, length(all_ids)))
cat("  -> Đã chọn", length(sampled_ids), "người\n")

# Lọc dữ liệu weather theo danh sách ID đã chọn
weather_sample <- gym_weather[gym_weather$short_p_id %in% sampled_ids, ]
cat("  -> Số dòng sau lọc:", nrow(weather_sample), "\n")

# Lưu file
write.csv(weather_sample, file.path(OUTPUT_DIR, "mvp_weather_behavior.csv"), row.names = FALSE)
cat("  -> Đã lưu: data_analysis/mvp_weather_behavior.csv\n\n")

# Giải phóng bộ nhớ
rm(gym_weather)
gc()

# ============================================================
# BƯỚC 2: Lọc gym_demo_auc.csv theo danh sách ID
# ============================================================
cat("[2/4] Đang xử lý gym_demo_auc.csv...\n")
demo_df <- read.csv("Data/gym_demo_auc.csv")
cat("  -> Kích thước gốc:", nrow(demo_df), "dòng x", ncol(demo_df), "cột\n")

demo_sample <- demo_df[demo_df$short_p_id %in% sampled_ids, ]
cat("  -> Số dòng sau lọc:", nrow(demo_sample), "\n")

write.csv(demo_sample, file.path(OUTPUT_DIR, "mvp_gym_demo.csv"), row.names = FALSE)
cat("  -> Đã lưu: data_analysis/mvp_gym_demo.csv\n\n")
rm(demo_df); gc()

# ============================================================
# BƯỚC 3: Lọc gym_participant_id.csv theo short_p_id
# ============================================================
cat("[3/5] Đang xử lý gym_participant_id.csv...\n")
participant_df <- read.csv("Data/gym_participant_id.csv")
cat("  -> Kích thước gốc:", nrow(participant_df), "dòng x", ncol(participant_df), "cột\n")

participant_sample <- participant_df[participant_df$short_p_id %in% sampled_ids, ]
cat("  -> Số dòng sau lọc:", nrow(participant_sample), "\n")

write.csv(participant_sample, file.path(OUTPUT_DIR, "mvp_participant_id.csv"), row.names = FALSE)
cat("  -> Đã lưu: data_analysis/mvp_participant_id.csv\n\n")
rm(participant_df); gc()

# ============================================================
# BƯỚC 4: Lọc pptdata.csv theo participant_id
# (pptdata dùng participant_id dạng UUID, cần map qua demo)
# ============================================================
cat("[4/5] Đang xử lý pptdata.csv (file lớn ~596MB, vui lòng chờ)...\n")

# Lấy danh sách participant_id tương ứng từ demo
sampled_participant_ids <- demo_sample$participant_id

# Đọc theo chunk để tiết kiệm RAM
chunk_size <- 500000
ppt_sample <- data.frame()
con <- file("Data/pptdata.csv", open="r")
header <- readLines(con, n=1)
col_names <- strsplit(header, ",")[[1]]

repeat {
  lines <- readLines(con, n=chunk_size)
  if (length(lines) == 0) break
  
  chunk <- read.csv(text=c(header, lines))
  matched <- chunk[chunk$participant_id %in% sampled_participant_ids, ]
  ppt_sample <- rbind(ppt_sample, matched)
  cat("  -> Đã đọc chunk, tổng dòng khớp:", nrow(ppt_sample), "\r")
}
close(con)

cat("\n  -> Tổng số dòng pptdata sau lọc:", nrow(ppt_sample), "\n")
write.csv(ppt_sample, file.path(OUTPUT_DIR, "mvp_ppt_weekly.csv"), row.names = FALSE)
cat("  -> Đã lưu: data_analysis/mvp_ppt_weekly.csv\n\n")
rm(ppt_sample); gc()

# ============================================================
# BƯỚC 4: Lấy toàn bộ Census_Data (nhỏ, là bảng tra cứu)
# ============================================================
cat("[5/5] Đang xử lý Census_Data.csv...\n")
census_df <- read.csv("Data/Census_Data.csv")
cat("  -> Kích thước:", nrow(census_df), "dòng x", ncol(census_df), "cột\n")

write.csv(census_df, file.path(OUTPUT_DIR, "mvp_census.csv"), row.names = FALSE)
cat("  -> Đã lưu: data_analysis/mvp_census.csv\n\n")

# ============================================================
# HOÀN TẤT
# ============================================================
cat("========================================\n")
cat("  HOÀN TẤT! Các file MVP đã được lưu:\n")
cat("  - data_analysis/mvp_weather_behavior.csv  (hành vi ngày - CHÍNH)\n")
cat("  - data_analysis/mvp_gym_demo.csv          (hồ sơ học viên)\n")
cat("  - data_analysis/mvp_participant_id.csv    (bảng tra cứu ID + att_rate)\n")
cat("  - data_analysis/mvp_ppt_weekly.csv        (hành vi tuần + treatment)\n")
cat("  - data_analysis/mvp_census.csv            (kinh tế khu vực)\n")
cat("========================================\n")
cat("Tổng ID đã sample:", length(sampled_ids), "người\n")
cat("Seed sử dụng:", SEED, "(để tái tạo kết quả)\n")
