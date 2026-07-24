from google import genai
import streamlit as st

import os

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

MODEL = "gemini-2.5-flash"

# ---------------- COMMON FUNCTION ---------------- #

def ask_gemini(prompt):

    if client is None:
        return "⚠️ Gemini API key is not configured yet."

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text


# ---------------- AI TUTOR ---------------- #

def ask_ai(question):
    prompt = f"""
You are a friendly AI Study Tutor.

Question:
{question}

Explain clearly using simple English.
"""
    return ask_gemini(prompt)


# ---------------- STUDY PLAN ---------------- #

def generate_study_plan(subjects, exam_date, study_hours, goal, weak_subjects):
    prompt = f"""
Create a 7-day study plan.

Subjects:
{subjects}

Exam Date:
{exam_date}

Study Hours:
{study_hours}

Goal:
{goal}

Weak Subjects:
{weak_subjects}

Return ONLY a markdown table.
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

def generate_study_session(study_hours):
    prompt = f"""
Create a productive study session for {study_hours} hours.
"""
    return ask_gemini(prompt)


# ---------------- SUBJECT PRIORITY ---------------- #

def analyze_subject_priority(weak_subjects, goal):
    prompt = f"""
Weak Subjects:
{weak_subjects}

Goal:
{goal}

Suggest subject priority.
"""
    return ask_gemini(prompt)


# ---------------- NOTES ---------------- #

def generate_notes(topic):
    prompt = f"""
Create detailed study notes for:

{topic}

Include:
- Definition
- Important Points
- Examples
- Summary
"""
    return ask_gemini(prompt)


# ---------------- FLASHCARDS ---------------- #

def generate_flashcards(topic):
    prompt = f"""
Create 15 flashcards for:

{topic}

Return as:

Question
Answer
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

def generate_quiz(subject):
    prompt = f"""
Generate 10 MCQs on:

{subject}

Include answers at the end.
"""
    return ask_gemini(prompt)


# ---------------- EXAM ---------------- #

def generate_exam(subject):
    prompt = f"""
Generate a 25-mark exam paper for:

{subject}

Include:
- MCQs
- Short Answers
- Long Answers
"""
    return ask_gemini(prompt)
