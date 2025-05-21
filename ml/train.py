import os
from preprocessing import NutritionDataPreprocessor
from models import NutritionPredictor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def train_nutrition_model(data_path, model_type='random_forest', save_path=None):
    """
    Train a nutrition prediction model
    
    Args:
        data_path (str): Path to the nutrition dataset
        model_type (str): Type of model to train ('random_forest', 'gradient_boosting', or 'linear')
        save_path (str): Path to save the trained model (optional)
    
    Returns:
        dict: Model evaluation metrics
    """
    # Initialize preprocessor
    preprocessor = NutritionDataPreprocessor()
    
    # Load and preprocess data
    print("Loading and preprocessing data...")
    df = preprocessor.load_data(data_path)
    df_processed = preprocessor.preprocess_data(df)
    
    # Prepare training data
    print("Preparing training data...")
    X_train, X_test, y_train, y_test = preprocessor.prepare_training_data(df_processed)
    
    # Initialize and train model
    print(f"Training {model_type} model...")
    model = NutritionPredictor(model_type=model_type)
    model.train(X_train, y_train)
    
    # Evaluate model
    print("\nEvaluating model...")
    predictions = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    # Calculate accuracy (as percentage of predictions within 10% of actual values)
    accuracy = np.mean(np.abs((predictions - y_test) / y_test) <= 0.1) * 100
    
    # Print detailed metrics
    print("\nModel Performance Metrics:")
    print("=" * 50)
    print(f"Model Type: {model_type.upper()}")
    print(f"Accuracy (within 10%): {accuracy:.2f}%")
    print(f"R² Score: {r2:.4f}")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"Root Mean Squared Error: {rmse:.2f}")
    print(f"Mean Squared Error: {mse:.2f}")
    print("=" * 50)
    
    metrics = {
        'accuracy': accuracy,
        'r2': r2,
        'mae': mae,
        'rmse': rmse,
        'mse': mse
    }
    
    # Save model if path is provided
    if save_path:
        print(f"\nSaving model to {save_path}...")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        model.save_model(save_path)
    
    return metrics

if __name__ == "__main__":
    # Get the absolute path to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct absolute paths
    data_path = os.path.join(project_root, "data", "daily_food_nutrition_dataset.csv")
    model_path = os.path.join(project_root, "ml", "models", "nutrition_model.joblib")
    
    # Train model
    metrics = train_nutrition_model(
        data_path=data_path,
        model_type='random_forest',
        save_path=model_path
    ) 

    