"""
Quiz Module
-----------
EduGenie generates three multiple-choice questions (MCQs) from a given
passage or topic, each containing four carefully crafted options. It uses
Gemini 1.5 Pro to comprehend the context and produce relevant questions with
plausible distractors. The output is structured JSON for easy frontend
integration.
"""

import os
import re
import json
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def clean_json_block(text: str) -> str:
    """Strip Markdown code fences (```json ... ```) that Gemini sometimes wraps around JSON."""
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()
    return text


def generate_quiz(passage: str):
    """
    Generate exactly 3 MCQs (4 options each) from the given passage/topic.

    Returns either:
      - a list of dicts: [{"question": ..., "options": [...], "answer_index": int}, ...]
      - a dict: {"error": "..."} on failure
    """
    passage = (passage or "").strip()
    if not passage:
        return {"error": "Please provide a passage or topic to generate a quiz."}

    if not API_KEY:
        return {"error": "GEMINI_API_KEY is not set. Add it to your .env file."}

    prompt = (
        "Based on the following passage or topic, generate exactly 3 multiple-choice "
        "questions (MCQs). Each question must have exactly 4 options, with only one "
        "correct answer. Respond ONLY with valid JSON — no markdown, no explanations, "
        "no extra text — in exactly this shape:\n\n"
        '[\n'
        '  {"question": "...", "options": ["A", "B", "C", "D"], "answer_index": 0},\n'
        '  {"question": "...", "options": ["A", "B", "C", "D"], "answer_index": 1},\n'
        '  {"question": "...", "options": ["A", "B", "C", "D"], "answer_index": 2}\n'
        ']\n\n'
        "answer_index is the zero-based index of the correct option.\n\n"
        f"Passage/topic:\n{passage}"
    )

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        cleaned = clean_json_block(response.text)
        questions = json.loads(cleaned)

        # Basic validation of the expected shape
        if not isinstance(questions, list) or len(questions) == 0:
            return {"error": "Gemini did not return a valid list of questions."}
        for q in questions:
            if "question" not in q or "options" not in q or "answer_index" not in q:
                return {"error": "Gemini's response was missing required quiz fields."}

        return questions
    except json.JSONDecodeError as e:
        return {"error": f"Could not parse quiz JSON from the model response: {e}"}
    except Exception as e:
        return {"error": f"Error generating quiz: {e}"}