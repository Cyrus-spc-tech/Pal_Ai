# Entry point: Run this to fire up the app (e.g., CLI chat loop).
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import create_tables
from database import init_db
from user.profile import create_or_get_user, update_user_goals
from user.activities import log_activity, get_today_activities, get_food_logs
from nutrition.food_db import get_nutrition
import json

def display_banner():
    """Show welcome banner"""
    print("\n" + "="*60)
    print("🤖  COMRAD.AI - Your Personal AI Assistant")
    print("="*60)
    print("Your friendly AI pal for tracking activities, nutrition, and more!")
    print("="*60 + "\n")

def onboard_user():
    """Onboard new user or get existing user"""
    print("\n👋 Hey there! Let's get you set up.\n")
    name = input("What's your name? ").strip()
    
    print("\nAre you a:")
    print("  1. Student")
    print("  2. Working professional")
    print("  3. Other")
    role_choice = input("Pick one (1-3): ").strip()
    
    role_map = {"1": "student", "2": "working", "3": "other"}
    role = role_map.get(role_choice, "other")
    
    goals = input("\nWhat are your main goals? (e.g., 'Stay healthy and ace exams'): ").strip()
    
    cal_input = input("\nDaily calorie goal? (press Enter for default 2000): ").strip()
    daily_cal = float(cal_input) if cal_input else 2000.0
    
    user = create_or_get_user(name, role, goals, daily_cal)
    return user

def show_menu():
    """Display main menu"""
    print("\n" + "-"*60)
    print("MAIN MENU")
    print("-"*60)
    print("  1. Log Food")
    print("  2. Log Workout")
    print("  3. Log Mood")
    print("  4. View Today's Activities")
    print("  5. Analyze Today's Nutrition")
    print("  6. Update Goals")
    print("  7. Exit")
    print("-"*60)

def log_food_activity(user_id):
    """Log food with nutrition lookup"""
    print("\n🍎 FOOD LOGGING")
    food_desc = input("What did you eat? (e.g., 'chicken breast and rice'): ").strip()
    
    if not food_desc:
        print("⚠️  No food entered.")
        return
    
    print("\n🔍 Looking up nutrition data...")
    nutrition_data = get_nutrition(food_desc)
    
    if nutrition_data and 'items' in nutrition_data and len(nutrition_data['items']) > 0:
        # Aggregate nutrition from all items
        total_cal = sum(item.get('calories', 0) for item in nutrition_data['items'])
        total_protein = sum(item.get('protein_g', 0) for item in nutrition_data['items'])
        total_carbs = sum(item.get('carbohydrates_total_g', 0) for item in nutrition_data['items'])
        total_fat = sum(item.get('fat_total_g', 0) for item in nutrition_data['items'])
        
        nutrition_summary = {
            'calories': round(total_cal, 1),
            'protein_g': round(total_protein, 1),
            'carbs_g': round(total_carbs, 1),
            'fat_g': round(total_fat, 1)
        }
        
        print(f"\n📊 Nutrition Info:")
        print(f"   Calories: {nutrition_summary['calories']} kcal")
        print(f"   Protein: {nutrition_summary['protein_g']}g")
        print(f"   Carbs: {nutrition_summary['carbs_g']}g")
        print(f"   Fat: {nutrition_summary['fat_g']}g")
        
        log_activity(user_id, 'food', food_desc, nutrition_summary)
    else:
        print("⚠️  Couldn't fetch nutrition data. Logging without it.")
        log_activity(user_id, 'food', food_desc)

def log_workout_activity(user_id):
    """Log workout"""
    print("\n💪 WORKOUT LOGGING")
    workout_desc = input("What workout did you do? (e.g., '30 min run'): ").strip()
    
    if workout_desc:
        log_activity(user_id, 'workout', workout_desc)
    else:
        print("⚠️  No workout entered.")

def log_mood_activity(user_id):
    """Log mood"""
    print("\n😊 MOOD LOGGING")
    mood_desc = input("How are you feeling? (e.g., 'energized and focused'): ").strip()
    
    if mood_desc:
        log_activity(user_id, 'mood', mood_desc)
    else:
        print("⚠️  No mood entered.")

def view_today_activities(user_id):
    """Display today's activities"""
    print("\n📅 TODAY'S ACTIVITIES")
    print("-"*60)
    
    activities = get_today_activities(user_id)
    
    if not activities:
        print("No activities logged today yet.")
        return
    
    for activity in activities:
        timestamp = activity.timestamp.strftime("%H:%M")
        print(f"\n[{timestamp}] {activity.type.upper()}")
        print(f"  {activity.description}")
        
        if activity.nutrition_data:
            try:
                nutrition = json.loads(activity.nutrition_data)
                print(f"  Nutrition: {nutrition.get('calories', 'N/A')} cal, "
                      f"{nutrition.get('protein_g', 'N/A')}g protein")
            except:
                pass
    
    print("-"*60)

def analyze_nutrition(user_id, user):
    """Analyze today's nutrition"""
    print("\n📊 NUTRITION ANALYSIS")
    print("-"*60)
    
    food_logs = get_food_logs(user_id, days_back=1)
    
    if not food_logs:
        print("No food logged today yet.")
        return
    
    total_cal = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for food in food_logs:
        nutrition = food.get('nutrition', {})
        total_cal += nutrition.get('calories', 0)
        total_protein += nutrition.get('protein_g', 0)
        total_carbs += nutrition.get('carbs_g', 0)
        total_fat += nutrition.get('fat_g', 0)
    
    print(f"\n📈 Today's Totals:")
    print(f"   Calories: {round(total_cal, 1)} / {user.daily_cal_goal} kcal")
    print(f"   Protein: {round(total_protein, 1)}g")
    print(f"   Carbs: {round(total_carbs, 1)}g")
    print(f"   Fat: {round(total_fat, 1)}g")
    
    # Simple feedback
    cal_diff = user.daily_cal_goal - total_cal
    if cal_diff > 500:
        print(f"\n💡 You have {round(cal_diff)} calories left for today. Keep it up!")
    elif cal_diff > 0:
        print(f"\n💡 Almost there! {round(cal_diff)} calories to go.")
    elif cal_diff > -200:
        print(f"\n💡 Right on target! Great job balancing your intake.")
    else:
        print(f"\n💡 You're over by {round(abs(cal_diff))} calories. No worries, tomorrow's a new day!")
    
    print("-"*60)

def update_goals_menu(user_id):
    """Update user goals"""
    print("\n🎯 UPDATE GOALS")
    new_goals = input("Enter your new goals: ").strip()
    
    if new_goals:
        update_user_goals(user_id, new_goals)
    else:
        print("⚠️  No goals entered.")

def main():
    """Main application loop"""
    # Initialize database
    print("🔧 Initializing database...")
    try:
        create_tables()
        print("✅ Database ready!")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")
        print("Continuing anyway...")
    
    display_banner()
    
    # Onboard or get user
    user = onboard_user()
    
    # Main menu loop
    while True:
        show_menu()
        choice = input("\nChoose an option (1-7): ").strip()
        
        if choice == '1':
            log_food_activity(user.id)
        elif choice == '2':
            log_workout_activity(user.id)
        elif choice == '3':
            log_mood_activity(user.id)
        elif choice == '4':
            view_today_activities(user.id)
        elif choice == '5':
            analyze_nutrition(user.id, user)
        elif choice == '6':
            update_goals_menu(user.id)
        elif choice == '7':
            print("\n👋 See you later! Keep crushing those goals!\n")
            break
        else:
            print("\n⚠️  Invalid choice. Please pick 1-7.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Caught ya! Exiting gracefully...\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()