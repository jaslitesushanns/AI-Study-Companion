import google.generativeai as genai
import os


def configure_gemini(api_key):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

    return model



def ask_gemini(model, prompt):

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error: {e}"



def clean_response(text):

    if text is None:
        return ""

    return text.strip()
