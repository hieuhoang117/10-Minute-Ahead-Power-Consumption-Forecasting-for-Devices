"""Chạy đánh giá cuối cùng trên tập test — CHỈ CHẠY MỘT LẦN."""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from data import RAW_DIR, CSV_NAME
from features import build_features, split_by_time, FEATURE_COLS


def mae_rmse(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    return mae, rmse


if __name__ == "__main__":
    df = pd.read_csv(RAW_DIR / CSV_NAME, parse_dates=["date"])
    df = build_features(df)
    train, val, test = split_by_time(df)

    # Huấn luyện lại trên train (giống cấu hình đã chọn ở tuần 3)
    model = RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=20,
        random_state=42, n_jobs=-1,
    )
    model.fit(train[FEATURE_COLS], train["target"])

    print("=== KẾT QUẢ TEST CUỐI CÙNG (chỉ chạy 1 lần) ===\n")

    # Persistence trên test
    pred_persist = test["Appliances"]
    mae_p, rmse_p = mae_rmse(test["target"], pred_persist)
    print(f"[Persistence - TEST] MAE={mae_p:.3f}  RMSE={rmse_p:.3f}")

    # RandomForest trên test
    pred_rf = model.predict(test[FEATURE_COLS])
    mae_rf, rmse_rf = mae_rmse(test["target"], pred_rf)
    print(f"[RandomForest - TEST] MAE={mae_rf:.3f}  RMSE={rmse_rf:.3f}")

    # MAE giờ cao điểm trên test
    peak = test[test["hour"].isin([17, 18, 19])]
    pred_peak_persist = peak["Appliances"]
    pred_peak_rf = model.predict(peak[FEATURE_COLS])
    mae_peak_p = mean_absolute_error(peak["target"], pred_peak_persist)
    mae_peak_rf = mean_absolute_error(peak["target"], pred_peak_rf)
    print(f"[Persistence - TEST giờ cao điểm] MAE={mae_peak_p:.3f}")
    print(f"[RandomForest - TEST giờ cao điểm] MAE={mae_peak_rf:.3f}")

    # MAE theo tháng trên test
    print("\n=== MAE theo tháng (RandomForest, TEST) ===")
    test = test.copy()
    test["pred"] = pred_rf
    monthly = test.groupby(test["date"].dt.month).apply(
        lambda g: mean_absolute_error(g["target"], g["pred"])
    )
    print(monthly)

    # Lưu dự đoán để vẽ biểu đồ phân tích lỗi
    out = test[["date", "target", "pred", "hour"]].copy()
    out["persistence_pred"] = pred_persist.values
    out.to_csv("reports/test_predictions.csv", index=False)
    print("\nĐã lưu reports/test_predictions.csv để phân tích lỗi")