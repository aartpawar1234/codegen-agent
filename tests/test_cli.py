"""
Tests for the CLI module.

Tests CLI commands using subprocess.
"""
import subprocess
import sys
from pathlib import Path


def run_cli_command(args):
    """Helper to run a CLI command and return output."""
    cmd = [sys.executable, "-m", "src.cli"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


def test_cli_add_task(tmp_path):
    """Test adding a task via CLI."""
    # Override storage path for testing
    cmd = [sys.executable, "-m", "src.cli", "add", "Test Task", "--description", "Test Description"]
    env = {"TODO_LIST_STORAGE_PATH": str(tmp_path / "tasks.json")}
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert "Task added: Test Task" in result.stdout


def test_cli_list_tasks_empty(tmp_path):
    """Test listing tasks when no tasks exist."""
    cmd = [sys.executable, "-m", "src.cli", "list"]
    env = {"TODO_LIST_STORAGE_PATH": str(tmp_path / "tasks.json")}
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert "No tasks found." in result.stdout


def test_cli_complete_task(tmp_path):
    """Test completing a task via CLI."""
    # Add a task first
    cmd_add = [sys.executable, "-m", "src.cli", "add", "Test Task"]
    env = {"TODO_LIST_STORAGE_PATH": str(tmp_path / "tasks.json")}
    subprocess.run(cmd_add, capture_output=True, text=True, env=env)

    # Get the task ID (this is a bit hacky, but works for testing)
    cmd_list = [sys.executable, "-m", "src.cli", "list"]
    result_list = subprocess.run(cmd_list, capture_output=True, text=True, env=env)
    task_id = result_list.stdout.split("\n")[0].split(":")[0].split("[")[1].strip()

    # Complete the task
    cmd_complete = [sys.executable, "-m", "src.cli", "complete", task_id]
    result_complete = subprocess.run(cmd_complete, capture_output=True, text=True, env=env)
    assert "Task completed: Test Task" in result_complete.stdout


def test_cli_remove_task(tmp_path):
    """Test removing a task via CLI."""
    # Add a task first
    cmd_add = [sys.executable, "-m", "src.cli", "add", "Test Task"]
    env = {"TODO_LIST_STORAGE_PATH": str(tmp_path / "tasks.json")}
    subprocess.run(cmd_add, capture_output=True, text=True, env=env)

    # Get the task ID
    cmd_list = [sys.executable, "-m", "src.cli", "list"]
    result_list = subprocess.run(cmd_list, capture_output=True, text=True, env=env)
    task_id = result_list.stdout.split("\n")[0].split(":")[0].split("[")[1].strip()

    # Remove the task
    cmd_remove = [sys.executable, "-m", "src.cli", "remove", task_id]
    result_remove = subprocess.run(cmd_remove, capture_output=True, text=True, env=env)
    assert "Task removed:" in result_remove.stdout
