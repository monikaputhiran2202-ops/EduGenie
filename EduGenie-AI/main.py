from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="EduGenie AI",
    description="AI-powered educational assistant",
    version="1.0.0"
)


# =========================================================
# Request Models
# =========================================================

class QuizRequest(BaseModel):
    topic: str = "General Knowledge"
    difficulty: str = "medium"
    number_of_questions: int = 5


# =========================================================
# HOME
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EduGenie AI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                text-align: center;
                padding-top: 100px;
            }

            .container {
                background: white;
                width: 500px;
                margin: auto;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }

            h1 {
                color: #4f46e5;
            }

            p {
                color: #555;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>EduGenie AI</h1>

            <p>
                AI-powered educational assistant
            </p>

            <p>
                Backend is running successfully!
            </p>

            <p>
                Open <b>/docs</b> to test the API.
            </p>

        </div>

    </body>
    </html>
    """


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health_check():
    return {
        "status": "success",
        "message": "EduGenie AI backend is running"
    }


# =========================================================
# QUIZ ENDPOINT
# =========================================================

@app.post("/quiz")
async def generate_quiz(request: QuizRequest):

    topic = request.topic
    difficulty = request.difficulty
    number_of_questions = request.number_of_questions

    # Prevent invalid question count
    if number_of_questions < 1:
        number_of_questions = 1

    if number_of_questions > 20:
        number_of_questions = 20

    # Temporary quiz response
    # Later Gemini AI can be connected here.

    questions = []

    for i in range(1, number_of_questions + 1):

        questions.append({
            "question_number": i,
            "question": f"What is an important concept related to {topic}?",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A"
        })

    return {
        "success": True,
        "topic": topic,
        "difficulty": difficulty,
        "number_of_questions": number_of_questions,
        "questions": questions
    }


# =========================================================
# SIMPLE QUIZ TEST ENDPOINT
# =========================================================

@app.get("/quiz")
async def quiz_get():

    return {
        "success": True,
        "message": "Quiz API is working!",
        "endpoint": "POST /quiz",
        "example_request": {
            "topic": "Python",
            "difficulty": "easy",
            "number_of_questions": 5
        }
    }


# =========================================================
# STUDY ENDPOINT
# =========================================================

@app.post("/study")
async def study_topic(request: Request):

    try:
        data = await request.json()
    except Exception:
        data = {}

    topic = data.get("topic", "General Studies")

    return {
        "success": True,
        "topic": topic,
        "message": f"Study material for {topic} will be generated here."
    }


# =========================================================
# SUMMARY ENDPOINT
# =========================================================

@app.post("/summary")
async def generate_summary(request: Request):

    try:
        data = await request.json()
    except Exception:
        data = {}

    text = data.get("text", "")

    if not text:
        return {
            "success": False,
            "message": "Please provide text to summarize."
        }

    return {
        "success": True,
        "summary": text[:500]
    }


# =========================================================
# RUN INFORMATION
# =========================================================

@app.get("/api")
async def api_info():

    return {
        "project": "EduGenie AI",
        "version": "1.0.0",
        "status": "running",
        "available_endpoints": [
            "GET /",
            "GET /health",
            "GET /docs",
            "GET /quiz",
            "POST /quiz",
            "POST /study",
            "POST /summary"
        ]
    }