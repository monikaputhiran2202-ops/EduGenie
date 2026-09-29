import os
from gemini_client import generate_text


LOCAL_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)


def local_explanation(concept: str) -> str:
    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model=LOCAL_MODEL,
        device=-1
    )

    prompt = f"""
Explain this educational concept to a beginner.

Use:
- Simple language
- Short paragraphs
- One example
- Clear explanation

Concept:

{concept}
"""

    result = generator(
        prompt,
        max_new_tokens=250,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


def explain_concept(concept: str) -> str:
    concept = concept.strip()

    if not concept:
        raise ValueError("Please provide a concept.")

    use_local = os.getenv(
        "USE_LOCAL_EXPLANATION",
        "false"
    ).lower() == "true"

    if use_local:
        try:
            return local_explanation(concept)
        except Exception:
            pass

    prompt = f"""
You are EduGenie, a friendly educational tutor.

Explain the following concept to a beginner.

Requirements:
- Use very simple language.
- Explain the main idea.
- Break difficult ideas into smaller parts.
- Give one easy example.
- Use bullet points when helpful.
- Avoid unnecessary technical terminology.

Concept:

{concept}
"""

    return generate_text(prompt)