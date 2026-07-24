import bcrypt
from database import get_connection


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def register_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed = hash_password(password)

        cursor.execute("""
            INSERT INTO users (email, password)
            VALUES (?, ?)
        """, (email, hashed))

        conn.commit()
        return True, "Account created successfully!"

    except Exception:
        return False, "Email already exists."

    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    if user:
        if verify_password(password, user["password"]):
            return user

    return None


def update_profile(user_id, username, student_class, board, study_hours, goal, weak_subjects):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            username=?,
            student_class=?,
            board=?,
            study_hours=?,
            goal=?,
            weak_subjects=?
        WHERE id=?
    """, (
        username,
        student_class,
        board,
        study_hours,
        goal,
        weak_subjects,
        user_id
    ))

    conn.commit()
    conn.close()
def is_profile_complete(user):
    return (
        user["username"] is not None and
        user["student_class"] is not None and
        user["board"] is not None
    )
