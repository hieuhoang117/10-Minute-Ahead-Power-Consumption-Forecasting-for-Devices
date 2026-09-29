"""Baseline persistence: dự đoán Appliances(t+1) = Appliances(t)."""
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time


def evaluate_persistence(df, label):
    pred = df["Appliances"]          # dự đoán t+1 bằng giá trị tại t
    y_true = df["target"]
    mae = mean_absolute_error(y_true, pred)
    rmse = mean_squared_error(y_true, pred) ** 0.5
    print(f"[{label}] Persistence — MAE={mae:.3f}  RMSE={rmse:.3f}")
    return mae, rmse

def evaluate_peak_hours(df, label, peak_hours=(17, 18, 19)):
    peak = df[df["hour"].isin(peak_hours)]
    pred = peak["Appliances"]
    y_true = peak["target"]
    mae = mean_absolute_error(y_true, pred)
    print(f"[{label}] Persistence — MAE giờ cao điểm (17-19h)={mae:.3f}")
    return mae

if __name__ == "__main__":
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])
    df = build_features(df)
    train, val, test = split_by_time(df)

    evaluate_persistence(train, "train")
    evaluate_persistence(val, "validation")
    evaluate_peak_hours(val, "validation")