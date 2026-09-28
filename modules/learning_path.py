"""
Learning Path Module
----------------------
get_learning_recommendations() uses Google Gemini to generate a personalized,
structured learning path for any given topic — from beginner to advanced —
organized by difficulty and supported with resources (videos, articles,
books). Handles API errors gracefully.
"""

import os
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def get_learning_recommendations(topic: str) -> str:
    """Generate a structured beginner -> advanced learning path for a topic."""
    topic = (topic or "").strip()
    if not topic:
        return "Please enter a topic to get learning recommendations."

    if not API_KEY:
        return "Error: GEMINI_API_KEY is not set. Add it to your .env file."

    prompt = (
        f"Create a structured learning path for someone who wants to learn "
        f"'{topic}', progressing from beginner to advanced. For each level "
        "(Beginner, Intermediate, Advanced) include:\n"
        "- Estimated time to complete\n"
        "- Key topics to learn\n"
        "- 2-3 recommended resources (books, courses, sites, or videos)\n\n"
        "End with a short list of adaptive learning tips. "
        "Format the response with clear headings for readability."
    )

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        if not response or not response.text:
            return "The model did not return a valid learning path. Please try again."
        return response.text.strip()
    except Exception as e:
        return f"Error generating learning recommendations: {e}"