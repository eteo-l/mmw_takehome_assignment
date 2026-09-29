# Two functions import roster data from CSV rows, one for teachers and one
# for students. They're nearly identical.

# Refactor to remove the duplication without changing the behavior of either function
# (including the error case).

# Add a third importer, for administrators (no `grade_level`, otherwise identical to
# teacher), using whatever structure your refactor produces.

from typing import Sequence

def _import_row_base(row: Sequence[str], role: str) -> dict[str, str]:
    name = row[0].strip()
    email = row[1].strip().lower()
    if not name or not email:
        raise ValueError("missing required field")
    return {"name": name, "email": email, "role": role}

def import_teacher_row(row: Sequence[str]) -> dict[str, str]:
    return _import_row_base(row, "teacher")

def import_student_row(row: Sequence[str]) -> dict[str, str]:
    result = _import_row_base(row, "student")
    result["grade_level"] = row[2]
    return result

def import_administrator_row(row: Sequence[str]) -> dict[str, str]:
    return _import_row_base(row, "administrator")
