"""
EduGenie: Google Gemini Powered Learning Assistant
FastAPI backend entrypoint.

Run with:  uvicorn main:app --reload
Then open: http://127.0.0.1:8000
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load GEMINI_API_KEY (and any other vars) from .env BEFORE importing the
# modules below — each module reads the key at import time, so .env must
# already be loaded into the environment by that point.
load_dotenv()

from modules import qa, explain, quiz, summary, learning_path

app = FastAPI(title="EduGenie", description="Google Gemini Powered Learning Assistant")

# Static files (CSS/JS) and HTML templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------------
# Frontend page
# ---------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------------------------------------------------
# API endpoints (one per module, as per project spec)
# ---------------------------------------------------------------------

@app.post("/qa")
async def qa_endpoint(question: str = Form(...)):
    """Q&A module — powered by Gemini 1.5 Pro."""
    answer = qa.get_answer(question)
    return JSONResponse({"result": answer})


@app.post("/explain")
async def explain_endpoint(topic: str = Form(...)):
    """Explanation module — powered by local LaMini-Flan-T5-783M."""
    explanation = explain.explain_topic(topic)
    return JSONResponse({"result": explanation})


@app.post("/quiz")
async def quiz_endpoint(passage: str = Form(...)):
    """Quiz module — Gemini generates 3 MCQs (4 options each) as JSON."""
    questions = quiz.generate_quiz(passage)
    return JSONResponse({"result": questions})


@app.post("/summarize")
async def summarize_endpoint(content: str = Form(...)):
    """Summary module — powered by Gemini 1.5 Pro."""
    result = summary.summarize_text(content)
    return JSONResponse({"result": result})


@app.post("/learn/recommendations")
async def learn_endpoint(topic: str = Form(...)):
    """Learning Path module — beginner-to-advanced roadmap via Gemini."""
    result = learning_path.get_learning_recommendations(topic)
    return JSONResponse({"result": result})


# ---------------------------------------------------------------------
# Simple health check (useful for testing the server is alive)
# ---------------------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}