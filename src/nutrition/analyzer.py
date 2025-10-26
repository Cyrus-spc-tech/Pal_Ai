class FoodAnalyzer:
    def __init__(self, food_db):
        self.food_db = food_db

    def analyze_food(self, food_desc):
        nutrition_data = self.food_db.get_nutrition(food_desc)
        if nutrition_data and 'items' in nutrition_data:
            total_cal = sum(item.get('calories', 0) for item in nutrition_data['items'])
            total_protein = sum(item.get('protein_g', 0) for item in nutrition_data['items'])
            total_carbs = sum(item.get('carbohydrates_total_g', 0) for item in nutrition_data['items'])
            total_fat = sum(item.get('fat_total_g', 0) for item in nutrition_data['items'])
            return {
                'calories': round(total_cal, 1),
                'protein_g': round(total_protein, 1),
                'carbs_g': round(total_carbs, 1),
                'fat_g': round(total_fat, 1)
            }

# Example usage
if __name__ == "__main__":
    from food_db import get_nutrition
    
    food_input = input("Enter food item: ")
    result = get_nutrition(food_input)
    if result:
        print(f"Nutrition data for {food_input} (100g):")
        for item in result.get('items', []):
            print(f"  {item.get('name')}: {item.get('calories')} cal,\n    carbs: {item.get('carbohydrates_total_g')}g,\n    protein: {item.get('protein_g')}g,\n    fat: {item.get('fat_total_g')}g,\n    sugar: {item.get('sugar_g')}g")
    else:
        print("Failed to get nutrition data")