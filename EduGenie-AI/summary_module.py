from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text.strip()

    if not text:
        raise ValueError("Please provide text to summarize.")

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational passage.

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Make it useful for revision.
- Preserve important facts.
- Use bullet points where appropriate.

Educational Passage:

{text}
"""

    return generate_text(prompt)