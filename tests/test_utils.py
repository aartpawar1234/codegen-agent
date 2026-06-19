"""Test suite for utils.py module."""

import pytest
from src.utils import reverse_string


class TestReverseString:
    """Test cases for the reverse_string function."""

    def test_reverse_string_basic(self):
        """Test reversing a basic string."""
        assert reverse_string("hello") == "olleh"
        assert reverse_string("Python") == "nohtyP"

    def test_reverse_string_empty(self):
        """Test reversing an empty string."""
        assert reverse_string("") == ""

    def test_reverse_string_single_char(self):
        """Test reversing a single character string."""
        assert reverse_string("a") == "a"

    def test_reverse_string_palindrome(self):
        """Test reversing a palindrome string."""
        assert reverse_string("madam") == "madam"

    def test_reverse_string_with_spaces(self):
        """Test reversing a string with spaces."""
        assert reverse_string("hello world") == "dlrow olleh"

    def test_reverse_string_with_special_chars(self):
        """Test reversing a string with special characters."""
        assert reverse_string("hello@world!") == "!dlrow@olleh"

    def test_reverse_string_with_unicode(self):
        """Test reversing a string with unicode characters."""
        assert reverse_string("こんにちは") == "はちにんこ"
        assert reverse_string("123😊abc") == "cba😊321"

    def test_reverse_string_with_mixed_case(self):
        """Test reversing a string with mixed case."""
        assert reverse_string("HeLLo") == "oLLeH"

    def test_reverse_string_with_numbers(self):
        """Test reversing a string with numbers."""
        assert reverse_string("12345") == "54321"

    def test_reverse_string_with_newline(self):
        """Test reversing a string with newline characters."""
        assert reverse_string("hello\nworld") == "dlrow\nolleh"

    def test_reverse_string_with_tab(self):
        """Test reversing a string with tab characters."""
        assert reverse_string("hello\tworld") == "dlrow\tolleh"
