# Bảng thí nghiệm — Vòng 1 (tuần 3)

| Ngày | Mô hình | Tham số | MAE (train) | MAE (val) | RMSE (val) | Ghi chú |
|---|---|---|---|---|---|---|
| 2026-09-30 | Persistence | - | 30.833 | 25.786 | 65.513 | Baseline |
| 2026-09-30 | Ridge (v1) | alpha=100 (CV) | 31.744 | 28.174 | 60.012 | Alpha ở biên lưới ban đầu |
| 2026-09-30 | Ridge (v2) | alpha=300 (CV, lưới mở rộng) | 31.753 | 27.896 | 60.019 | Cải thiện nhẹ, không còn ở biên |
| 2026-09-30 | RandomForest | depth=8, leaf=20 | 26.840 | 26.210 | 57.211 | Ứng viên tốt nhất, mang sang tuần 4 |

## Nhận xét
RandomForest được chọn làm mô hình chính cho các thí nghiệm bắt buộc (tuần 4),
vì có MAE gần sát persistence và RMSE thấp nhất trong ba mô hình. Cả hai mô hình
ML đều không đánh bại persistence về MAE trên validation — điều này phù hợp với
phân tích tương quan ở tuần 2 (Appliances(t) có tương quan 0.76 với target,
mạnh hơn mọi lag). Sẽ giải thích rõ hiện tượng này trong phần phân tích lỗi.

## Cấu hình chạy
- random_state: 42 (dùng thống nhất cho Ridge và RandomForest)
- Python: 3.11.9
- Thư viện: xem requirements.txt
- Ngày chạy vòng 1: 2026-09-30