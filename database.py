import sqlite3

DB_NAME = "students.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()



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



def get_student_profile():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC LIMIT 1"
    )

    data = cursor.fetchone()

    conn.close()

    return data
