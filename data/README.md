# Dữ liệu: Appliances Energy Prediction

## Nguồn
- Trang dữ liệu: https://archive.ics.uci.edu/dataset/374/appliances%2Benergy%2Bprediction
- DOI: https://doi.org/10.24432/C5VC8G
- Tệp sử dụng: `energydata_complete.csv`

## Thông tin tải
- Ngày tải: 28/09/2026
- SHA-256: `2820bf712ad0275cb18b85a05250926100d8e65ebb9f4d2d016ca91ea152a25d`
- Quy mô: 19.735 bản ghi, mỗi 10 phút, khoảng 4,5 tháng (11/01/2016 – 27/05/2016), 29 cột

## Giấy phép
CC BY 4.0. Được dùng và chia sẻ, với điều kiện ghi nguồn.

## Trích dẫn
Candanedo, L. (2017). Appliances Energy Prediction [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5VC8G

Bài báo gốc:
Candanedo, L. M., Feldheim, V., & Deramaix, D. (2017). Data driven prediction models of energy use of appliances in a low-energy house. *Energy and Buildings*, 140, 81–97.

## Cách tái tạo
1. Tạo môi trường và cài thư viện: `pip install -r requirements.txt`
2. Chạy `python src/data.py` từ thư mục gốc repo.
3. So sánh SHA-256 in ra với giá trị ở trên. Nếu khác thì file đã bị thay đổi.

## Lưu ý
- Dữ liệu từ **một ngôi nhà ở Bỉ** (thị trấn gần Chievres). Không khái quát cho mọi hộ gia đình.
- Không đưa file CSV vào Git (đã thêm `data/raw/` vào `.gitignore`).
- Xem `data/raw/data_dictionary.md` để biết chi tiết từng biến.
