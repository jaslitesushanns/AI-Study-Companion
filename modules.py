from utils import ask_gemini


# 1. Study Plan Generator

def generate_study_plan(
    model,
    student_name,
    student_class,
    board,
    percentage,
    study_hours,
    goal,
    weak_subjects
):

    prompt = f"""
Create a 7 day study plan.

Student Name: {student_name}
Class: {student_class}
Board: {board}
Percentage: {percentage}
Available Study Hours: {study_hours}
Goal: {goal}
Weak Subjects: {weak_subjects}

Return ONLY a markdown table.

Columns:
| Day | Subject | Topic | Hours |

Do not write explanations.
"""

    return ask_gemini(model, prompt)



# 2. Smart Timetable Generator

def generate_smart_timetable(
    model,
    student_class,
    study_hours,
    weak_subjects
):

    prompt = f"""
Create a weekly smart timetable.

Class: {student_class}
Study Hours: {study_hours}
Weak Subjects: {weak_subjects}

Include:
- Subjects
- Breaks
- Revision
- Weak subject priority

Return ONLY markdown table.

Columns:
| Time | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
"""

    return ask_gemini(model, prompt)



# 3. Subject Priority Analyzer

def analyze_subject_priority(
    model,
    percentage,
    weak_subjects,
    goal
):

    prompt = f"""
Analyze student's subject priorities.

Percentage: {percentage}
Weak Subjects: {weak_subjects}
Goal: {goal}

Return:
| Subject | Priority | Reason |
Only table format.
"""

    return ask_gemini(model, prompt)



# 4. Study Session Planner

def generate_study_session(
    model,
    study_hours
):

    prompt = f"""
Create a focused study session.

Available time:
{study_hours}

Include:
- Study time
- Break time
- Revision

Return table format.
"""

    return ask_gemini(model, prompt)



# 5. AI Quiz Generator

def generate_quiz(
    model,
    subject,
    student_class
):

    prompt = f"""
Generate a quiz.

Subject:
{subject}

Class:
{student_class}

Create 10 questions with options.

Format:

Question |
A |
B |
C |
D |
Answer |
"""

    return ask_gemini(model, prompt)



# 6. Progress Tracker

def generate_progress(
    model,
    completed_topics,
    total_topics
):

    prompt = f"""
Calculate learning progress.

Completed Topics:
{completed_topics}

Total Topics:
{total_topics}

Give percentage and suggestions.
"""

    return ask_gemini(model, prompt)



# 7. Motivation Generator

def generate_motivation(
    model,
    goal
):

    prompt = f"""
Generate motivation message.

Student Goal:
{goal}

Make it inspiring.
"""

    return ask_gemini(model, prompt)



# 8. AI Study Assistant

def ask_ai(
    model,
    question
):

    prompt = f"""
You are an AI Study Assistant.

Answer this student question:

{question}

Explain clearly.
"""

    return ask_gemini(model, prompt)



# Study Notifications

def study_notifications():

    return """
📚 Study Reminder

Stay consistent!
Complete your daily goals and keep learning.
"""
