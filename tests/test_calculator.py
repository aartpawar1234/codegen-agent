import pytest
from calculator.calculator import Calculator
from calculator.operations import add, subtract, multiply, divide


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance."""
    return Calculator()


class TestCalculatorAdd:
    """Test cases for Calculator.add method."""

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
    def test_add_happy_path(self, calculator, a, b, expected):
        """Test Calculator.add with valid inputs."""
        result = calculator.add(a, b)
        assert result == expected

    def test_add_delegates_to_operations_add(self, calculator, mocker):
        """Test that Calculator.add delegates to operations.add."""
        mock_add = mocker.patch("calculator.operations.add", return_value=5)
        result = calculator.add(2, 3)
        mock_add.assert_called_once_with(2, 3)
        assert result == 5

    def test_add_with_none(self, calculator):
        """Test Calculator.add with None input."""
        with pytest.raises(TypeError):
            calculator.add(None, 1)

    def test_add_with_string(self, calculator):
        """Test Calculator.add with string input."""
        with pytest.raises(TypeError):
            calculator.add("1", 2)


class TestCalculatorSubtract:
    """Test cases for Calculator.subtract method."""

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
    def test_subtract_happy_path(self, calculator, a, b, expected):
        """Test Calculator.subtract with valid inputs."""
        result = calculator.subtract(a, b)
        assert result == expected

    def test_subtract_delegates_to_operations_subtract(self, calculator, mocker):
        """Test that Calculator.subtract delegates to operations.subtract."""
        mock_subtract = mocker.patch("calculator.operations.subtract", return_value=2)
        result = calculator.subtract(5, 3)
        mock_subtract.assert_called_once_with(5, 3)
        assert result == 2

    def test_subtract_with_none(self, calculator):
        """Test Calculator.subtract with None input."""
        with pytest.raises(TypeError):
            calculator.subtract(None, 1)

    def test_subtract_with_string(self, calculator):
        """Test Calculator.subtract with string input."""
        with pytest.raises(TypeError):
            calculator.subtract("5", 3)


class TestCalculatorMultiply:
    """Test cases for Calculator.multiply method."""

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
    def test_multiply_happy_path(self, calculator, a, b, expected):
        """Test Calculator.multiply with valid inputs."""
        result = calculator.multiply(a, b)
        assert result == expected

    def test_multiply_delegates_to_operations_multiply(self, calculator, mocker):
        """Test that Calculator.multiply delegates to operations.multiply."""
        mock_multiply = mocker.patch("calculator.operations.multiply", return_value=6)
        result = calculator.multiply(2, 3)
        mock_multiply.assert_called_once_with(2, 3)
        assert result == 6

    def test_multiply_with_none(self, calculator):
        """Test Calculator.multiply with None input."""
        with pytest.raises(TypeError):
            calculator.multiply(None, 2)

    def test_multiply_with_string(self, calculator):
        """Test Calculator.multiply with string input."""
        with pytest.raises(TypeError):
            calculator.multiply("2", 3)


class TestCalculatorDivide:
    """Test cases for Calculator.divide method."""

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
    def test_divide_happy_path(self, calculator, a, b, expected):
        """Test Calculator.divide with valid inputs."""
        result = calculator.divide(a, b)
        assert result == expected

    def test_divide_by_zero(self, calculator):
        """Test Calculator.divide by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="division by zero"):
            calculator.divide(1, 0)

    def test_divide_delegates_to_operations_divide(self, calculator, mocker):
        """Test that Calculator.divide delegates to operations.divide."""
        mock_divide = mocker.patch("calculator.operations.divide", return_value=2.0)
        result = calculator.divide(6, 3)
        mock_divide.assert_called_once_with(6, 3)
        assert result == 2.0

    def test_divide_with_none(self, calculator):
        """Test Calculator.divide with None input."""
        with pytest.raises(TypeError):
            calculator.divide(None, 2)

    def test_divide_with_string(self, calculator):
        """Test Calculator.divide with string input."""
        with pytest.raises(TypeError):
            calculator.divide("6", 3)