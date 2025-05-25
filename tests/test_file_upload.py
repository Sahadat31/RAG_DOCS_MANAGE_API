import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def token():
    res = client.post("/user/login", json={"email": "john@example.com", "password": "secure123"})
    return res.json()["access_token"]

def test_upload_files(token):
    with open("sample.pdf", "rb") as f:
        res = client.post(
            "documents/upload",
            files={"files": f},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 200
        assert "chunks" in res.json()

def test_ask_question(token):
    res = client.post(
        "documents/ask",
        json={"question": "What is in the document?"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert "answer" in res.json()

def test_upload_protected_route_requires_auth():
    response = client.post("documents/upload")
    assert response.status_code == 401

def test_ask_question_requires_auth():
    response = client.post("documents/ask", json={"question": "What is this?"})
    assert response.status_code == 401
