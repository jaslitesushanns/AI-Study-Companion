import sqlite3


DATABASE = "students.db"


def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course TEXT,
        percentage REAL,
        board TEXT,
        study_hours TEXT,
        goal TEXT,
        weak_subjects TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_student(
    name,
    age,
    course,
    percentage,
    board,
    study_hours,
    goal,
    weak_subjects
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name, age, course, percentage, board, study_hours, goal, weak_subjects)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        age,
        course,
        percentage,
        board,
        study_hours,
        goal,
        weak_subjects
    ))

    conn.commit()
    conn.close()


def get_students():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return data
