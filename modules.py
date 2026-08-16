import google.generativeai as genai
import streamlit as st
import os

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.6-flash")
else:
    model = None
# ---------------- COMMON FUNCTION ---------------- #

def ask_gemini(prompt):

    try:

        if model is None:
            return "❌ Gemini API key not found."

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI Error: {e}"

# ---------------- AI TUTOR ---------------- #

def ask_ai(
    subject,
    chapter,
    question,
    explain
):

    prompt = f"""
You are an expert AI Tutor.

Subject:
{subject}

Chapter:
{chapter}

Student Question:
{question}

Explain in:
{explain} mode.

Include:

1. Simple explanation
2. Real-life example
3. Important points
4. Exam tips
5. Quick revision notes

Use simple English.
"""

    return ask_gemini(prompt)


# ---------------- STUDY PLAN ---------------- #

from datetime import date


def generate_study_plan(
    subject,
    chapters,
    exam_date,
    study_hours,
    difficulty,
    goal,
    weak_subjects,
    student_class,
    board
):

    today = date.today()

    if hasattr(exam_date, "date"):
        exam_date = exam_date.date()

    days_remaining = (exam_date - today).days

    if days_remaining < 0:
        days_remaining = 0

    prompt = f"""
You are an expert AI Study Planner.

IMPORTANT DATE RULES:

Today's date:
{today}

Actual examination date:
{exam_date}

Number of days remaining:
{days_remaining}

You MUST use the exact examination date provided above.
Do NOT assume a different examination date.
Do NOT invent an examination date.
Do NOT create study days after the examination date.

Student Details:

Class:
{student_class}

Board:
{board}

Goal:
{goal}

Subject:
{subject}

Chapters:
{chapters}

Weak Subjects:
{weak_subjects}

Difficulty:
{difficulty}

Available Study Hours:
{study_hours} hour(s) per day.

Create a detailed study plan that fits within the exact number of days remaining before the examination.

Include:

1. Daily timetable.
2. Which chapter to study each day.
3. Revision days.
4. Practice test days.
5. Break timings.
6. Motivation for each day.
7. Important tips.

Make sure the final study/revision day is before the examination date.

Return the answer as a neat markdown table.
"""

    return ask_gemini(prompt)


# ---------------- STUDY SESSION ---------------- #

def generate_study_session(
    subject,
    chapter,
    study_hours,
    energy,
    goal
):

    prompt = f"""
You are an AI Study Coach.

Create a detailed study session.

Subject:
{subject}

Chapter:
{chapter}

Study Time:
{study_hours} hour(s)

Energy Level:
{energy}

Today's Goal:
{goal}

Include:

1. Warm-up (5 minutes)
2. Main Study Session
3. Practice Questions
4. Short Breaks
5. Revision
6. Self Test
7. Motivation

Return as a neat markdown table.
"""

    return ask_gemini(prompt)


# ---------------- SUBJECT PRIORITY ---------------- #

def analyze_subject_priority(
    subjects,
    weak_subjects,
    subject_exam_dates,
    goal
):

    prompt = f"""
You are an AI Study Planner.

The student has the following subjects:

{subjects}

Weak Subjects:
{weak_subjects}

Exam dates for each subject:

{subject_exam_dates}

Goal:
{goal}

Analyze the student's subjects and create an intelligent priority ranking.

For each subject, consider:

1. How soon its examination is.
2. Whether it is a weak subject.
3. The amount of preparation required.
4. The student's available preparation time.
5. The urgency of the examination.

Give higher priority to subjects with earlier examination dates
and subjects that are weak or require more preparation.

Return the result as a neat markdown table with:

| Subject | Exam Date | Priority | Reason | Recommended Study Time |

Do not invent examination dates.
Use the exact examination dates provided by the student.
"""

    return ask_gemini(prompt)

# ---------------- NOTES ---------------- #
def generate_notes(
    subject,
    chapter,
    notes_type
):

    prompt = f"""
Create {notes_type} for the student.

Subject:
{subject}

Chapter:
{chapter}

Include:

1. Definition
2. Important concepts
3. Key formulas (if any)
4. Examples
5. Memory tricks
6. 5-mark exam answer
7. Quick revision summary

Use simple student-friendly English.
"""

    return ask_gemini(prompt)


# ---------------- FLASHCARDS ---------------- #

def generate_flashcards(
    subject,
    chapter,
    cards
):

    prompt = f"""
You are an AI Flashcard Generator.

Subject:
{subject}

Chapter:
{chapter}

Create {cards} flashcards.

Each flashcard must contain:

Question:
Answer:

Keep them short, simple and exam-friendly.
"""

    return ask_gemini(prompt)

# ---------------- STORY LEARNING ---------------- #

def generate_story(topic):
    prompt = f"""
    Explain

    {topic}

    using an interesting story for students.
    """
    return ask_gemini(prompt)


# ---------------- QUIZ ---------------- #

def generate_quiz(
    subject,
    chapter,
    difficulty,
    questions
):

    prompt = f"""
You are an AI Quiz Generator.

Subject:
{subject}

Chapter:
{chapter}

Difficulty:
{difficulty}

Generate {questions} multiple choice questions.

Each question should contain:

Question

A)

B)

C)

D)

Correct Answer

Explanation

Keep the questions suitable for students.
"""

    return ask_gemini(prompt)

# ---------------- EXAM ---------------- #
def generate_exam(
    subject,
    chapter,
    duration,
    marks,
    difficulty
):

    prompt = f"""
You are an AI Exam Paper Generator.

Subject:
{subject}

Chapter:
{chapter}

Difficulty:
{difficulty}

Duration:
{duration} minutes

Total Marks:
{marks}

Create a complete exam paper.

Include:

1. Multiple Choice Questions
2. Short Answer Questions
3. Long Answer Questions
4. Total Marks
5. Time Required
6. Answer Key at the end

Return the paper in neat markdown format.
"""

    return ask_gemini(prompt)

# ---------------- MEMORY BOOSTER ---------------- #

def memory_booster(
    subject,
    chapter,
    game
):

    prompt = f"""
You are an AI Educational Game Creator.

Subject:
{subject}

Chapter:
{chapter}

Game Type:
{game}

Create an interactive learning game.

Include:

1. Instructions
2. Questions
3. Answers
4. Score System
5. Bonus Challenge

Keep it fun and suitable for students.
"""

    return ask_gemini(prompt)

# ---------------- PROGRESS ANALYSIS ---------------- #

def analyze_progress(
    subject,
    completed,
    total,
    hours
):

    prompt = f"""
You are an AI Study Progress Analyzer.

Subject:
{subject}

Completed Topics:
{completed}

Total Topics:
{total}

Study Hours:
{hours}

Analyze:

1. Progress Percentage
2. Strong Areas
3. Weak Areas
4. Suggestions
5. Weekly Goal
6. Motivation

Return the result in markdown.
"""

    return ask_gemini(prompt)


# ---------------- REPORT GENERATOR ---------------- #
def generate_report(
    subject,
    completed,
    total
):

    prompt = f"""
Create a professional student report.

Subject:
{subject}

Completed Topics:
{completed}

Total Topics:
{total}

Include:

1. Percentage
2. Performance
3. Strengths
4. Weaknesses
5. Suggestions
6. Motivation

Return in markdown.
"""

    return ask_gemini(prompt)
def ai_agent(
    subject,
    chapter,
    mood,
    question,
    goal,
    weak_subjects
):

    prompt = f"""
You are an intelligent AI Study Companion.

Student Goal:
{goal}

Weak Subjects:
{weak_subjects}

Current Mood:
{mood}

Subject:
{subject}

Chapter:
{chapter}

Question:
{question}

Your job is to:

1. Answer the student's question.
2. Explain in simple language.
3. Give study tips.
4. Suggest today's study plan.
5. Encourage the student.
6. Recommend revision strategy.
7. Mention common mistakes to avoid.

Return the response in beautiful markdown.
"""

    return ask_gemini(prompt)

# ---------------- SMART TIMETABLE ---------------- #

# ---------------- SMART TIMETABLE ---------------- #

def generate_timetable(
    study_hours,
    subjects,
    weak_subjects,
    subject_exam_dates
):

    prompt = f"""
You are an expert AI Smart Timetable Planner.

IMPORTANT RULES:

1. Use ONLY the subjects provided by the student.
2. Do NOT invent, add, or assume any other subjects.
3. Use the exact examination dates provided.
4. Give higher priority to subjects with earlier examination dates.
5. Give extra attention to weak subjects.
6. Balance the timetable according to the available study hours.

Subjects the student is studying:
{subjects}

Weak Subjects:
{weak_subjects}

Exam Dates for Each Subject:
{subject_exam_dates}

Available Study Hours:
{study_hours} hour(s) per day.

Create a balanced weekly study timetable.

The timetable should:

1. Use only the student's actual subjects.
2. Give more study time to weak subjects.
3. Give higher priority to subjects with earlier examination dates.
4. Distribute the remaining subjects fairly.
5. Include revision time.
6. Include practice/question-solving time.
7. Include short breaks.
8. Avoid overloading the student.
9. Keep the timetable realistic and student-friendly.
10. Consider both examination urgency and subject weakness when allocating study time.

Return ONLY a neat markdown table with:

| Time | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
"""

    return ask_gemini(prompt)
