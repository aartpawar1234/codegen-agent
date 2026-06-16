"""Core arithmetic operations as pure functions."""

from typing import Union

Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Sum of a and b.
    """
    return a + b

def subtract(a: Number, b: Number) -> Number:
    """Subtract two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Difference of a and b.
    """
    return a - b

def multiply(a: Number, b: Number) -> Number:
    """Multiply two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Product of a and b.
    """
    return a * b

def divide(a: Number, b: Number) -> Number:
    """Divide two numbers.

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        Quotient of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b