"""Thí nghiệm 4: kiểm tra rv1/rv2 có cải thiện ổn định không, qua nhiều seed."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time, FEATURE_COLS

SEEDS = [0, 1, 2, 3, 4]


def fit_eval(train, val, cols, seed):
    model = RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=20,
        random_state=seed, n_jobs=-1,
    )
    model.fit(train[cols], train["target"])
    pred = model.predict(val[cols])
    return mean_absolute_error(val["target"], pred)


if __name__ == "__main__":
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])
    df = build_features(df)
    train, val, _ = split_by_time(df)

    cols_without = FEATURE_COLS
    cols_with = FEATURE_COLS + ["rv1", "rv2"]

    mae_without = [fit_eval(train, val, cols_without, s) for s in SEEDS]
    mae_with = [fit_eval(train, val, cols_with, s) for s in SEEDS]

    print("Không rv1/rv2:", [f"{m:.3f}" for m in mae_without])
    print(f"  Trung bình={np.mean(mae_without):.3f}  Std={np.std(mae_without):.3f}")

    print("Có rv1/rv2:   ", [f"{m:.3f}" for m in mae_with])
    print(f"  Trung bình={np.mean(mae_with):.3f}  Std={np.std(mae_with):.3f}")

    diff = np.array(mae_with) - np.array(mae_without)
    print(f"\nChênh lệch (có - không), từng seed: {[f'{d:.3f}' for d in diff]}")
    print(f"Chênh lệch trung bình: {diff.mean():.4f} ± {diff.std():.4f}")