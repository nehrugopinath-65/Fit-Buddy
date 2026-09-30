from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker


# ==============================
# DATABASE CONFIGURATION
# ==============================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ==============================
# USER TABLE
# ==============================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    username = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    goal = Column(
        String(50),
        nullable=False
    )

    intensity = Column(
        String(20),
        nullable=False
    )

    original_plan = Column(
        Text,
        nullable=False
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=False
    )

    feedback = Column(
        Text,
        nullable=True
    )


# ==============================
# CREATE DATABASE
# ==============================

def init_db():

    Base.metadata.create_all(
        bind=engine
    )


# ==============================
# SAVE USER
# ==============================

def save_user(
    user_id,
    username,
    age,
    weight,
    goal,
    intensity,
    original_plan,
    nutrition_tip
):

    with SessionLocal() as db:

        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if user:

            user.username = username
            user.age = age
            user.weight = weight
            user.goal = goal
            user.intensity = intensity
            user.original_plan = original_plan
            user.updated_plan = None
            user.nutrition_tip = nutrition_tip
            user.feedback = None

        else:

            user = User(
                user_id=user_id,
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                original_plan=original_plan,
                nutrition_tip=nutrition_tip
            )

            db.add(user)

        db.commit()
        db.refresh(user)

        return user


# ==============================
# GET USER
# ==============================

def get_user(user_id):

    with SessionLocal() as db:

        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )


# ==============================
# GET ALL USERS
# ==============================

def get_all_users():

    with SessionLocal() as db:

        return (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )


# ==============================
# UPDATE PLAN
# ==============================

def update_plan(
    user_id,
    updated_plan,
    feedback,
    nutrition_tip=None
):

    with SessionLocal() as db:

        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:
            return None

        user.updated_plan = updated_plan
        user.feedback = feedback

        if nutrition_tip:
            user.nutrition_tip = nutrition_tip

        db.commit()
        db.refresh(user)

        return user


# ==============================
# DELETE USER
# ==============================

def delete_user(user_id):

    with SessionLocal() as db:

        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:
            return False

        db.delete(user)
        db.commit()

        return True