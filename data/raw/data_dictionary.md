# Data Dictionary — Appliances Energy Prediction

Đơn vị quan sát: 1 dòng = 1 khoảng 10 phút. Dữ liệu đã sắp xếp theo `date`.

| Biến | Kiểu | Đơn vị | Vai trò | Có sẵn tại thời điểm t? | Mô tả |
|---|---|---|---|---|---|
| date | datetime | - | Thời gian/khóa | Có | Mốc thời gian của bản ghi, bước 10 phút |
| Appliances | int | Wh | Target (sau khi shift) | Có (là target khi shift(-1)) | Điện năng tiêu thụ bởi thiết bị gia dụng |
| lights | int | Wh | Feature | Có | Điện năng tiêu thụ bởi đèn |
| T1 | float | °C | Feature | Có | Nhiệt độ trong bếp |
| RH_1 | float | % | Feature | Có | Độ ẩm tương đối trong bếp |
| T2 | float | °C | Feature | Có | Nhiệt độ phòng khách |
| RH_2 | float | % | Feature | Có | Độ ẩm phòng khách |
| T3 | float | °C | Feature | Có | Nhiệt độ phòng giặt |
| RH_3 | float | % | Feature | Có | Độ ẩm phòng giặt |
| T4 | float | °C | Feature | Có | Nhiệt độ văn phòng |
| RH_4 | float | % | Feature | Có | Độ ẩm văn phòng |
| T5 | float | °C | Feature | Có | Nhiệt độ phòng tắm |
| RH_5 | float | % | Feature | Có | Độ ẩm phòng tắm |
| T6 | float | °C | Feature | Có | Nhiệt độ ngoài trời (phía bắc nhà) |
| RH_6 | float | % | Feature | Có | Độ ẩm ngoài trời (phía bắc nhà) |
| T7 | float | °C | Feature | Có | Nhiệt độ phòng ủi |
| RH_7 | float | % | Feature | Có | Độ ẩm phòng ủi |
| T8 | float | °C | Feature | Có | Nhiệt độ phòng ngủ thiếu niên |
| RH_8 | float | % | Feature | Có | Độ ẩm phòng ngủ thiếu niên |
| T9 | float | °C | Feature | Có | Nhiệt độ phòng ngủ bố mẹ |
| RH_9 | float | % | Feature | Có | Độ ẩm phòng ngủ bố mẹ |
| T_out | float | °C | Feature | Có | Nhiệt độ ngoài trời, từ trạm thời tiết Chievres |
| Press_mm_hg | float | mm Hg | Feature | Có | Áp suất khí quyển |
| RH_out | float | % | Feature | Có | Độ ẩm ngoài trời |
| Windspeed | float | m/s | Feature | Có | Tốc độ gió |
| Visibility | float | km | Feature | Có | Tầm nhìn |
| Tdewpoint | float | °C | Feature | Có | Điểm sương |
| rv1 | float | - | Loại khỏi mô hình chính | Có | Biến ngẫu nhiên, dùng riêng cho thí nghiệm 4 |
| rv2 | float | - | Loại khỏi mô hình chính | Có | Biến ngẫu nhiên, dùng riêng cho thí nghiệm 4 |

## Đặc trưng phái sinh (tạo trong `src/features.py`, không có sẵn trong file gốc)

| Biến | Công thức | Vai trò | Có sẵn tại thời điểm t? |
|---|---|---|---|
| lag_1 | Appliances.shift(1) | Feature | Có (là giá trị tại t-1) |
| lag_6 | Appliances.shift(6) | Feature | Có (là giá trị tại t-6, tức 1 giờ trước) |
| lag_144 | Appliances.shift(144) | Feature | Có (là giá trị tại t-144, tức 1 ngày trước) |
| hour | date.dt.hour | Feature | Có |
| dayofweek | date.dt.dayofweek | Feature | Có |
| target | Appliances.shift(-1) | Target | Không — đây là giá trị tương lai (t+1), chỉ dùng làm nhãn |

## Ghi chú quan trọng

- Dữ liệu từ **một ngôi nhà ở Bỉ** (thị trấn gần Chievres), khoảng 4,5 tháng (11/01/2016 – 27/05/2016). Không khái quát cho mọi hộ gia đình.
- `rv1`, `rv2` là biến ngẫu nhiên (theo mô tả gốc của tác giả dữ liệu), dùng để kiểm tra xem pipeline/mô hình có bị "học nhiễu" hay không, không đưa vào mô hình chính.
- Tạo `lag_144` sẽ làm mất 144 dòng đầu (do chưa có đủ lịch sử 1 ngày trước), và `target` làm mất 1 dòng cuối (do chưa có t+1). Tổng cộng mất 145 dòng sau khi `dropna()`.
- Không dùng `Appliances` tại t+1 hay bất kỳ biến thời tiết nào của tương lai để tạo feature — đây chính là quy tắc chống rò rỉ dữ liệu của đề.