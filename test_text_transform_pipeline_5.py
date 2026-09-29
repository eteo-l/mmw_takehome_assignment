# Tests for problem 5: text transform pipeline
import pytest
from text_transform_pipeline_5 import (
    trim_whitespace,
    collapse_spaces,
    remove_repeated_words,
    normalize_line_breaks,
    run_pipeline
)


class TestTrimWhitespace:
    """Test suite for trim_whitespace."""

    def test_trim_leading_whitespace(self):
        assert trim_whitespace("  hello") == "hello"

    def test_trim_trailing_whitespace(self):
        assert trim_whitespace("hello  ") == "hello"

    def test_trim_both_ends(self):
        assert trim_whitespace("  hello  ") == "hello"

    def test_preserve_internal_whitespace(self):
        assert trim_whitespace("  hello  world  ") == "hello  world"

    def test_empty_string(self):
        assert trim_whitespace("") == ""

    def test_only_whitespace(self):
        assert trim_whitespace("   ") == ""


class TestCollapseSpaces:
    """Test suite for collapse_spaces."""

    def test_collapse_double_space(self):
        assert collapse_spaces("hello  world") == "hello world"

    def test_collapse_multiple_spaces(self):
        assert collapse_spaces("hello     world") == "hello world"

    def test_collapse_multiple_groups(self):
        assert collapse_spaces("a  b   c    d") == "a b c d"

    def test_single_space_unchanged(self):
        assert collapse_spaces("hello world") == "hello world"

    def test_no_spaces_unchanged(self):
        assert collapse_spaces("hello") == "hello"

    def test_does_not_affect_newlines(self):
        # collapse_spaces only handles spaces, not other whitespace
        assert collapse_spaces("hello\n\nworld") == "hello\n\nworld"


class TestRemoveRepeatedWords:
    """Test suite for remove_repeated_words."""

    def test_remove_duplicate_lowercase(self):
        assert remove_repeated_words("the the cat") == "the cat"

    def test_remove_duplicate_case_insensitive(self):
        assert remove_repeated_words("The the cat") == "The cat"

    def test_remove_duplicate_uppercase(self):
        assert remove_repeated_words("THE THE CAT") == "THE CAT"

    def test_multiple_duplicates(self):
        assert remove_repeated_words("the the cat cat sat") == "the cat sat"

    def test_no_duplicates_unchanged(self):
        assert remove_repeated_words("the cat sat") == "the cat sat"

    def test_removes_valid_had_had(self):
        """Test that 'had had' is removed (known limitation)."""
        assert remove_repeated_words("I had had enough") == "I had enough"

    def test_removes_valid_that_that(self):
        """Test that 'that that' is removed (known limitation)."""
        assert remove_repeated_words("I know that that is true") == "I know that is true"

    def test_triple_word_removes_once(self):
        """Test that three consecutive words become two."""
        assert remove_repeated_words("go go go") == "go go"

    def test_word_boundary_required(self):
        """Test that duplicates need word boundaries."""
        # "isis" should not match "is is" within it
        assert remove_repeated_words("crisis") == "crisis"


class TestNormalizeLineBreaks:
    """Test suite for normalize_line_breaks."""

    def test_normalize_crlf_to_lf(self):
        assert normalize_line_breaks("hello\r\nworld") == "hello\nworld"

    def test_normalize_cr_to_lf(self):
        assert normalize_line_breaks("hello\rworld") == "hello\nworld"

    def test_lf_unchanged(self):
        assert normalize_line_breaks("hello\nworld") == "hello\nworld"

    def test_collapse_three_newlines_to_two(self):
        assert normalize_line_breaks("hello\n\n\nworld") == "hello\n\nworld"

    def test_collapse_many_newlines_to_two(self):
        assert normalize_line_breaks("hello\n\n\n\n\nworld") == "hello\n\nworld"

    def test_preserve_two_newlines(self):
        assert normalize_line_breaks("hello\n\nworld") == "hello\n\nworld"

    def test_preserve_single_newline(self):
        assert normalize_line_breaks("hello\nworld") == "hello\nworld"

    def test_mixed_line_breaks(self):
        assert normalize_line_breaks("hello\r\nworld\rtest\nok") == "hello\nworld\ntest\nok"


class TestRunPipeline:
    """Test suite for run_pipeline function."""

    def test_empty_pipeline(self):
        """Test that empty transform list returns original text."""
        assert run_pipeline("hello  world", []) == "hello  world"

    def test_single_transform(self):
        """Test pipeline with one transform."""
        result = run_pipeline("  hello  ", [trim_whitespace])
        assert result == "hello"

    def test_multiple_transforms(self):
        """Test pipeline with multiple transforms."""
        text = "  hello   world  "
        result = run_pipeline(text, [trim_whitespace, collapse_spaces])
        assert result == "hello world"

    def test_order_matters_trim_then_collapse(self):
        """Test that trim → collapse gives expected result."""
        text = "  hello   world  "
        result = run_pipeline(text, [trim_whitespace, collapse_spaces])
        assert result == "hello world"

    def test_order_matters_collapse_then_trim(self):
        """Test that collapse → trim gives same result (both work)."""
        text = "  hello   world  "
        result = run_pipeline(text, [collapse_spaces, trim_whitespace])
        assert result == "hello world"

    def test_order_changes_result_with_repeated_words(self):
        """Test that transform order can change the result."""
        # Use newlines to show order matters
        text = "the\nthe cat"

        # \s+ in regex matches newlines, so duplicates ARE removed
        result1 = run_pipeline(text, [normalize_line_breaks, remove_repeated_words])
        assert result1 == "the cat"

        # Replace newline with space first, then duplicates are removed
        def newline_to_space(t):
            return t.replace('\n', ' ')

        result2 = run_pipeline(text, [newline_to_space, remove_repeated_words])
        assert result2 == "the cat"

    def test_all_transforms_together(self):
        """Test all four transforms in a realistic pipeline."""
        text = "  hello\r\n\r\nthe  the   world  \n\n\n\nend  "
        result = run_pipeline(text, [
            normalize_line_breaks,
            trim_whitespace,
            collapse_spaces,
            remove_repeated_words
        ])
        # Note: trailing space after "world" is preserved (before newline)
        assert result == "hello\n\nthe world \n\nend"

    def test_realistic_text_cleanup(self):
        """Test realistic text cleanup scenario."""
        messy_text = """

        This  is  a   test  test  document.



        It has  extra   spaces.
        """

        result = run_pipeline(messy_text.strip(), [
            normalize_line_breaks,
            collapse_spaces,
            remove_repeated_words
        ])

        # Leading space before "It" is preserved (single space after newline)
        expected = "This is a test document.\n\n It has extra spaces."
        assert result == expected


class TestCapitalizationEdgeCases:
    """Test capitalization behavior (not implemented, documenting expected behavior)."""

    def test_pi_sentence(self):
        """Document expected behavior for 'pi is 3.14. next'."""
        # If we had capitalize_sentences, it should handle:
        # "pi is 3.14. next" -> "Pi is 3.14. Next"
        # The decimal point shouldn't be treated as sentence end
        text = "pi is 3.14. next"
        # No capitalize_sentences implemented, so unchanged
        result = run_pipeline(text, [])
        assert result == "pi is 3.14. next"

    def test_abbreviation_sentence(self):
        """Document expected behavior for 'e.g. this'."""
        # If we had capitalize_sentences, it should handle:
        # "e.g. this" -> "E.g. this" (abbreviation, not sentence end)
        text = "e.g. this"
        # No capitalize_sentences implemented, so unchanged
        result = run_pipeline(text, [])
        assert result == "e.g. this"
