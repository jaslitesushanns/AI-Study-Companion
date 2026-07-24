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

    st.success("Login Successful 🎉")

    st.write("Welcome!")

    st.write(st.session_state.user["email"])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
        
