from gemini_client import generate_text


def answer_question(question: str) -> str:
    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question accurately and clearly.

Rules:
- Give a direct answer.
- Explain important reasoning when necessary.
- Use simple language.
- Use examples when useful.
- Do not make the answer unnecessarily long.
- If the question is ambiguous, clearly mention the assumption.

Student Question:

{question}
"""

    return generate_text(prompt)