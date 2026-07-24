import streamlit as st
from database import create_tables
from auth import register_user, login_user, update_profile, is_profile_complete

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Study Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DATABASE ---------------- #
create_tables()

# ---------------- SESSION ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- TITLE ---------------- #
st.title("📚 AI Study Companion")
st.subheader("Your Smart AI Learning Partner 📚🤖")
import streamlit as st
from database import create_tables
from auth import register_user, login_user

st.set_page_config(
    page_title="AI Study Companion",
    page_icon="📚",
    layout="wide"
)

create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

st.title("📚 AI Study Companion")
st.markdown("### Welcome to your Smart AI Learning Partner 🤖")

if not st.session_state.logged_in:

    option = st.sidebar.selectbox(
        "Choose",
        ["Login", "Sign Up"]
    )

    if option == "Sign Up":

        st.header("📝 Create Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):

            if password != confirm:
                st.error("Passwords do not match.")

            elif len(password) < 6:
                st.error("Password must contain at least 6 characters.")

            else:

                success, message = register_user(email, password)

                if success:
                    st.success(message)

                else:
                    st.error(message)

    else:

        st.header("🔐 Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(email, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()

            else:
                st.error("Invalid email or password.")

else:

   user = st.session_state.user

if not is_profile_complete(user):

    st.header("👤 Complete Your Profile")

    username = st.text_input("Username")

    student_class = st.selectbox(
        "Class",
        ["6","7","8","9","10","11","12","College"]
    )

    board = st.selectbox(
        "Board",
        ["State Board","CBSE","ICSE","IB","Other"]
    )

    study_hours = st.slider(
        "Study Hours per Day",
        1,
        12,
        2
    )

    goal = st.text_input("Your Goal")

    weak_subjects = st.text_input(
        "Weak Subjects (comma separated)"
    )

    if st.button("Save Profile"):

        update_profile(
            user["id"],
            username,
            student_class,
            board,
            study_hours,
            goal,
            weak_subjects
        )

        st.success("Profile Saved Successfully 🎉")

        st.rerun()

else:

   else:

    menu = st.sidebar.radio(
        "📚 Navigation",
        [
            "🏠 Dashboard",
            "📅 Study Plan",
            "🗓️ Smart Timetable",
            "📖 Study Session",
            "📊 Subject Priority",
            "🤖 AI Tutor",
            "📝 AI Notes",
            "🧠 Flashcards",
            "📚 Story Learning",
            "❓ Quiz",
            "🎯 Exam Simulator",
            "🎮 Memory Booster",
            "📈 Progress",
            "📄 Reports",
            "⚙️ Settings"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.write(f"👤 {user['username']}")
    st.sidebar.write(f"🎯 Goal: {user['goal']}")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    if menu == "🏠 Dashboard":
        st.title("🏠 Dashboard")
        st.success(f"Welcome back, {user['username']}! 🎉")
        st.info("Your AI Study Companion is ready.")

    else:
        st.title(menu)
        st.info("This module will be built next.")
