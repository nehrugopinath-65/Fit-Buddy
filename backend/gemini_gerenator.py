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


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is missing in .env"
        )

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day workout plan.

User information:

Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Create exactly seven days.

For each day include:

1. Focus
2. Warm-up
3. Main workout
4. Sets and repetitions or duration
5. Rest guidance
6. Cooldown/recovery

Make the plan practical and easy to follow.

Do not provide medical diagnosis or treatment.

Return the answer as clean plain text.
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