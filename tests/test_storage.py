"""
Tests for the storage module (save_tasks and load_tasks functions).
"""
import json
import tempfile
from pathlib import Path
from src.models import Task
from src.storage import save_tasks, load_tasks


class TestStorage:
    """Test cases for the storage module."""

    def test_save_and_load_tasks(self):
        """Test saving and loading tasks from a JSON file."""
        tasks = [
            Task(id=1, title="Task 1", description="Description 1", completed=False),
            Task(id=2, title="Task 2", description="Description 2", completed=True),
        ]

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            # Save tasks
            save_tasks(tasks, tmp_path)

            # Verify file exists and contains expected data
            assert tmp_path.exists()
            with tmp_path.open("r") as f:
                saved_data = json.load(f)
            assert len(saved_data) == 2
            assert saved_data[0]["id"] == 1
            assert saved_data[0]["title"] == "Task 1"
            assert saved_data[0]["description"] == "Description 1"
            assert saved_data[0]["completed"] is False
            assert saved_data[1]["id"] == 2
            assert saved_data[1]["title"] == "Task 2"
            assert saved_data[1]["description"] == "Description 2"
            assert saved_data[1]["completed"] is True

            # Load tasks
            loaded_tasks = load_tasks(tmp_path)
            assert len(loaded_tasks) == 2
            assert loaded_tasks[0].id == 1
            assert loaded_tasks[0].title == "Task 1"
            assert loaded_tasks[0].description == "Description 1"
            assert loaded_tasks[0].completed is False
            assert loaded_tasks[1].id == 2
            assert loaded_tasks[1].title == "Task 2"
            assert loaded_tasks[1].description == "Description 2"
            assert loaded_tasks[1].completed is True

        finally:
            # Clean up
            if tmp_path.exists():
                tmp_path.unlink()

    def test_load_tasks_nonexistent_file(self):
        """Test loading tasks from a non-existent file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            # Ensure file does not exist
            tmp_path.unlink()
            assert not tmp_path.exists()

            # Load tasks (should return empty list)
            loaded_tasks = load_tasks(tmp_path)
            assert loaded_tasks == []

        finally:
            # Clean up (no-op if file doesn't exist)
            if tmp_path.exists():
                tmp_path.unlink()

    def test_save_and_load_empty_tasks(self):
        """Test saving and loading an empty list of tasks."""
        tasks = []

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            # Save tasks
            save_tasks(tasks, tmp_path)

            # Load tasks
            loaded_tasks = load_tasks(tmp_path)
            assert loaded_tasks == []

        finally:
            # Clean up
            if tmp_path.exists():
                tmp_path.unlink()