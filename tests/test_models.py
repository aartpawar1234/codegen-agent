import pytest
from models import Todo, TodoCreate

def test_todo_creation():
    todo_data = TodoCreate(title="Test Todo")
    todo = Todo(id=1, title=todo_data.title)
    assert todo.title == todo_data.title
    assert todo.done is False

def test_todo_creation_invalid():
    with pytest.raises(ValueError):
        Todo(id=1, title=None)  # Title cannot be None
