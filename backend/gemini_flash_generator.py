import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-2.5-flash"
)

client = None

if API_KEY:
    client = genai.Client(
        api_key=API_KEY
    )


def generate_nutrition_tip_with_flash(goal):

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is missing in .env"
        )

    prompt = f"""
You are FitBuddy nutrition assistant.

Fitness goal:
{goal}

Give one short and practical
nutrition or recovery tip.

Keep it below 100 words.

Do not provide medical diagnosis
or treatment.
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