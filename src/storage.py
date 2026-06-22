"""
Handles persistent storage of tasks using JSON files.
"""
import json
from pathlib import Path
from typing import List

from src.models import Task


def save_tasks(tasks: List[Task], filepath: str = "tasks.json") -> None:
    """
    Save a list of tasks to a JSON file.

    Args:
        tasks (List[Task]): List of tasks to save.
        filepath (str): Path to the JSON file. Defaults to "tasks.json".
    """
    task_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
        }
        for task in tasks
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(task_data, f, indent=4)


def load_tasks(filepath: str = "tasks.json") -> List[Task]:
    """
    Load a list of tasks from a JSON file.

    Args:
        filepath (str): Path to the JSON file. Defaults to "tasks.json".

    Returns:
        List[Task]: List of tasks loaded from the file.
    """
    if not Path(filepath).exists():
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        task_data = json.load(f)

    tasks = [
        Task(
            id=task["id"],
            title=task["title"],
            description=task.get("description"),
            completed=task.get("completed", False),
        )
        for task in task_data
    ]
    return tasks