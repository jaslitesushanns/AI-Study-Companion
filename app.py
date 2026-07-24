import os
import streamlit as st
import google.generativeai as genai

from auth import (
    register_user,
    login_user,
    update_profile,
    get_user,
    profile_completed
)

from database import (
    create_tables,
    save_report,
    get_reports
)

from modules import *
from utils import *

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Powered Study Companion",
    page_icon="📚",
    layout="wide"
)

# ---------------- DATABASE ---------------- #

create_tables()

# ---------------- GEMINI ---------------- #

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

# ---------------- SESSION STATE ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main{
    background:#f5f7ff;
}

.stButton>button{
    width:100%;
    height:48px;
    border-radius:12px;
    border:none;
    background:#4F46E5;
    color:white;
    font-weight:bold;
    font-size:16px;
}

.stButton>button:hover{
    background:#4338CA;
}

div[data-testid="stSidebar"]{
    background:#111827;
}

div[data-testid="stSidebar"] *{
    color:white;
}

h1,h2,h3{
    color:#1F2937;
}

</style>
""", unsafe_allow_html=True)
# ---------------- LOGIN / SIGNUP ---------------- #

if not st.session_state.logged_in:

    st.title("📚 AI Powered Study Companion")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    # ---------- LOGIN ---------- #

    with tab1:

        st.subheader("Login")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            user = login_user(
                login_email,
                login_password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user = dict(user)

                st.success("Login Successful 🎉")
                st.rerun()

            else:

                st.error("Invalid Email or Password")

    # ---------- SIGNUP ---------- #

    with tab2:

        st.subheader("Create Account")

        signup_email = st.text_input(
            "Email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button("Create Account"):

            success, message = register_user(
                signup_email,
                signup_password
            )

            if success:

                st.success(message)

            else:

                st.error(message)

else:

    user = get_user(
        st.session_state.user["id"]
    )            
    # ---------------- PROFILE ---------------- #

    if not profile_completed(user):

        st.title("👤 Complete Your Profile")

        username = st.text_input(
            "👤 Full Name",
            value=user["username"] or ""
        )

        student_class = st.text_input(
            "🎓 Class",
            value=user["student_class"] or ""
        )

        board = st.selectbox(
            "🏫 Board",
            [
                "State Board",
                "CBSE",
                "ICSE",
                "IB",
                "Other"
            ]
        )

        study_hours = st.slider(
            "⏰ Daily Study Hours",
            1,
            12,
            user["study_hours"] if user["study_hours"] else 2
        )

        goal = st.text_input(
            "🎯 Goal",
            value=user["goal"] or ""
        )

        weak_subjects = st.text_input(
            "📚 Weak Subjects",
            value=user["weak_subjects"] or ""
        )

        if st.button("💾 Save Profile"):

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
                # ---------------- SIDEBAR ---------------- #

        menu = st.sidebar.radio(
            "📚 Navigation",
            [
                "🏠 Dashboard",
                "📅 Study Plan",
                "🗓️ Timetable",
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
                "⚙️ Settings",
                "🤖 AI Agent"
            ]
        )

        st.sidebar.markdown("---")
        st.sidebar.write(f"👤 {user['username']}")
        st.sidebar.write(f"🎯 {user['goal']}")

        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.success("🤖 AI Powered Study Companion")

        # ---------------- DASHBOARD ---------------- #

        if menu == "🏠 Dashboard":

            st.title("🏠 Student Dashboard")

            st.success(f"Welcome back, {user['username']}! 🌸")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("🔥 Streak", user["streak"])

            with col2:
                st.metric("⭐ XP", user["xp"])

            with col3:
                st.metric("📚 Study Hours", user["study_hours"])

            with col4:
                st.metric("🎯 Goal", "Active")

            st.markdown("---")

            st.subheader("👤 Profile")

            st.info(f"""
👤 Name : {user['username']}

🎓 Class : {user['student_class']}

🏫 Board : {user['board']}

🎯 Goal : {user['goal']}

📚 Weak Subjects : {user['weak_subjects']}
""")

            st.markdown("---")

            st.subheader("📈 Overall Progress")

            progress = st.slider(
                "Completion",
                0,
                100,
                35
            )

            st.progress(progress / 100)

            st.markdown("---")

            st.subheader("✅ Today's Tasks")

            st.checkbox("📖 Finish today's study plan")
            st.checkbox("📝 Revise yesterday's lesson")
            st.checkbox("🎮 Play Memory Booster")
            st.checkbox("😴 Sleep before 10 PM")
                    # ---------------- STUDY PLAN ---------------- #

        elif menu == "📅 Study Plan":

            st.title("📅 AI Study Plan Generator")

            subject = st.text_input("📚 Subject")

            chapters = st.text_area(
                "📖 Chapters"
            )

            exam_date = st.date_input(
                "📅 Exam Date"
            )

            study_hours = st.slider(
                "⏰ Study Hours",
                1,
                12,
                user["study_hours"]
            )

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ]
            )

            if st.button("✨ Generate Study Plan"):

                result = generate_study_plan(
                    subject,
                    chapters,
                    exam_date,
                    study_hours,
                    difficulty,
                    user["goal"],
                    user["weak_subjects"],
                    user["student_class"],
                    user["board"]
                )

                st.markdown(result)

        # ---------------- TIMETABLE ---------------- #

        elif menu == "🗓️ Timetable":

            st.title("🗓️ Smart Timetable")

            study_hours = st.slider(
                "Study Hours",
                1,
                12,
                user["study_hours"],
                key="tt"
            )

            if st.button("Generate Timetable"):

                timetable = generate_timetable(
                    study_hours,
                    user["weak_subjects"]
                )

                st.markdown(timetable)
                        # ---------------- STUDY SESSION ---------------- #

        elif menu == "📖 Study Session":

            st.title("📖 AI Study Session Planner")

            subject = st.text_input("📚 Subject")
            chapter = st.text_input("📖 Chapter")

            study_hours = st.slider(
                "Study Hours",
                1,
                8,
                user["study_hours"],
                key="session"
            )

            energy = st.selectbox(
                "Energy Level",
                ["Low", "Medium", "High"]
            )

            goal = st.text_input("Today's Goal")

            if st.button("Generate Study Session"):

                session = generate_study_session(
                    subject,
                    chapter,
                    study_hours,
                    energy,
                    goal
                )

                st.markdown(session)

        # ---------------- SUBJECT PRIORITY ---------------- #

        elif menu == "📊 Subject Priority":

            st.title("📊 Subject Priority Analyzer")

            subjects = st.text_input(
                "Subjects (comma separated)"
            )

            exam_date = st.date_input(
                "Exam Date",
                key="priority_date"
            )

            if st.button("Analyze"):

                result = analyze_subject_priority(
                    subjects,
                    user["weak_subjects"],
                    exam_date,
                    user["goal"]
                )

                st.markdown(result)

        # ---------------- AI TUTOR ---------------- #

        elif menu == "🤖 AI Tutor":

            st.title("🤖 AI Tutor")

            subject = st.text_input(
                "Subject",
                key="ai_subject"
            )

            chapter = st.text_input(
                "Chapter",
                key="ai_chapter"
            )

            question = st.text_area(
                "Ask your question"
            )

            explain = st.selectbox(
                "Explanation Style",
                [
                    "Simple",
                                       "Detailed",
                    "Exam Oriented"
                ]
            )

            if st.button("Ask AI Tutor"):

                answer = ask_ai(
                    subject,
                    chapter,
                    question,
                    explain
                )

                st.markdown(answer)
                        # ---------------- AI NOTES ---------------- #

        elif menu == "📝 AI Notes":

            st.title("📝 AI Notes Generator")

            subject = st.text_input("📚 Subject")
            chapter = st.text_input("📖 Chapter")

            notes_type = st.selectbox(
                "Notes Type",
                [
                    "Short Notes",
                    "Detailed Notes",
                    "Revision Notes"
                ]
            )

            if st.button("Generate Notes"):

                notes = generate_notes(
                    subject,
                    chapter,
                    notes_type
                )

                st.markdown(notes)

        # ---------------- FLASHCARDS ---------------- #

        elif menu == "🧠 Flashcards":

            st.title("🧠 AI Flashcards")

            subject = st.text_input(
                "Subject",
                key="flash_subject"
            )

            chapter = st.text_input(
                "Chapter",
                key="flash_chapter"
            )

            cards = st.slider(
                "Number of Flashcards",
                5,
                30,
                10
            )

            if st.button("Generate Flashcards"):

                flashcards = generate_flashcards(
                    subject,
                    chapter,
                    cards
                )

                st.markdown(flashcards)

        # ---------------- STORY LEARNING ---------------- #

        elif menu == "📚 Story Learning":

            st.title("📚 Story Learning")

            topic = st.text_input("Enter Topic")

            if st.button("Generate Story"):

                story = generate_story(topic)

                st.markdown(story)

        # ---------------- QUIZ ---------------- #

        elif menu == "❓ Quiz":

            st.title("❓ AI Quiz Generator")

            subject = st.text_input(
                "Subject",
                key="quiz_subject"
            )

            chapter = st.text_input(
                "Chapter",
                key="quiz_chapter"
            )

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ]
            )

            questions = st.slider(
                "Questions",
                5,
                20,
                10
            )

            if st.button("Generate Quiz"):

                quiz = generate_quiz(
                    subject,
                    chapter,
                    difficulty,
                    questions
                )

                st.markdown(quiz)

        # ---------------- EXAM SIMULATOR ---------------- #

        elif menu == "🎯 Exam Simulator":

            st.title("🎯 AI Exam Simulator")

            subject = st.text_input(
                "Subject",
                key="exam_subject"
            )

            chapter = st.text_input(
                "Chapter",
                key="exam_chapter"
            )

            duration = st.slider(
                "Duration (Minutes)",
                30,
                180,
                60
            )

            marks = st.slider(
                "Marks",
                25,
                100,
                50
            )

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ]
            )

            if st.button("Generate Exam"):

                exam = generate_exam(
                    subject,
                    chapter,
                    duration,
                    marks,
                    difficulty
                )

                st.markdown(exam)
                        # ---------------- MEMORY BOOSTER ---------------- #

        elif menu == "🎮 Memory Booster":

            st.title("🎮 Memory Booster")

            topic = st.text_input("📚 Topic")

            level = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ]
            )

            if st.button("Start Memory Booster"):

                game = memory_booster(
                    topic,
                    level
                )

                st.markdown(game)

        # ---------------- PROGRESS ---------------- #

        elif menu == "📈 Progress":

            st.title("📈 Progress Tracker")

            st.subheader("📅 Weekly Study Chart")
            st.plotly_chart(
                weekly_chart(),
                use_container_width=True
            )

            st.subheader("📊 Monthly Progress")
            st.plotly_chart(
                monthly_chart(),
                use_container_width=True
            )

            completed = st.slider(
                "Completed Topics",
                0,
                100,
                35
            )

            progress = analyze_progress(
                completed
            )

            st.markdown(progress)

        # ---------------- REPORTS ---------------- #

        elif menu == "📄 Reports":

            st.title("📄 AI Reports")

            report = generate_report(user)

            st.markdown(report)

            if st.button("📥 Download PDF"):

                filename = create_pdf(
                    "AI Study Report",
                    report,
                    "study_report.pdf"
                )

                with open(filename, "rb") as file:

                    st.download_button(
                        "⬇ Download Report",
                        file,
                        file_name="study_report.pdf",
                        mime="application/pdf"
                    )

        # ---------------- SETTINGS ---------------- #

        elif menu == "⚙️ Settings":

            st.title("⚙️ Settings")

            st.info("Profile settings will be added here.")

            if st.button("Reset Progress"):

                st.warning("Feature coming soon.")

        # ---------------- AI AGENT ---------------- #

        elif menu == "🤖 AI Agent":

            st.title("🤖 Personal AI Study Agent")

            prompt = st.text_area(
                "Ask anything..."
            )

            if st.button("Ask Agent"):

                answer = ai_agent(
                    prompt
                )

                st.markdown(answer)
                
