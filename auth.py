import bcrypt

from database import get_connection


# ---------------- PASSWORD HASHING ---------------- #

def hash_password(password):

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


# ---------------- PASSWORD VERIFICATION ---------------- #

def verify_password(password, hashed_password):

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ---------------- REGISTER USER ---------------- #

def register_user(email, password):

    conn = get_connection()
    cur = conn.cursor()

    try:

        email = email.strip().lower()

        hashed = hash_password(password)

        cur.execute("""
            INSERT INTO users(
                email,
                password,
                progress,
                xp,
                streak
            )
            VALUES (?, ?, 0, 0, 0)
        """, (
            email,
            hashed
        ))

        conn.commit()

        return True, "Account created successfully!"

    except Exception as e:

        return False, "Email already exists."

    finally:

        conn.close()


# ---------------- LOGIN USER ---------------- #

def login_user(email, password):

    conn = get_connection()
    cur = conn.cursor()

    email = email.strip().lower()

    cur.execute("""
        SELECT *
        FROM users
        WHERE email=?
    """, (
        email,
    ))

    user = cur.fetchone()

    conn.close()

    if user:

        try:

            if verify_password(
                password,
                user["password"]
            ):

                return user

        except Exception:

            return None

    return None


# ---------------- UPDATE PROFILE ---------------- #

def update_profile(
    user_id,
    username,
    student_class,
    board,
    study_hours,
    goal,
    subjects,
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
            subjects=?,
            weak_subjects=?
        WHERE id=?
    """, (
        username,
        student_class,
        board,
        study_hours,
        goal,
        subjects,
        weak_subjects,
        user_id
    ))

    conn.commit()
    conn.close()


# ---------------- GET USER ---------------- #

def get_user(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM users
        WHERE id=?
    """, (
        user_id,
    ))

    user = cur.fetchone()

    conn.close()

    return user


# ---------------- CHECK PROFILE ---------------- #

def profile_completed(user):

    if user is None:
        return False

    return (
        user["username"] is not None
        and user["username"].strip() != ""
        and user["student_class"] is not None
        and user["student_class"].strip() != ""
        and user["board"] is not None
        and user["board"].strip() != ""
        and user["subjects"] is not None
        and user["subjects"].strip() != ""
        and user["weak_subjects"] is not None
        and user["weak_subjects"].strip() != ""
        and user["goal"] is not None
        and user["goal"].strip() != ""
    )


# ---------------- UPDATE PROGRESS ---------------- #

def update_user_progress(user_id, progress):

    progress = max(
        0,
        min(100, int(progress))
    )

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
