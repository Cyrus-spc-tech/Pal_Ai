# Central spot for configs: DB paths, API endpoints, default advice tones.
import os
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NUTRITIONIX_APP_ID = os.getenv('NUTRITIONIX_APP_ID')
NUTRITIONIX_API_KEY = os.getenv('NUTRITIONIX_API_KEY')

# Paths
DB_PATH = os.getenv('DB_PATH', 'data/friend_ai.db')

# Chat Vibes
FRIEND_TONE = os.getenv('FRIEND_TONE', 'casual_and_encouraging')
ADVICE_PROMPT_TEMPLATE = f"""
You are a super chill friend chatting with {FRIEND_TONE}. Be supportive, funny when it fits, and real.
User said: {{user_input}}
Context: {{user_context}}
Respond like: "Hey man, that sounds tough – here's a quick win..."
"""

# Nutrition defaults
DAILY_CALORIES_GOAL = 2000  # Customizable per user later
NUTRITION_INDEX_WEIGHT = {'calories': 0.3, 'protein': 0.25, 'carbs': 0.25, 'fats': 0.2}  # For scoring balance