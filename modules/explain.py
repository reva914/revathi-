"""
Explanation Module
-------------------
EduGenie utilizes the LaMini-Flan-T5-783M model, a lightweight yet powerful
local generative model, to deliver simplified, context-aware explanations of
any topic. Because it runs locally (CPU-compatible, works well on Mac M1),
it needs no API key and adds no external cost for this module.

The model is downloaded once (a few hundred MB) the first time this module
is used, then cached by Hugging Face locally for subsequent runs.
"""

from transformers import pipeline

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

_explainer = None  # lazy-loaded singleton so the app starts up fast


def _get_explainer():
    global _explainer
    if _explainer is None:
        _explainer = pipeline("text2text-generation", model=MODEL_NAME)
    return _explainer


def explain_topic(topic: str) -> str:
    """Generate a simple, beginner-friendly explanation of a topic."""
    topic = (topic or "").strip()
    if not topic:
        return "Please enter a topic to explain."

    prompt = (
        f"Explain the concept of '{topic}' in simple, clear language "
        "suitable for a beginner student. Keep it concise."
    )

    try:
        explainer = _get_explainer()
        result = explainer(prompt, max_length=256, do_sample=False)
        return result[0]["generated_text"].strip()
    except Exception as e:
        return f"Error generating explanation: {e}"
