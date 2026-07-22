from .operations import add, subtract, multiply, divide
import math


def power(base: float, exponent: float) -> float:
    """Return the result of raising base to the power of exponent."""
    return base ** exponent


def square_root(value: float) -> float:
    """Return the square root of value. Raises ValueError if value is negative."""
    if value < 0:
        raise ValueError("Cannot take the square root of a negative number")
    return math.sqrt(value)
