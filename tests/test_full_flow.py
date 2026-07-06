def test_full_flow(client):
    # register
    client.post(
        "/users/register",
        json={"username": "flowuser", "email": "flow@test.com", "password": "1234"},
    )

    # login
    login = client.post(
        "/users/login", json={"email": "flow@test.com", "password": "1234"}
    )

    cookies = login.cookies

    # verify
    verify = client.get("/users/verify", cookies=cookies)
    assert verify.status_code == 200

    # create task
    task = client.post(
        "/tasks/",
        json={"title": "Flow Task", "description": "Testing flow", "status": "Pending"},
        cookies=cookies,
    )

    assert task.status_code in [200, 201]
