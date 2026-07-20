import sqlite3
import hashlib

DB_NAME = "students.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        class_name TEXT NOT NULL,
        board TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(full_name, email, password, class_name, board):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (full_name, email, password, class_name, board)
        VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            hash_password(password),
            class_name,
            board
        ))

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def login_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE email=? AND password=?
    """, (
        email,
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    return user
