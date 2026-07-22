import streamlit as st
import google.generativeai as genai


# ---------------------------------
# Configure Gemini
# ---------------------------------
def configure_gemini():
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash-lite")

# ---------------------------------
# Study Plan Generator
# ---------------------------------
def generate_study_plan(
    model,
    student_name,
    student_class,
    board,
    subjects,
    weak_subjects,
    study_hours,
    exam_date,
    goal
):

    prompt = f"""
You are an expert AI Study Planner.

Create a 7-day study plan.

Student Name: {student_name}
Class: {student_class}
Board: {board}
Subjects: {subjects}
Weak Subjects: {weak_subjects}
Daily Study Hours: {study_hours}
Exam Date: {exam_date}
Goal: {goal}

Return ONLY a markdown table.

Columns:

| Day | Subject | Topic | Hours |

Do not explain anything.
"""

    response = model.generate_content(prompt)

    return response.text


# ---------------------------------
# Motivation Generator
# ---------------------------------
def generate_motivation(model, goal):

    prompt = f"""
Give one short motivational quote for a student whose goal is:

{goal}

Keep it under 40 words.
"""

    response = model.generate_content(prompt)

    return response.text
# ---------------------------------
# Smart Timetable Generator
# ---------------------------------
def generate_smart_timetable(
    model,
    school_hours,
    tuition_hours,
    study_hours,
    sleep_hours,
    meal_times,
    weak_subjects
):

    prompt = f"""
Create a weekly smart timetable.

Details:
- School Hours: {school_hours}
- Tuition Hours: {tuition_hours}
- Daily Study Hours: {study_hours}
- Sleep Hours: {sleep_hours}
- Meal Times: {meal_times}
- Weak Subjects: {weak_subjects}

Return ONLY a markdown table.

Columns:

| Time | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |

Rules:
- Include breaks.
- Balance all subjects.
- Give extra time for weak subjects.
- Include revision sessions.
- Keep Sunday lighter with revision.
"""

    response = model.generate_content(prompt)

    return response.text


# ---------------------------------
# Subject Priority Analyzer
# ---------------------------------
def analyze_subject_priority(
    model,
    subjects,
    weak_subjects,
    goal
):

    prompt = f"""
You are an AI Study Advisor.

Subjects:
{subjects}

Weak Subjects:
{weak_subjects}

Goal:
{goal}

Rank every subject as:

High
Medium
Low

Return ONLY a markdown table.

Columns:

| Subject | Priority | Reason |
"""

    response = model.generate_content(prompt)

    return response.text


# ---------------------------------
# Study Session Planner
# ---------------------------------
def generate_study_session(
    model,
    subject,
    available_hours
):

    prompt = f"""
Create a study session for:

Subject:
{subject}

Available Hours:
{available_hours}

Split the session into:

- Learning
- Practice
- Revision
- Short Breaks

Return ONLY a markdown table.

Columns:

| Time | Activity |
"""

    response = model.generate_content(prompt)

    return response.text
# ---------------------------------
# AI Quiz Generator
# ---------------------------------
def generate_quiz(
    model,
    subject,
    student_class,
    difficulty
):

    prompt = f"""
Generate exactly 15 multiple-choice questions.

Subject: {subject}
Class: {student_class}
Difficulty: {difficulty}

Rules:
- Exactly 15 questions
- 4 options (A, B, C, D)
- Mention the correct answer after each question
- Return in Markdown format
"""

    response = model.generate_content(prompt)

    return response.text


# ---------------------------------
# Progress Tracker
# ---------------------------------
def generate_progress(completed_topics, total_topics):

    if total_topics == 0:
        return 0

    percentage = (completed_topics / total_topics) * 100

    return round(percentage, 2)


# ---------------------------------
# AI Motivation Generator
# ---------------------------------
def generate_daily_motivation(model):

    prompt = """
Generate one short motivational quote for students.

Maximum 30 words.
"""

    response = model.generate_content(prompt)

    return response.text


# ---------------------------------
# AI Study Assistant
# ---------------------------------
def ask_ai(model, question):

    response = model.generate_content(question)

    return response.text


# ---------------------------------
# Study Notifications
# ---------------------------------
def study_notification():

    return "⏰ Time to study! Stay focused and achieve your goal."


# ---------------------------------
# Pomodoro Timer
# ---------------------------------
def pomodoro_timer():

    return {
        "Study": 25,
        "Short Break": 5,
        "Long Break": 15
    }
