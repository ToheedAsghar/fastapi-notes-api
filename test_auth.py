def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "supersecret"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "alice@example.com"
    assert "password" not in data
    assert "password_hash" not in data

def test_register_duplicate_email_fails(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "supersecret"
    }

    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409

def test_login_wrong_password_fails(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "supersecret"
    }

    client.post("/auth/register", json=payload)

    response = client.post("/auth/login", data={
        "username": "alice@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401