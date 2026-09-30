"""API phục vụ dự báo Appliances(t+1). Chỉ load mô hình, không huấn luyện lại."""
import json
import sys
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from features import build_single_prediction_row  # noqa: E402

MODELS_DIR = ROOT / "models"

# Miền giá trị hợp lệ, ước lượng từ dữ liệu train (nên thay bằng số liệu thật của bạn)
VALID_RANGES = {
    "T1": (-10, 40), "RH_1": (0, 100), "T2": (-10, 40), "RH_2": (0, 100),
    "T3": (-10, 40), "RH_3": (0, 100), "T4": (-10, 40), "RH_4": (0, 100),
    "T5": (-10, 40), "RH_5": (0, 100), "T6": (-30, 40), "RH_6": (0, 100),
    "T7": (-10, 40), "RH_7": (0, 100), "T8": (-10, 40), "RH_8": (0, 100),
    "T9": (-10, 40), "RH_9": (0, 100), "T_out": (-30, 40), "Press_mm_hg": (700, 800),
    "RH_out": (0, 100), "Windspeed": (0, 20), "Visibility": (0, 70),
    "Tdewpoint": (-30, 30), "lights": (0, 100),
}

app = FastAPI(title="Appliances Energy Forecast API")
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory=str(ROOT / "app" / "static")), name="static")
app.mount("/figures", StaticFiles(directory=str(ROOT / "reports" / "figures")), name="figures")
from fastapi.responses import FileResponse

@app.get("/")
def serve_index():
    return FileResponse(ROOT / "app" / "static" / "index.html")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"],
)

# Load một lần lúc khởi động, KHÔNG train lại mỗi request
try:
    model = joblib.load(MODELS_DIR / "serving_model.joblib")
    with open(MODELS_DIR / "model_config.json", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    model, config = None, None


class SensorReading(BaseModel):
    T1: float; RH_1: float; T2: float; RH_2: float
    T3: float; RH_3: float; T4: float; RH_4: float
    T5: float; RH_5: float; T6: float; RH_6: float
    T7: float; RH_7: float; T8: float; RH_8: float
    T9: float; RH_9: float
    T_out: float; Press_mm_hg: float; RH_out: float
    Windspeed: float; Visibility: float; Tdewpoint: float
    lights: float


class PredictRequest(BaseModel):
    appliances_history: list[float] = Field(
        ..., min_length=145, max_length=145,
        description="145 giá trị Appliances liên tiếp, từ t-144 đến t (Wh)",
    )
    current_sensors: SensorReading
    timestamp: str = Field(..., description="ISO 8601, ví dụ 2016-05-10T18:30:00")


class PredictResponse(BaseModel):
    prediction_wh: float
    unit: str = "Wh"
    model_version: str


@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/api/next-energy", response_model=PredictResponse)
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(500, "Mô hình chưa được huấn luyện/lưu. Chạy src/train_final.py trước.")

    if any(v < 0 for v in req.appliances_history):
        raise HTTPException(422, "appliances_history không được chứa giá trị âm")

    try:
        dt = datetime.fromisoformat(req.timestamp)
    except ValueError:
        raise HTTPException(422, "timestamp không đúng định dạng ISO 8601")

    sensors = req.current_sensors.model_dump()
    for name, value in sensors.items():
        if name in VALID_RANGES:
            lo, hi = VALID_RANGES[name]
            if not (lo <= value <= hi):
                raise HTTPException(
                    422, f"{name}={value} nằm ngoài miền hợp lệ [{lo}, {hi}]"
                )

    row = build_single_prediction_row(req.appliances_history, sensors, dt)
    X = pd.DataFrame([row])[config["feature_cols"]]
    pred = float(model.predict(X)[0])

    return PredictResponse(prediction_wh=round(pred, 2), model_version="rf_v1")