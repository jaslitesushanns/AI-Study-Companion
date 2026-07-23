import streamlit as st

from database import create_database, save_student
from auth import (
    create_users_table,
    register_user,
    login_user
)

from utils import configure_gemini

from modules import (
    generate_study_plan,
    generate_smart_timetable,
    analyze_subject_priority,
    generate_study_session,
    generate_quiz,
    generate_progress,
    generate_motivation,
    ask_ai,
    study_notifications
)


# ---------------------------
# Database Setup
# ---------------------------

create_database()
create_users_table()


# ---------------------------
# Page Setup
# ---------------------------

st.set_page_config(
    page_title="AI Study Companion",
    page_icon="📚",
    layout="wide"
)


# ---------------------------
# CSS
# ---------------------------

st.markdown("""
<style>

.main {
background-color:#f5f7ff;
}

h1 {
color:#4b4bff;
}

.stButton button {

background:#6c63ff;
color:white;
border-radius:10px;

}

</style>
""",
unsafe_allow_html=True)



# ---------------------------
# Session
# ---------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False



# ---------------------------
# Login / Register
# ---------------------------

if not st.session_state.logged_in:

    st.title("📚 AI Powered Study Companion")


    choice = st.selectbox(
        "Choose",
        [
            "Login",
            "Register"
        ]
    )


    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )


    if choice=="Register":

        if st.button("Create Account"):

            if register_user(username,password):
                st.success(
                    "Account created!"
                )

            else:
                st.error(
                    "Username already exists"
                )


    else:

        if st.button("Login"):

            if login_user(username,password):

                st.session_state.logged_in=True
                st.success(
                    "Login successful"
                )
                st.rerun()

            else:
                st.error(
                    "Wrong username/password"
                )


    st.stop()



# ---------------------------
# Sidebar
# ---------------------------


st.sidebar.title(
    "⚙️ Settings"
)


api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)


model=None

if api_key:

    model=configure_gemini(
        api_key
    )



page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Study Plan",
        "Smart Timetable",
        "Subject Priority",
        "Study Session",
        "Quiz Generator",
        "Progress Tracker",
        "Motivation",
        "AI Assistant"
    ]
)



# ---------------------------
# Dashboard
# ---------------------------

if page=="Dashboard":

    st.title(
        "🎓 Student Dashboard"
    )


    name=st.text_input(
        "Student Name"
    )

    age=st.number_input(
        "Age",
        min_value=1
    )

    course=st.text_input(
        "Class / Course"
    )

    percentage=st.number_input(
        "Percentage"
    )

    board=st.text_input(
        "Board"
    )

    hours=st.text_input(
        "Daily Study Hours"
    )

    goal=st.text_input(
        "Goal"
    )

    weak=st.text_input(
        "Weak Subjects"
    )


    if st.button("Save Profile"):

        save_student(
            name,
            age,
            course,
            percentage,
            board,
            hours,
            goal,
            weak
        )

        st.success(
            "Profile Saved"
        )



# ---------------------------
# AI Modules
# ---------------------------

elif page=="Study Plan":

    st.header(
        "📅 Study Plan Generator"
    )

    if model:

        if st.button("Generate"):

            result=generate_study_plan(
                model,
                name,
                course,
                board,
                percentage,
                hours,
                goal,
                weak
            )

            st.markdown(result)


elif page=="Smart Timetable":

    st.header(
        "🕒 Smart Timetable"
    )

    if model:

        if st.button("Generate"):

            st.markdown(
                generate_smart_timetable(
                    model,
                    course,
                    hours,
                    weak
                )
            )


elif page=="Subject Priority":

    st.header(
        "📊 Subject Analyzer"
    )

    if model:

        st.markdown(
            analyze_subject_priority(
                model,
                percentage,
                weak,
                goal
            )
        )


elif page=="Study Session":

    st.header(
        "⏳ Study Session Planner"
    )

    if model:

        st.markdown(
            generate_study_session(
                model,
                hours
            )
        )


elif page=="Quiz Generator":

    st.header(
        "📝 AI Quiz"
    )

    subject=st.text_input(
        "Subject"
    )

    if model:

        st.markdown(
            generate_quiz(
                model,
                subject,
                course
            )
        )


elif page=="Progress Tracker":

    st.header(
        "📈 Progress"
    )

    completed=st.number_input(
        "Completed Topics"
    )

    total=st.number_input(
        "Total Topics"
    )

    if model:

        st.markdown(
            generate_progress(
                model,
                completed,
                total
            )
        )


elif page=="Motivation":

    st.header(
        "🔥 Motivation"
    )

    if model:

        st.write(
            generate_motivation(
                model,
                goal
            )
        )


elif page=="AI Assistant":

    st.header(
        "🤖 Ask AI"
    )

    question=st.text_input(
        "Your Question"
    )

    if model:

        st.write(
            ask_ai(
                model,
                question
            )
        )


st.sidebar.info(
    study_notifications()
)
