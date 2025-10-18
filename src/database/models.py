# DB schemas: User table, Activity logs, Advice history (SQLite to start, easy upgrade to Postgres).
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config.settings import DB_PATH

# DB engine – points to your .env path
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)  # echo=True for debug logs
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# User table: Core profile stuff
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "Alex"
    role = Column(String)  # "student" or "working"
    goals = Column(Text)  # "Crush finals" or "Hit gym 3x/week"
    daily_cal_goal = Column(Float, default=2000.0)  # Personalized calories
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # One-to-many: User has many activities
    activities = relationship("Activity", back_populates="owner")
    advice_history = relationship("AdviceHistory", back_populates="user")

# Activities table: Daily logs (food, workouts, mood)
class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String)  # "food", "workout", "mood"
    description = Column(Text)  # "Ate pizza: 2 slices pepperoni"
    nutrition_data = Column(Text)  # JSON string: {'calories': 800, 'protein_g': 30, ...} from analyzer
    timestamp = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="activities")

# AdviceHistory: Past tips for convo context
class AdviceHistory(Base):
    __tablename__ = 'advice_history'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    advice_text = Column(Text)  # "Bump those veggies, champ!"
    triggered_by = Column(String)  # "low_protein" or "stress_mood"
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="advice_history")

# Create all tables (call this in init_db.py)
def create_tables():
    Base.metadata.create_all(bind=engine)

# Helper: Get a DB session (use in other modules)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()