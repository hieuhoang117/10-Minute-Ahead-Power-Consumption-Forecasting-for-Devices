"""Thí nghiệm 2: so sánh random split và time split để lộ ra lạc quan giả."""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time, FEATURE_COLS


def fit_eval(X_train, y_train, X_val, y_val, label):
    model = RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=20,
        random_state=42, n_jobs=-1,
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_val)
    mae = mean_absolute_error(y_val, pred)
    rmse = mean_squared_error(y_val, pred) ** 0.5
    print(f"[{label}] MAE={mae:.3f}  RMSE={rmse:.3f}")
    return mae, rmse


if __name__ == "__main__":
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])
    df = build_features(df)

    frac_val = 0.15
    n = len(df)
    i_split = int(n * (1 - frac_val))

    # Time split: 85% đầu để train, 15% cuối để validation (giữ đúng thứ tự thời gian)
    train_t, val_t = df.iloc[:i_split], df.iloc[i_split:]
    fit_eval(train_t[FEATURE_COLS], train_t["target"],
             val_t[FEATURE_COLS], val_t["target"], "Time split (85/15)")

    # Random split: CÙNG tỷ lệ 85/15, nhưng xáo trộn ngẫu nhiên toàn bộ dữ liệu
    train_r, val_r = train_test_split(df, test_size=frac_val, random_state=42, shuffle=True)
    fit_eval(train_r[FEATURE_COLS], train_r["target"],
             val_r[FEATURE_COLS], val_r["target"], "Random split (85/15)")