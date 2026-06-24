import pytest
from calculator.core import add, subtract, multiply, divide


class TestAdd:
    """Test cases for the add function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2.0, 3.0) == 5.0

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add(-2.0, -3.0) == -5.0

    def test_add_mixed_numbers(self):
        """Test adding a positive and a negative number."""
        assert add(2.0, -3.0) == -1.0

    def test_add_zero(self):
        """Test adding zero to a number."""
        assert add(5.0, 0.0) == 5.0
        assert add(0.0, 5.0) == 5.0

    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(1.5, 2.5) == 4.0

    def test_add_large_numbers(self):
        """Test adding very large numbers."""
        assert add(1e10, 1e10) == 2e10


class TestSubtract:
    """Test cases for the subtract function."""

    def test_subtract_positive_numbers(self):
        """Test subtracting two positive numbers."""
        assert subtract(5.0, 3.0) == 2.0

    def test_subtract_negative_numbers(self):
        """Test subtracting two negative numbers."""
        assert subtract(-2.0, -3.0) == 1.0

    def test_subtract_mixed_numbers(self):
        """Test subtracting a negative number from a positive number."""
        assert subtract(2.0, -3.0) == 5.0

    def test_subtract_zero(self):
        """Test subtracting zero from a number."""
        assert subtract(5.0, 0.0) == 5.0

    def test_subtract_floats(self):
        """Test subtracting floating point numbers."""
        assert subtract(3.5, 1.5) == 2.0

    def test_subtract_large_numbers(self):
        """Test subtracting very large numbers."""
        assert subtract(1e10, 1e9) == 9e9


class TestMultiply:
    """Test cases for the multiply function."""

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert multiply(2.0, 3.0) == 6.0

    def test_multiply_negative_numbers(self):
        """Test multiplying two negative numbers."""
        assert multiply(-2.0, -3.0) == 6.0

    def test_multiply_mixed_numbers(self):
        """Test multiplying a positive and a negative number."""
        assert multiply(2.0, -3.0) == -6.0

    def test_multiply_by_zero(self):
        """Test multiplying a number by zero."""
        assert multiply(5.0, 0.0) == 0.0
        assert multiply(0.0, 5.0) == 0.0

    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        assert multiply(1.5, 2.0) == 3.0

    def test_multiply_large_numbers(self):
        """Test multiplying very large numbers."""
        assert multiply(1e5, 1e5) == 1e10


class TestDivide:
    """Test cases for the divide function."""

    def test_divide_positive_numbers(self):
        """Test dividing two positive numbers."""
        assert divide(6.0, 3.0) == 2.0

    def test_divide_negative_numbers(self):
        """Test dividing two negative numbers."""
        assert divide(-6.0, -3.0) == 2.0

    def test_divide_mixed_numbers(self):
        """Test dividing a positive number by a negative number."""
        assert divide(6.0, -3.0) == -2.0

    def test_divide_by_one(self):
        """Test dividing a number by one."""
        assert divide(5.0, 1.0) == 5.0

    def test_divide_floats(self):
        """Test dividing floating point numbers."""
        assert divide(3.0, 2.0) == 1.5

    def test_divide_large_numbers(self):
        """Test dividing very large numbers."""
        assert divide(1e10, 1e5) == 1e5

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises a ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5.0, 0.0)

    def test_divide_zero_by_nonzero(self):
        """Test dividing zero by a non-zero number."""
        assert divide(0.0, 5.0) == 0.0


class TestPublicAPI:
    """Test cases for the public API of the calculator package."""

    def test_import_add_from_package(self):
        """Test that add can be imported from the package."""
        from calculator import add
        assert callable(add)

    def test_import_subtract_from_package(self):
        """Test that subtract can be imported from the package."""
        from calculator import subtract
        assert callable(subtract)

    def test_import_multiply_from_package(self):
        """Test that multiply can be imported from the package."""
        from calculator import multiply
        assert callable(multiply)

    def test_import_divide_from_package(self):
        """Test that divide can be imported from the package."""
        from calculator import divide
        assert callable(divide)

    def test_all_functions_exported(self):
        """Test that all functions are exported in __all__."""
        import calculator
        assert set(calculator.__all__) == {"add", "subtract", "multiply", "divide"}