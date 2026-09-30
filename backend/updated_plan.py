import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-2.5-pro"
)

client = None

if API_KEY:
    client = genai.Client(
        api_key=API_KEY
    )


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is missing in .env"
        )

    prompt = f"""
You are FitBuddy.

Update the following 7-day workout plan
based on user feedback.

Fitness Goal:
{goal}

Intensity:
{intensity}

ORIGINAL PLAN:
----------------
{original_plan}
----------------

USER FEEDBACK:
----------------
{feedback}
----------------

Create a revised seven-day plan.

Keep:

- Day 1 to Day 7
- Warm-up
- Main workout
- Sets/repetitions or duration
- Rest guidance
- Cooldown/recovery

Address the user's feedback.

Return only the revised plan.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()