"""
Handles persistence of to-do list data.

Provides functions to save and load tasks from a file.
"""
import json
from pathlib import Path
from typing import Optional

from src.models import TaskList


DEFAULT_STORAGE_PATH = Path.home() / ".todo_list" / "tasks.json"


def save_tasks(task_list: TaskList, storage_path: Optional[Path] = None) -> None:
    """
    Save the task list to a file.

    Args:
        task_list (TaskList): The task list to save.
        storage_path (Optional[Path]): Path to the storage file. Defaults to DEFAULT_STORAGE_PATH.
    """
    storage_path = storage_path or DEFAULT_STORAGE_PATH
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    data = task_list.to_dict()
    with storage_path.open("w") as f:
        json.dump(data, f, indent=2)


def load_tasks(storage_path: Optional[Path] = None) -> TaskList:
    """
    Load the task list from a file.

    Args:
        storage_path (Optional[Path]): Path to the storage file. Defaults to DEFAULT_STORAGE_PATH.

    Returns:
        TaskList: The loaded task list.
    """
    storage_path = storage_path or DEFAULT_STORAGE_PATH

    if not storage_path.exists():
        return TaskList()

    with storage_path.open("r") as f:
        data = json.load(f)

    return TaskList.from_dict(data)
