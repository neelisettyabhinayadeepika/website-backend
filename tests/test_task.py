def test_get_tasks_unauthorized(client):
    response = client.get("/tasks/")
    assert response.status_code == 401


def test_create_task_without_auth(client):
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Testing", "status": "Pending"},
    )

    assert response.status_code == 401


def test_get_tasks_authorized(client):
    # simulate login first
    login = client.post(
        "/users/login", json={"email": "test@example.com", "password": "test123"}
    )

    cookies = login.cookies

    response = client.get("/tasks/", cookies=cookies)

    assert response.status_code == 200
