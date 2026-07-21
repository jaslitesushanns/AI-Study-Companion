import streamlit as st
from database import create_database
from auth import register_user, login_user
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
