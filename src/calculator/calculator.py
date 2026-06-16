"""Calculator class that uses core arithmetic operations."""

from typing import Union

from .operations import add, subtract, multiply, divide

Number = Union[int, float]

class Calculator:
    """A simple calculator that performs basic arithmetic operations."""

    def add(self, a: Number, b: Number) -> Number:
        """Add two numbers.

        Args:
            a: First number.
            b: Second number.

        Returns:
            Sum of a and b.
        """
        return add(a, b)

    def subtract(self, a: Number, b: Number) -> Number:
        """Subtract two numbers.

        Args:
            a: First number.
            b: Second number.

        Returns:
            Difference of a and b.
        """
        return subtract(a, b)

    def multiply(self, a: Number, b: Number) -> Number:
        """Multiply two numbers.

        Args:
            a: First number.
            b: Second number.

        Returns:
            Product of a and b.
        """
        return multiply(a, b)

    def divide(self, a: Number, b: Number) -> Number:
        """Divide two numbers.

        Args:
            a: Dividend.
            b: Divisor.

        Returns:
            Quotient of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        return divide(a, b)