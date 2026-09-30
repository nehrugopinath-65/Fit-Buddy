from fastapi import APIRouter
from fastapi import HTTPException

from database import (
    save_user,
    get_user,
    get_all_users,
    update_plan,
    delete_user
)

from gemini_gerenator import generate_workout_gemini
from gemini_flash_generator import generate_nutrition_tip_with_flash
from updated_plan import update_workout_plan


router = APIRouter()


# =========================================================
# HOME
# =========================================================

@router.get("/")
def home():

    return {
        "message": "FitBuddy Backend is running",
        "frontend": "Open frontend/index.html",
        "docs": "/docs",
        "health": "/health"
    }


# =========================================================
# GENERATE WORKOUT
# =========================================================

@router.post("/generate-workout")
def generate_workout(data: dict):

    try:

        username = data.get("username")
        user_id = data.get("user_id")
        age = data.get("age")
        weight = data.get("weight")
        goal = data.get("goal")
        intensity = data.get("intensity")

        if not username:
            raise HTTPException(
                status_code=400,
                detail="Username is required"
            )

        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="User ID is required"
            )

        # Generate workout
        workout_plan = generate_workout_gemini(
            username,
            age,
            weight,
            goal,
            intensity
        )

        # Generate nutrition tip
        nutrition_tip = generate_nutrition_tip_with_flash(
            goal
        )

        # Save user
        save_user(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            original_plan=workout_plan,
            nutrition_tip=nutrition_tip
        )

        return {
            "success": True,
            "message": "Workout plan generated successfully",
            "user_id": user_id,
            "username": username,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@router.post("/feedback")
def feedback(data: dict):

    try:

        user_id = data.get("user_id")
        feedback_text = data.get("feedback")

        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="User ID is required"
            )

        if not feedback_text:
            raise HTTPException(
                status_code=400,
                detail="Feedback is required"
            )

        # Find user
        user = get_user(user_id)

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User ID not found"
            )

        # Get current plan
        current_plan = (
            user.updated_plan
            or user.original_plan
        )

        # Generate revised plan
        revised_plan = update_workout_plan(
            current_plan,
            feedback_text,
            user.goal,
            user.intensity
        )

        # Generate nutrition tip
        nutrition_tip = generate_nutrition_tip_with_flash(
            user.goal
        )

        # Update database
        update_plan(
            user_id=user_id,
            updated_plan=revised_plan,
            feedback=feedback_text,
            nutrition_tip=nutrition_tip
        )

        return {
            "success": True,
            "message": "Workout plan updated successfully",
            "user_id": user_id,
            "workout_plan": revised_plan,
            "nutrition_tip": nutrition_tip
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET USER
# =========================================================

@router.get("/user/{user_id}")
def get_single_user(user_id: str):

    user = get_user(user_id)

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user.user_id,
        "username": user.username,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "original_plan": user.original_plan,
        "updated_plan": user.updated_plan,
        "nutrition_tip": user.nutrition_tip,
        "feedback": user.feedback
    }


# =========================================================
# VIEW ALL USERS
# =========================================================

@router.get("/view-all-users")
def view_all_users():

    users = get_all_users()

    result = []

    for user in users:

        result.append({
            "user_id": user.user_id,
            "username": user.username,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": (
                user.updated_plan
                or user.original_plan
            ),
            "nutrition_tip": user.nutrition_tip,
            "feedback": user.feedback
        })

    return {
        "success": True,
        "users": result
    }


# =========================================================
# DELETE USER
# =========================================================

@router.delete("/delete-user/{user_id}")
def remove_user(user_id: str):

    deleted = delete_user(user_id)

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "User deleted successfully"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")
def health():

    return {
        "status": "ok",
        "application": "FitBuddy"
    }