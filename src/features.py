"""Tạo đặc trưng lag/lịch và chia tập theo thời gian."""

FEATURE_COLS = [
    "T1", "RH_1", "T2", "RH_2", "T3", "RH_3", "T4", "RH_4",
    "T5", "RH_5", "T6", "RH_6", "T7", "RH_7", "T8", "RH_8",
    "T9", "RH_9", "T_out", "Press_mm_hg", "RH_out",
    "Windspeed", "Visibility", "Tdewpoint", "lights",
    "Appliances", "lag_1", "lag_6", "lag_144", "hour", "dayofweek",
]


def build_features(df):
    """Sắp xếp theo thời gian, tạo lag, đặc trưng lịch và target t+1."""
    df = df.sort_values("date").reset_index(drop=True).copy()
    for k in (1, 6, 144):
        df[f"lag_{k}"] = df["Appliances"].shift(k)      # chỉ nhìn về quá khứ
    df["hour"] = df["date"].dt.hour
    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month                   # chỉ để phân tích, KHÔNG đưa vào feature
    df["target"] = df["Appliances"].shift(-1)            # tương lai, chỉ làm nhãn
    return df.dropna().reset_index(drop=True)             # mất 144 dòng đầu + 1 dòng cuối


def split_by_time(df, train_frac=0.70, val_frac=0.15):
    """Chia theo thứ tự thời gian: train -> validation -> test."""
    n = len(df)
    i_val = int(n * train_frac)
    i_test = int(n * (train_frac + val_frac))
    return df.iloc[:i_val], df.iloc[i_val:i_test], df.iloc[i_test:]

def build_single_prediction_row(appliances_history, current_sensors, current_datetime):
    """
    Tạo 1 dòng đặc trưng để dự đoán, dùng CHUNG logic với lúc huấn luyện.
    appliances_history: list 145 giá trị Appliances, từ t-144 đến t (thứ tự tăng dần thời gian)
    current_sensors: dict các cảm biến tại t (T1, RH_1, ..., lights)
    current_datetime: datetime tại t
    """
    row = dict(current_sensors)
    row["Appliances"] = appliances_history[-1]        # giá trị tại t
    row["lag_1"] = appliances_history[-2]              # t-1
    row["lag_6"] = appliances_history[-7]               # t-6
    row["lag_144"] = appliances_history[0]               # t-144
    row["hour"] = current_datetime.hour
    row["dayofweek"] = current_datetime.weekday()
    return row