"""String utility functions module."""

import re
from collections import defaultdict
from typing import Dict

def count_word_frequency(text: str) -> Dict[str, int]:
    """
    Count the frequency of each word in the given text.

    The function is case-insensitive and strips punctuation from words.
    Returns an empty dictionary if the input text is empty.

    Args:
        text: The input text to analyze.

    Returns:
        A dictionary mapping each word to its frequency count.

    Examples:
        >>> count_word_frequency("Hello, world! Hello Python.")
        {'hello': 2, 'world': 1, 'python': 1}

        >>> count_word_frequency("")
        {}
    """
    if not text:
        return {}

    # Convert to lowercase and remove punctuation
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    words = cleaned_text.split()

    frequency = defaultdict(int)
    for word in words:
        frequency[word] += 1

    return dict(frequency)