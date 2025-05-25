import pytest
import os

@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("MONGODB_URL", "mongodb+srv://USER:PASSWORD@localhost/test")
    monkeypatch.setenv("DB_USERNAME", "testuser")
    monkeypatch.setenv("DB_PASSWORD", "testpass")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-api-key")
