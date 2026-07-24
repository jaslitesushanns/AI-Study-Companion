import sqlite3

DB_NAME = "study_companion.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        username TEXT,
        student_class TEXT,
        board TEXT,
        study_hours INTEGER,
        goal TEXT,
        weak_subjects TEXT,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject TEXT,
        score INTEGER,
        total INTEGER,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
def save_report(user_id, subject, score, total, feedback):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports(
            user_id,
            subject,
            score,
            total,
            feedback
        )
        VALUES (?, ?, ?, ?, ?)
    """,(
        user_id,
        subject,
        score,
        total,
        feedback
    ))

    conn.commit()
    conn.close()


def get_reports(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM reports
        WHERE user_id=?
        ORDER BY created_at DESC
    """,(user_id,))

    reports = cur.fetchall()

    conn.close()

    return reports
    
