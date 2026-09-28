"""Tải và kiểm tra dữ liệu Appliances Energy Prediction (UCI, dataset 374)."""
import hashlib
import io
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip"
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CSV_NAME = "energydata_complete.csv"


def sha256_of_file(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk_size), b""):
            h.update(block)
    return h.hexdigest()


def download_data(force=False):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RAW_DIR / CSV_NAME
    if csv_path.exists() and not force:
        print(f"Đã có {csv_path}, bỏ qua bước tải.")
        return csv_path

    print("Đang tải dữ liệu từ UCI...")
    with urllib.request.urlopen(URL, timeout=60) as resp:
        content = resp.read()
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        member = next(n for n in z.namelist() if n.endswith(CSV_NAME))
        csv_path.write_bytes(z.read(member))
    print(f"Đã lưu {csv_path}")
    return csv_path


def check_schema(csv_path):
    df = pd.read_csv(csv_path, parse_dates=["date"])
    print(f"Số dòng: {len(df)} (kỳ vọng 19735)")
    print(f"Số cột: {df.shape[1]} (kỳ vọng 29)")
    print(f"Từ {df['date'].min()} đến {df['date'].max()}")
    print(f"Trùng mốc thời gian: {df['date'].duplicated().sum()}")
    print(f"Ô thiếu: {int(df.isna().sum().sum())}")
    return df


if __name__ == "__main__":
    path = download_data()
    print("SHA-256:", sha256_of_file(path))
    print("Ngày chạy:", date.today().isoformat())
    check_schema(path)