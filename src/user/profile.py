# Manages user details: Student? Job? Goals? Saves/loads from DB.
from sqlalchemy.orm import Session
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add src to path
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from database.models import User, get_db
from config.settings import DB_PATH

# Helper to get DB session (import get_db from models if needed)
def get_session():
    return next(get_db())

def create_or_get_user(name: str, role: str, goals: str, daily_cal_goal: float = 2000.0) -> User:
    """
    Onboard new user or fetch existing. Call this in main.py after intro questions.
    """
    db: Session = get_session()
    try:
        # Check if user exists (simple name match for now – add email later?)
        user = db.query(User).filter(User.name == name).first()
        if not user:
            user = User(
                name=name,
                role=role,
                goals=goals,
                daily_cal_goal=daily_cal_goal
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"👋 Welcome, {name}! You're a {role} chasing {goals}. Let's make today epic.")
        else:
            print(f"Yo {name}, back for more? Still {role} mode, right?")
        return user
    finally:
        db.close()

def update_user_goals(user_id: int, new_goals: str):
    """
    Quick update, e.g., from chat: "My goals changed to hit the gym."
    """
    db: Session = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.goals = new_goals
            db.commit()
            print("Goals updated – you're evolving, friend!")
        else:
            print("User not found – double-check that ID.")
    finally:
        db.close()

# Example usage (for testing)
if __name__ == "__main__":
    user = create_or_get_user("Alex", "student", "Ace exams while staying sane", 1800.0)
    print(f"User ID: {user.id}, Goals: {user.goals}")