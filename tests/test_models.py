"""
Tests for the models module (Task and TaskList classes).
"""
import pytest
from src.models import Task, TaskList


class TestTask:
    """Test cases for the Task class."""

    def test_task_initialization(self):
        """Test that a Task is initialized correctly."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_default_values(self):
        """Test that a Task uses default values for optional fields."""
        task = Task(id=1, title="Test Task")
        assert task.description is None
        assert task.completed is False


class TestTaskList:
    """Test cases for the TaskList class."""

    def test_add_task(self):
        """Test adding a task to the TaskList."""
        task_list = TaskList()
        task = Task(id=1, title="Test Task")
        task_list.add_task(task)
        assert len(task_list.list_tasks()) == 1
        assert task_list.list_tasks()[0] == task

    def test_remove_task_success(self):
        """Test removing a task from the TaskList."""
        task_list = TaskList()
        task = Task(id=1, title="Test Task")
        task_list.add_task(task)
        assert task_list.remove_task(1) is True
        assert len(task_list.list_tasks()) == 0

    def test_remove_task_failure(self):
        """Test removing a non-existent task from the TaskList."""
        task_list = TaskList()
        assert task_list.remove_task(1) is False
        assert len(task_list.list_tasks()) == 0

    def test_get_task_success(self):
        """Test retrieving a task from the TaskList."""
        task_list = TaskList()
        task = Task(id=1, title="Test Task")
        task_list.add_task(task)
        retrieved_task = task_list.get_task(1)
        assert retrieved_task == task

    def test_get_task_failure(self):
        """Test retrieving a non-existent task from the TaskList."""
        task_list = TaskList()
        assert task_list.get_task(1) is None

    def test_list_tasks(self):
        """Test listing all tasks in the TaskList."""
        task_list = TaskList()
        task1 = Task(id=1, title="Test Task 1")
        task2 = Task(id=2, title="Test Task 2")
        task_list.add_task(task1)
        task_list.add_task(task2)
        tasks = task_list.list_tasks()
        assert len(tasks) == 2
        assert tasks[0] == task1
        assert tasks[1] == task2