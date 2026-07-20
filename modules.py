import pandas as pd
import google.generativeai as genai


# ---------------------------------
# Configure Gemini
# ---------------------------------
def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


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
