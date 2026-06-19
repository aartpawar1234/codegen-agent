"""
Tests for the models module.

Tests Task and TaskList classes.
"""
import pytest
from datetime import datetime
from src.models import Task, TaskList


def test_task_initialization():
    """Test that a Task is initialized correctly."""
    task = Task(id="1", title="Test Task", description="Test Description")
    assert task.id == "1"
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)
    assert task.completed_at is None


def test_task_complete():
    """Test marking a task as completed."""
    task = Task(id="1", title="Test Task")
    task.complete()
    assert task.completed is True
    assert isinstance(task.completed_at, datetime)


def test_task_to_dict():
    """Test converting a Task to a dictionary."""
    task = Task(id="1", title="Test Task", description="Test Description")
    task_dict = task.to_dict()
    assert task_dict["id"] == "1"
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "Test Description"
    assert task_dict["completed"] is False
    assert isinstance(task_dict["created_at"], str)
    assert task_dict["completed_at"] is None


def test_task_from_dict():
    """Test creating a Task from a dictionary."""
    data = {
        "id": "1",
        "title": "Test Task",
        "description": "Test Description",
        "completed": True,
        "created_at": "2023-01-01T00:00:00",
        "completed_at": "2023-01-02T00:00:00",
    }
    task = Task.from_dict(data)
    assert task.id == "1"
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is True
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.completed_at, datetime)


def test_task_list_initialization():
    """Test that a TaskList is initialized correctly."""
    task_list = TaskList()
    assert task_list.tasks == []

    task = Task(id="1", title="Test Task")
    task_list = TaskList([task])
    assert len(task_list.tasks) == 1
    assert task_list.tasks[0].id == "1"


def test_task_list_add_task():
    """Test adding a task to a TaskList."""
    task_list = TaskList()
    task = Task(id="1", title="Test Task")
    task_list.add_task(task)
    assert len(task_list.tasks) == 1
    assert task_list.tasks[0].id == "1"


def test_task_list_get_task():
    """Test getting a task by ID from a TaskList."""
    task = Task(id="1", title="Test Task")
    task_list = TaskList([task])
    retrieved_task = task_list.get_task("1")
    assert retrieved_task == task
    assert retrieved_task.id == "1"

    assert task_list.get_task("2") is None


def test_task_list_remove_task():
    """Test removing a task by ID from a TaskList."""
    task1 = Task(id="1", title="Test Task 1")
    task2 = Task(id="2", title="Test Task 2")
    task_list = TaskList([task1, task2])

    assert task_list.remove_task("1") is True
    assert len(task_list.tasks) == 1
    assert task_list.tasks[0].id == "2"

    assert task_list.remove_task("3") is False
    assert len(task_list.tasks) == 1


def test_task_list_to_dict():
    """Test converting a TaskList to a dictionary."""
    task = Task(id="1", title="Test Task")
    task_list = TaskList([task])
    task_list_dict = task_list.to_dict()
    assert "tasks" in task_list_dict
    assert len(task_list_dict["tasks"]) == 1
    assert task_list_dict["tasks"][0]["id"] == "1"


def test_task_list_from_dict():
    """Test creating a TaskList from a dictionary."""
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
    task_list = TaskList.from_dict(data)
    assert len(task_list.tasks) == 1
    assert task_list.tasks[0].id == "1"
    assert task_list.tasks[0].title == "Test Task"
