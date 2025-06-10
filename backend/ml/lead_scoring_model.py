import xgboost as xgb
import pandas as pd
import numpy as np
import json
import os
from typing import Dict, Any
from .base_model import BasePredictiveModel

class LeadScoringModel(BasePredictiveModel):
    """
    XGBoost implementation for lead scoring
    Predicts lead conversion probability
    """
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.features = None
        self.target = "conversion_probability"
    
    def train(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Train model on lead data
        Expected columns:
        - features: industry, budget, contact_frequency, etc.
        - target: conversion_probability (0-1)
        """
        # Prepare data
        self.features = [col for col in data.columns if col != self.target]
        X = data[self.features]
        y = data[self.target]
        
        # Train XGBoost model
        self.model = xgb.XGBRegressor(
            objective='reg:logistic',
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1
        )
        self.model.fit(X, y)
        self._is_trained = True
        
        # Return training metrics
        train_pred = self.model.predict(X)
        mse = np.mean((train_pred - y) ** 2)
        
        return {
            "status": "success",
            "metrics": {
                "mse": mse,
                "feature_importance": dict(zip(
                    self.features, 
                    self.model.feature_importances_.tolist()
                ))
            }
        }
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict conversion probability for a single lead"""
        if not self._is_trained:
            raise ValueError("Model not trained")
            
        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Ensure all features are present
        missing_features = [f for f in self.features if f not in input_df.columns]
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")
        
        # Make prediction
        prediction = self.model.predict(input_df[self.features])[0]
        
        return {
            "lead_id": input_data.get("lead_id"),
            "conversion_probability": float(prediction),
            "features": input_data
        }
    
    def save(self, model_path: str) -> None:
        """Save model and metadata"""
        if not self._is_trained:
            raise ValueError("Model not trained")
            
        # Create directory if needed
        os.makedirs(model_path, exist_ok=True)
        
        # Save model
        self.model.save_model(os.path.join(model_path, "model.xgb"))
        
        # Save metadata
        with open(os.path.join(model_path, "metadata.json"), "w") as f:
            json.dump({
                "features": self.features,
                "target": self.target
            }, f)
    
    @classmethod
    def load(cls, model_path: str) -> 'LeadScoringModel':
        """Load saved model"""
        instance = cls()
        
        # Load model
        instance.model = xgb.XGBRegressor()
        instance.model.load_model(os.path.join(model_path, "model.xgb"))
        
        # Load metadata
        with open(os.path.join(model_path, "metadata.json"), "r") as f:
            metadata = json.load(f)
            instance.features = metadata["features"]
            instance.target = metadata["target"]
        
        instance._is_trained = True
        return instance
