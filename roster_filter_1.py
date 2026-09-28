# A class roster is a list of student `dict`s.

# Add a function that groups students into "needs attention" (grade below 70 OR 
# attendance below 0.8) and "on track" (everyone else) and returns both groups along 
# with each group's average grade. Handle an empty roster without crashing.

roster = [
    {"name": "Amara Singh", "grade": 91, "attendance": 0.95},
    {"name": "Liam Chen", "grade": 68, "attendance": 0.72},
    {"name": "Priya Nair", "grade": 84, "attendance": 0.88},
]

def average_grade(roster):
    return sum(s["grade"] for s in roster) / len(roster)
