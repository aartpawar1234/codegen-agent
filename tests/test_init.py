import pytest
from calculator import Calculator, add, subtract, multiply, divide


def test_import_calculator():
    """Test that Calculator is imported correctly."""
    assert Calculator is not None


def test_import_add():
    """Test that add is imported correctly."""
    assert add is not None


def test_import_subtract():
    """Test that subtract is imported correctly."""
    assert subtract is not None


def test_import_multiply():
    """Test that multiply is imported correctly."""
    assert multiply is not None


def test_import_divide():
    """Test that divide is imported correctly."""
    assert divide is not None