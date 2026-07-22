from .operations import add, subtract, multiply, divide
from .advanced_operations import power, square_root


class Calculator:
    """A simple calculator class to perform basic and advanced operations."""

    def calculate(self, operation: str, *args: float) -> float:
        """Perform the specified operation with the given arguments."""
        if operation == 'add':
            return add(*args)
        elif operation == 'subtract':
            return subtract(*args)
        elif operation == 'multiply':
            return multiply(*args)
        elif operation == 'divide':
            return divide(*args)
        elif operation == 'power':
            return power(*args)
        elif operation == 'square_root':
            return square_root(args[0])
        else:
            raise ValueError(f"Unknown operation: {operation}")
