from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "JWT Authentication API"}