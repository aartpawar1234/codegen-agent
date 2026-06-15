import pytest
from src.string_utils import count_word_frequency


class TestCountWordFrequency:
    """Test suite for count_word_frequency function."""

    def test_empty_string(self):
        """Test that empty string returns empty dictionary."""
        result = count_word_frequency("")
        assert result == {}

    def test_single_word(self):
        """Test counting frequency of a single word."""
        result = count_word_frequency("hello")
        assert result == {"hello": 1}

    def test_multiple_words(self):
        """Test counting frequency of multiple words."""
        result = count_word_frequency("hello world hello")
        assert result == {"hello": 2, "world": 1}

    def test_case_insensitivity(self):
        """Test that function is case-insensitive."""
        result = count_word_frequency("Hello hello HELLO")
        assert result == {"hello": 3}

    def test_punctuation_removal(self):
        """Test that punctuation is stripped from words."""
        result = count_word_frequency("Hello, world! Hello Python.")
        assert result == {"hello": 2, "world": 1, "python": 1}

    def test_multiple_punctuation_marks(self):
        """Test handling of multiple punctuation marks around words."""
        result = count_word_frequency("Hello!!! world??? Hello...")
        assert result == {"hello": 2, "world": 1}

    def test_numbers_and_underscores(self):
        """Test that numbers and underscores are treated as part of words."""
        result = count_word_frequency("hello_123 world 456_hello")
        assert result == {"hello_123": 1, "world": 1, "456_hello": 1}

    def test_whitespace_handling(self):
        """Test handling of multiple spaces and tabs."""
        result = count_word_frequency("hello   world\t\tpython")
        assert result == {"hello": 1, "world": 1, "python": 1}

    def test_special_characters(self):
        """Test handling of special characters in text."""
        result = count_word_frequency("hello@world hello#world")
        assert result == {"helloworld": 2}

    def test_unicode_characters(self):
        """Test handling of unicode characters."""
        result = count_word_frequency("café café café")
        assert result == {"café": 3}

    def test_mixed_content(self):
        """Test with mixed content including numbers, punctuation, and case variations."""
        result = count_word_frequency("Hello123, world! hello123 Python.")
        assert result == {"hello123": 2, "world": 1, "python": 1}

    def test_large_text(self):
        """Test with a large text to ensure performance and correctness."""
        large_text = "word " * 1000 + "unique"
        result = count_word_frequency(large_text)
        assert result == {"word": 1000, "unique": 1}

    @pytest.mark.parametrize(
        "input_text, expected",
        [
            ("  ", {}),
            ("\t\n", {}),
            ("   hello   ", {"hello": 1}),
            ("hello\nworld", {"hello": 1, "world": 1}),
        ],
    )
    def test_whitespace_variations(self, input_text, expected):
        """Test various whitespace combinations."""
        result = count_word_frequency(input_text)
        assert result == expected

    @pytest.mark.parametrize(
        "input_text, expected",
        [
            ("a a a a", {"a": 4}),
            ("a b c d e", {"a": 1, "b": 1, "c": 1, "d": 1, "e": 1}),
            ("a", {"a": 1}),
        ],
    )
    def test_simple_repetitions(self, input_text, expected):
        """Test simple word repetitions."""
        result = count_word_frequency(input_text)
        assert result == expected