# Nhật ký thực hiện — 6 tuần

## Tuần 1 (28/09 – 04/10/2026)
**Người thực hiện:** Hoàng Minh Hiếu | **Giờ ước lượng:** ~8h

| Công việc | Kết quả | Ghi chú |
|---|---|---|
| Đọc đề bài, chốt câu hỏi nghiên cứu | `project_brief.md` | Câu hỏi: pipeline time-split có tốt hơn persistence? |
| Tạo repo Git, cấu trúc thư mục | Repo trên GitHub | `src/`, `app/`, `data/`, `models/`, `reports/`, `tests/` |
| Viết script tải dữ liệu từ UCI | `src/data.py` | Download + SHA-256 + kiểm tra schema |
| Viết data dictionary | `data/raw/data_dictionary.md` | 29 biến gốc + 6 biến phái sinh, ghi rõ thời điểm có sẵn |
| Viết data README | `data/README.md` | Nguồn, giấy phép, checksum, trích dẫn |

**Vấn đề:** Không có vấn đề lớn. Dữ liệu sạch (0 missing, 0 trùng lặp).

---

## Tuần 2 (05/10 – 11/10/2026)
**Người thực hiện:** Hoàng Minh Hiếu | **Giờ ước lượng:** ~10h

| Công việc | Kết quả | Ghi chú |
|---|---|---|
| Báo cáo chất lượng dữ liệu | `src/data_quality.py` | IQR outlier: 6.8% dòng vượt ngưỡng Appliances |
| EDA trên tập train | `src/eda.py`, 3 biểu đồ | Target lệch phải mạnh; giờ cao điểm 17–19h; lag_1 tương quan 0.548 |
| Xây dựng features + time split | `src/features.py` | Lag 1/6/144, hour, dayofweek; chia 70/15/15 theo thời gian |
| Baseline persistence | `src/baseline.py` | MAE train=30.833, MAE val=25.786 |

**Vấn đề:** Target phân bố lệch phải rất mạnh (median 60, mean 97), cần lưu ý khi đánh giá sai số tại đỉnh.

**Quyết định:** Xác định giờ cao điểm 17–19h từ biểu đồ EDA → dùng cho metric phụ.

---

## Tuần 3 (12/10 – 18/10/2026)
**Người thực hiện:** Hoàng Minh Hiếu | **Giờ ước lượng:** ~12h

| Công việc | Kết quả | Ghi chú |
|---|---|---|
| Huấn luyện Ridge (GridSearchCV + TimeSeriesSplit) | `src/train.py` | Alpha tốt nhất = 300, MAE val = 27.896 |
| Huấn luyện RandomForest | `src/train.py` | MAE val = 26.210, RMSE val = 57.211 — ứng viên tốt nhất |
| Lưu pipeline | `models/ridge_pipeline.joblib`, `models/rf_pipeline.joblib` | Cả scaler + model trong Pipeline |
| Ghi bảng thí nghiệm vòng 1 | `reports/experiments.md` | So sánh 3 mô hình trên cùng split |

**Vấn đề:** Cả Ridge và RF đều không đánh bại persistence về MAE trên val. RF gần nhất (26.210 vs 25.786). RMSE của RF tốt hơn persistence (57.211 vs 65.513).

**Quyết định:** Chọn RF làm mô hình chính (MAE gần sát persistence, RMSE tốt nhất). Sẽ giải thích rõ trong phân tích lỗi.

---

## Tuần 4 (19/10 – 25/10/2026)
**Người thực hiện:** Hoàng Minh Hiếu | **Giờ ước lượng:** ~14h

| Công việc | Kết quả | Ghi chú |
|---|---|---|
| TN2: Random split vs Time split | `src/exp_random_split.py` | Random split MAE=28.881 > Time split MAE=28.436 — ngược kỳ vọng, do mùa vụ |
| TN3: Ablation lag | `src/exp_ablation_lag.py` | lag_1 cải thiện MAE 1.38 Wh; lag_6/144 cải thiện nhẹ |
| TN4: rv1/rv2 | `src/exp_random_vars.py` | Chênh lệch 0.0044 ± 0.0094 — rv1/rv2 không có tín hiệu |
| Đánh giá cuối trên test (1 lần) | `src/final_evaluation.py` | MAE test = 30.920, RMSE test = 62.271 |
| Phân tích lỗi | `src/error_analysis.py`, 3 biểu đồ | MAE đỉnh 108.6 vs bình thường 21.8; giờ 17h sai nhất |
| Model card nháp | `reports/model_card.md` | Ghi rõ giới hạn: 1 nhà, không tính tiền, sai nhiều ở đỉnh |

**Vấn đề:** TN2 cho kết quả ngược chiều: random split không lạc quan hơn time split. Phân tích cho thấy do validation của random split trải đều 4.5 tháng (gồm mùa đông biến động), còn time split chỉ nằm cuối tháng 4–5.

**Quyết định:** Vẫn dùng time split vì đúng phương pháp (mô phỏng triển khai thực tế). Ghi nhận xét trung thực trong experiments.md.

---

## Tuần 5 (26/10 – 01/11/2026)
**Người thực hiện:** Hoàng Minh Hiếu | **Giờ ước lượng:** ~14h

| Công việc | Kết quả | Ghi chú |
|---|---|---|
| Huấn luyện mô hình phục vụ (train+val) | `src/train_final.py` | `models/serving_model.joblib` + `model_config.json` |
| Xây dựng API FastAPI | `app/main.py` | POST /api/next-energy, validation Pydantic + VALID_RANGES |
| Xây dựng giao diện web 3 màn hình | `app/static/index.html` | Giới thiệu, Dự báo, Đánh giá & Model Card |
| Viết test API + test features | `tests/test_api.py`, `tests/test_features.py` | 4 test API (happy path + 3 lỗi), 4 test features |
| Kiểm tra input xấu không crash | Test thủ công | Thiếu history → 422, ngoài miền → 422, giá trị âm → 422 |

**Vấn đề:** Cần hàm `build_single_prediction_row()` trong features.py để tạo 1 dòng đặc trưng cho API, dùng cùng logic với lúc huấn luyện (tránh train/serving skew).

---

## Tuần 6 (02/11 – 08/11/2026)
**Người thực hiện:** Hoàng Minh Hiếu | **Giờ ước lượng:** ~10h

| Công việc | Kết quả | Ghi chú |
|---|---|---|
| Viết README project đầy đủ | `README.md` | Hướng dẫn cài đặt, chạy pipeline, ví dụ API |
| Hoàn thiện nhật ký, phân công, tự đánh giá | `reports/weekly_log.md`, `project_brief.md` | File này |
| Tái lập trên môi trường sạch | Test thủ công | Clone repo → pip install → data.py → train_final.py → uvicorn → OK |
| Rà soát code: đường dẫn tuyệt đối, seed | Sửa nếu có | Không có đường dẫn tuyệt đối cá nhân |
| Chuẩn bị báo cáo và slide | *(đang thực hiện)* | |

**Vấn đề:** Không có vấn đề kỹ thuật lớn ở tuần cuối.
