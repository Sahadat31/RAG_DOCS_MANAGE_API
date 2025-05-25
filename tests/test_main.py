from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_status():
    response = client.get("/")
    assert response.status_code in [404, 200]  # if no root route, it should be 404

def test_routes_loaded():
    routes = [route.path for route in app.routes]
    assert "documents/upload" in routes or "/user/register" in routes
