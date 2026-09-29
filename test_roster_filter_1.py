# Tests for problem 1: roster filter
import pytest
from roster_filter_1 import group_students, average_grade


class TestGroupStudents:
    """Test suite for group_students function."""

    def test_empty_roster(self):
        """Test that empty roster doesn't crash and returns empty groups with None averages."""
        result = group_students([])
        assert result == {
            "needs_attention": [],
            "needs_attention_average": None,
            "on_track": [],
            "on_track_average": None
        }

    def test_all_need_attention(self):
        """Test when all students need attention - on_track group is empty."""
        roster = [
            {"name": "Student A", "grade": 65, "attendance": 0.75},
            {"name": "Student B", "grade": 50, "attendance": 0.70}
        ]
        result = group_students(roster)
        assert len(result["needs_attention"]) == 2
        assert len(result["on_track"]) == 0
        assert result["needs_attention_average"] == 57.5
        assert result["on_track_average"] is None

    def test_all_on_track(self):
        """Test when all students are on track - needs_attention group is empty."""
        roster = [
            {"name": "Student A", "grade": 85, "attendance": 0.90},
            {"name": "Student B", "grade": 90, "attendance": 0.95}
        ]
        result = group_students(roster)
        assert len(result["needs_attention"]) == 0
        assert len(result["on_track"]) == 2
        assert result["needs_attention_average"] is None
        assert result["on_track_average"] == 87.5

    def test_grade_70_is_on_track(self):
        """Test that grade exactly 70 with good attendance is on track."""
        roster = [{"name": "Student A", "grade": 70, "attendance": 0.90}]
        result = group_students(roster)
        assert len(result["on_track"]) == 1
        assert len(result["needs_attention"]) == 0
        assert result["on_track"][0]["name"] == "Student A"

    def test_attendance_0_8_is_on_track(self):
        """Test that attendance exactly 0.8 with good grade is on track."""
        roster = [{"name": "Student A", "grade": 80, "attendance": 0.8}]
        result = group_students(roster)
        assert len(result["on_track"]) == 1
        assert len(result["needs_attention"]) == 0
        assert result["on_track"][0]["name"] == "Student A"

    def test_grade_69_needs_attention(self):
        """Test that grade 69 needs attention even with perfect attendance."""
        roster = [{"name": "Student A", "grade": 69, "attendance": 1.0}]
        result = group_students(roster)
        assert len(result["needs_attention"]) == 1
        assert len(result["on_track"]) == 0
        assert result["needs_attention"][0]["name"] == "Student A"

    def test_attendance_0_79_needs_attention(self):
        """Test that attendance 0.79 needs attention even with perfect grade."""
        roster = [{"name": "Student A", "grade": 100, "attendance": 0.79}]
        result = group_students(roster)
        assert len(result["needs_attention"]) == 1
        assert len(result["on_track"]) == 0
        assert result["needs_attention"][0]["name"] == "Student A"

    def test_low_grade_only(self):
        """Test student needs attention due to low grade only."""
        roster = [{"name": "Student A", "grade": 60, "attendance": 0.95}]
        result = group_students(roster)
        assert len(result["needs_attention"]) == 1
        assert result["needs_attention"][0]["name"] == "Student A"

    def test_low_attendance_only(self):
        """Test student needs attention due to low attendance only."""
        roster = [{"name": "Student A", "grade": 90, "attendance": 0.70}]
        result = group_students(roster)
        assert len(result["needs_attention"]) == 1
        assert result["needs_attention"][0]["name"] == "Student A"

    def test_both_low_grade_and_attendance(self):
        """Test student needs attention when both grade and attendance are low."""
        roster = [{"name": "Student A", "grade": 65, "attendance": 0.75}]
        result = group_students(roster)
        assert len(result["needs_attention"]) == 1
        assert result["needs_attention"][0]["name"] == "Student A"

    def test_mixed_roster(self):
        """Test roster with both groups populated."""
        roster = [
            {"name": "Amara Singh", "grade": 91, "attendance": 0.95},
            {"name": "Liam Chen", "grade": 68, "attendance": 0.72},
            {"name": "Priya Nair", "grade": 84, "attendance": 0.88},
        ]
        result = group_students(roster)

        assert len(result["needs_attention"]) == 1
        assert len(result["on_track"]) == 2

        assert result["needs_attention"][0]["name"] == "Liam Chen"
        assert result["on_track"][0]["name"] == "Amara Singh"
        assert result["on_track"][1]["name"] == "Priya Nair"

        assert result["needs_attention_average"] == 68
        assert result["on_track_average"] == 87.5

    def test_averages_are_floats(self):
        """Test that averages are computed as floats."""
        roster = [
            {"name": "Student A", "grade": 85, "attendance": 0.90},
            {"name": "Student B", "grade": 90, "attendance": 0.95}
        ]
        result = group_students(roster)
        assert isinstance(result["on_track_average"], (int, float))
        assert result["on_track_average"] == 87.5


class TestAverageGrade:
    """Test that average_grade function is not modified."""

    def test_average_grade_unchanged(self):
        """Verify average_grade still works as before."""
        roster = [
            {"name": "Amara Singh", "grade": 91, "attendance": 0.95},
            {"name": "Liam Chen", "grade": 68, "attendance": 0.72},
            {"name": "Priya Nair", "grade": 84, "attendance": 0.88},
        ]
        assert average_grade(roster) == (91 + 68 + 84) / 3
