"""
Comprehensive pytest tests for the Stack class.

This module tests all public methods of the Stack class for correctness,
edge cases, and error conditions.
"""

import pytest
from src.stack import Stack


class TestStackInitialization:
    """Test stack initialization and initial state."""

    def test_initially_empty(self) -> None:
        """Test that a new stack is initially empty."""
        stack = Stack[int]()
        assert stack.is_empty()
        assert stack.size() == 0
        assert stack.peek() is None

    def test_initially_empty_with_any_type(self) -> None:
        """Test that a new stack is initially empty for any type."""
        stack = Stack[str]()
        assert stack.is_empty()
        assert stack.size() == 0
        assert stack.peek() is None


class TestStackPush:
    """Test the push operation."""

    def test_push_single_item(self) -> None:
        """Test pushing a single item onto the stack."""
        stack = Stack[int]()
        stack.push(10)
        assert not stack.is_empty()
        assert stack.size() == 1
        assert stack.peek() == 10

    def test_push_multiple_items(self) -> None:
        """Test pushing multiple items onto the stack."""
        stack = Stack[str]()
        stack.push("a")
        stack.push("b")
        stack.push("c")
        assert stack.size() == 3
        assert stack.peek() == "c"

    def test_push_different_types(self) -> None:
        """Test pushing items of different types (if needed)."""
        stack = Stack[object]()
        stack.push(1)
        stack.push("hello")
        stack.push(3.14)
        assert stack.size() == 3
        assert stack.peek() == 3.14


class TestStackPop:
    """Test the pop operation."""

    def test_pop_single_item(self) -> None:
        """Test popping the only item from the stack."""
        stack = Stack[int]()
        stack.push(10)
        item = stack.pop()
        assert item == 10
        assert stack.is_empty()
        assert stack.size() == 0

    def test_pop_multiple_items(self) -> None:
        """Test popping multiple items from the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1
        assert stack.is_empty()

    def test_pop_empty_stack_raises_error(self) -> None:
        """Test that popping from an empty stack raises IndexError."""
        stack = Stack[int]()
        with pytest.raises(IndexError, match="pop from empty stack"):
            stack.pop()


class TestStackPeek:
    """Test the peek operation."""

    def test_peek_single_item(self) -> None:
        """Test peeking at the only item in the stack."""
        stack = Stack[int]()
        stack.push(10)
        assert stack.peek() == 10
        assert stack.size() == 1  # Ensure peek does not remove the item

    def test_peek_multiple_items(self) -> None:
        """Test peeking at the top item in a stack with multiple items."""
        stack = Stack[str]()
        stack.push("a")
        stack.push("b")
        assert stack.peek() == "b"
        assert stack.size() == 2  # Ensure peek does not remove the item

    def test_peek_empty_stack_returns_none(self) -> None:
        """Test that peeking at an empty stack returns None."""
        stack = Stack[int]()
        assert stack.peek() is None


class TestStackIsEmpty:
    """Test the is_empty operation."""

    def test_is_empty_on_new_stack(self) -> None:
        """Test that a new stack is empty."""
        stack = Stack[int]()
        assert stack.is_empty()

    def test_is_empty_after_push(self) -> None:
        """Test that a stack is not empty after pushing an item."""
        stack = Stack[int]()
        stack.push(10)
        assert not stack.is_empty()

    def test_is_empty_after_pop(self) -> None:
        """Test that a stack is empty after popping the last item."""
        stack = Stack[int]()
        stack.push(10)
        stack.pop()
        assert stack.is_empty()


class TestStackSize:
    """Test the size operation."""

    def test_size_on_new_stack(self) -> None:
        """Test that a new stack has size 0."""
        stack = Stack[int]()
        assert stack.size() == 0

    def test_size_after_single_push(self) -> None:
        """Test that the size is 1 after pushing one item."""
        stack = Stack[int]()
        stack.push(10)
        assert stack.size() == 1

    def test_size_after_multiple_pushes(self) -> None:
        """Test that the size is correct after multiple pushes."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.size() == 3

    def test_size_after_multiple_pops(self) -> None:
        """Test that the size is correct after multiple pops."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.pop()
        stack.pop()
        assert stack.size() == 1


class TestStackMixedOperations:
    """Test mixed stack operations."""

    def test_mixed_operations(self) -> None:
        """Test a sequence of push, pop, peek, and size operations."""
        stack = Stack[str]()
        assert stack.is_empty()
        stack.push("first")
        stack.push("second")
        assert stack.size() == 2
        assert stack.peek() == "second"
        assert stack.pop() == "second"
        assert stack.size() == 1
        stack.push("third")
        assert stack.size() == 2
        assert stack.pop() == "third"
        assert stack.pop() == "first"
        assert stack.is_empty()
