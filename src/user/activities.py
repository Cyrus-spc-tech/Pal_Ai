# Daily logs: Food intake, workouts, mood – timestamps everything.
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.models import Activity, get_db
from datetime import datetime, timedelta
import json

def get_session():
    return next(get_db())

def log_activity(user_id: int, activity_type: str, description: str, nutrition_data: dict = None):
    """
    Log anything: food, workout, mood. Nutrition_data is optional dict from analyzer.
    E.g., log_activity(1, 'food', 'Apple + yogurt', {'calories': 200, 'protein_g': 15})
    """
    db: Session = get_session()
    try:
        activity = Activity(
            user_id=user_id,
            type=activity_type,
            description=description,
            nutrition_data=json.dumps(nutrition_data) if nutrition_data else None,
            timestamp=datetime.utcnow()
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        print(f"📝 Logged {activity_type}: {description}")
        return activity
    finally:
        db.close()

def get_today_activities(user_id: int) -> list[Activity]:
    """
    Pull today's logs for nutrition summary or chat context.
    """
    db: Session = get_session()
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        activities = db.query(Activity).filter(
            Activity.user_id == user_id,
            Activity.timestamp >= today_start
        ).all()
        return activities
    finally:
        db.close()

def get_food_logs(user_id: int, days_back: int = 1) -> list[dict]:
    """
    Get recent food with nutrition – for analyzer.
    """
    db: Session = get_session()
    from_date = datetime.utcnow() - timedelta(days=days_back)
    try:
        foods = db.query(Activity).filter(
            Activity.user_id == user_id,
            Activity.type == 'food',
            Activity.timestamp >= from_date
        ).all()
        return [{'desc': f.description, 'nutrition': json.loads(f.nutrition_data) if f.nutrition_data else {}} for f in foods]
    finally:
        db.close()

# Example usage
if __name__ == "__main__":
    # Assume user ID 1 from test user
    log_activity(1, 'food', 'Morning oatmeal', {'calories': 300, 'carbs_g': 50})
    log_activity(1, 'mood', 'Feeling pumped after coffee')
    todays = get_today_activities(1)
    print(f"Today's logs: {len(todays)} activities")