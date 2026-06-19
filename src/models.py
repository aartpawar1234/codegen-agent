"""
Core data model for the to-do list application.

Defines the Task class and related data structures.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Task:
    """
    Represents a task in the to-do list.

    Attributes:
        id (str): Unique identifier for the task.
        title (str): Title or description of the task.
        description (Optional[str]): Detailed description of the task.
        completed (bool): Whether the task is completed.
        created_at (datetime): When the task was created.
        completed_at (Optional[datetime]): When the task was completed.
    """

    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate and set default values after initialization."""
        if not self.id:
            self.id = str(uuid.uuid4())

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.completed_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert the task to a dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            completed=data.get("completed", False),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
        )


@dataclass
class TaskList:
    """
    Represents a collection of tasks.

    Attributes:
        tasks (List[Task]): List of tasks.
    """

    tasks: List[Task] = None

    def __init__(self, tasks: Optional[List[Task]] = None):
        self.tasks = tasks if tasks is not None else []

    def add_task(self, task: Task) -> None:
        """Add a task to the list."""
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by its ID.

        Returns:
            bool: True if the task was found and removed, False otherwise.
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False

    def to_dict(self) -> dict:
        """Convert the task list to a dictionary for serialization."""
        return {
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskList":
        """Create a TaskList instance from a dictionary."""
        return cls(
            tasks=[Task.from_dict(task_data) for task_data in data["tasks"]],
        )
