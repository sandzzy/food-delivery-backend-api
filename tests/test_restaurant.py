import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_owner_token():
    client.post("/api/v1/auth/register", json={
        "name": "Owner", "email": "owner@example.com",
        "password": "pass123", "role": "restaurant_owner"
    })
    res = client.post("/api/v1/auth/login", json={"email": "owner@example.com", "password": "pass123"})
    return res.json().get("access_token")


def test_list_restaurants():
    response = client.get("/api/v1/restaurants/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_restaurant():
    token = get_owner_token()
    response = client.post(
        "/api/v1/restaurants/",
        json={"name": "Test Restaurant", "description": "Great food", "phone": "1234567890"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Restaurant"


def test_get_restaurant():
    token = get_owner_token()
    create = client.post(
        "/api/v1/restaurants/",
        json={"name": "Pizza Place"},
        headers={"Authorization": f"Bearer {token}"},
    )
    rid = create.json()["id"]
    response = client.get(f"/api/v1/restaurants/{rid}")
    assert response.status_code == 200
