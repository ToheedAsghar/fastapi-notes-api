def register_and_login(client, email: str) -> dict:
    """Registers a user and return an auth header dict for them"""

    client.post("/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": "supersecret"
    })
    response = client.post("/auth/login", data = {
        "username": email,
        "password": "supersecret"
    })

    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

def test_create_and_get_own_note(client):
    headers = register_and_login(client, "alice@example.com")

    create_resp = client.post("/notes", json={
        "title": "My Note",
        "content": "Hello"
    }, headers=headers)

    assert create_resp.status_code == 201

    notes_id = create_resp.json()["id"]

    # fetching it back
    get_resp = client.get(f"/notes/{notes_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "My Note"

def test_cannot_read_another_users_note(client):
    alice = register_and_login(client, "alice@example.com")

    create_resp = client.post("/notes", json={
        "title": "My Note",
        "content": "Secret"
    }, headers=alice)

    alice_note_id = create_resp.json()["id"]

    bob_headers = register_and_login(client, "bob@example.com")

    # Bob trying to access the Alice
    response = client.get(f"/notes/{alice_note_id}", headers=bob_headers)

    assert response.status_code == 404

def test_list_only_returns_own_notes(client):
    # Alice creates two notes
    alice = register_and_login(client, "alice@example.com")
    client.post("/notes", json={"title": "A1", "content": "x"}, headers=alice)
    client.post("/notes", json={"title": "A2", "content": "y"}, headers=alice)

    # Bob creates on note
    bob = register_and_login(client, "bob@example.com")
    client.post("/notes", json={"title": "B1", "content": "z"}, headers=bob)

    # Bob lists notes, should see only his notes
    response = client.get("/notes", headers=bob)
    assert response.status_code == 200

    notes = response.json()

    assert len(notes) == 1
    assert notes[0]["title"] == "B1"

def test_unauthenticated_request_rejected(client):
    response = client.get("/notes")

    assert response.status_code == 401
