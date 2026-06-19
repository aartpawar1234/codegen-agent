"""Utility module containing string manipulation functions."""


def reverse_string(s: str) -> str:
    """Reverse the input string.

    Args:
        s: The string to reverse.

    Returns:
        The reversed string.

    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("Python")
        'nohtyP'
        >>> reverse_string("")
        ''
    """
    return s[::-1]