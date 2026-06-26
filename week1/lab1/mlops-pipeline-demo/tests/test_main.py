from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_doubles_value():
    response = client.post("/predict", json={"value": 21})
    assert response.status_code == 200
    assert response.json() == {"result": 42}


def test_predict_handles_negative_values():
    response = client.post("/predict", json={"value": -5})
    assert response.status_code == 200
    assert response.json()["result"] == -10


def test_predict_rejects_bad_input():
    response = client.post("/predict", json={"value": "not-a-number"})
    assert response.status_code == 422
