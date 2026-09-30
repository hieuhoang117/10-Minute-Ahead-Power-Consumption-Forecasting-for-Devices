"""Phân tích lỗi trên tập test: biểu đồ dự báo vs thực tế, sai số theo giờ, ở đỉnh."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "reports" / "figures"


def run():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ROOT / "reports" / "test_predictions.csv", parse_dates=["date"])

    # 1. Dự báo vs thực tế theo thời gian (7 ngày đầu của test, cho dễ nhìn)
    sample = df.iloc[:7 * 144]  # 144 điểm/ngày x 7 ngày
    plt.figure(figsize=(14, 4))
    plt.plot(sample["date"], sample["target"], label="Thực tế", alpha=0.8)
    plt.plot(sample["date"], sample["pred"], label="RandomForest", alpha=0.8)
    plt.plot(sample["date"], sample["persistence_pred"], label="Persistence", alpha=0.6, linestyle="--")
    plt.title("Dự báo vs thực tế — 7 ngày đầu tập test")
    plt.xlabel("Thời gian")
    plt.ylabel("Wh")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "error_forecast_vs_actual.png", dpi=150)
    plt.close()

    # 2. Phần dư (residual) theo thời gian
    df["residual"] = df["target"] - df["pred"]
    plt.figure(figsize=(14, 4))
    plt.scatter(df["date"], df["residual"], s=3, alpha=0.4)
    plt.axhline(0, color="red", linewidth=1)
    plt.title("Phần dư (thực tế - dự báo) theo thời gian — RandomForest, tập test")
    plt.xlabel("Thời gian")
    plt.ylabel("Sai số (Wh)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "error_residuals_over_time.png", dpi=150)
    plt.close()

    # 3. MAE theo giờ
    df["abs_error"] = (df["target"] - df["pred"]).abs()
    mae_by_hour = df.groupby("hour")["abs_error"].mean()
    plt.figure(figsize=(8, 4))
    mae_by_hour.plot(kind="bar")
    plt.title("MAE theo giờ — RandomForest, tập test")
    plt.xlabel("Giờ")
    plt.ylabel("MAE (Wh)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "error_mae_by_hour.png", dpi=150)
    plt.close()
    print("MAE theo giờ:")
    print(mae_by_hour.sort_values(ascending=False))

    # 4. Sai số tại các đỉnh (target cao) so với phần còn lại
    threshold = df["target"].quantile(0.9)
    peak = df[df["target"] >= threshold]
    normal = df[df["target"] < threshold]
    print(f"\nNgưỡng đỉnh (top 10%): {threshold:.1f} Wh")
    print(f"MAE tại đỉnh: {peak['abs_error'].mean():.3f}")
    print(f"MAE bình thường: {normal['abs_error'].mean():.3f}")


if __name__ == "__main__":
    run()