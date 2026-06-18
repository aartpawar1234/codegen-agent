"""Test suite for the greet utility function."""

import pytest
from src.utils.greet import greet


class TestGreet:
    """Test cases for the greet function."""

    def test_greet_basic(self) -> None:
        """Test greet with a standard name."""
        result = greet("Alice")
        assert result == "Hello, Alice!"

    def test_greet_empty_string(self) -> None:
        """Test greet with an empty string."""
        result = greet("")
        assert result == "Hello, !"

    def test_greet_special_chars(self) -> None:
        """Test greet with special characters in the name."""
        result = greet("!@#$%^&*()")
        assert result == "Hello, !@#$%^&*()!"

    def test_greet_whitespace(self) -> None:
        """Test greet with whitespace in the name."""
        result = greet("  spaces  ")
        assert result == "Hello,   spaces  !"

    def test_greet_non_string_input(self) -> None:
        """Test greet with non-string input (should raise TypeError)."""
        with pytest.raises(TypeError):
            greet(123)  # type: ignore

    def test_greet_none_input(self) -> None:
        """Test greet with None input (should raise TypeError)."""
        with pytest.raises(TypeError):
            greet(None)  # type: ignore
