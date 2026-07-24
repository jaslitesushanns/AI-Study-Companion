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

        st.sidebar.markdown("---")

        st.sidebar.success("🤖 AI Study Companion")

        st.sidebar.caption("Version 2.0")

        st.sidebar.caption("Made with ❤️ using Streamlit")
                    # ---------------- DASHBOARD ---------------- #

      # ---------------- DASHBOARD ---------------- #

if menu == "🏠 Dashboard":

    st.title("🏠 Student Dashboard")

    st.success(f"Welcome back, {user['username']}! 🌸")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🔥 Streak", "12 Days")

    with col2:
        st.metric("⭐ XP", user["xp"])

    with col3:
        st.metric("📚 Study Hours", user["study_hours"])

    with col4:
        st.metric("🎯 Goal", "Active")

    st.markdown("---")

    st.subheader("📖 Profile")

    st.info(f"""
👤 Name : {user['username']}

🎓 Class : {user['student_class']}

🏫 Board : {user['board']}

🎯 Goal : {user['goal']}

💪 Weak Subjects : {user['weak_subjects']}
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

    st.subheader("📌 Today's Tasks")

    st.checkbox("📖 Finish today's study plan")

    st.checkbox("📝 Revise yesterday's chapter")

    st.checkbox("🎮 Play Memory Booster")
    if menu == "🏠 Dashboard":
        st.checkbox("😴 Sleep before 10 PM")
                    # ---------------- STUDY PLAN ---------------- #

     elif menu == "📅 Study Plan":
         st.title("📅 AI Study Plan")

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
        st.success("Study Plan Generated Successfully! 🎉")
        st.markdown(plan)
        st.balloons()
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

       st.success("Timetable Generated Successfully! 🎉")

st.markdown(timetable)

st.balloons()
       

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

        st.success("Study Session Generated Successfully! 🎉")

st.markdown(session)

st.balloons()

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

       st.success("Analysis Completed! 🎉")

st.markdown(result)

st.balloons()
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

        st.success("Response Generated! 🎉")

st.markdown(answer)

st.balloons()
        # ---------------- AI NOTES ---------------- #

        elif menu == "📝 AI Notes":

    st.title("📝 AI Notes Generator")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter / Lesson")

    notes_type = st.selectbox(
        "📄 Notes Type",
        [
            "Short Notes",
            "Detailed Notes",
            "Exam Revision Notes"
        ]
    )

    if st.button("📖 Generate Notes"):

        notes = generate_notes(
            subject,
            chapter,
            notes_type
        )

        st.success("Notes Generated! 🎉")

st.markdown(notes)

st.balloons()
        # ---------------- FLASHCARDS ---------------- #

        elif menu == "🧠 Flashcards":

    st.title("🧠 AI Flashcards")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter")

    cards = st.slider(
        "🎴 Number of Flashcards",
        5,
        30,
        10
    )

    if st.button("🎴 Generate Flashcards"):

        flashcards = generate_flashcards(
            subject,
            chapter,
            cards
        )

        st.success("Flashcards Generated! 🎉")

st.markdown(flashcards)

st.balloons()

        # ---------------- STORY LEARNING ---------------- #

       elif menu == "📚 Story Learning":

    st.title("📚 AI Story Learning")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter")

    age = st.selectbox(
        "👦 Student Level",
        [
            "Primary",
            "Middle School",
            "High School",
            "College"
        ]
    )

    if st.button("📖 Generate Story"):

        story = generate_story(
            subject,
            chapter,
            age
        ) 

        st.success("Story Generated! 🎉")

st.markdown(story)

st.balloons()

        # ---------------- QUIZ ---------------- #

       elif menu == "❓ Quiz":

    st.title("❓ AI Quiz Generator")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter")

    difficulty = st.selectbox(
        "🎯 Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    questions = st.slider(
        "📝 Number of Questions",
        5,
        30,
        10
    )

    if st.button("📝 Generate Quiz"):

        quiz = generate_quiz(
            subject,
            chapter,
            difficulty,
            questions
        )

        st.success("Quiz Generated! 🎉")

st.markdown(quiz)

st.balloons()

        # ---------------- EXAM SIMULATOR ---------------- #

      elif menu == "🎯 Exam Simulator":

    st.title("🎯 AI Exam Simulator")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter")

    duration = st.slider(
        "⏰ Exam Duration (Minutes)",
        30,
        180,
        60
    )

    marks = st.slider(
        "📝 Total Marks",
        25,
        100,
        50
    )

    difficulty = st.selectbox(
        "🎯 Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    if st.button("🚀 Generate Exam Paper"):

        exam = generate_exam(
            subject,
            chapter,
            duration,
            marks,
            difficulty
        )

        st.success("Exam Paper Generated! 🎉")

st.markdown(exam)

st.balloons()

            # ---------------- MEMORY BOOSTER ---------------- #

        elif menu == "🎮 Memory Booster":

    st.title("🎮 AI Memory Booster")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter")

    game = st.selectbox(
        "🎲 Game Type",
        [
            "Memory Match",
            "Fill in the Blanks",
            "Guess the Word",
            "Rapid Recall"
        ]
    )

    if st.button("🧠 Generate Game"):

        result = memory_booster(
            subject,
            chapter,
            game
        )

        st.success("Memory Game Generated! 🎉")

st.markdown(result)

st.balloons()


        # ---------------- PROGRESS ---------------- #

       elif menu == "📈 Progress":

    st.title("📈 AI Progress Tracker")

    subject = st.text_input("📚 Subject")

    completed = st.number_input(
        "✅ Completed Topics",
        min_value=0,
        value=0
    )

    total = st.number_input(
        "📖 Total Topics",
        min_value=1,
        value=10
    )

    hours = st.number_input(
        "⏰ Study Hours Completed",
        min_value=0,
        value=0
    )

    if st.button("📊 Analyze Progress"):

        result = analyze_progress(
            subject,
            completed,
            total,
            hours
        )

       st.success("Progress Analysis Completed! 🎉")

st.markdown(result)

st.balloons()

        progress = completed / total

        st.progress(progress)

        st.metric(
            "Completion",
            f"{progress*100:.1f}%"
        )


        # ---------------- REPORTS ---------------- #

        elif menu == "📄 Reports":

    st.title("📄 AI Study Report")

    subject = st.text_input("📚 Subject")

    completed = st.number_input(
        "Completed Topics",
        min_value=0
    )

    total = st.number_input(
        "Total Topics",
        min_value=1
    )

    if st.button("📄 Generate Report"):

        report = generate_report(
            subject,
            completed,
            total
        )

       st.success("Report Generated! 🎉")

st.markdown(report)

st.balloons()

        st.download_button(
            "⬇ Download Report",
            report,
            file_name="study_report.txt"
        )
        # ---------------- AI AGENT ---------------- #

      elif menu == "🤖 AI Agent":

    st.title("🤖 Personal AI Study Agent")

    subject = st.text_input("📚 Subject")

    chapter = st.text_input("📖 Chapter")

    mood = st.selectbox(
        "😊 Current Mood",
        [
            "Happy",
            "Confused",
            "Stressed",
            "Tired",
            "Motivated"
        ]
    )

    question = st.text_area(
        "💬 What do you need help with?"
    )

    if st.button("🚀 Ask AI Agent"):

        answer = ai_agent(
            subject,
            chapter,
            mood,
            question,
            user["goal"],
            user["weak_subjects"]
        )

      st.success("AI Agent Response Ready! 🎉")

st.markdown(answer)

st.balloons()
                            # ---------------- SETTINGS ---------------- #

       elif menu == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.subheader("🎨 Theme")

    theme = st.selectbox(
        "Choose Theme",
        [
            "Light",
            "Dark",
            "Blue",
            "Purple",
            "Green"
        ]
    )

    st.subheader("🔔 Notifications")

    reminder = st.checkbox(
        "Enable Study Reminder",
        value=True
    )

    st.subheader("🎵 Study Music")

    music = st.selectbox(
        "Music",
        [
            "Lo-fi",
            "Rain",
            "Nature",
            "Piano",
            "None"
        ]
    )

    if st.button("💾 Save Settings"):
        st.success("Settings Saved Successfully ✅")
        
