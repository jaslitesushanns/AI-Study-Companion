import bcrypt
from database import get_connection


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def register_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        hashed = hash_password(password)

        cur.execute("""
            INSERT INTO users(email, password)
            VALUES(?, ?)
        """, (email, hashed))

        conn.commit()
        return True, "Account created successfully!"

    except Exception:
        return False, "Email already exists."

    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()

    conn.close()

    if user and verify_password(password, user["password"]):
        return user

    return None


def update_profile(
    user_id,
    username,
    student_class,
    board,
    study_hours,
    goal,
    weak_subjects
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
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


def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()

    conn.close()

    return user


def profile_completed(user):
    return (
        user["username"] is not None
        and user["student_class"] is not None
        and user["board"] is not None
    )
