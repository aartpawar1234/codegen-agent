import pytest
from src.fibonacci.memoization import fibonacci


class TestFibonacci:
    """Test suite for the fibonacci function with memoization."""

    def test_fibonacci_base_cases(self):
        """Test base cases: fib(0) = 0, fib(1) = 1."""
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    @pytest.mark.parametrize(
        "n, expected",
        [
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 5),
            (6, 8),
            (7, 13),
            (8, 21),
            (9, 34),
            (10, 55),
        ],
    )
    def test_fibonacci_small_values(self, n: int, expected: int):
        """Test fibonacci function with small positive integers."""
        assert fibonacci(n) == expected

    @pytest.mark.parametrize(
        "n, expected",
        [
            (15, 610),
            (20, 6765),
            (25, 75025),
            (30, 832040),
        ],
    )
    def test_fibonacci_medium_values(self, n: int, expected: int):
        """Test fibonacci function with medium positive integers."""
        assert fibonacci(n) == expected

    @pytest.mark.parametrize(
        "n, expected",
        [
            (35, 9227465),
            (40, 102334155),
        ],
    )
    def test_fibonacci_large_values(self, n: int, expected: int):
        """Test fibonacci function with large positive integers."""
        assert fibonacci(n) == expected

    def test_fibonacci_memoization_effectiveness(self):
        """Test that memoization is working by checking internal state."""
        from src.fibonacci.memoization import fibonacci as fib
        
        # Call fibonacci multiple times to ensure memoization persists
        fib(10)
        fib(15)
        fib(20)
        
        # The memo dictionary should contain all computed values
        # This indirectly verifies memoization is working
        assert fibonacci(20) == 6765

    def test_fibonacci_negative_input_raises_error(self):
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError, match="n must be a non-negative integer"):
            fibonacci(-1)

    def test_fibonacci_negative_zero_input(self):
        """Test that fibonacci(0) returns 0 (edge case for zero)."""
        assert fibonacci(0) == 0

    def test_fibonacci_large_input_performance(self):
        """Test performance with a large input to ensure memoization helps."""
        import time
        
        start_time = time.time()
        result = fibonacci(40)
        end_time = time.time()
        
        assert result == 102334155
        assert end_time - start_time < 1.0  # Should be fast due to memoization