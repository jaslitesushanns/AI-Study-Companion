import streamlit as st
from database import register_user, login_user


def signup_page():
    st.subheader("📝 Create Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    class_name = st.selectbox(
        "Class",
        ["8", "9", "10", "11", "12"]
    )

    board = st.selectbox(
        "Board",
        ["CBSE", "ICSE", "State Board", "IB", "Other"]
    )

    if st.button("Create Account"):

        if not full_name:
            st.error("Enter your name.")

        elif not email:
            st.error("Enter your email.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:
            success = register_user(
                full_name,
                email,
                password,
                class_name,
                board
           )

           if success:
               st.success("✅ Account Created Successfully!")

           else:
               st.error("Email already exists.")


def login_page():
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = login_user(email, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login Successful!")
            st.rerun()

        else:
            st.error("Invalid Email or Password")
            


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
