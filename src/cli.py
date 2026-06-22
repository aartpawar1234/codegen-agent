"""
Implements a command-line interface for interacting with the to-do list.
"""
import argparse
from typing import Optional

from src.models import Task, TaskList
from src.storage import load_tasks, save_tasks


def display_tasks(task_list: TaskList) -> None:
    """Display all tasks in the task list."""
    tasks = task_list.list_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "✓" if task.completed else "✗"
        print(f"[{status}] {task.id}: {task.title}")
        if task.description:
            print(f"  Description: {task.description}")


def add_task(task_list: TaskList, title: str, description: Optional[str]) -> None:
    """Add a new task to the task list."""
    if not title:
        print("Error: Task title cannot be empty.")
        return

    new_id = max((task.id for task in task_list.list_tasks()), default=0) + 1
    task = Task(id=new_id, title=title, description=description)
    task_list.add_task(task)
    save_tasks(task_list.list_tasks())
    print(f"Task added: {title}")


def remove_task(task_list: TaskList, task_id: int) -> None:
    """Remove a task from the task list."""
    if task_list.remove_task(task_id):
        save_tasks(task_list.list_tasks())
        print(f"Task {task_id} removed.")
    else:
        print(f"Error: Task {task_id} not found.")


def mark_completed(task_list: TaskList, task_id: int) -> None:
    """Mark a task as completed."""
    task = task_list.get_task(task_id)
    if task:
        task.completed = True
        save_tasks(task_list.list_tasks())
        print(f"Task {task_id} marked as completed.")
    else:
        print(f"Error: Task {task_id} not found.")


def main() -> None:
    """Entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="To-Do List CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List tasks
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Add task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")
    add_parser.add_argument("--description", type=str, help="Description of the task")

    # Remove task
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("task_id", type=int, help="ID of the task to remove")

    # Mark task as completed
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to mark as completed")

    args = parser.parse_args()

    task_list = TaskList()
    tasks = load_tasks()
    for task in tasks:
        task_list.add_task(task)

    if args.command == "list":
        display_tasks(task_list)

    elif args.command == "add":
        add_task(task_list, args.title, args.description)

    elif args.command == "remove":
        remove_task(task_list, args.task_id)

    elif args.command == "complete":
        mark_completed(task_list, args.task_id)


if __name__ == "__main__":
    main()