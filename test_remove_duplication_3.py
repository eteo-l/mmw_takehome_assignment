# Tests for problem 3: remove duplication
import pytest
from remove_duplication_3 import import_teacher_row, import_student_row


class TestImportTeacherRow:
    """Test suite for import_teacher_row to pin down current behavior."""

    def test_valid_teacher_row(self):
        """Test importing a valid teacher row."""
        row = ["John Doe", "john.doe@example.com"]
        result = import_teacher_row(row)
        assert result == {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "role": "teacher"
        }

    def test_teacher_name_with_whitespace(self):
        """Test that names are stripped of leading/trailing whitespace."""
        row = ["  Jane Smith  ", "jane@example.com"]
        result = import_teacher_row(row)
        assert result["name"] == "Jane Smith"

    def test_teacher_email_with_whitespace(self):
        """Test that emails are stripped of leading/trailing whitespace."""
        row = ["Bob Jones", "  bob@example.com  "]
        result = import_teacher_row(row)
        assert result["email"] == "bob@example.com"

    def test_teacher_email_lowercased(self):
        """Test that emails are converted to lowercase."""
        row = ["Alice Brown", "ALICE@EXAMPLE.COM"]
        result = import_teacher_row(row)
        assert result["email"] == "alice@example.com"

    def test_teacher_email_mixed_case_lowercased(self):
        """Test that mixed case emails are converted to lowercase."""
        row = ["Tom Wilson", "Tom.Wilson@Example.Com"]
        result = import_teacher_row(row)
        assert result["email"] == "tom.wilson@example.com"

    def test_teacher_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        row = ["", "email@example.com"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_teacher_row(row)

    def test_teacher_whitespace_only_name_raises_error(self):
        """Test that whitespace-only name raises ValueError."""
        row = ["   ", "email@example.com"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_teacher_row(row)

    def test_teacher_empty_email_raises_error(self):
        """Test that empty email raises ValueError."""
        row = ["John Doe", ""]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_teacher_row(row)

    def test_teacher_whitespace_only_email_raises_error(self):
        """Test that whitespace-only email raises ValueError."""
        row = ["John Doe", "   "]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_teacher_row(row)

    def test_teacher_both_empty_raises_error(self):
        """Test that both empty name and email raises ValueError."""
        row = ["", ""]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_teacher_row(row)

    def test_teacher_missing_column_raises_index_error(self):
        """Test that row with only one column raises IndexError."""
        row = ["John Doe"]
        with pytest.raises(IndexError):
            import_teacher_row(row)

    def test_teacher_empty_row_raises_index_error(self):
        """Test that empty row raises IndexError."""
        row = []
        with pytest.raises(IndexError):
            import_teacher_row(row)

    def test_teacher_none_name_raises_attribute_error(self):
        """Test that None name raises AttributeError."""
        row = [None, "email@example.com"]
        with pytest.raises(AttributeError):
            import_teacher_row(row)

    def test_teacher_none_email_raises_attribute_error(self):
        """Test that None email raises AttributeError."""
        row = ["John Doe", None]
        with pytest.raises(AttributeError):
            import_teacher_row(row)


class TestImportStudentRow:
    """Test suite for import_student_row to pin down current behavior."""

    def test_valid_student_row(self):
        """Test importing a valid student row."""
        row = ["Emily Davis", "emily.davis@example.com", "10"]
        result = import_student_row(row)
        assert result == {
            "name": "Emily Davis",
            "email": "emily.davis@example.com",
            "role": "student",
            "grade_level": "10"
        }

    def test_student_name_with_whitespace(self):
        """Test that names are stripped of leading/trailing whitespace."""
        row = ["  Michael Lee  ", "michael@example.com", "9"]
        result = import_student_row(row)
        assert result["name"] == "Michael Lee"

    def test_student_email_with_whitespace(self):
        """Test that emails are stripped of leading/trailing whitespace."""
        row = ["Sarah Kim", "  sarah@example.com  ", "11"]
        result = import_student_row(row)
        assert result["email"] == "sarah@example.com"

    def test_student_email_lowercased(self):
        """Test that emails are converted to lowercase."""
        row = ["David Park", "DAVID@EXAMPLE.COM", "12"]
        result = import_student_row(row)
        assert result["email"] == "david@example.com"

    def test_student_email_mixed_case_lowercased(self):
        """Test that mixed case emails are converted to lowercase."""
        row = ["Lisa Wang", "Lisa.Wang@Example.Com", "10"]
        result = import_student_row(row)
        assert result["email"] == "lisa.wang@example.com"

    def test_student_grade_level_not_stripped(self):
        """Test that grade_level is stored as-is from row[2] without stripping."""
        row = ["Chris Taylor", "chris@example.com", " 9 "]
        result = import_student_row(row)
        assert result["grade_level"] == " 9 "

    def test_student_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        row = ["", "email@example.com", "10"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_student_row(row)

    def test_student_whitespace_only_name_raises_error(self):
        """Test that whitespace-only name raises ValueError."""
        row = ["   ", "email@example.com", "11"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_student_row(row)

    def test_student_empty_email_raises_error(self):
        """Test that empty email raises ValueError."""
        row = ["John Doe", "", "12"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_student_row(row)

    def test_student_whitespace_only_email_raises_error(self):
        """Test that whitespace-only email raises ValueError."""
        row = ["John Doe", "   ", "9"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_student_row(row)

    def test_student_both_empty_raises_error(self):
        """Test that both empty name and email raises ValueError."""
        row = ["", "", "10"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_student_row(row)

    def test_student_two_column_empty_name_raises_value_error(self):
        """Test that validation happens before accessing row[2]."""
        row = ["", "a@x.com"]
        with pytest.raises(ValueError, match="^missing required field$"):
            import_student_row(row)

    def test_student_missing_column_raises_index_error(self):
        """Test that row with only one column raises IndexError."""
        row = ["Ada"]
        with pytest.raises(IndexError):
            import_student_row(row)

    def test_student_empty_row_raises_index_error(self):
        """Test that empty row raises IndexError."""
        row = []
        with pytest.raises(IndexError):
            import_student_row(row)

    def test_student_none_name_raises_attribute_error(self):
        """Test that None name raises AttributeError."""
        row = [None, "a@x.com", "10"]
        with pytest.raises(AttributeError):
            import_student_row(row)

    def test_student_none_email_raises_attribute_error(self):
        """Test that None email raises AttributeError."""
        row = ["John Doe", None, "10"]
        with pytest.raises(AttributeError):
            import_student_row(row)

    def test_student_valid_two_columns_raises_index_error(self):
        """Test that valid name/email but only two columns raises IndexError."""
        row = ["Anna Johnson", "anna@example.com"]
        with pytest.raises(IndexError):
            import_student_row(row)
