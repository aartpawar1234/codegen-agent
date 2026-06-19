"""
Command-line interface for the to-do list application.

Provides commands to add, list, complete, and remove tasks.
"""
import argparse
from typing import Optional
import os
import uuid

from src.models import Task

from src.storage import load_tasks, save_tasks


def get_storage_path() -> Optional[str]:
    """Get the storage path from environment variable or return None."""
    return os.getenv("TODO_LIST_STORAGE_PATH")


def add_task(args: argparse.Namespace) -> None:
    """Add a new task to the task list."""
    task_list = load_tasks(get_storage_path())

    task = Task(
        id=str(uuid.uuid4()),
        title=args.title,
        description=args.description,
    )
    task_list.add_task(task)
    save_tasks(task_list, get_storage_path())

    print(f"Task added: {task.title} (ID: {task.id})")


def list_tasks(args: argparse.Namespace) -> None:
    """List all tasks in the task list."""
    task_list = load_tasks(get_storage_path())

    if not task_list.tasks:
        print("No tasks found.")
        return

    for task in task_list.tasks:
        status = "✓" if task.completed else "✗"
        print(f"[{status}] {task.id}: {task.title}")
        if task.description:
            print(f"  {task.description}")


def complete_task(args: argparse.Namespace) -> None:
    """Mark a task as completed."""
    task_list = load_tasks(get_storage_path())

    task = task_list.get_task(args.task_id)
    if not task:
        print(f"Task with ID {args.task_id} not found.")
        return

    task.complete()
    save_tasks(task_list, get_storage_path())

    print(f"Task completed: {task.title}")


def remove_task(args: argparse.Namespace) -> None:
    """Remove a task from the task list."""
    task_list = load_tasks(get_storage_path())

    if task_list.remove_task(args.task_id):
        save_tasks(task_list, get_storage_path())
        print(f"Task removed: {args.task_id}")
    else:
        print(f"Task with ID {args.task_id} not found.")


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="To-Do List CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")
    add_parser.add_argument("--description", type=str, help="Description of the task")
    add_parser.set_defaults(func=add_task)

    # List tasks command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=list_tasks)

    # Complete task command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=str, help="ID of the task to complete")
    complete_parser.set_defaults(func=complete_task)

    # Remove task command
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("task_id", type=str, help="ID of the task to remove")
    remove_parser.set_defaults(func=remove_task)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
