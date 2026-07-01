import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models import User
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.schemas import UserCreate, UserLogin

# Create a test client using the FastAPI app
client = TestClient(app)

# Dependency override to use the test database
@pytest.fixture(scope="module")
def test_db():
    # Create the database tables
    User.metadata.create_all(bind=engine)
    yield SessionLocal()
    User.metadata.drop_all(bind=engine)

def test_register(test_db):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_login(test_db):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_read_users_me(test_db):
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    access_token = login_response.json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
