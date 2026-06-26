from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_orders_require_auth():
    response = client.get("/api/v1/orders/")
    assert response.status_code == 401


def test_place_order_empty_cart():
    client.post("/api/v1/auth/register", json={
        "name": "Order User", "email": "orderuser@example.com",
        "password": "pass123", "role": "customer"
    })
    token_res = client.post("/api/v1/auth/login", json={"email": "orderuser@example.com", "password": "pass123"})
    token = token_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/v1/orders/",
        json={"restaurant_id": 1},
        headers=headers,
    )
    # Cart is empty so should return 400
    assert response.status_code == 400
