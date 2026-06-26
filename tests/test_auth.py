import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

REGISTER_PAYLOAD = {
    "name": "Test User",
    "email": "testuser@example.com",
    "phone": "9876543210",
    "password": "secret123",
    "role": "customer",
}


def test_register():
    response = client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    assert response.status_code in (201, 400)  # 400 if already registered


def test_login():
    client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": REGISTER_PAYLOAD["email"], "password": REGISTER_PAYLOAD["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": REGISTER_PAYLOAD["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_me():
    client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    login = client.post(
        "/api/v1/auth/login",
        json={"email": REGISTER_PAYLOAD["email"], "password": REGISTER_PAYLOAD["password"]},
    )
    token = login.json()["access_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == REGISTER_PAYLOAD["email"]
