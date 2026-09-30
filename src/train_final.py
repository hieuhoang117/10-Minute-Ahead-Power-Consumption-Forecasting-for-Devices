"""Huấn luyện mô hình cuối để phục vụ qua API (train + validation, không đụng test)."""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time, FEATURE_COLS

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"

if __name__ == "__main__":
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])
    df = build_features(df)
    train, val, test = split_by_time(df)

    # Gộp train+val để tận dụng tối đa dữ liệu cho mô hình phục vụ thực tế
    train_val = pd.concat([train, val]).sort_values("date").reset_index(drop=True)

    model = RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=20,
        random_state=42, n_jobs=-1,
    )
    model.fit(train_val[FEATURE_COLS], train_val["target"])

    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODELS_DIR / "serving_model.joblib")

    config = {
        "feature_cols": FEATURE_COLS,
        "n_lag": 144,              # cần 145 giá trị lịch sử: t-144 đến t
        "random_state": 42,
        "model_type": "RandomForestRegressor",
        "test_mae": 30.920,        # điền đúng số bạn có từ tuần 4
        "test_rmse": 62.271,
        "trained_on": "train+validation (2016-01-12 to 2016-05-07)",
    }
    with open(MODELS_DIR / "model_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print("Đã lưu models/serving_model.joblib và models/model_config.json")