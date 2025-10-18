# Local or API wrapper for food data (e.g., quick lookup for 'apple' = 52 cal, 14g carbs).
import requests
from config.settings import CALORIE_NINJAS_API_KEY

def get_nutrition(food_query):
    url = "https://api.calorieninjas.com/v1/nutrition"
    headers = {"X-Api-Key": CALORIE_NINJAS_API_KEY}
    params = {"query": food_query}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()  # e.g., {'items': [{'name': 'chicken', 'calories': 165, 'protein_g': 31, ...}]}
    return None