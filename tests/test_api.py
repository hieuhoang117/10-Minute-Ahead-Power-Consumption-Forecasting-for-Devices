import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import app

client = TestClient(app)

VALID_SENSORS = {
    "T1": 20, "RH_1": 40, "T2": 20, "RH_2": 40,
    "T3": 20, "RH_3": 40, "T4": 20, "RH_4": 40,
    "T5": 20, "RH_5": 40, "T6": 15, "RH_6": 50,
    "T7": 20, "RH_7": 40, "T8": 20, "RH_8": 40,
    "T9": 20, "RH_9": 40,
    "T_out": 15, "Press_mm_hg": 750, "RH_out": 60,
    "Windspeed": 3, "Visibility": 40, "Tdewpoint": 8,
    "lights": 0,
}


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_predict_valid_request():
    payload = {
        "appliances_history": [60.0] * 145,
        "current_sensors": VALID_SENSORS,
        "timestamp": "2016-05-10T18:30:00",
    }
    resp = client.post("/api/next-energy", json=payload)
    assert resp.status_code == 200
    assert "prediction_wh" in resp.json()


def test_predict_missing_history_rejected():
    payload = {
        "appliances_history": [60.0] * 100,  # thiếu, cần đúng 145
        "current_sensors": VALID_SENSORS,
        "timestamp": "2016-05-10T18:30:00",
    }
    resp = client.post("/api/next-energy", json=payload)
    assert resp.status_code == 422


def test_predict_out_of_range_sensor_rejected():
    bad_sensors = dict(VALID_SENSORS)
    bad_sensors["RH_1"] = 500  # ngoài miền 0-100
    payload = {
        "appliances_history": [60.0] * 145,
        "current_sensors": bad_sensors,
        "timestamp": "2016-05-10T18:30:00",
    }
    resp = client.post("/api/next-energy", json=payload)
    assert resp.status_code == 422


def test_predict_negative_history_rejected():
    payload = {
        "appliances_history": [-5.0] * 145,
        "current_sensors": VALID_SENSORS,
        "timestamp": "2016-05-10T18:30:00",
    }
    resp = client.post("/api/next-energy", json=payload)
    assert resp.status_code == 422