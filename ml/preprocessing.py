import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

class NutritionDataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self, file_path):
        """Load the nutrition dataset"""
        return pd.read_csv(file_path)
    
    def preprocess_data(self, df):
        """Preprocess the nutrition data"""
        # Create a copy to avoid modifying the original data
        df_processed = df.copy()
        
        # Convert date to datetime
        df_processed['Date'] = pd.to_datetime(df_processed['Date'])
        
        # Extract date features
        df_processed['Day_of_Week'] = df_processed['Date'].dt.dayofweek
        df_processed['Month'] = df_processed['Date'].dt.month
        
        # Encode categorical variables
        categorical_columns = ['Food_Item', 'Category', 'Meal_Type']
        for column in categorical_columns:
            if column not in self.label_encoders:
                self.label_encoders[column] = LabelEncoder()
            df_processed[column] = self.label_encoders[column].fit_transform(df_processed[column])
        
        # Scale numerical features
        numerical_columns = ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 
                           'Fat (g)', 'Fiber (g)', 'Sugars (g)', 'Sodium (mg)', 
                           'Cholesterol (mg)', 'Water_Intake (ml)']
        
        df_processed[numerical_columns] = self.scaler.fit_transform(df_processed[numerical_columns])
        
        return df_processed
    
    def prepare_training_data(self, df_processed, target_column='Calories (kcal)', test_size=0.2):
        """Prepare data for training"""
        # Define features and target
        X = df_processed.drop(['Date', target_column], axis=1)
        y = df_processed[target_column]
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        return X_train, X_test, y_train, y_test
    
    def inverse_transform_predictions(self, predictions):
        """Convert scaled predictions back to original scale"""
        return self.scaler.inverse_transform(predictions.reshape(-1, 1)).flatten() 