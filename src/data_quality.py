"""Báo cáo chất lượng dữ liệu thô, chạy trên toàn bộ file (trước khi chia tập)."""
import pandas as pd
from data import RAW_DIR, CSV_NAME


def run():
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])

    print("=== Khoảng cách thời gian ===")
    print(df["date"].diff().value_counts().head())

    print("\n=== Thống kê Appliances ===")
    print(df["Appliances"].describe())

    print("\n=== Cột có giá trị hằng (nunique == 1) ===")
    const_cols = df.columns[df.nunique() == 1].tolist()
    print(const_cols if const_cols else "Không có")

    print("\n=== Ngoại lệ Appliances (IQR) ===")
    q1, q3 = df["Appliances"].quantile([0.25, 0.75])
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    n_outliers = (df["Appliances"] > upper).sum()
    print(f"Ngưỡng trên: {upper:.1f} Wh, số dòng vượt ngưỡng: {n_outliers} "
          f"({n_outliers/len(df)*100:.1f}%)")

    print("\n=== Missing / trùng lặp (đã biết từ tuần 1) ===")
    print("Ô thiếu:", int(df.isna().sum().sum()))
    print("Trùng mốc thời gian:", df["date"].duplicated().sum())


if __name__ == "__main__":
    run()