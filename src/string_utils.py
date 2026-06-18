"""
String utilities module.

This module provides helper functions for common string operations:
- reverse_string: Reverse the input string.
- count_words: Count the number of words in a string.
- is_palindrome: Check if a string is a palindrome.
"""


def reverse_string(s: str) -> str:
    """
    Reverse the input string.

    Args:
        s: The string to reverse.

    Returns:
        The reversed string.

    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("")
        ''
    """
    return s[::-1]


def count_words(s: str) -> int:
    """
    Count the number of words in a string.

    Words are defined as sequences of characters separated by whitespace.

    Args:
        s: The string to count words in.

    Returns:
        The number of words in the string.

    Examples:
        >>> count_words("Hello world")
        2
        >>> count_words("  Leading and trailing spaces  ")
        4
        >>> count_words("")
        0
    """
    return len(s.split())


def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.

    A palindrome is a string that reads the same backward as forward,
    ignoring case and non-alphanumeric characters.

    Args:
        s: The string to check.

    Returns:
        True if the string is a palindrome, False otherwise.

    Examples:
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
    """
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = ''.join(c for c in s if c.isalnum()).lower()
    return cleaned == cleaned[::-1]
