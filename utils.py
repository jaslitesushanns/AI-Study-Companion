import random
from datetime import datetime


# -----------------------------
# Greeting Message
# -----------------------------
def get_greeting():
    hour = datetime.now().hour

    if hour < 12:
        return "🌞 Good Morning!"

    elif hour < 17:
        return "☀️ Good Afternoon!"

    else:
        return "🌙 Good Evening!"


# -----------------------------
# Progress Calculator
# -----------------------------
def calculate_progress(completed, total):
    if total == 0:
        return 0

    return round((completed / total) * 100, 2)


# -----------------------------
# Study Streak
# -----------------------------
def calculate_streak(days):
    return max(0, days)


# -----------------------------
# Motivational Quotes
# -----------------------------
def get_motivation():
    quotes = [
        "📚 Success is the sum of small efforts repeated every day.",
        "🎯 Stay focused. Your future self will thank you.",
        "💪 Every chapter you complete brings you closer to your goal.",
        "🌟 Believe in yourself. You are capable of amazing things.",
        "🚀 Dream big. Study smart. Achieve more."
    ]

    return random.choice(quotes)


# -----------------------------
# Timer Formatter
# -----------------------------
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


# -----------------------------
# Validate Email
# -----------------------------
def validate_email(email):
    return "@" in email and "." in email


# -----------------------------
# Validate Password
# -----------------------------
def validate_password(password):
    return len(password) >= 6
