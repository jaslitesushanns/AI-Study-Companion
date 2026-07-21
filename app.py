import streamlit as st
from reportlab.pdfgen import canvas
from database import create_database
from auth import signup_page, login_page, logout
from utils import get_greeting
from modules import (
    configure_gemini,
    generate_study_plan,
    generate_smart_timetable,
    analyze_subject_priority,
    generate_study_session,
    generate_quiz,
    generate_progress,
    generate_daily_motivation,
    ask_ai
)
def create_pdf(content):

    pdf_file = "Study_Report.pdf"

    c = canvas.Canvas(pdf_file)

    y = 800

    for line in content.split("\n"):
        c.drawString(40, y, line)
        y -= 20

    c.save()

    return pdf_file
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

       user = st.session_state.user

       st.subheader(f"Welcome, {user[1]} 👋")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"📧 Email: {user[2]}")
        st.info(f"🎓 Class: {user[4]}")

    with col2:
        st.info(f"📖 Board: {user[5]}")
        st.info("🔥 Study Streak: 0 Days")

    st.divider()

    st.subheader("📈 Overall Progress")

    progress = 0

    st.progress(progress)

    st.write("Progress: 0%")

    st.divider()

    st.subheader("💪 Today's Motivation")

    st.success("Small progress each day leads to big success!")

    st.divider()

    st.subheader("📅 Quick Access")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("📅 Study Plan")

    with c2:
        st.button("🗓 Timetable")

    with c3:
        st.button("❓ Quiz")
# ==============================
# AI STUDY PLAN GENERATOR
# ==============================

elif page == "📅 Study Plan":

    st.header("📅 AI Study Plan Generator")

    st.write("Fill in your study details below.")

    student_name = st.text_input("Student Name")

    student_class = st.selectbox(
        "Class",
        ["8", "9", "10", "11", "12"]
    )

    board = st.selectbox(
        "Board",
        ["CBSE", "ICSE", "State Board", "IB", "Other"]
    )

    subjects = st.text_area(
        "Subjects",
        placeholder="Maths, Science, English..."
    )

    weak_subjects = st.text_input(
        "Weak Subjects"
    )

    study_hours = st.slider(
        "Daily Study Hours",
        1,
        12,
        4
    )

    exam_date = st.date_input("Exam Date")

    goal = st.text_input(
        "Goal",
        placeholder="Example: Score above 90%"
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    if st.button("Generate Study Plan"):

        if api_key == "":
            st.error("Please enter your Gemini API Key.")

        else:

            model = configure_gemini(api_key)

            result = generate_study_plan(
                model,
                student_name,
                student_class,
                board,
                subjects,
                weak_subjects,
                study_hours,
                exam_date,
                goal
            )

            st.markdown(result) 
          
            pdf = create_pdf(result)

with open(pdf, "rb") as file:

    st.download_button(
        label="📥 Download Study Plan PDF",
        data=file,
        file_name="Study_Plan.pdf",
        mime="application/pdf"
    )
# ==============================
# SMART TIMETABLE
# ==============================

elif page == "🗓 Smart Timetable":

    st.header("🗓 AI Smart Timetable")

    school_hours = st.text_input(
        "School Hours",
        placeholder="8:30 AM - 3:30 PM"
    )

    tuition_hours = st.text_input(
        "Tuition Hours",
        placeholder="5:00 PM - 6:30 PM"
    )

    study_hours = st.slider(
        "Daily Study Hours",
        1,
        12,
        4
    )

    sleep_hours = st.slider(
        "Sleep Hours",
        5,
        10,
        8
    )

    meal_times = st.text_input(
        "Meal Times",
        placeholder="8 AM, 1 PM, 8 PM"
    )

    weak_subjects = st.text_input("Weak Subjects")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        key="tt_api"
    )

    if st.button("Generate Timetable"):

        if api_key == "":
            st.error("Please enter your Gemini API Key.")

        else:

            model = configure_gemini(api_key)

            timetable = generate_smart_timetable(
                model,
                school_hours,
                tuition_hours,
                study_hours,
                sleep_hours,
                meal_times,
                weak_subjects
            )

            st.markdown(timetable)

pdf = create_pdf(timetable)

with open(pdf, "rb") as file:

    st.download_button(
        label="📥 Download Timetable PDF",
        data=file,
        file_name="Smart_Timetable.pdf",
        mime="application/pdf"
    )
# ==============================
# SUBJECT PRIORITY ANALYZER
# ==============================

elif page == "📊 Subject Priority":

    st.header("📊 Subject Priority Analyzer")

    subjects = st.text_area(
        "Enter all subjects",
        placeholder="Maths, Science, English, Social..."
    )

    weak_subjects = st.text_input("Weak Subjects")

    goal = st.text_input(
        "Goal",
        placeholder="Example: Score above 95%"
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        key="priority_api"
    )

    if st.button("Analyze Priority"):

        if api_key == "":
            st.error("Please enter your Gemini API Key.")

        else:

            model = configure_gemini(api_key)

            result = analyze_subject_priority(
                model,
                subjects,
                weak_subjects,
                goal
            )

            st.markdown(result)
# ==============================
# STUDY SESSION PLANNER
# ==============================

elif page == "📖 Study Session":

    st.header("📖 AI Study Session Planner")

    subject = st.text_input("Subject")

    available_hours = st.slider(
        "Available Study Hours",
        1,
        12,
        3
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        key="session_api"
    )

    if st.button("Generate Study Session"):

        if api_key == "":
            st.error("Please enter your Gemini API Key.")

        else:

            model = configure_gemini(api_key)

            session = generate_study_session(
                model,
                subject,
                available_hours
            )

            st.markdown(session)
# ==============================
# AI QUIZ GENERATOR
# ==============================

elif page == "❓ AI Quiz":

    st.header("❓ AI Quiz Generator")

    subject = st.text_input("Subject")

    student_class = st.selectbox(
        "Class",
        ["8", "9", "10", "11", "12"],
        key="quiz_class"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        key="quiz_api"
    )

    if st.button("Generate Quiz"):

        if api_key == "":
            st.error("Please enter your Gemini API Key.")

        else:

            model = configure_gemini(api_key)

            quiz = generate_quiz(
                model,
                subject,
                student_class,
                difficulty
            )

            st.markdown(quiz)

pdf = create_pdf(quiz)

with open(pdf, "rb") as file:

    st.download_button(
        label="📥 Download Quiz PDF",
        data=file,
        file_name="Quiz.pdf",
        mime="application/pdf"
    )
# ==============================
# PROGRESS TRACKER
# ==============================

elif page == "📈 Progress":

    st.header("📈 Progress Tracker")

    completed_topics = st.number_input(
        "Completed Topics",
        min_value=0,
        value=0
    )

    total_topics = st.number_input(
        "Total Topics",
        min_value=1,
        value=1
    )

    if st.button("Calculate Progress"):

        progress = generate_progress(
            completed_topics,
            total_topics
        )

        st.progress(progress / 100)

        st.success(f"Overall Progress: {progress}%")
# ==============================
# MOTIVATION GENERATOR
# ==============================

elif page == "💪 Motivation":

    st.header("💪 Daily Motivation")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        key="motivation_api"
    )

    if st.button("Generate Motivation"):

        if api_key == "":
            st.error("Please enter your Gemini API Key.")

        else:

            model = configure_gemini(api_key)

            motivation = generate_daily_motivation(model)

            st.success(motivation)

pdf = create_pdf(motivation)

with open(pdf, "rb") as file:

    st.download_button(
        label="📥 Download Motivation PDF",
        data=file,
        file_name="Motivation.pdf",
        mime="application/pdf"
    )
# ==============================
# AI STUDY ASSISTANT
# ==============================

elif page == "🤖 AI Assistant":

    st.header("🤖 AI Study Assistant")

    question = st.text_area(
        "Ask any study-related question"
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        key="assistant_api"
    )

    if st.button("Ask AI"):

        if api_key == "":
            st.error("Please enter your Gemini API Key.")

        elif question.strip() == "":
            st.error("Please enter a question.")

        else:

            model = configure_gemini(api_key)

            answer = ask_ai(
                model,
                question
            )

            st.markdown(answer)

pdf = create_pdf(answer)

with open(pdf, "rb") as file:

    st.download_button(
        label="📥 Download Answer PDF",
        data=file,
        file_name="AI_Answer.pdf",
        mime="application/pdf"
    )
# ==============================
# STUDY TIMER
# ==============================

elif page == "⏱ Study Timer":

    st.header("⏱ Study Timer")

    timer_type = st.radio(
        "Select Timer",
        ["Pomodoro", "Custom"]
    )

    if timer_type == "Pomodoro":

        st.success("📚 Study: 25 Minutes")
        st.info("☕ Short Break: 5 Minutes")
        st.warning("🌴 Long Break: 15 Minutes")

    else:

        hours = st.number_input(
            "Hours",
            min_value=0,
            max_value=10,
            value=1
        )

        minutes = st.number_input(
            "Minutes",
            min_value=0,
            max_value=59,
            value=0
        )

        if st.button("Start Timer"):

            total_seconds = (hours * 3600) + (minutes * 60)

            st.success(f"✅ Timer Started for {hours} hour(s) {minutes} minute(s).")

            st.info(f"Total Time: {total_seconds} seconds")
            # ==============================
# STUDY NOTIFICATIONS
# ==============================

elif page == "🔔 Notifications":

    st.header("🔔 Study Notifications")

    st.success("📚 Time to study!")

    st.info("⏰ Complete today's study plan.")

    st.warning("💧 Drink water and take short breaks.")

    st.success("🎯 Stay focused and achieve your goal!")
