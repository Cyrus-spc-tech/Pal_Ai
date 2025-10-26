class FoodAnalyzer:
    def __init__(self, food_db_instance):
        self.food_db = food_db_instance

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
    from nutrition.food_db import FoodDB
    
    food_db = FoodDB()
    analyzer = FoodAnalyzer(food_db)
    result = analyzer.analyze_food("apple")
    print(result)