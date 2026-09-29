# Tests for problem 2: grade converter
import pytest
import math
from grade_converter_2 import letter_grade


class TestLetterGradeNormalValues:
    """Test letter_grade with typical valid inputs."""

    def test_grade_a_95(self):
        """Test that 95 returns A."""
        assert letter_grade(95) == "A"

    def test_grade_b_85(self):
        """Test that 85 returns B."""
        assert letter_grade(85) == "B"

    def test_grade_c_75(self):
        """Test that 75 returns C."""
        assert letter_grade(75) == "C"

    def test_grade_d_65(self):
        """Test that 65 returns D."""
        assert letter_grade(65) == "D"

    def test_grade_f_50(self):
        """Test that 50 returns F."""
        assert letter_grade(50) == "F"

    def test_grade_f_0(self):
        """Test that 0 returns F."""
        assert letter_grade(0) == "F"


class TestLetterGradeExactBoundaries:
    """Test letter_grade at exact grade boundaries."""

    def test_grade_90_is_a(self):
        """Test that exactly 90 returns A."""
        assert letter_grade(90) == "A"

    def test_grade_89_99_is_b(self):
        """Test that 89.99 returns B."""
        assert letter_grade(89.99) == "B"

    def test_grade_80_is_b(self):
        """Test that exactly 80 returns B."""
        assert letter_grade(80) == "B"

    def test_grade_79_99_is_c(self):
        """Test that 79.99 returns C."""
        assert letter_grade(79.99) == "C"

    def test_grade_70_is_c(self):
        """Test that exactly 70 returns C."""
        assert letter_grade(70) == "C"

    def test_grade_69_99_is_d(self):
        """Test that 69.99 returns D."""
        assert letter_grade(69.99) == "D"

    def test_grade_60_is_d(self):
        """Test that exactly 60 returns D."""
        assert letter_grade(60) == "D"

    def test_grade_59_99_is_f(self):
        """Test that 59.99 returns F."""
        assert letter_grade(59.99) == "F"


class TestLetterGradeEdgeCases:
    """Test letter_grade with edge cases and invalid inputs."""

    def test_negative_score(self):
        """Test that negative score returns F."""
        assert letter_grade(-10) == "F"

    def test_score_over_100(self):
        """Test that score over 100 returns A."""
        assert letter_grade(105) == "A"

    def test_score_exactly_100(self):
        """Test that exactly 100 returns A."""
        assert letter_grade(100) == "A"

    def test_nan_score(self):
        """Test behavior with NaN score."""
        result = letter_grade(float('nan'))
        # NaN comparisons always return False, so it will fall through to else
        assert result == "F"

    def test_infinity_score(self):
        """Test behavior with positive infinity."""
        assert letter_grade(float('inf')) == "A"

    def test_negative_infinity_score(self):
        """Test behavior with negative infinity."""
        assert letter_grade(float('-inf')) == "F"

    def test_string_score_raises_error(self):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            letter_grade("85")

    def test_none_score_raises_error(self):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            letter_grade(None)
