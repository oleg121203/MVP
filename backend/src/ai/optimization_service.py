import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from joblib import load, dump
import pandas as pd

class HVACOptimizer:
    def __init__(self):
        self.model = self._load_model()
        
    def _load_model(self):
        try:
            return load('ai/models/hvac_model.joblib')
        except:
            # Initialize new model if none exists
            return GradientBoostingRegressor(n_estimators=100)
            
    def optimize(self, building_params):
        """
        Args:
            building_params: Dict containing:
                - area (sqm)
                - occupancy
                - climate_zone
                - current_system_type
                
        Returns:
            Dict of optimized parameters and energy savings
        """
        # Convert to DataFrame for model
        X = pd.DataFrame([building_params])
        
        # Make prediction
        predictions = self.model.predict(X)
        
        return {
            'recommended_system': predictions[0]['system_type'],
            'estimated_savings': predictions[0]['savings'],
            'payback_period': predictions[0]['payback']
        }

    def train(self, training_data):
        """ Train model with new data """
        df = pd.DataFrame(training_data)
        X = df.drop(['system_type', 'savings', 'payback'], axis=1)
        y = df[['system_type', 'savings', 'payback']]
        
        self.model.fit(X, y)
        dump(self.model, 'ai/models/hvac_model.joblib')
