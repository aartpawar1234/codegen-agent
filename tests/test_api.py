"""
Tests for the API module.

Tests FastAPI endpoints using httpx.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api import app
from src.models import Task, TaskList


client = TestClient(app)


@pytest.fixture
def mock_empty_storage():
    """Mock storage to return an empty TaskList."""
    with patch("src.api.load_tasks") as mock_load:
        mock_load.return_value = TaskList()
        yield


@pytest.fixture
def mock_storage_with_task():
    """Mock storage to return a TaskList with a task."""
    task = Task(id="1", title="Test Task", description="Test Description")
    task_list = TaskList([task])
    with patch("src.api.load_tasks") as mock_load, \
         patch("src.api.save_tasks") as mock_save:
        mock_load.return_value = task_list
        yield mock_load, mock_save


def test_list_tasks_empty(mock_empty_storage):
    """Test listing tasks when no tasks exist."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_add_task(mock_storage_with_task):
    """Test adding a new task."""
    task_data = {"title": "New Task", "description": "New Description"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "New Description"
    assert data["completed"] is False
    assert "id" in data


def test_get_task(mock_storage_with_task):
    """Test getting a task by ID."""
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1"
    assert data["title"] == "Test Task"


def test_get_task_not_found():
    """Test getting a nonexistent task."""
    with patch("src.api.load_tasks") as mock_load:
        mock_load.return_value = TaskList()
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"


def test_complete_task(mock_storage_with_task):
    """Test marking a task as completed."""
    response = client.put("/tasks/1/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_complete_task_not_found():
    """Test completing a nonexistent task."""
    with patch("src.api.load_tasks") as mock_load:
        mock_load.return_value = TaskList()
        response = client.put("/tasks/999/complete")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"


def test_remove_task(mock_storage_with_task):
    """Test removing a task."""
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Task removed"


def test_remove_task_not_found():
    """Test removing a nonexistent task."""
    with patch("src.api.load_tasks") as mock_load:
        mock_load.return_value = TaskList()
        response = client.delete("/tasks/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"