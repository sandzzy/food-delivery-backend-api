from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def setup_owner_and_restaurant():
    client.post("/api/v1/auth/register", json={
        "name": "MenuOwner", "email": "menuowner@example.com",
        "password": "pass123", "role": "restaurant_owner"
    })
    token_res = client.post("/api/v1/auth/login", json={"email": "menuowner@example.com", "password": "pass123"})
    token = token_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    rest = client.post("/api/v1/restaurants/", json={"name": "Burger Joint"}, headers=headers)
    return token, rest.json()["id"], headers


def test_create_menu_item():
    token, rid, headers = setup_owner_and_restaurant()
    response = client.post(
        "/api/v1/menu/",
        json={"restaurant_id": rid, "name": "Cheeseburger", "price": 9.99},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Cheeseburger"


def test_list_menu():
    token, rid, headers = setup_owner_and_restaurant()
    client.post("/api/v1/menu/", json={"restaurant_id": rid, "name": "Fries", "price": 3.49}, headers=headers)
    response = client.get(f"/api/v1/menu/?restaurant_id={rid}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
