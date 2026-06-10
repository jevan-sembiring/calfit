from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_assessment_valid_data():
    payload = {
        "weight_kg": 90.0,
        "height_cm": 165.0,
        "age": 30,
        "gender": "Laki-laki"
    }
    response = client.post("/api/v1/assessment", json=payload)
    assert response.status_code == 200
    assert "status" in response.json()

def test_assessment_invalid_data():
    payload = {"weight_kg": -10} # Data salah (berat minus)
    response = client.post("/api/v1/assessment", json=payload)
    assert response.status_code == 422