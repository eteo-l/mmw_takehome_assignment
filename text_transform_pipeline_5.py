# Build a pipeline that runs a sequence of text transformations over an input string.
# Some examples might be: trim whitespace, collapse repeated spaces, capitalize the
# first letter of each sentence.  But be creative: supply your own!

# Implement at least three transformations of your choice.

import re
from typing import Callable


def trim_whitespace(text: str) -> str:
    """Remove leading and trailing whitespace."""
    return text.strip()


def collapse_spaces(text: str) -> str:
    """Replace multiple consecutive spaces with a single space."""
    return re.sub(r' +', ' ', text)


def remove_repeated_words(text: str) -> str:
    """
    Remove consecutive duplicate words (case-insensitive).

    Note: This will remove ALL consecutive duplicates, including valid English
    constructions like "had had" and "that that". This is a known limitation.
    For production use, you'd need a whitelist of valid duplicates or more
    sophisticated NLP.

    Examples:
        "the the cat" -> "the cat"
        "had had been" -> "had been"  (removes valid "had had")
    """
    return re.sub(r'\b(\w+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)


def normalize_line_breaks(text: str) -> str:
    """
    Normalize line breaks to \\n and collapse multiple blank lines to at most two newlines.

    - Converts \\r\\n and \\r to \\n
    - Collapses 3+ consecutive newlines to 2 (preserving paragraph breaks)
    """
    # Normalize all line break styles to \n
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Collapse 3+ newlines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def run_pipeline(text: str, transforms: list[Callable[[str], str]]) -> str:
    """
    Run a sequence of text transformations on the input text.

    Args:
        text: The input text to transform
        transforms: List of transformation functions to apply in order

    Returns:
        The transformed text after applying all transformations
    """
    result = text
    for transform in transforms:
        result = transform(result)
    return result


# Known limitations:
# 1. remove_repeated_words removes ALL consecutive duplicates, including valid English
#    like "had had", "that that", "can can" (the dance), etc.
# 2. No sentence capitalization implemented - would need to handle abbreviations
#    (e.g., i.e., Dr., Mr.) and edge cases (ellipsis, multiple punctuation)
# 3. collapse_spaces only handles spaces, not other whitespace (tabs, non-breaking spaces)
# 4. normalize_line_breaks preserves at most 2 newlines - may not suit all use cases
# 5. remove_repeated_words only works on word boundaries (\b) - won't catch duplicates
#    with intervening punctuation like "word, word"
