import sqlite3
import hashlib

# ============================================
# DATABASE NAME
# ============================================

DB_NAME = "students.db"


# ============================================
# DATABASE CONNECTION
# ============================================

def get_connection():
    """
    Returns a connection to the SQLite database.
    """
    return sqlite3.connect(DB_NAME)


# ============================================
# PASSWORD HASHING
# ============================================

def hash_password(password):
    """
    Encrypt password before saving.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================
# CREATE DATABASE
# ============================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ========================================
    # USERS TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        class_name TEXT,

        board TEXT,

        school TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()
      # ========================================
    # STUDENT PROFILE TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_profile (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subjects TEXT,

        weak_subjects TEXT,

        target_percentage TEXT,

        daily_study_hours INTEGER,

        exam_date TEXT,

        exam_portions TEXT,

        learning_style TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)
      # ========================================
    # STUDY PROGRESS TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        completed_topics INTEGER DEFAULT 0,

        total_topics INTEGER DEFAULT 0,

        progress_percentage REAL DEFAULT 0,

        quiz_score REAL DEFAULT 0,

        study_streak INTEGER DEFAULT 0,

        total_study_hours REAL DEFAULT 0,

        journey_stage TEXT DEFAULT 'Beginner',

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)
      # ========================================
    # QUIZ HISTORY TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subject TEXT,

        topic TEXT,

        difficulty TEXT,

        score REAL,

        total_questions INTEGER,

        percentage REAL,

        strengths TEXT,

        weaknesses TEXT,

        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)
      # ========================================
    # STUDY PLANS TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_plans (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subject TEXT,

        exam_portions TEXT,

        target_percentage TEXT,

        study_hours INTEGER,

        exam_date TEXT,

        generated_plan TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)
      # ========================================
    # FLASHCARDS TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subject TEXT,

        topic TEXT,

        question TEXT,

        answer TEXT,

        mastered INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)
      # ========================================
    # EXAM SIMULATOR TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subject TEXT,

        topic TEXT,

        total_marks INTEGER,

        obtained_marks INTEGER,

        percentage REAL,

        difficulty TEXT,

        ai_feedback TEXT,

        strengths TEXT,

        weaknesses TEXT,

        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)


    # ========================================
    # MODEL QUESTION PAPER TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_papers (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subject TEXT,

        portions TEXT,

        total_marks INTEGER,

        difficulty TEXT,

        generated_questions TEXT,

        answer_key TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)
      # ========================================
    # NOTIFICATIONS TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        title TEXT,

        message TEXT,

        is_read INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)


    # ========================================
    # DAILY MOTIVATION TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_motivation (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        quote TEXT,

        generated_date TEXT,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)


    # ========================================
    # LEARNING JOURNEY TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_journey (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        current_stage TEXT DEFAULT 'Beginner',

        progress INTEGER DEFAULT 0,

        completed_modules TEXT,

        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)


    # ========================================
    # STUDY SESSIONS TABLE
    # ========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        subject TEXT,

        topic TEXT,

        duration INTEGER,

        break_taken INTEGER DEFAULT 0,

        session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)


    conn.commit()
    conn.close()
  
