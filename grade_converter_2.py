# Write a test suite for it.  If you find a real bug either fix it or defer it 
# (explain your decisions in the write-up).

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
