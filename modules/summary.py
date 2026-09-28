"""
Summary Module
---------------
Leverages Gemini's generative capabilities to summarize long educational
passages into concise, easy-to-understand versions — ideal for quick
revision — while retaining core information and eliminating redundancy.
"""

import os
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def summarize_text(content: str) -> str:
    """Summarize a long passage into a short, clear summary."""
    content = (content or "").strip()
    if not content:
        return "Please paste some content to summarize."

    if not API_KEY:
        return "Error: GEMINI_API_KEY is not set. Add it to your .env file."

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = (
            "Summarize the following educational content into a short, clear "
            "summary (3-5 sentences). Retain the key facts and ideas, and "
            "remove redundancy:\n\n"
            f"{content}"
        )
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No summary was returned."
    except Exception as e:
        return f"Error generating summary: {e}"