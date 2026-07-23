import streamlit as st
import sqlite3
from database import (
    create_session,
    delete_session
)

DB_NAME = "students.db"


# ---------------------------------------
# LOGIN
# ---------------------------------------

def login():

    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            session_id = create_session(user[0])

            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.session_id = session_id

            st.success("✅ Login Successful")

            st.rerun()

        else:

            st.error("Invalid Email or Password")


# ---------------------------------------
# SIGNUP
# ---------------------------------------

def signup():

    st.subheader("📝 Create Account")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    password = st.text_input("Password", type="password")

    class_name = st.selectbox(
        "Class",
        ["8","9","10","11","12"]
    )

    board = st.selectbox(
        "Board",
        ["CBSE","ICSE","State Board","IB","Other"]
    )

    if st.button("Create Account", use_container_width=True):

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO users
            (full_name,email,password,class_name,board)
            VALUES (?,?,?,?,?)
            """,
            (
                name,
                email,
                password,
                class_name,
                board
            ))

            conn.commit()

            st.success("✅ Account Created Successfully")

        except:

            st.error("Email already exists.")

        conn.close()


# ---------------------------------------
# LOGOUT
# ---------------------------------------

def logout():

    if "session_id" in st.session_state:

        delete_session(
            st.session_state.session_id
        )

    st.session_state.clear()

    st.rerun()
