# Dự báo điện năng thiết bị gia dụng — 10 phút kế tiếp

> **Đồ án kết thúc học phần Học máy cơ bản** — Project 21  
> Chủ đề: Bài 7 — Rò rỉ dữ liệu, chia tập đúng và đánh giá trung thực  
> Lớp: 12523W.1 • GV: PGS.TS. Nguyễn Văn Hậu

## Câu hỏi nghiên cứu

Pipeline theo thời gian có dự báo tốt hơn baseline persistence mà không sử dụng thông tin tương lai không?

## Mô tả ngắn

Hệ thống dự báo mức tiêu thụ điện của thiết bị gia dụng (Appliances, đơn vị Wh)
ở bước 10 phút kế tiếp (t+1), dựa trên lịch sử cảm biến nhiệt/ẩm trong nhà,
thời tiết, và lag của Appliances.

- **Dữ liệu:** [Appliances Energy Prediction](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction) — UCI, CC BY 4.0
- **Mô hình chính:** RandomForestRegressor (n_estimators=200, max_depth=8)
- **Baseline:** Persistence — dự đoán t+1 bằng Appliances tại t
- **Chỉ số:** MAE, RMSE; MAE giờ cao điểm (17–19h), MAE theo tháng

## Cấu trúc thư mục

```
├── app/                    # Ứng dụng web (FastAPI + HTML/CSS/JS)
│   ├── main.py             # API server
│   └── static/index.html   # Giao diện 3 màn hình
├── data/
│   ├── README.md           # Nguồn, giấy phép, checksum, trích dẫn
│   └── raw/
│       ├── data_dictionary.md  # Mô tả từng biến
│       └── energydata_complete.csv  # (tải bằng script, không có trong Git)
├── models/
│   ├── model_config.json        # Cấu hình + seed + metric
│   ├── serving_model.joblib     # Mô hình phục vụ API (train+val)
│   ├── rf_pipeline.joblib       # Mô hình thí nghiệm
│   └── ridge_pipeline.joblib    # Mô hình thí nghiệm
├── reports/
│   ├── experiments.md           # Bảng thí nghiệm 4 TN bắt buộc
│   ├── error_analysis_notes.md  # Nhận xét phân tích lỗi
│   ├── model_card.md            # Model card
│   ├── weekly_log.md            # Nhật ký 6 tuần
│   ├── test_predictions.csv     # Dự đoán trên tập test
│   └── figures/                 # Biểu đồ EDA + phân tích lỗi
├── src/
│   ├── data.py              # Tải + kiểm tra dữ liệu
│   ├── data_quality.py      # Báo cáo chất lượng dữ liệu
│   ├── features.py          # Tạo lag, đặc trưng lịch, chia tập
│   ├── eda.py               # EDA trên tập train
│   ├── baseline.py          # Baseline persistence
│   ├── train.py             # Huấn luyện Ridge + RF, chọn tham số
│   ├── train_final.py       # Huấn luyện mô hình phục vụ (train+val)
│   ├── final_evaluation.py  # Đánh giá cuối trên test (chỉ chạy 1 lần)
│   ├── error_analysis.py    # Vẽ biểu đồ phân tích lỗi
│   ├── exp_random_split.py  # TN2: Random split vs Time split
│   ├── exp_ablation_lag.py  # TN3: Ablation lag
│   └── exp_random_vars.py   # TN4: rv1/rv2
├── tests/
│   ├── test_features.py     # Test tạo đặc trưng
│   └── test_api.py          # Test API
├── project_brief.md         # Định nghĩa bài toán
├── requirements.txt         # Thư viện Python
└── README.md                # File này
```

## Hướng dẫn chạy từ máy mới

### 1. Cài đặt môi trường

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Tải dữ liệu

```bash
cd src
python data.py
```

Script sẽ tải file từ UCI, giải nén, lưu vào `data/raw/energydata_complete.csv`,
in SHA-256 để đối chiếu với `data/README.md`.

### 3. Chạy pipeline phân tích (tùy chọn, kết quả đã có sẵn)

```bash
cd src

# Báo cáo chất lượng dữ liệu
python data_quality.py

# EDA (lưu biểu đồ vào reports/figures/)
python eda.py

# Baseline persistence
python baseline.py

# Huấn luyện + chọn mô hình (Ridge, RandomForest)
python train.py

# Thí nghiệm bắt buộc
python exp_random_split.py    # TN2
python exp_ablation_lag.py    # TN3
python exp_random_vars.py     # TN4

# Đánh giá cuối trên test (CHỈ CHẠY MỘT LẦN)
python final_evaluation.py

# Phân tích lỗi (vẽ biểu đồ)
python error_analysis.py
```

### 4. Huấn luyện mô hình phục vụ API

```bash
cd src
python train_final.py
```

Lưu `models/serving_model.joblib` và `models/model_config.json`.

### 5. Chạy ứng dụng web

```bash
# Từ thư mục gốc repo
uvicorn app.main:app --reload --port 8000
```

Truy cập:
- **Giao diện web:** http://localhost:8000
- **API docs (Swagger):** http://localhost:8000/docs
- **API endpoint:** `POST http://localhost:8000/api/next-energy`

### 6. Chạy test

```bash
pytest tests/ -v
```

## Ví dụ sử dụng API

### Request

```bash
curl -X POST http://localhost:8000/api/next-energy \
  -H "Content-Type: application/json" \
  -d '{
    "appliances_history": [60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60, 60, 50, 60, 50, 60, 50, 60, 50, 60],
    "current_sensors": {
      "T1": 20, "RH_1": 40, "T2": 20, "RH_2": 40,
      "T3": 20, "RH_3": 40, "T4": 20, "RH_4": 40,
      "T5": 20, "RH_5": 40, "T6": 15, "RH_6": 50,
      "T7": 20, "RH_7": 40, "T8": 20, "RH_8": 40,
      "T9": 20, "RH_9": 40,
      "T_out": 15, "Press_mm_hg": 750, "RH_out": 60,
      "Windspeed": 3, "Visibility": 40, "Tdewpoint": 8,
      "lights": 0
    },
    "timestamp": "2016-05-10T18:30:00"
  }'
```

### Response (thành công — 200)

```json
{
  "prediction_wh": 58.42,
  "unit": "Wh",
  "model_version": "rf_v1"
}
```

### Response (lỗi đầu vào — 422)

```json
{
  "detail": "RH_1=500 nằm ngoài miền hợp lệ [0, 100]"
}
```

## Kết quả chính (tập test)

| Chỉ số | Persistence | RandomForest |
|---|---|---|
| MAE | 26.723 Wh | 30.920 Wh |
| RMSE | 66.786 Wh | 62.271 Wh |
| MAE giờ cao điểm (17–19h) | 46.667 Wh | 61.985 Wh |

> **Lưu ý:** Mô hình ML không đánh bại persistence về MAE trên tập test.
> RandomForest tốt hơn ở RMSE (sai số lớn), nhưng kém ở MAE.
> Xem phân tích chi tiết tại `reports/experiments.md` và `reports/model_card.md`.

## Trích dẫn

```
Candanedo, L. (2017). Appliances Energy Prediction [Dataset].
UCI Machine Learning Repository. https://doi.org/10.24432/C5VC8G
```

## Công cụ hỗ trợ

Có sử dụng AI (Google Gemini) để hỗ trợ viết code và debug. Toàn bộ code
đã được kiểm tra, hiểu và chỉnh sửa bởi thành viên nhóm. Kết quả thí nghiệm
được chạy và xác minh độc lập.