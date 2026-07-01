import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("title, expected_status", [
    ("Test Todo", 200),
    ("", 422),  # Empty title should fail
])
def test_create_todo(title, expected_status):
    response = client.post("/todos", json={"title": title})
    assert response.status_code == expected_status

def test_list_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "todos" in response.json()

@pytest.mark.parametrize("todo_id, expected_status", [
    (1, 200),
    (999, 404),  # Non-existent todo should fail
])
def test_mark_todo_done(todo_id, expected_status):
    response = client.put(f"/todos/{todo_id}")
    assert response.status_code == expected_status

@pytest.mark.parametrize("todo_id, expected_status", [
    (1, 200),
    (999, 404),  # Non-existent todo should fail
])
def test_delete_todo(todo_id, expected_status):
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == expected_status
