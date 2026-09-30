"""Thí nghiệm 3: ablation các mức lag."""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time

BASE_COLS = [
    "T1", "RH_1", "T2", "RH_2", "T3", "RH_3", "T4", "RH_4",
    "T5", "RH_5", "T6", "RH_6", "T7", "RH_7", "T8", "RH_8",
    "T9", "RH_9", "T_out", "Press_mm_hg", "RH_out",
    "Windspeed", "Visibility", "Tdewpoint", "lights",
    "Appliances", "hour", "dayofweek",
]

CONFIGS = {
    "no_lag": [],
    "lag_1": ["lag_1"],
    "lag_1_6": ["lag_1", "lag_6"],
    "lag_1_6_144": ["lag_1", "lag_6", "lag_144"],
}


def fit_eval(train, val, cols, label):
    model = RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=20,
        random_state=42, n_jobs=-1,
    )
    model.fit(train[cols], train["target"])
    pred = model.predict(val[cols])
    mae = mean_absolute_error(val["target"], pred)
    rmse = mean_squared_error(val["target"], pred) ** 0.5
    print(f"[{label}] cols={len(cols)}  MAE={mae:.3f}  RMSE={rmse:.3f}")
    return mae, rmse


if __name__ == "__main__":
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])
    df = build_features(df)
    train, val, _ = split_by_time(df)

    for name, lag_cols in CONFIGS.items():
        cols = BASE_COLS + lag_cols
        fit_eval(train, val, cols, name)