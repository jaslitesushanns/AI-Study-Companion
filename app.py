import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

from utils import *
from modules import *

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Powered Study Companion",
    page_icon="📚",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #f5f7ff;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:50px;
    background:#4f46e5;
    color:white;
    font-size:17px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#4338ca;
}

div[data-testid="stSidebar"]{
    background:#111827;
}

div[data-testid="stSidebar"] *{
    color:white;
}

h1,h2,h3{
    color:#1f2937;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI ---------------- #

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None
    
