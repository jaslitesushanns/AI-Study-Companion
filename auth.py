import streamlit as st

from database import (
    get_connection,
    hash_password
)
# ==========================================
# REGISTER NEW USER
# ==========================================

def register_user(full_name, email, password, class_name, board, school):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False, "Email already registered."

    # Insert new user
    cursor.execute("""
        INSERT INTO users
        (full_name, email, password, class_name, board, school)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (

        full_name,

        email,

        hash_password(password),

        class_name,

        board,

        school

    ))

    conn.commit()
    conn.close()

    return True, "Account created successfully!"
    # ==========================================
# LOGIN USER
# ==========================================

def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ?
        AND password = ?
    """, (
        email,
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    return user
    # ==========================================
# SIGNUP PAGE
# ==========================================

def signup_page():

    st.subheader("📝 Create Your Account")

    full_name = st.text_input("👤 Full Name")

    email = st.text_input("📧 Email")

    password = st.text_input("🔒 Password", type="password")

    class_name = st.selectbox(
        "🎓 Class",
        [
            "6", "7", "8", "9", "10",
            "11", "12"
        ]
    )

    board = st.selectbox(
        "📚 Board",
        [
            "CBSE",
            "ICSE",
            "State Board",
            "IB",
            "IGCSE",
            "Other"
        ]
    )

    school = st.text_input("🏫 School Name")

    if st.button("✅ Create Account", use_container_width=True):

        if (
            full_name == ""
            or email == ""
            or password == ""
            or school == ""
        ):

            st.warning("Please fill all the fields.")

        else:

            success, message = register_user(
                full_name,
                email,
                password,
                class_name,
                board,
                school
            )

            if success:
                st.success(message)
                st.balloons()

            else:
                st.error(message)
                # ==========================================
# LOGIN PAGE
# ==========================================

def login_page():

    st.subheader("🔐 Login")

    email = st.text_input("📧 Email", key="login_email")

    password = st.text_input(
        "🔒 Password",
        type="password",
        key="login_password"
    )

    remember_me = st.checkbox("Remember Me")

    if st.button("🚀 Login", use_container_width=True):

        user = login_user(email, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.user = user

            if remember_me:
                st.session_state.remember_me = True

            st.success(f"Welcome back, {user[1]} 👋")
            st.rerun()

        else:

            st.error("Invalid Email or Password")
            # ==========================================
# LOGOUT
# ==========================================

def logout():

    if st.button("🚪 Logout", use_container_width=True):

        # Clear all session data
        st.session_state.clear()

        st.success("Logged out successfully!")

        st.rerun()
        
