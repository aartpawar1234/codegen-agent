import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.session import SessionLocal
from src.schemas.auth import UserCreate, UserLogin

client = TestClient(app)

@pytest.fixture
def create_user():
    user_data = UserCreate(username="testuser", email="test@example.com", password="testpassword")
    response = client.post("/auth/register", json=user_data.dict())
    return response


def test_register(create_user):
    assert create_user.status_code == 200


def test_login(create_user):
    login_data = UserLogin(email="test@example.com", password="testpassword")
    response = client.post("/auth/login", json=login_data.dict())
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_user():
    login_data = UserLogin(email="invalid@example.com", password="wrongpassword")
    response = client.post("/auth/login", json=login_data.dict())
    assert response.status_code == 401


def test_read_users_me(create_user):
    login_data = UserLogin(email="test@example.com", password="testpassword")
    login_response = client.post("/auth/login", json=login_data.dict())
    token = login_response.json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

