# MMW Co-op Take-Home

## How I used AI

I used Claude Code in VS Code to write and run the code, and a separate Claude chat to occasionally review its output to double check and save time. 

## Time

About 50 minutes, I started with Problem 3 and was careful with it: tests to pin down the original behavior first, then filling the gaps in those tests, then the refactor. I also tried to make the commit history show that process. Then I found out that it took almost half the session, so I got panicked and moved faster afterwards. Therefore some mistakes were made during the later half of the session. I didn't make a decision on the Problem 2 bugs.

## What the AI got wrong, and how I caught it

- **Problem 3:** In the AI's first tests, every student error case had three columns, so a refactor that read `row[2]` before validating would still pass. I added `["", "a@x.com"]`, which must raise `ValueError`, not `IndexError`. I also found that the test named "not stripped" used `"9"`, which has no whitespace, so it tested nothing; that error messages were checked with a regex search instead of an exact match; and that there were no `IndexError` or `AttributeError` cases. After the refactor, it picked `"administrator"` as the role without asking and left out type hints. Both broke the rules I set at the start, and it acknowledged both.
- **Problem 1:** The AI re-implemented the average instead of reusing the existing `average_grade`. I had it call `average_grade` only for non-empty groups.
- **Problem 2:** The AI said there were no real bugs because the function works for inputs from 0 to 100. The function doesn't restrict inputs to that range; the AI assumed it. I disagree that NaN returning "F" is just an unclear requirement. 


## Changes by hand

None. Every change was a new instruction to the AI, which I then checked by reading the code and the test output.
