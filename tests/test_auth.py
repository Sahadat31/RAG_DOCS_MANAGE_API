from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    payload = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "password": "secure123"
    }
    res = client.post("/user/register", json=payload)
    assert res.status_code in [200, 400]
    if res.status_code == 200:
        assert "user_id" in res.json()

def test_login_user():
    payload = {
        "email": "john@example.com",
        "password": "secure123"
    }
    res = client.post("/user/login", json=payload)
    assert res.status_code == 200
    assert "access_token" in res.json()
