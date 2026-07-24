import streamlit as st
import os
from auth import *
from database import *
from modules import *

st.set_page_config(
    page_title="AI Study Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

def load_css():
    if os.path.exists("style.css"):
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

st.markdown(
"""
<div class="main-title">
🌈 AI Study Companion
</div>
<div class="subtitle">
Your Personal AI Learning Partner 🤖
</div>
""",
unsafe_allow_html=True
)

if not st.session_state.logged_in:

    choice = st.sidebar.selectbox(
        "Choose",
        [
            "Login",
            "Sign Up"
        ]
    )

    if choice == "Sign Up":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.header("📝 Create Account")

        email = st.text_input("📧 Email")

        password = st.text_input(
            "🔒 Password",
            type="password"
        )

        confirm = st.text_input(
            "✅ Confirm Password",
            type="password"
        )

        if st.button("Create Account 🚀"):

            if password != confirm:
                st.error("Passwords do not match.")

            elif len(password) < 6:
                st.error("Password should be at least 6 characters.")

            else:

                success, msg = register_user(
                    email,
                    password
                )

                if success:
                    st.success(msg)

                else:
                    st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.header("🔐 Login")

        email = st.text_input("📧 Email")

        password = st.text_input(
            "🔒 Password",
            type="password"
        )

        if st.button("Login 💖"):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user

                st.rerun()

            else:

                st.error("Invalid Email or Password.")

        st.markdown("</div>", unsafe_allow_html=True)

else:

    user = get_user(
        st.session_state.user["id"]
    )

    st.session_state.user = user
    # ---------------- PROFILE ---------------- #

    if not profile_completed(user):

        st.header("👤 Complete Your Profile")

        username = st.text_input("👤 Username")

        student_class = st.selectbox(
            "🎓 Class",
            [
                "6","7","8","9","10","11","12","College"
            ]
        )

        board = st.selectbox(
            "📚 Board",
            [
                "State Board",
                "CBSE",
                "ICSE",
                "IB",
                "Other"
            ]
        )

        study_hours = st.slider(
            "⏰ Study Hours",
            1,
            12,
            2
        )

        goal = st.text_input(
            "🎯 Goal"
        )

        weak_subjects = st.text_input(
            "📖 Weak Subjects (comma separated)"
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
                    # ---------------- DASHBOARD ---------------- #

        if menu == "🏠 Dashboard":

            st.title("🏠 Dashboard")

            st.success(f"Welcome back, {user['username']}! 🌸")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("""
                <div class="small-card">
                    <h3>🔥 Study Streak</h3>
                    <h1>0 Days</h1>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="small-card">
                    <h3>⭐ XP Points</h3>
                    <h1>{user['xp']}</h1>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="small-card">
                    <h3>⏰ Study Hours</h3>
                    <h1>{user['study_hours']}</h1>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            st.subheader("📌 Today's Goal")
            st.info(user["goal"])

            st.subheader("📚 Weak Subjects")
            st.warning(user["weak_subjects"])

            st.subheader("🤖 AI Recommendation")

            st.success(
                f"""
Study for **{user['study_hours']} hour(s)** today.

Start with:

📖 {user['weak_subjects']}

Stay focused and complete today's goal:
🎯 {user['goal']}
"""
            )

            st.markdown("---")

            st.subheader("🔔 Today's Reminders")

            st.info("📚 Finish today's study session.")
            st.info("💧 Drink water every hour.")
            st.info("😴 Take a 10-minute break after 50 minutes.")
            st.info("📝 Revise before sleeping.")

            st.markdown("---")

            st.subheader("📈 Progress")

            progress = st.slider(
                "Overall Progress",
                0,
                100,
                35
            )

            st.progress(progress / 100)

            st.balloons()
                    # ---------------- STUDY PLAN ---------------- #

      elif menu == "📅 Study Plan":

    st.title("📅 AI Study Plan")

    subject = st.text_input("📚 Subject")

    chapters = st.text_area(
        "📖 Chapter(s) / Lesson(s)",
        placeholder="Example:\nChapter 1 - Electricity\nChapter 2 - Magnetism"
    )

    exam_date = st.date_input("📅 Exam Date")

    study_hours = st.slider(
        "⏰ Study Hours Per Day",
        1,
        12,
        user["study_hours"]
    )

    difficulty = st.selectbox(
        "🎯 Difficulty Level",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    if st.button("✨ Generate Study Plan"):

        plan = generate_study_plan(
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

        st.markdown(plan)
        # ---------------- TIMETABLE ---------------- #
elif menu == "🗓️ Timetable":

    st.title("🗓️ AI Smart Timetable")

    wake_up = st.time_input("🌅 Wake-up Time")

    school_start = st.time_input("🏫 School/College Start Time")

    school_end = st.time_input("🏫 School/College End Time")

    tuition = st.text_input("📚 Tuition Timing (Optional)")

    hobbies = st.text_input("🎮 Hobbies")

    sleep = st.time_input("😴 Sleep Time")

    study_hours = st.slider(
        "⏰ Study Hours Per Day",
        1,
        12,
        user["study_hours"]
    )

    if st.button("✨ Generate Smart Timetable"):

        timetable = generate_timetable(
            wake_up,
            school_start,
            school_end,
            tuition,
            hobbies,
            sleep,
            study_hours,
            user["weak_subjects"],
            user["goal"]
        )

        st.markdown(timetable)
       

        # ---------------- STUDY SESSION ---------------- #

        elif menu == "📖 Study Session":

    st.title("📖 AI Study Session Planner")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter / Lesson")

    study_hours = st.slider(
        "⏰ Study Duration (Hours)",
        1,
        8,
        user["study_hours"]
    )

    energy = st.selectbox(
        "⚡ Energy Level",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    goal = st.text_input(
        "🎯 Today's Goal",
        placeholder="Example: Finish Chapter 5"
    )

    if st.button("🚀 Generate Study Session"):

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

    st.title("📊 AI Subject Priority Analyzer")

    subjects = st.text_input("📚 Subjects")

    weak_subjects = st.text_input("💪 Weak Subjects")

    exam_date = st.date_input("📅 Exam Date")

    goal = st.text_input("🎯 Goal")

    if st.button("📊 Analyze Priority"):

        result = analyze_subject_priority(
            subjects,
            weak_subjects,
            exam_date,
            goal
        )

        st.markdown(result)
                        # ---------------- AI TUTOR ---------------- #

        elif menu == "🤖 AI Tutor":

    st.title("🤖 AI Study Tutor")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter")

    question = st.text_area(
        "❓ Ask your question"
    )

    explain = st.selectbox(
        "Explain as",
        [
            "Simple",
            "Detailed",
            "Exam Point of View"
        ]
    )

    if st.button("💬 Ask AI"):

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

            topic = st.text_input("Topic")

            if st.button("📖 Generate Notes"):

                notes = generate_notes(topic)

                st.markdown(notes)

        # ---------------- FLASHCARDS ---------------- #

        elif menu == "🧠 Flashcards":

            st.title("🧠 AI Flashcards")

            topic = st.text_input("Flashcard Topic")

            if st.button("🎴 Generate Flashcards"):

                flashcards = generate_flashcards(topic)

                st.markdown(flashcards)

        # ---------------- STORY LEARNING ---------------- #

        elif menu == "📚 Story Learning":

            st.title("📚 AI Story Learning")

            topic = st.text_input("Concept")

            if st.button("📖 Create Story"):

                story = generate_story(topic)

                st.markdown(story)

        # ---------------- QUIZ ---------------- #

        elif menu == "❓ Quiz":

            st.title("❓ AI Quiz Generator")

            subject = st.text_input("Subject")

            if st.button("📝 Generate Quiz"):

                quiz = generate_quiz(subject)

                st.markdown(quiz)

        # ---------------- EXAM SIMULATOR ---------------- #

        elif menu == "🎯 Exam Simulator":

            st.title("🎯 Exam Simulator")

            subject = st.text_input("Exam Subject")

            if st.button("🚀 Start Exam"):

                exam = generate_exam(subject)

                st.markdown(exam)

            # ---------------- MEMORY BOOSTER ---------------- #

        elif menu == "🎮 Memory Booster":

            st.title("🎮 Memory Booster")

            topic = st.text_input(
                "📚 Enter topic"
            )

            if st.button("🧠 Create Memory Game"):

                result = memory_booster(topic)

                st.markdown(result)


        # ---------------- PROGRESS ---------------- #

        elif menu == "📈 Progress":

            st.title("📈 My Progress")

            score = st.number_input(
                "Your Score",
                min_value=0,
                value=8
            )

            total = st.number_input(
                "Total Marks",
                min_value=1,
                value=10
            )

            if st.button("📊 Analyze Progress"):

                result = analyze_progress(
                    score,
                    total
                )

                st.markdown(result)


        # ---------------- REPORTS ---------------- #

        elif menu == "📄 Reports":

            st.title("📄 Student Reports")

            subject = st.text_input(
                "📚 Subject"
            )

            score = st.number_input(
                "Score",
                min_value=0
            )

            total = st.number_input(
                "Total",
                min_value=1
            )

            if st.button("📝 Generate Report"):

                report = generate_report(
                    subject,
                    score,
                    total
                )

                st.markdown(report)

                st.download_button(
                    "📥 Download Report",
                    report,
                    file_name="study_report.txt"
                )
        # ---------------- AI AGENT ---------------- #

        elif menu == "🤖 AI Agent":

            st.title("🤖 AI Study Agent")

            question = st.text_area(
                "Ask your AI Agent anything 📚"
            )

            if st.button("🚀 Ask Agent"):

                if question:

                    answer = ask_ai(question)

                    st.success("AI Response")

                    st.write(answer)

                else:
                    st.warning("Enter a question first.")
                            # ---------------- SETTINGS ---------------- #

        elif menu == "⚙️ Settings":

            st.title("⚙️ Settings")

            st.subheader("👤 Profile Information")

            st.write(
                f"Username: {user['username']}"
            )

            st.write(
                f"Class: {user['student_class']}"
            )

            st.write(
                f"Board: {user['board']}"
            )

            st.write(
                f"Study Goal: {user['goal']}"
            )


            st.subheader("🎨 Theme")

            st.info(
                "Your AI Study Companion uses a colorful student-friendly theme 🌈"
            )


            st.subheader("🔔 Reminder Settings")

            reminder = st.checkbox(
                "Enable daily study reminders",
                value=True
            )

            if reminder:
                st.success(
                    "Daily reminders enabled 🔔"
                )
            else:
                st.warning(
                    "Reminders disabled"
                )
                
