# Model Card — Dự báo Appliances (Wh) tại t+1

## Mục đích
Dự báo điện năng tiêu thụ bởi thiết bị gia dụng trong 10 phút kế tiếp, dựa trên
cảm biến nhiệt độ/độ ẩm, thời tiết, và lịch sử tiêu thụ gần đây.

## Dữ liệu huấn luyện
Một ngôi nhà tại Bỉ, 11/01/2016 - 16/04/2016 (13,713 bản ghi, mỗi 10 phút).
Nguồn: UCI Appliances Energy Prediction, giấy phép CC BY 4.0.

## Mô hình
RandomForestRegressor (n_estimators=200, max_depth=8, min_samples_leaf=20,
random_state=42). Đặc trưng: cảm biến tại t, lag_1/6/144 của Appliances,
giờ, thứ trong tuần.

## Hiệu năng (tập test, 07/05/2016 - 27/05/2016, 2,939 bản ghi)
- MAE: 30.920 Wh (so với persistence: 26.723 Wh — mô hình KHÔNG đánh bại baseline)
- RMSE: 62.271 Wh (so với persistence: 66.786 Wh — tốt hơn ở các sai số lớn)
- MAE giờ cao điểm (17h-19h): 61.985 Wh
- MAE tại đỉnh tiêu thụ (top 10%): 108.612 Wh, so với 21.825 Wh ở mức bình thường

## Giới hạn quan trọng
- Chỉ đại diện cho MỘT ngôi nhà, KHÔNG khái quát cho hộ gia đình khác.
- KHÔNG dùng để tính tiền điện hay ra quyết định tài chính.
- Tập test chỉ nằm trong tháng 5 (do dữ liệu ngắn, 4.5 tháng), có thể có phân bố
  mùa vụ khác train — hiệu năng thực tế ở các tháng khác chưa được kiểm chứng.
- Sai số tăng mạnh (gấp ~5 lần) tại các thời điểm tiêu thụ đột biến (đỉnh),
  do các đặc trưng đầu vào không nắm bắt được hành vi bật thiết bị của con người.
- Trên tập test độc lập, mô hình ML không đánh bại baseline persistence về MAE.
  Xem reports/experiments.md để biết phân tích chi tiết.

## Yêu cầu đầu vào khi triển khai (API)
Cần đủ lịch sử Appliances 145 giá trị gần nhất (để tính lag_144) và các cảm
biến hiện tại trong miền giá trị của tập huấn luyện. Không tự điền giá trị
thiếu — trả lỗi nếu đầu vào không hợp lệ.