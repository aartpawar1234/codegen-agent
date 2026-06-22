"""
Defines the core data model for the to-do list, including the Task class.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Task:
    """
    Represents a single task in the to-do list.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title or description of the task.
        description (Optional[str]): Detailed description of the task.
        completed (bool): Whether the task is completed.
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskList:
    """
    Represents a collection of tasks.

    Attributes:
        tasks (List[Task]): List of tasks.
    """

    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the list."""
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Returns:
            bool: True if task was found and removed, False otherwise.
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Returns:
            Optional[Task]: The task if found, None otherwise.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self) -> List[Task]:
        """Return a list of all tasks."""
        return self.tasks

    def clear_tasks(self) -> None:
        """Remove all tasks from the list."""
        self.tasks.clear()