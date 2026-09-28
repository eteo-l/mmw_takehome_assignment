# MMW Co-op Take-Home Assignment

Thank you for your interest in a co-op term with Mark My Work.

Please complete this take-home assignment and submit it the day before your interview, at the latest.  It consists of several problems to be solved with AI assistance.  

# Submission Guidelines

## How to Complete the Assignment
- Use any AI assistance you wish
- For problems that ask you to correct existing code: your solutions should be in Python
- For problems that ask you to write code from scratch: use any language you like
- Time-box your work to 45 minutes; if you don't finish all the problems, that's OK: just explain what happened

## What to Submit
1. Your final code
2. A short write-up (bullet points are fine) covering:
   1. The prompts you used, roughly, and how many iterations it took -- or: the actual raw session.
   1. What AI got wrong, missed, or handled poorly, and how you caught it
   1. Anything you changed by hand after the AI's output
   1. Additional notes specific to each problem.
3. How long you actually spent on the assignment

## How to Submit your Responses
- Create a GitHub repo (or repos) to store your responses.
- Share the repo(s) with us.

## Suggestions

Here are some suggestions:
- Read all the problems first; that may help you prioritize your work
- Exporting and sharing the raw AI sessions may be easier and faster than tracking or recreating your AI prompts and your thinking.  Give some thought about how to submit your AI interactions before you begin.
- We are looking for:
  - How well you can direct an AI coding tool and judge its output -- not whether you can write the solution unaided
  - Whether you can judge a good design from bad

# Problems

## Problem: "Add a roster filter"

A class roster is a list of student `dict`s.

```python
roster = [
    {"name": "Amara Singh", "grade": 91, "attendance": 0.95},
    {"name": "Liam Chen", "grade": 68, "attendance": 0.72},
    {"name": "Priya Nair", "grade": 84, "attendance": 0.88},
]

def average_grade(roster):
    return sum(s["grade"] for s in roster) / len(roster)
```

### Task

Add a function that groups students into "needs attention" (grade below 70 OR attendance below 0.8) and "on track" (everyone else) and returns both groups along with each group's average grade. Handle an empty roster without crashing.

## Problem: "Write tests for the grade converter"

This function has no tests.

```python
def letter_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
```

### Task

Write a test suite for it.  If you find a real bug either fix it or defer it (explain your decisions in the write-up).

## Problem: "Remove the duplication"

Two functions import roster data from CSV rows, one for teachers and one for students. They're nearly identical.

```python
def import_teacher_row(row):
    name = row[0].strip()
    email = row[1].strip().lower()
    if not name or not email:
        raise ValueError("missing required field")
    return {"name": name, "email": email, "role": "teacher"}

def import_student_row(row):
    name = row[0].strip()
    email = row[1].strip().lower()
    if not name or not email:
        raise ValueError("missing required field")
    return {"name": name, "email": email, "role": "student", "grade_level": row[2]}
```

### Tasks

Refactor to remove the duplication without changing the behavior of either function (including the error case).

Add a third importer, for administrators (no `grade_level`, otherwise identical to teacher), using whatever structure your refactor produces.

## Problem: "Design a rate limiter"

Design and implement an in-memory rate limiter with one method, `allow(client_id) -> bool`, returning whether a request from that client is allowed under a limit of N requests per rolling W-second window. Assume a single process -- no distributed or multi-server concerns.

### Task

Build it, then structure it so a second limiting strategy (for example, a fixed window instead of a rolling one) could be added later without changing how callers use `allow()`. You don't need to implement the second strategy -- but explain in your write-up how a second strategy would plug in.

## Problem: "Design a text-transform pipeline"

Build a pipeline that runs a sequence of text transformations over an input string.  Some examples might be: trim whitespace, collapse repeated spaces, capitalize the first letter of each sentence.  But be creative: supply your own!

### Task

Implement at least three transformations of your choice.
