# Local or API wrapper for food data (e.g., quick lookup for 'apple' = 52 cal, 14g carbs).
import requests
import json

def get_nutrition(food_query):
    url = "https://api.calorieninjas.com/v1/nutrition"
    headers = {"X-Api-Key": "+bHULqO/72eGAajoGVe2Kw==o7Nc11wsHxbzDZzO"}
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
# if __name__ == "__main__":
#     result = get_nutrition("paneer")
#     if result:
#         print("Nutrition data for paneer:")
#         print(json.dumps(result, indent=4))
#     else:
#         print("Failed to get nutrition data")
