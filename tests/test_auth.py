import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.schemas import LoginRequest, LogoutRequest, RefreshRequest

client = TestClient(app)


def test_login_success():
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_failure():
    response = client.post("/auth/login", json={"email": "wrong@example.com", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"


def test_logout():
    response = client.post("/auth/logout", json={"refresh_token": "some_refresh_token"})
    assert response.status_code == 200
    assert response.json()["msg"] == "Successfully logged out"


def test_refresh():
    response = client.post("/auth/refresh", json={"refresh_token": "some_refresh_token"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_revoked_token():
    response = client.post("/auth/refresh", json={"refresh_token": "revoked_token"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Token has been revoked"