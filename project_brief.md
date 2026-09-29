# Project Brief — Dự báo điện năng thiết bị 10 phút kế tiếp

## Câu hỏi nghiên cứu
Pipeline theo thời gian có dự báo tốt hơn baseline persistence mà không dùng thông tin tương lai không?

## Định nghĩa bài toán
- Thời điểm dự đoán: t (đã biết mọi thứ đến t)
- Đầu ra: Appliances (Wh) tại t+1
- Đầu vào: cảm biến, thời tiết tại t; lag 1/6/144 của Appliances; đặc trưng lịch
- Loại bỏ: rv1, rv2 khỏi mô hình chính

## Chỉ số đánh giá
MAE, RMSE (chính); MAE giờ cao điểm, MAE theo tháng (phụ)

## Baseline
Persistence: dự đoán t+1 bằng Appliances tại t

## Tiêu chí thành công
Chạy được trên máy khác; đánh bại hoặc giải thích rõ khi không đánh bại persistence; chứng minh không rò rỉ dữ liệu

## Dữ liệu
Xem data/README.md — 19,735 bản ghi, 4.5 tháng, CC BY 4.0

## Kế hoạch 6 tuần
[dán bảng kế hoạch từ đề bài]

## Phân công
[dán bảng phân công]