import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from features import build_features


def make_dummy_df(n=300):
    dates = pd.date_range("2016-01-01", periods=n, freq="10min")
    sensor_cols = [
        "T1", "RH_1", "T2", "RH_2", "T3", "RH_3", "T4", "RH_4",
        "T5", "RH_5", "T6", "RH_6", "T7", "RH_7", "T8", "RH_8",
        "T9", "RH_9", "T_out", "Press_mm_hg", "RH_out",
        "Windspeed", "Visibility", "Tdewpoint", "rv1", "rv2",
    ]
    return pd.DataFrame({
        "date": dates,
        "Appliances": range(n),
        "lights": [0] * n,
        **{col: [1.0] * n for col in sensor_cols},
    })


def test_lag_1_matches_previous_row():
    df = build_features(make_dummy_df())
    row = df.iloc[10]
    assert row["lag_1"] == row["Appliances"] - 1


def test_target_is_next_step():
    df = build_features(make_dummy_df())
    row = df.iloc[10]
    assert row["target"] == row["Appliances"] + 1


def test_no_missing_after_build():
    df = build_features(make_dummy_df())
    assert df.isna().sum().sum() == 0


def test_dropped_rows_count():
    n = 300
    df = build_features(make_dummy_df(n))
    assert len(df) == n - 144 - 1