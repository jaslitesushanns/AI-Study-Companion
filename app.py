import streamlit as st
from database import create_database
from auth import signup_page, login_page, logout
from utils import get_greeting
from modules import configure_gemini

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Study Companion",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# Create Database
# -----------------------------
create_database()

# -----------------------------
# Custom Green & White Theme
# -----------------------------
st.markdown("""
<style>

.stApp{
    background-color:#f8fff8;
}

h1,h2,h3{
    color:#1B5E20;
}

.stButton>button{
    background:#2E7D32;
    color:white;
    border-radius:10px;
    height:45px;
    width:100%;
    border:none;
}

.stButton>button:hover{
    background:#1B5E20;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# -----------------------------
# Title
# -----------------------------
st.title("📚 AI Powered Study Companion")

st.write(get_greeting())

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Sign Up"]
)
# -----------------------------
# Login & Sign Up Pages
# -----------------------------

if not st.session_state.logged_in:

    if menu == "Login":
        login_page()

    elif menu == "Sign Up":
        signup_page()

else:

    st.sidebar.success("✅ Logged In")

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    st.success(f"Welcome {st.session_state.user[1]} 🎉")

    st.write("You have successfully logged into AI Powered Study Companion.")

    st.info("➡️ Dashboard modules will appear in the next step.")
# ==============================
# STUDENT DASHBOARD
# ==============================

if st.session_state.logged_in:

    st.sidebar.title("📚 Navigation")

    page = st.sidebar.radio(
        "Choose Module",
        [
            "🏠 Dashboard",
            "📅 Study Plan",
            "🗓 Smart Timetable",
            "📊 Subject Priority",
            "📖 Study Session",
            "❓ AI Quiz",
            "📈 Progress",
            "💪 Motivation",
            "🤖 AI Assistant",
            "⏱ Study Timer",
            "🔔 Notifications"
        ]
    )

    if page == "🏠 Dashboard":

        st.header("🏠 Student Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Completed Topics", "0")

        with col2:
            st.metric("Progress", "0%")

        st.write("---")

        st.subheader("🎯 Today's Goal")

        st.info("No goal set yet.")

        st.subheader("📅 Today's Study Plan")

        st.info("Generate your study plan from the Study Plan module.")

        st.subheader("💪 Daily Motivation")

        st.success("Every small step today builds your success tomorrow.")
