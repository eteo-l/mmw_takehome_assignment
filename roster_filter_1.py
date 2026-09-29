# A class roster is a list of student `dict`s.

# Add a function that groups students into "needs attention" (grade below 70 OR
# attendance below 0.8) and "on track" (everyone else) and returns both groups along
# with each group's average grade. Handle an empty roster without crashing.

from typing import Any

roster = [
    {"name": "Amara Singh", "grade": 91, "attendance": 0.95},
    {"name": "Liam Chen", "grade": 68, "attendance": 0.72},
    {"name": "Priya Nair", "grade": 84, "attendance": 0.88},
]

def average_grade(roster):
    return sum(s["grade"] for s in roster) / len(roster)

def group_students(roster: list[dict[str, Any]]) -> dict[str, Any]:
    needs_attention = []
    on_track = []

    for student in roster:
        if student["grade"] < 70 or student["attendance"] < 0.8:
            needs_attention.append(student)
        else:
            on_track.append(student)

    return {
        "needs_attention": needs_attention,
        "needs_attention_average": average_grade(needs_attention) if needs_attention else None,
        "on_track": on_track,
        "on_track_average": average_grade(on_track) if on_track else None
    }
