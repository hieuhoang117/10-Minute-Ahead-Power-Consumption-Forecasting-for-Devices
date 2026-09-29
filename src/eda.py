"""EDA trên tập train, các biểu đồ phục vụ quyết định tiền xử lý."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "reports" / "figures"


def run():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])
    df = build_features(df)
    train, val, test = split_by_time(df)

    print(f"Train: {len(train)} dòng ({train['date'].min()} -> {train['date'].max()})")
    print(f"Val:   {len(val)} dòng ({val['date'].min()} -> {val['date'].max()})")
    print(f"Test:  {len(test)} dòng ({test['date'].min()} -> {test['date'].max()})")

    # 1. Target theo thời gian
    plt.figure(figsize=(12, 4))
    plt.plot(train["date"], train["target"])
    plt.title("Appliances (Wh) theo thời gian — tập train")
    plt.xlabel("Thời gian")
    plt.ylabel("Wh")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "eda_target_over_time.png", dpi=150)
    plt.close()

    # 2. Phân bố target
    plt.figure(figsize=(6, 4))
    plt.hist(train["target"], bins=50)
    plt.title("Phân bố Appliances — tập train")
    plt.xlabel("Wh")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "eda_target_distribution.png", dpi=150)
    plt.close()

    # 3. Trung bình theo giờ trong ngày -> quyết định "giờ cao điểm"
    by_hour = train.groupby("hour")["target"].mean()
    plt.figure(figsize=(8, 4))
    by_hour.plot(kind="bar")
    plt.title("Appliances trung bình theo giờ — tập train")
    plt.xlabel("Giờ")
    plt.ylabel("Wh trung bình")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "eda_mean_by_hour.png", dpi=150)
    plt.close()
    print("\nGiờ cao điểm (top 3):")
    print(by_hour.sort_values(ascending=False).head(3))

    # 4. Tương quan lag với target
    print("\nTương quan với target:")
    print(train[["lag_1", "lag_6", "lag_144", "Appliances", "target"]].corr()["target"])


if __name__ == "__main__":
    run()