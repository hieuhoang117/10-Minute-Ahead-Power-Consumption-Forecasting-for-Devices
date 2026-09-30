## Nhận xét từ biểu đồ

### Dự báo vs thực tế (error_forecast_vs_actual.png)
RandomForest có xu hướng làm mượt các đỉnh nhọn, dự báo thấp hơn giá trị thực
tế tại hầu hết các đợt tăng đột biến. Persistence bám sát đỉnh tốt hơn (dù trễ
đúng 1 bước 10 phút), giải thích vì sao persistence có MAE tại đỉnh thấp hơn.

### Phần dư theo thời gian (error_residuals_over_time.png)
Phần dư dao động ổn định quanh 0 trong suốt tập test, không có xu hướng trôi
dạt theo thời gian — cho thấy mô hình không bị lệch hệ thống dù test rơi vào
giai đoạn (tháng 5) khác với phần lớn dữ liệu train. Các điểm ngoại lệ đều
lệch về phía dương (thực tế cao hơn dự báo), xác nhận mô hình có thiên hướng
đoán thấp tại các đỉnh tiêu thụ, chứ không đoán quá cao.