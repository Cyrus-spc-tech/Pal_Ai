from .models import create_tables
from .models import SessionLocal
from .models import User

def init_db():
    create_tables()
    print("🗄️  Tables created! Checking for default user...")
    
    # Quick check: Add a dummy if empty (remove for prod)
    db = next(SessionLocal())
    if not db.query(User).first():
        dummy_user = User(
            name="Test Buddy",
            role="student",
            goals="Build cool AI friends",
            daily_cal_goal=2200.0
        )
        db.add(dummy_user)
        db.commit()
        print("👋 Added a test user. Ready to chat!")
    else:
        print("User exists – all good.")
    db.close()

if __name__ == "__main__":
    init_db()