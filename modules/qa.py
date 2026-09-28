"""
QnA Module
----------
EduGenie is powered by Gemini 1.5 Pro, enabling it to handle a wide range of
general knowledge and academic question-answering tasks with precision.
"""

import os
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def get_answer(question: str) -> str:
    """Send a question to Gemini 1.5 Pro and return a concise answer."""
    question = (question or "").strip()
    if not question:
        return "Please enter a question."

    if not API_KEY:
        return "Error: GEMINI_API_KEY is not set. Add it to your .env file."

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = (
            "Answer the following question clearly, accurately, and concisely, "
            "in a way a student could easily understand:\n\n"
            f"{question}"
        )
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No answer was returned."
    except Exception as e:
        return f"Error generating answer: {e}"