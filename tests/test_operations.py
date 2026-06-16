import pytest
from calculator.operations import add, subtract, multiply, divide


class TestAdd:
    """Test cases for the add function."""

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1, 2, 3),
            (-1, 1, 0),
            (0, 0, 0),
            (1.5, 2.5, 4.0),
            (-1.5, -2.5, -4.0),
            (10**6, 10**6, 2 * 10**6),
        ],
    )
    def test_add_happy_path(self, a, b, expected):
        """Test add with valid inputs."""
        result = add(a, b)
        assert result == expected

    def test_add_with_none(self):
        """Test add with None input."""
        with pytest.raises(TypeError):
            add(None, 1)

    def test_add_with_string(self):
        """Test add with string input."""
        with pytest.raises(TypeError):
            add("1", 2)


class TestSubtract:
    """Test cases for the subtract function."""

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (5, 3, 2),
            (-1, -1, 0),
            (0, 0, 0),
            (5.5, 2.5, 3.0),
            (-5.5, -2.5, -3.0),
            (10**6, 10**6 - 1, 1),
        ],
    )
    def test_subtract_happy_path(self, a, b, expected):
        """Test subtract with valid inputs."""
        result = subtract(a, b)
        assert result == expected

    def test_subtract_with_none(self):
        """Test subtract with None input."""
        with pytest.raises(TypeError):
            subtract(None, 1)

    def test_subtract_with_string(self):
        """Test subtract with string input."""
        with pytest.raises(TypeError):
            subtract("5", 3)


class TestMultiply:
    """Test cases for the multiply function."""

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (2, 3, 6),
            (-1, 1, -1),
            (0, 5, 0),
            (2.5, 4, 10.0),
            (-2.5, -4, 10.0),
            (10**3, 10**3, 10**6),
        ],
    )
    def test_multiply_happy_path(self, a, b, expected):
        """Test multiply with valid inputs."""
        result = multiply(a, b)
        assert result == expected

    def test_multiply_with_none(self):
        """Test multiply with None input."""
        with pytest.raises(TypeError):
            multiply(None, 2)

    def test_multiply_with_string(self):
        """Test multiply with string input."""
        with pytest.raises(TypeError):
            multiply("2", 3)


class TestDivide:
    """Test cases for the divide function."""

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (6, 3, 2.0),
            (-6, 3, -2.0),
            (6, -3, -2.0),
            (-6, -3, 2.0),
            (5.0, 2.0, 2.5),
            (1, 10**6, 1e-6),
        ],
    )
    def test_divide_happy_path(self, a, b, expected):
        """Test divide with valid inputs."""
        result = divide(a, b)
        assert result == expected

    def test_divide_by_zero(self):
        """Test divide by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="division by zero"):
            divide(1, 0)

    def test_divide_with_none(self):
        """Test divide with None input."""
        with pytest.raises(TypeError):
            divide(None, 2)

    def test_divide_with_string(self):
        """Test divide with string input."""
        with pytest.raises(TypeError):
            divide("6", 3)