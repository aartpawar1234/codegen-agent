"""
REST API interface for the to-do list application.

Provides endpoints to manage tasks via HTTP requests.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

from src.models import Task
from src.storage import load_tasks, save_tasks


app = FastAPI(title="To-Do List API")


class TaskCreate(BaseModel):
    """Model for creating a new task."""

    title: str
    description: Optional[str] = None


class TaskResponse(BaseModel):
    """Model for task responses."""

    id: str
    title: str
    description: Optional[str]
    completed: bool

    @classmethod
    def from_task(cls, task: Task) -> "TaskResponse":
        """Convert a Task instance to a TaskResponse."""
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )


@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks() -> List[TaskResponse]:
    """List all tasks."""
    task_list = load_tasks()
    return [TaskResponse.from_task(task) for task in task_list.tasks]


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def add_task(task_create: TaskCreate) -> TaskResponse:
    """Add a new task."""
    task_list = load_tasks()

    task = Task(
        id=str(uuid.uuid4()),
        title=task_create.title,
        description=task_create.description,
    )
    task_list.add_task(task)
    save_tasks(task_list)

    return TaskResponse.from_task(task)


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str) -> TaskResponse:
    """Get a task by ID."""
    task_list = load_tasks()
    task = task_list.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse.from_task(task)


@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: str) -> TaskResponse:
    """Mark a task as completed."""
    task_list = load_tasks()
    task = task_list.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.complete()
    save_tasks(task_list)

    return TaskResponse.from_task(task)


@app.delete("/tasks/{task_id}")
def remove_task(task_id: str) -> dict:
    """Remove a task by ID."""
    task_list = load_tasks()

    if not task_list.remove_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")

    save_tasks(task_list)
    return {"detail": "Task removed"}
