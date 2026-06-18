"""
Test suite for string_utils module.

This module tests the following functions:
- reverse_string
- count_words
- is_palindrome
"""

import pytest
from src.string_utils import reverse_string, count_words, is_palindrome


class TestReverseString:
    """Test cases for reverse_string function."""

    def test_reverse_string_normal(self):
        """Test reversing a normal string."""
        assert reverse_string("hello") == "olleh"
        assert reverse_string("Python") == "nohtyP"

    def test_reverse_string_empty(self):
        """Test reversing an empty string."""
        assert reverse_string("") == ""

    def test_reverse_string_single_char(self):
        """Test reversing a single character string."""
        assert reverse_string("a") == "a"

    def test_reverse_string_with_spaces(self):
        """Test reversing a string with spaces."""
        assert reverse_string("hello world") == "dlrow olleh"

    def test_reverse_string_palindrome(self):
        """Test reversing a palindrome string."""
        assert reverse_string("racecar") == "racecar"


class TestCountWords:
    """Test cases for count_words function."""

    def test_count_words_normal(self):
        """Test counting words in a normal string."""
        assert count_words("Hello world") == 2
        assert count_words("Python is great") == 3

    def test_count_words_empty(self):
        """Test counting words in an empty string."""
        assert count_words("") == 0

    def test_count_words_single_word(self):
        """Test counting words in a single word string."""
        assert count_words("Hello") == 1

    def test_count_words_with_extra_spaces(self):
        """Test counting words with extra spaces."""
        assert count_words("  Leading and trailing spaces  ") == 4
        assert count_words("Multiple   spaces   between  words") == 4

    def test_count_words_with_punctuation(self):
        """Test counting words with punctuation."""
        assert count_words("Hello, world!") == 2


class TestIsPalindrome:
    """Test cases for is_palindrome function."""

    def test_is_palindrome_normal(self):
        """Test checking a normal palindrome."""
        assert is_palindrome("racecar") is True
        assert is_palindrome("A man, a plan, a canal: Panama") is True

    def test_is_palindrome_not_palindrome(self):
        """Test checking a non-palindrome string."""
        assert is_palindrome("hello") is False
        assert is_palindrome("Python") is False

    def test_is_palindrome_empty(self):
        """Test checking an empty string."""
        assert is_palindrome("") is True

    def test_is_palindrome_single_char(self):
        """Test checking a single character string."""
        assert is_palindrome("a") is True

    def test_is_palindrome_with_spaces(self):
        """Test checking a string with spaces."""
        assert is_palindrome("was it a car or a cat I saw") is True

    def test_is_palindrome_case_insensitive(self):
        """Test checking a palindrome with mixed case."""
        assert is_palindrome("RaceCar") is True

    def test_is_palindrome_with_punctuation(self):
        """Test checking a palindrome with punctuation."""
        assert is_palindrome("A man, a plan, a canal: Panama!") is True

    def test_is_palindrome_numbers(self):
        """Test checking a palindrome with numbers."""
        assert is_palindrome("12321") is True
        assert is_palindrome("12345") is False


class TestEdgeCases:
    """Test edge cases for all functions."""

    def test_reverse_string_unicode(self):
        """Test reversing a string with unicode characters."""
        assert reverse_string("こんにちは") == "はちにんこ"

    def test_count_words_unicode(self):
        """Test counting words in a string with unicode characters."""
        assert count_words("こんにちは 世界") == 2

    def test_is_palindrome_unicode(self):
        """Test checking a palindrome with unicode characters."""
        assert is_palindrome("上海自来水来自海上") is True


if __name__ == "__main__":
    pytest.main([__file__])