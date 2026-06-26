from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_payment_requires_auth():
    response = client.post("/api/v1/payments/", json={"order_id": 1, "payment_method": "cash"})
    assert response.status_code == 401


def test_payment_invalid_order():
    client.post("/api/v1/auth/register", json={
        "name": "Pay User", "email": "payuser@example.com",
        "password": "pass123", "role": "customer"
    })
    token_res = client.post("/api/v1/auth/login", json={"email": "payuser@example.com", "password": "pass123"})
    token = token_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/v1/payments/",
        json={"order_id": 99999, "payment_method": "cash"},
        headers=headers,
    )
    assert response.status_code == 404
