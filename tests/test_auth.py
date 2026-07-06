def test_register(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123",
        },
    )

    assert response.status_code in [200, 201]


def test_login(client):
    response = client.post(
        "/users/login", json={"email": "test@example.com", "password": "test123"}
    )

    assert response.status_code == 200
    assert "Login successful" in response.json()["message"]


def test_verify_without_cookie(client):
    response = client.get("/users/verify")

    assert response.status_code == 401
