import pytest
from src.math.operations import add


class TestAddFunction:
    """Test suite for the add function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        result = add(2.5, 3.5)
        assert result == 6.0

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        result = add(-2.5, -3.5)
        assert result == -6.0

    def test_add_mixed_numbers(self):
        """Test adding a positive and a negative number."""
        result = add(5.0, -3.0)
        assert result == 2.0

    def test_add_zero(self):
        """Test adding zero to a number."""
        result = add(0.0, 5.0)
        assert result == 5.0
        result = add(5.0, 0.0)
        assert result == 5.0

    def test_add_floats_with_decimals(self):
        """Test adding floats with multiple decimal places."""
        result = add(1.111, 2.222)
        assert result == pytest.approx(3.333)

    def test_add_large_numbers(self):
        """Test adding very large numbers."""
        result = add(1e10, 2e10)
        assert result == 3e10

    def test_add_small_numbers(self):
        """Test adding very small numbers."""
        result = add(1e-10, 2e-10)
        assert result == pytest.approx(3e-10)

    def test_add_integers(self):
        """Test adding integers (implicit conversion to float)."""
        result = add(2, 3)
        assert result == 5.0

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (0, 0, 0.0),
            (-0.0, 0.0, 0.0),
            (float('inf'), 1.0, float('inf')),
            (float('-inf'), -1.0, float('-inf')),
            (float('inf'), float('-inf'), float('nan')),
        ],
    )
    def test_add_special_floats(self, a, b, expected):
        """Test adding special float values (inf, -inf, nan)."""
        result = add(a, b)
        if expected != expected:  # Check for NaN
            assert result != result
        else:
            assert result == expected

    def test_add_non_numeric_inputs_raises_type_error(self):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            add("2", 3)
        with pytest.raises(TypeError):
            add(2, "3")
        with pytest.raises(TypeError):
            add("a", "b")

    def test_add_none_inputs_raises_type_error(self):
        """Test that None inputs raise TypeError."""
        with pytest.raises(TypeError):
            add(None, 1)
        with pytest.raises(TypeError):
            add(1, None)
        with pytest.raises(TypeError):
            add(None, None)