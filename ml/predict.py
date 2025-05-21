import pandas as pd
import numpy as np
from .preprocessing import NutritionDataPreprocessor
from .models import NutritionPredictor

class NutritionPredictionService:
    def __init__(self, model_path=None):
        self.preprocessor = NutritionDataPreprocessor()
        self.model = None
        if model_path:
            self.model = NutritionPredictor.load_model(model_path)
    
    def prepare_input_data(self, food_data):
        """Prepare input data for prediction"""
        # Convert input data to DataFrame
        if isinstance(food_data, dict):
            food_data = pd.DataFrame([food_data])
        
        # Preprocess the input data
        processed_data = self.preprocessor.preprocess_data(food_data)
        
        # Remove the target column if it exists
        if 'Calories (kcal)' in processed_data.columns:
            processed_data = processed_data.drop('Calories (kcal)', axis=1)
        
        return processed_data
    
    def predict_nutrition(self, food_data):
        """Make nutrition predictions"""
        if self.model is None:
            raise ValueError("Model not loaded. Please load a trained model first.")
        
        # Prepare input data
        processed_data = self.prepare_input_data(food_data)
        
        # Make predictions
        predictions = self.model.predict(processed_data)
        
        # Convert predictions back to original scale
        original_scale_predictions = self.preprocessor.inverse_transform_predictions(predictions)
        
        return original_scale_predictions
    
    def predict_meal_nutrition(self, meal_items):
        """Predict nutrition for a complete meal"""
        total_nutrition = {
            'Calories (kcal)': 0,
            'Protein (g)': 0,
            'Carbohydrates (g)': 0,
            'Fat (g)': 0,
            'Fiber (g)': 0,
            'Sugars (g)': 0,
            'Sodium (mg)': 0,
            'Cholesterol (mg)': 0
        }
        
        for item in meal_items:
            predictions = self.predict_nutrition(item)
            for key in total_nutrition:
                if key in item:
                    total_nutrition[key] += item[key]
        
        return total_nutrition 