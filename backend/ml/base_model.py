from abc import ABC, abstractmethod
from typing import Any, Dict
import pandas as pd

class BasePredictiveModel(ABC):
    """
    Abstract base class for all predictive models
    """
    
    def __init__(self):
        self._is_trained = False
    
    @abstractmethod
    def train(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Train the model on provided data"""
        pass
    
    @abstractmethod
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions using the trained model"""
        pass
    
    @abstractmethod
    def save(self, model_path: str) -> None:
        """Save model to disk"""
        pass
    
    @classmethod
    @abstractmethod
    def load(cls, model_path: str) -> 'BasePredictiveModel':
        """Load model from disk"""
        pass
    
    @property
    def is_trained(self) -> bool:
        """Check if model is trained"""
        return self._is_trained
