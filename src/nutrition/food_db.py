# Local or API wrapper for food data (e.g., quick lookup for 'apple' = 52 cal, 14g carbs).
import requests
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import config.settings as settings

def get_nutrition(food_query):
    url = "https://api.calorieninjas.com/v1/nutrition"
    api_key = getattr(settings, '+bHULqO/72eGAajoGVe2Kw==o7Nc11wsHxbzDZzO', None)
    if not api_key:
        print(" CALORIE_NINJAS_API_KEY not found in .env")
        return None
    headers = {"X-Api-Key": api_key}
    params = {"query": food_query}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json() 
        else:
            print(f" Nutrition API error: {response.status_code}")
            return None
    except Exception as e:
        print(f" Error calling nutrition API: {e}")
        return None

# Test function
if __name__ == "__main__":
    result = get_nutrition("apple")
    if result:
        print("Nutrition data for apple:")
        for item in result.get('items', []):
            print(f"  {item.get('name')}: {item.get('calories')} cal, {item.get('carbohydrates_total_g')}g carbs")
    else:
        print("Failed to get nutrition data")