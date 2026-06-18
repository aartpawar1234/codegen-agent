"""Simple utility functions for greetings."""


def greet(name: str) -> str:
    """Generate a greeting message for the given name.

    Args:
        name: The name to greet.

    Returns:
        A greeting string in the format 'Hello, {name}!'.

    Examples:
        >>> greet("Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name}!"
