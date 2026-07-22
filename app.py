import streamlit as st
from reportlab.pdfgen import canvas

from database import create_database
from auth import signup_page, login_page, logout

from modules import (
    configure_gemini,
    generate_study_plan,
    generate_smart_timetable,
    analyze_subject_priority,
    generate_study_session,
    generate_quiz,
    generate_progress,
    generate_motivation,
    generate_daily_motivation,
    ask_ai,
    study_notification,
    pomodoro_timer
)
# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI Powered Study Companion",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------
# Database Initialization
# ---------------------------------

create_database()

# ---------------------------------
# Session State
# ---------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None
    # ---------------------------------
# Custom CSS
# ---------------------------------

st.markdown("""
<style>

.main {
    background-color: #f8fff8;
}

h1, h2, h3 {
    color: #2e7d32;
    font-weight: bold;
}

.stButton>button {
    background-color: #2e7d32;
    color: white;
    border-radius: 10px;
    width: 100%;
    height: 45px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #1b5e20;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #e8f5e9;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 10px;
    border-radius: 10px;
    border: 2px solid #2e7d32;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------
# PDF Generator
# ---------------------------------

def create_pdf(content):

    pdf_file = "Study_Report.pdf"

    c = canvas.Canvas(pdf_file)

    y = 800

    for line in str(content).split("\n"):
        c.drawString(40, y, line)
        y -= 20

        if y < 40:
            c.showPage()
            y = 800

    c.save()

    return pdf_file
       # ---------------------------------
# Main Title
# ---------------------------------

st.title("📚 AI Powered Study Companion")

st.caption("Your Personal AI Learning Partner")
# ---------------------------------
# Login / Signup Menu
# ---------------------------------

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Create Account"]
    )

    if menu == "Login":
        login_page()

    else:
        signup_page()

    st.stop()
    # ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.title("📚 Navigation")

page = st.sidebar.radio(
    "Choose a Module",
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

st.sidebar.write("---")

if st.sidebar.button("🚪 Logout"):
    logout()
    st.rerun()
    # ---------------------------------
# Dashboard
# ---------------------------------

if page == "🏠 Dashboard":

    user = st.session_state.user

    st.header("🏠 Student Dashboard")

    st.success(f"Welcome, {user[1]} 👋")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"📧 Email: {user[2]}")
        st.info(f"🎓 Class: {user[4]}")

    with col2:
        st.info(f"📖 Board: {user[5]}")
        st.info("🔥 Study Streak: 0 Days")

    st.divider()

    st.subheader("📊 Progress")

    st.progress(0)

    st.write("Completed Topics: 0")

    st.write("Progress: 0%")

    st.divider()

    st.subheader("💡 Daily Motivation")

    st.success("Small progress every day leads to big success.")

    st.divider()

    st.subheader("🚀 Quick Access")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("📅 Study Plan")

    with c2:
        st.button("🗓 Timetable")

    with c3:
        st.button("❓ Quiz")
       # ---------------------------------
# Study Plan Generator
# ---------------------------------

elif page == "📅 Study Plan":

    st.header("📅 AI Study Plan Generator")

    student_name = st.text_input("Student Name")

    student_class = st.selectbox(
        "Class",
        ["8", "9", "10", "11", "12"],
        key="sp_class"
    )

    board = st.selectbox(
        "Board",
        ["CBSE", "ICSE", "State Board", "IB", "Other"],
        key="sp_board"
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

    if st.button("Generate Study Plan"):

        with st.spinner("Generating your personalized study plan..."):

            model = configure_gemini()

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

        st.success("✅ Study Plan Generated Successfully!")

        st.markdown(result)

        pdf = create_pdf(result)

        with open(pdf, "rb") as file:

            st.download_button(
                label="📥 Download Study Plan PDF",
                data=file,
                file_name="Study_Plan.pdf",
                mime="application/pdf"
            )
               # ---------------------------------
# Smart Timetable
# ---------------------------------

elif page == "🗓 Smart Timetable":

    st.header("🗓 AI Smart Timetable")

    school_hours = st.text_input(
        "School Hours",
        placeholder="8:00 AM - 3:00 PM"
    )

    tuition_hours = st.text_input(
        "Tuition Hours",
        placeholder="5:00 PM - 6:30 PM"
    )

    study_hours = st.slider(
        "Daily Study Hours",
        1,
        12,
        4,
        key="tt_hours"
    )

    sleep_hours = st.slider(
        "Sleep Hours",
        4,
        12,
        8
    )

    meal_times = st.text_input(
        "Meal Times",
        placeholder="8 AM, 1 PM, 8 PM"
    )

    weak_subjects = st.text_input(
        "Weak Subjects",
        key="tt_weak"
    )

    if st.button("Generate Timetable"):

        with st.spinner("Generating Smart Timetable..."):

            model = configure_gemini()

            timetable = generate_smart_timetable(
                model,
                school_hours,
                tuition_hours,
                study_hours,
                sleep_hours,
                meal_times,
                weak_subjects
            )

        st.success("✅ Timetable Generated Successfully!")

        st.markdown(timetable)

        pdf = create_pdf(timetable)

        with open(pdf, "rb") as file:

            st.download_button(
                label="📥 Download Timetable PDF",
                data=file,
                file_name="Smart_Timetable.pdf",
                mime="application/pdf"
            )
               # ---------------------------------
# Subject Priority Analyzer
# ---------------------------------

elif page == "📊 Subject Priority":

    st.header("📊 Subject Priority Analyzer")

    subjects = st.text_area(
        "Enter All Subjects",
        placeholder="Maths, Science, English, Social, Tamil"
    )

    weak_subjects = st.text_input(
        "Weak Subjects",
        key="priority_weak"
    )

    goal = st.text_input(
        "Goal",
        placeholder="Example: Score above 95%"
    )

    if st.button("Analyze Priority"):

        with st.spinner("Analyzing subject priority..."):

            model = configure_gemini()

            priority = analyze_subject_priority(
                model,
                subjects,
                weak_subjects,
                goal
            )

        st.success("✅ Analysis Completed!")

        st.markdown(priority)

        pdf = create_pdf(priority)

        with open(pdf, "rb") as file:

            st.download_button(
                label="📥 Download Priority Report",
                data=file,
                file_name="Subject_Priority.pdf",
                mime="application/pdf"
            )
               # ---------------------------------
# Study Session Planner
# ---------------------------------

elif page == "📖 Study Session":

    st.header("📖 AI Study Session Planner")

    subject = st.text_input(
        "Subject"
    )

    available_hours = st.slider(
        "Available Study Hours",
        1,
        12,
        3
    )

    if st.button("Generate Study Session"):

        with st.spinner("Generating study session..."):

            model = configure_gemini()

            session = generate_study_session(
                model,
                subject,
                available_hours
            )

        st.success("✅ Study Session Generated Successfully!")

        st.markdown(session)

        pdf = create_pdf(session)

        with open(pdf, "rb") as file:

            st.download_button(
                label="📥 Download Study Session PDF",
                data=file,
                file_name="Study_Session.pdf",
                mime="application/pdf"
            )
                # ---------------------------------
# AI Quiz Generator
# ---------------------------------

elif page == "❓ AI Quiz":

    st.header("❓ AI Quiz Generator")

    subject = st.text_input(
        "Subject",
        key="quiz_subject"
    )

    student_class = st.selectbox(
        "Class",
        ["8", "9", "10", "11", "12"],
        key="quiz_class"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("Generate Quiz"):

        with st.spinner("Generating quiz..."):

            model = configure_gemini()

            quiz = generate_quiz(
                model,
                subject,
                student_class,
                difficulty
            )

        st.success("✅ Quiz Generated Successfully!")

        st.markdown(quiz)

        pdf = create_pdf(quiz)

        with open(pdf, "rb") as file:

            st.download_button(
                label="📥 Download Quiz PDF",
                data=file,
                file_name="AI_Quiz.pdf",
                mime="application/pdf"
            )
                # ---------------------------------
# Progress Tracker
# ---------------------------------

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
     # ---------------------------------
# Motivation Generator
# ---------------------------------

elif page == "💪 Motivation":

    st.header("💪 Daily Motivation")

    goal = st.text_input(
        "Enter Your Goal",
        placeholder="Example: Score above 95%"
    )

    if st.button("Generate Motivation"):

        if goal.strip() == "":
            st.error("Please enter your goal.")

        else:

            with st.spinner("Generating motivation..."):

                model = configure_gemini()

                motivation = generate_motivation(
                    model,
                    goal
                )

            st.success("✅ Motivation Generated!")

            st.success(motivation)

            pdf = create_pdf(motivation)

            with open(pdf, "rb") as file:

                st.download_button(
                    label="📥 Download Motivation PDF",
                    data=file,
                    file_name="Motivation.pdf",
                    mime="application/pdf"
                )
               # ---------------------------------
# AI Study Assistant
# ---------------------------------

elif page == "🤖 AI Assistant":

    st.header("🤖 AI Study Assistant")

    question = st.text_area(
        "Ask your question"
    )

    if st.button("Ask AI"):

        if question.strip() == "":
            st.error("Please enter a question.")

        else:

            with st.spinner("Thinking..."):

                model = configure_gemini()

                answer = ask_ai(
                    model,
                    question
                )

            st.success("✅ Answer Generated!")

            st.markdown(answer)

            pdf = create_pdf(answer)

            with open(pdf, "rb") as file:

                st.download_button(
                    label="📥 Download Answer PDF",
                    data=file,
                    file_name="AI_Answer.pdf",
                    mime="application/pdf"
                )
                # ---------------------------------
# Study Timer
# ---------------------------------

elif page == "⏱ Study Timer":

    st.header("⏱ Study Timer")

    timer_type = st.radio(
        "Choose Timer",
        ["Pomodoro", "Custom"]
    )

    if timer_type == "Pomodoro":

        timer = pomodoro_timer()

        st.success(f"📚 Study Time : {timer['Study']} Minutes")
        st.info(f"☕ Short Break : {timer['Short Break']} Minutes")
        st.warning(f"🌴 Long Break : {timer['Long Break']} Minutes")

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

            st.success(
                f"Timer Started for {hours} hour(s) and {minutes} minute(s)"
            )

            st.info(f"Total Time: {total_seconds} seconds")
            # ---------------------------------
# Notifications
# ---------------------------------

elif page == "🔔 Notifications":

    st.header("🔔 Study Notifications")

    notification = study_notification()

    st.success(notification)

    st.info("📚 Complete today's study plan.")

    st.warning("💧 Drink water regularly.")

    st.info("😴 Get enough sleep.")

    st.success("🎯 Stay focused and keep learning!")
