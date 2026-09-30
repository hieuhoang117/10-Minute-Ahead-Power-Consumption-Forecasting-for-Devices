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

## Thí nghiệm 2: Random split vs Time split (RandomForest, cùng tỷ lệ 85/15)
| Cách chia | MAE (val) | RMSE (val) |
|---|---|---|
| Time split | 28.436 | 60.317 |
| Random split | 28.881 | 64.725 |

Nhận xét: Trái với giả thuyết thông thường rằng random split cho kết quả lạc
quan giả (MAE thấp hơn do rò rỉ dữ liệu giữa các mốc thời gian liền kề), ở đây
random split lại cho MAE và RMSE cao hơn. Khả năng cao nguyên nhân là do hai
tập validation có đặc điểm mùa khác nhau: validation của time split chỉ nằm
trong 15% cuối chuỗi (cuối tháng 4 - cuối tháng 5), trong khi validation của
random split trải đều trên toàn bộ 4,5 tháng bao gồm cả mùa đông. Nếu mùa đông
có mức tiêu thụ biến động và khó dự đoán hơn, hiệu ứng này có thể lấn át hiệu
ứng rò rỉ dữ liệu.

Dù kết quả số liệu không theo đúng chiều dự đoán thông thường, quyết định dùng
time split cho toàn bộ bai vẫn đúng về mặt phương pháp: đây là cách chia duy
nhất mô phỏng đúng tình huống triển khai thực tế, nơi mô hình chỉ có dữ liệu
quá khứ để dự đoán tương lai, không có quyền truy cập ngẫu nhiên vào các mốc
thời gian sau đó như random split vô tình cho phép. Time split vẫn là kết quả
chính được báo cáo trong toàn bộ bai.

## Thí nghiệm 3: Ablation lag (RandomForest)
| Cấu hình | Số cột | MAE (val) | RMSE (val) |
|---|---|---|---|
| Không lag | 28 | 27.727 | 60.171 |
| Chỉ lag_1 | 29 | 26.347 | 57.335 |
| lag_1 + lag_6 | 30 | 26.257 | 57.298 |
| lag_1 + lag_6 + lag_144 | 31 | 26.210 | 57.211 |

Nhận xét: lag_1 đóng góp cải thiện lớn nhất (MAE giảm 1.38), khớp với tương quan
đã thấy ở tuần 2 (lag_1 tương quan 0.548 với target, cao nhất trong các lag).
lag_6 và lag_144 chỉ cải thiện rất nhẹ, phù hợp với tương quan yếu hơn của chúng
(0.295 và 0.201). Vẫn giữ cả 3 lag trong mô hình cuối vì chúng không gây hại và
mang lại cải thiện dù nhỏ.

## Thí nghiệm 4: rv1/rv2 (RandomForest, 5 seed: 0-4)
| | MAE trung bình | Std |
|---|---|---|
| Không có rv1/rv2 | 26.216 | 0.037 |
| Có rv1/rv2 | 26.220 | 0.037 |

Chênh lệch trung bình (có - không): 0.0044 ± 0.0094

Nhận xét: Chênh lệch MAE khi thêm rv1/rv2 gần như bằng 0 (0.0044 Wh), nhỏ hơn
nhiều lần so với độ lệch chuẩn tự nhiên giữa các seed (0.037). Điều này khẳng
định rv1/rv2 — vốn là biến ngẫu nhiên theo mô tả gốc của bộ dữ liệu — không
mang lại thông tin dự báo nào, đúng như kỳ vọng. Đây là bằng chứng cho thấy
pipeline không bị overfitting vào nhiễu và hoạt động đúng như thiết kế.