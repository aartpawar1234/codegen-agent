"""
A generic Stack data structure implementation in Python.

This module provides a Stack class that supports standard stack operations
such as push, pop, peek, checking if the stack is empty, and getting the size.
"""

from typing import TypeVar, Generic, Optional

T = TypeVar('T')


class Stack(Generic[T]):
    """
    A generic stack data structure that follows the Last-In-First-Out (LIFO) principle.

    Attributes:
        _items (list[T]): Internal list to store stack elements.
    """

    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """
        Push an item onto the top of the stack.

        Args:
            item (T): The item to be pushed onto the stack.
        """
        self._items.append(item)

    def pop(self) -> T:
        """
        Remove and return the item at the top of the stack.

        Returns:
            T: The item at the top of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Optional[T]:
        """
        Return the item at the top of the stack without removing it.

        Returns:
            Optional[T]: The item at the top of the stack, or None if the stack is empty.
        """
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Return the number of items in the stack.

        Returns:
            int: The number of items in the stack.
        """
        return len(self._items)
