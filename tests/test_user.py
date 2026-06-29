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


def test_create_user():
    response = client.post("/users/", json={"email": "newuser@example.com", "password": "newpassword"})
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"
    assert "hashed_password" not in response.json()
