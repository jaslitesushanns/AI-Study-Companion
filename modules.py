import google.generativeai as genai
import streamlit as st
import os

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
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

    prompt = f"""
You are an expert AI Study Planner.

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

Exam Date:
{exam_date}

Available Study Hours:
{study_hours} hour(s) per day.

Create a detailed study plan.

Include:

1. Daily timetable.
2. Which chapter to study each day.
3. Revision days.
4. Practice test days.
5. Break timings.
6. Motivation for each day.
7. Important tips.

Return the answer as a neat markdown table.
"""

    return ask_gemini(prompt)

# ---------------- TIMETABLE ---------------- #

def generate_timetable(study_hours, weak_subjects):
    prompt = f"""
Create a weekly timetable.

Study Hours:
{study_hours}

Weak Subjects:
{weak_subjects}

Return ONLY a markdown table.
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
    exam_date,
    goal
):

    prompt = f"""
You are an AI Study Planner.

Subjects:
{subjects}

Weak Subjects:
{weak_subjects}

Exam Date:
{exam_date}

Goal:
{goal}

Analyze:

1. Which subject should be studied first.
2. Priority ranking.
3. Time allocation.
4. Daily revision plan.
5. Tips to improve weak subjects.

Return the answer as a neat markdown table.
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
