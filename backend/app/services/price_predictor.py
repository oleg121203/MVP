import logging
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PricePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.data = None

    def load_data(self) -> None:
        """Load price data for prediction. Currently using mock data for testing."""
        # Mock data for testing
        dates = pd.date_range(start='2025-01-01', end='2025-06-10', freq='D')
        prices = np.random.normal(loc=100, scale=10, size=len(dates)) + np.linspace(0, 20, len(dates))
        self.data = pd.DataFrame({'timestamp': dates, 'price': prices})
        logger.info("Price data loaded for prediction")

    def prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare features for prediction model."""
        if 'timestamp' in data.columns:
            data['days_since_start'] = (data['timestamp'] - data['timestamp'].min()).dt.days
            features = data[['days_since_start']].values
        else:
            features = np.array([]).reshape(-1, 1)
        return self.scaler.fit_transform(features) if features.size > 0 else features

    def train_model(self) -> None:
        """Train the prediction model using historical data."""
        if self.data is None or self.data.empty:
            self.load_data()

        if not self.data.empty:
            X = self.prepare_features(self.data)
            y = self.data['price'].values
            if X.size > 0:
                self.model.fit(X, y)
                logger.info("Price prediction model trained")
            else:
                logger.warning("No features available for training")
        else:
            logger.warning("No data available for training")

    def predict(self, future_days: int = 7) -> List[float]:
        """Predict future prices based on trained model."""
        if self.data is None or self.data.empty:
            self.load_data()
            self.train_model()

        last_date = self.data['timestamp'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=future_days, freq='D')
        future_df = pd.DataFrame({'timestamp': future_dates})
        X_future = self.prepare_features(future_df)
        if X_future.size > 0:
            predictions = self.model.predict(X_future)
            logger.info(f"Predicted prices for the next {future_days} days")
            return predictions.tolist()
        else:
            logger.warning("No features available for prediction")
            return []

    def evaluate_model(self) -> Dict[str, float]:
        """Evaluate the model's performance on historical data."""
        if self.data is None or self.data.empty:
            self.load_data()
            self.train_model()

        if not self.data.empty:
            X = self.prepare_features(self.data)
            if X.size > 0:
                predictions = self.model.predict(X)
                actuals = self.data['price'].values
                mse = np.mean((predictions - actuals) ** 2)
                r2 = self.model.score(X, actuals)
                logger.info("Price prediction model evaluated")
                return {'mse': mse, 'r2': r2}
            else:
                logger.warning("No features available for evaluation")
                return {'mse': 0.0, 'r2': 0.0}
        else:
            logger.warning("No data available for evaluation")
            return {'mse': 0.0, 'r2': 0.0}
