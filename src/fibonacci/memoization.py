"""Module implementing Fibonacci sequence calculation with memoization."""

from typing import Dict

def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using memoization.

    Args:
        n: The index of the Fibonacci number to compute (must be non-negative).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    memo: Dict[int, int] = {0: 0, 1: 1}

    def _fib(k: int) -> int:
        if k not in memo:
            memo[k] = _fib(k - 1) + _fib(k - 2)
        return memo[k]

    return _fib(n)