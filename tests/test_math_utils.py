"""
Test suite for math_utils module.
"""
import pytest
from src.math_utils import add


class TestAdd:
    """Test cases for the add function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add(-2, -3) == -5

    def test_add_mixed_numbers(self):
        """Test adding a positive and a negative number."""
        assert add(-1, 1) == 0

    def test_add_zero(self):
        """Test adding zero to a number."""
        assert add(0, 5) == 5
        assert add(5, 0) == 5

    def test_add_large_numbers(self):
        """Test adding large numbers."""
        assert add(1000000, 2000000) == 3000000

    def test_add_floats_raises_type_error(self):
        """Test that adding floats raises a TypeError."""
        with pytest.raises(TypeError):
            add(1.5, 2.5)

    def test_add_strings_raises_type_error(self):
        """Test that adding strings raises a TypeError."""
        with pytest.raises(TypeError):
            add("hello", "world")

    def test_add_none_raises_type_error(self):
        """Test that adding None raises a TypeError."""
        with pytest.raises(TypeError):
            add(None, 5)
