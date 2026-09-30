"""Huấn luyện mô hình chính, chọn tham số bằng validation theo thời gian."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time, FEATURE_COLS

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def train_ridge(X_train, y_train):
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(random_state=42)),
    ])
    param_grid = {"model__alpha": [0.1, 1.0, 10.0, 100.0, 300.0, 1000.0]}
    search = GridSearchCV(
        pipe, param_grid,
        cv=TimeSeriesSplit(n_splits=5),
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    print("Ridge — alpha tốt nhất:", search.best_params_)
    print("Ridge — MAE trung bình (CV):", -search.best_score_)
    return search.best_estimator_


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=20,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def evaluate(model, X, y, label):
    pred = model.predict(X)
    mae = mean_absolute_error(y, pred)
    rmse = mean_squared_error(y, pred) ** 0.5
    print(f"[{label}] MAE={mae:.3f}  RMSE={rmse:.3f}")
    return {"label": label, "mae": mae, "rmse": rmse}


if __name__ == "__main__":
    csv_path = RAW_DIR / CSV_NAME
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = build_features(df)
    train, val, test = split_by_time(df)

    X_train, y_train = train[FEATURE_COLS], train["target"]
    X_val, y_val = val[FEATURE_COLS], val["target"]

    print("=== Ridge ===")
    ridge_model = train_ridge(X_train, y_train)
    evaluate(ridge_model, X_train, y_train, "Ridge - train")
    evaluate(ridge_model, X_val, y_val, "Ridge - validation")

    print("\n=== RandomForest ===")
    rf_model = train_random_forest(X_train, y_train)
    evaluate(rf_model, X_train, y_train, "RandomForest - train")
    evaluate(rf_model, X_val, y_val, "RandomForest - validation")

    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(ridge_model, MODELS_DIR / "ridge_pipeline.joblib")
    joblib.dump(rf_model, MODELS_DIR / "rf_pipeline.joblib")
    print("\nĐã lưu models/ridge_pipeline.joblib và models/rf_pipeline.joblib")