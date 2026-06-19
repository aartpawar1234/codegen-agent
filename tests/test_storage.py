"""
Tests for the storage module.

Tests save_tasks and load_tasks functions.
"""
import pytest
import json
from pathlib import Path
from src.models import Task, TaskList
from src.storage import save_tasks, load_tasks, DEFAULT_STORAGE_PATH


@pytest.fixture
def temp_storage_path(tmp_path):
    """Fixture to provide a temporary storage path."""
    return tmp_path / "tasks.json"


def test_save_tasks(tmp_path):
    """Test saving a TaskList to a file."""
    task = Task(id="1", title="Test Task", description="Test Description")
    task_list = TaskList([task])
    storage_path = tmp_path / "tasks.json"

    save_tasks(task_list, storage_path)

    assert storage_path.exists()
    with storage_path.open("r") as f:
        data = json.load(f)
    assert data["tasks"][0]["id"] == "1"


def test_load_tasks_empty_file(tmp_path):
    """Test loading an empty task list from a file."""
    storage_path = tmp_path / "tasks.json"
    storage_path.touch()  # Create empty file

    task_list = load_tasks(storage_path)
    assert task_list.tasks == []


def test_load_tasks_nonexistent_file(tmp_path):
    """Test loading from a nonexistent file."""
    storage_path = tmp_path / "nonexistent.json"
    task_list = load_tasks(storage_path)
    assert task_list.tasks == []


def test_load_tasks_with_data(tmp_path):
    """Test loading a TaskList with data from a file."""
    data = {
        "tasks": [
            {
                "id": "1",
                "title": "Test Task",
                "description": "Test Description",
                "completed": False,
                "created_at": "2023-01-01T00:00:00",
                "completed_at": None,
            }
        ]
    }
    storage_path = tmp_path / "tasks.json"
    with storage_path.open("w") as f:
        json.dump(data, f)

    task_list = load_tasks(storage_path)
    assert len(task_list.tasks) == 1
    assert task_list.tasks[0].id == "1"
    assert task_list.tasks[0].title == "Test Task"


def test_save_tasks_default_path(tmp_path, monkeypatch):
    """Test saving to the default storage path."""
    monkeypatch.setattr("src.storage.DEFAULT_STORAGE_PATH", tmp_path / "default_tasks.json")

    task = Task(id="1", title="Test Task")
    task_list = TaskList([task])
    save_tasks(task_list)

    default_path = tmp_path / "default_tasks.json"
    assert default_path.exists()
