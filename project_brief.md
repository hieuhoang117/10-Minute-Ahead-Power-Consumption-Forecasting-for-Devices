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
Xem `data/README.md` — 19,735 bản ghi, 4.5 tháng, CC BY 4.0

## Kế hoạch 6 tuần

| Tuần | Công việc chính | Minh chứng đầu ra |
|---|---|---|
| 1 | Chốt câu hỏi, thời điểm dự đoán, nguồn/giấy phép; tạo repo | Project brief; data README; schema; baseline plan |
| 2 | Tải/làm sạch; EDA trên train; hoàn thiện split và baseline | Script dữ liệu (`src/data.py`); EDA (`src/eda.py`); baseline chạy được |
| 3 | Pipeline mô hình chính; validation/CV; theo dõi thí nghiệm | Bảng thí nghiệm vòng 1; Ridge + RF; kiểm thử preprocessing |
| 4 | Hoàn tất 4 thí nghiệm bắt buộc; test cuối; phân tích lỗi | Bảng kết quả đóng băng; figures; model card nháp |
| 5 | Đóng gói API và giao diện; tích hợp model; test đầu vào | Web demo end-to-end; API docs; test; model phục vụ |
| 6 | Hoàn thiện báo cáo/slide; tái lập trên môi trường sạch | Release cuối; báo cáo; slide |

## Thông tin nhóm

Nhóm **01 thành viên** (đã được giảng viên chấp thuận).

| Thành viên | MSSV | Email | Vai trò |
|---|---|---|---|
| Hoàng Minh Hiếu | 12523029 | hieuhoangminh2403@gmail.com | Toàn bộ pipeline: dữ liệu, mô hình, thí nghiệm, web, báo cáo |

## Tự đánh giá

| Tiêu chí | Tự chấm | Ghi chú |
|---|---|---|
| 1. Bài toán & phạm vi | 7/8 | Câu hỏi rõ, có đo được; tiêu chí thành công rõ |
| 2. Dữ liệu & EDA | 10/12 | Data dictionary đầy đủ; EDA dẫn tới quyết định giờ cao điểm |
| 3. Split, leakage & tái lập | 14/15 | Time split đúng; lag chỉ quá khứ; test 1 lần; random_state=42 |
| 4. Mô hình & thí nghiệm | 16/18 | Đủ 4 TN bắt buộc; nhận xét trung thực TN2 (random split không lạc quan như kỳ vọng) |
| 5. Đánh giá & phân tích lỗi | 15/18 | MAE/RMSE, giờ cao điểm, theo tháng, đỉnh vs bình thường; thừa nhận ML không beat persistence |
| 6. Web/API | 10/12 | 3 màn hình; API validation; model card trên web; tách train/serving |
| 7. Mã nguồn & bàn giao | 5/7 | Cấu trúc rõ; test cơ bản; README đầy đủ |
| 8. Báo cáo & trình bày | */10 | *(sẽ cập nhật sau khi hoàn thành báo cáo và slide)* |
| **Tổng ước tính** | **~77/100** | Chưa tính mục 8 |