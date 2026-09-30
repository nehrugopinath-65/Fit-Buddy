from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI(
    title="FitBuddy API"
)


# ==============================
# STATIC FILES
# ==============================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ==============================
# TEMPLATES
# ==============================

templates = Jinja2Templates(
    directory="templates"
)


# ==============================
# DATA MODEL
# ==============================

class UserData(BaseModel):

    username: str
    user_id: str
    age: int
    weight: float
    goal: str
    intensity: str


class FeedbackData(BaseModel):

    user_id: str
    feedback: str


# Temporary storage
# Later you can replace this with MySQL/SQLite.

users = {}


# ==============================
# HOME PAGE
# ==============================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "request": request
    }
)

# ==============================
# FEEDBACK PAGE
# ==============================
@app.get("/feedback")
async def feedback_page(
    request: Request,
    user_id: str = ""
):
    return templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context={
            "request": request,
            "user_id": user_id
        }
    )


# ==============================
# GENERATE WORKOUT
# ==============================

@app.post("/generate-workout")
async def generate_workout(
    user: UserData
):

    # --------------------------
    # Create workout plan
    # --------------------------

    plan = f"""
7-DAY FITNESS PLAN

Day 1 - Full Body
• Squats - 3 x 12
• Push-ups - 3 x 10
• Lunges - 3 x 10
• Plank - 3 x 30 seconds

Day 2 - Cardio
• Walking/Jogging - 30 minutes
• Jumping Jacks - 3 x 20
• Mountain Climbers - 3 x 15

Day 3 - Upper Body
• Push-ups - 3 x 10
• Shoulder Press - 3 x 12
• Triceps Dips - 3 x 10

Day 4 - Rest
• Light stretching
• Walking
• Recovery

Day 5 - Lower Body
• Squats - 3 x 12
• Lunges - 3 x 10
• Glute Bridges - 3 x 15

Day 6 - Cardio + Core
• Jogging - 25 minutes
• Crunches - 3 x 15
• Plank - 3 x 30 seconds

Day 7 - Recovery
• Light walking
• Full body stretching
• Recovery
"""


    nutrition_tip = (
        "Stay hydrated throughout the day. "
        "Eat balanced meals containing protein, "
        "vegetables, fruits and whole grains. "
        "Give your body enough time to recover."
    )


    # --------------------------
    # Save user
    # --------------------------

    users[user.user_id] = {

        "username": user.username,

        "user_id": user.user_id,

        "age": user.age,

        "weight": user.weight,

        "goal": user.goal,

        "intensity": user.intensity,

        "plan": plan,

        "nutrition_tip": nutrition_tip

    }


    # --------------------------
    # Send JSON to frontend
    # --------------------------

    return {

        "user": {

            "username": user.username,

            "user_id": user.user_id,

            "age": user.age,

            "weight": user.weight,

            "goal": user.goal,

            "intensity": user.intensity

        },

        "plan": plan,

        "nutrition_tip": nutrition_tip

    }


# ==============================
# SUBMIT FEEDBACK
# ==============================

@app.post("/submit-feedback")
async def submit_feedback(
    feedback: FeedbackData
):

    # Check user

    if feedback.user_id not in users:

        return JSONResponse(
            status_code=404,
            content={
                "detail": "User not found."
            }
        )


    user = users[feedback.user_id]


    # --------------------------
    # Here you can call your AI
    # --------------------------

    updated_plan = f"""
UPDATED 7-DAY FITNESS PLAN

User requested:

{feedback.feedback}

Day 1 - Full Body
• Squats - 3 x 12
• Push-ups - 3 x 10
• Lunges - 3 x 10

Day 2 - Cardio
• Walking/Jogging - 30 minutes
• Jumping Jacks - 3 x 20

Day 3 - Upper Body
• Push-ups - 3 x 10
• Shoulder Press - 3 x 12

Day 4 - Rest
• Light stretching
• Recovery

Day 5 - Lower Body
• Squats - 3 x 12
• Lunges - 3 x 10

Day 6 - Cardio + Core
• Jogging - 25 minutes
• Plank - 3 x 30 seconds

Day 7 - Recovery
• Walking
• Stretching
"""


    user["plan"] = updated_plan


    # --------------------------
    # Return updated result
    # --------------------------

    return {

        "user": {

            "username": user["username"],

            "user_id": user["user_id"],

            "age": user["age"],

            "weight": user["weight"],

            "goal": user["goal"],

            "intensity": user["intensity"]

        },

        "plan": updated_plan,

        "nutrition_tip":
            user["nutrition_tip"]

    }