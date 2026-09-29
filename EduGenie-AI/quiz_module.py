import json
import re

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```\s*", "", text)
    text = re.sub(r"\s*```", "", text)

    # Find JSON array
    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]

    return text


def validate_quiz(data):
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON list.")

    if len(data) != 3:
        raise ValueError(
            f"Quiz must contain exactly 3 questions. Received {len(data)}."
        )

    final_quiz = []

    for index, item in enumerate(data, start=1):

        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is invalid.")

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question:
            raise ValueError(f"Question {index} is missing.")

        if not isinstance(options, list):
            raise ValueError(
                f"Options for question {index} must be a list."
            )

        if len(options) != 4:
            raise ValueError(
                f"Question {index} must have exactly 4 options."
            )

        options = [str(option).strip() for option in options]

        # Sometimes Gemini returns an answer like "A", "B", "C", "D"
        if answer.upper() in ["A", "B", "C", "D"]:
            answer_index = ord(answer.upper()) - ord("A")
            answer = options[answer_index]

        # Sometimes Gemini returns 0,1,2,3
        elif answer.isdigit():
            answer_index = int(answer)

            if 0 <= answer_index < 4:
                answer = options[answer_index]

        if answer not in options:
            raise ValueError(
                f"Correct answer for question {index} "
                f"does not match any option."
            )

        final_quiz.append({
            "question": question,
            "options": options,
            "answer": answer,
            "explanation": explanation
        })

    return final_quiz


def generate_quiz(content: str):

    content = content.strip()

    if not content:
        raise ValueError("Please provide a topic or passage.")

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create EXACTLY 3 multiple-choice questions
from the content below.

Each question MUST contain:

- question
- exactly 4 options
- answer
- explanation

IMPORTANT:

1. Return ONLY valid JSON.
2. Do NOT use Markdown.
3. Do NOT use ```json.
4. Do NOT write anything before or after the JSON.
5. The answer MUST exactly match one of the four options.
6. Questions must be based only on the supplied content.

Use this exact structure:

[
  {{
    "question": "Question 1",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A",
    "explanation": "Short explanation."
  }},
  {{
    "question": "Question 2",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option B",
    "explanation": "Short explanation."
  }},
  {{
    "question": "Question 3",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option C",
    "explanation": "Short explanation."
  }}
]

CONTENT:

{content}
"""

    response = generate_text(prompt)

    cleaned = clean_json_block(response)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid JSON: {e}"
        )

    return validate_quiz(data)