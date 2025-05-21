import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

class NutritionPredictor:
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the specified model"""
        if self.model_type == 'random_forest':
            return RandomForestRegressor(n_estimators=100, random_state=42)
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingRegressor(n_estimators=100, random_state=42)
        elif self.model_type == 'linear':
            return LinearRegression()
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X_train, y_train):
        """Train the model"""
        self.model.fit(X_train, y_train)
        return self
    
    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """Evaluate the model"""
        predictions = self.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'r2': r2
        }
    
    def save_model(self, filepath):
        """Save the trained model"""
        joblib.dump(self.model, filepath)
    
    @classmethod
    def load_model(cls, filepath):
        """Load a trained model"""
        model = cls()
        model.model = joblib.load(filepath)
        return model 