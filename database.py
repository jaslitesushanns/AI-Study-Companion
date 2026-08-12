import sqlite3

DB_NAME = "study_companion.db"


# ---------------- DATABASE CONNECTION ---------------- #

def get_connection():
    conn = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


# ---------------- CREATE / UPDATE TABLES ---------------- #

def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    # Main users table
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
            subjects TEXT,
            weak_subjects TEXT,
            progress INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Reports table
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

    # ------------------------------------------------
    # DATABASE MIGRATION
    # ------------------------------------------------
    # These allow your OLD database to gain the new
    # columns without deleting existing accounts.
    # ------------------------------------------------

    cur.execute("PRAGMA table_info(users)")

    existing_columns = [
        column["name"]
        for column in cur.fetchall()
    ]

    if "subjects" not in existing_columns:

        cur.execute("""
            ALTER TABLE users
            ADD COLUMN subjects TEXT
        """)

    if "progress" not in existing_columns:

        cur.execute("""
            ALTER TABLE users
            ADD COLUMN progress INTEGER DEFAULT 0
        """)

    conn.commit()
    conn.close()


# ---------------- SAVE REPORT ---------------- #

def save_report(
    user_id,
    subject,
    score,
    total,
    feedback
):

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
    """, (
        user_id,
        subject,
        score,
        total,
        feedback
    ))

    conn.commit()
    conn.close()


# ---------------- GET REPORTS ---------------- #

def get_reports(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM reports
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (
        user_id,
    ))

    reports = cur.fetchall()

    conn.close()

    return reports


# ---------------- UPDATE PROGRESS ---------------- #

def update_progress(user_id, progress):

    progress = max(0, min(100, int(progress)))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET progress=?
        WHERE id=?
    """, (
        progress,
        user_id
    ))

    conn.commit()
    conn.close()
