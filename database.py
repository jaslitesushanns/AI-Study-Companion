import sqlite3
import uuid
from datetime import datetime

DB_NAME = "students.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

   # -----------------------------
   # Users Table
   # -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    class_name TEXT,
    board TEXT,
    created_at TEXT
)
""")
    # -----------------------------
    # Student Profile
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class_name TEXT,
        board TEXT,
        school TEXT,
        subjects TEXT,
        portions TEXT,
        goal TEXT,
        exam_date TEXT,
        study_hours TEXT
    )
    """)

    # -----------------------------
    # Login Sessions
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_sessions(
        session_id TEXT PRIMARY KEY,
        student_id INTEGER,
        created_at TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------------
# Save Student Profile
# -----------------------------------

def save_student_profile(data):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name, class_name, board, school, subjects, portions, goal, exam_date, study_hours)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        data["name"],
        data["class_name"],
        data["board"],
        data["school"],
        data["subjects"],
        data["portions"],
        data["goal"],
        data["exam_date"],
        data["study_hours"]
    ))

    conn.commit()
    conn.close()


# -----------------------------------
# Get Latest Student Profile
# -----------------------------------

def get_student_profile():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM students
    ORDER BY id DESC
    LIMIT 1
    """)

    data = cursor.fetchone()

    conn.close()

    return data


# -----------------------------------
# Session Management
# -----------------------------------

def create_session(student_id):

    session_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO user_sessions
    VALUES (?, ?, ?)
    """, (
        session_id,
        student_id,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    return session_id


def get_session(session_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM user_sessions
    WHERE session_id=?
    """, (session_id,))

    session = cursor.fetchone()

    conn.close()

    return session


def delete_session(session_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM user_sessions
    WHERE session_id=?
    """, (session_id,))

    conn.commit()
    conn.close()
