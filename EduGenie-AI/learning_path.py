from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    topic = topic.strip()
    level = level.strip()

    if not topic:
        raise ValueError("Please provide a learning topic.")

    if not level:
        level = "Beginner"

    prompt = f"""
You are EduGenie, an expert educational curriculum planner.

Create a personalized learning path.

Topic:
{topic}

Learner Level:
{level}

Include:

1. Learning goal
2. Stage-by-stage roadmap
3. Topics for each stage
4. Suggested timeline
5. Practice activities
6. Projects
7. Revision strategy
8. Recommended resource TYPES such as:
   - Videos
   - Articles
   - Books
   - Documentation

Do not invent specific URLs.

Make the plan practical and easy for a student to follow.
"""

    return generate_text(prompt)