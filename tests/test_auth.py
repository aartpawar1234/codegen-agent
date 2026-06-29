import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import SessionLocal
from src import crud, schemas

@pytest.fixture()
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[crud.get_db] = override_get_db

client = TestClient(app)


def test_login():
    response = client.post("/login", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_logout():
    # Assuming you have a valid token to test logout
    token = "valid_token"
    response = client.post("/logout", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"msg": "Successfully logged out"}


def test_refresh():
    # Assuming you have a valid refresh token
    refresh_token = "valid_refresh_token"
    response = client.post("/refresh", json={"token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
