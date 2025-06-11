from typing import List, Dict, Any, Tuple, Optional
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

class PredictiveAnalytics:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False

    def prepare_data(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare data for predictive modeling"""
        df = pd.DataFrame(data)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['days'] = (df['date'] - df['date'].min()).dt.days
        return df

    def train_model(self, data: List[Dict[str, Any]], target_column: str = 'cost') -> Tuple[bool, str]:
        """Train the predictive model with historical data"""
        df = self.prepare_data(data)
        if len(df) < 2:
            return False, "Insufficient data for training"

        X = df[['days']]
        y = df[target_column]
        
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        return True, "Model trained successfully"

    def predict_trend(self, data: List[Dict[str, Any]], future_days: int = 7) -> Tuple[Optional[List[Dict[str, Any]]], str]:
        """Predict future trends based on historical data"""
        if not self.is_trained:
            return None, "Model not trained yet"
        
        df = self.prepare_data(data)
        if len(df) == 0:
            return None, "No data provided for prediction"

        last_day = df['days'].max()
        future_days_range = np.array(range(last_day + 1, last_day + future_days + 1)).reshape(-1, 1)
        predictions = self.model.predict(future_days_range)
        
        # Adjust predictions with a simple confidence interval
        confidence = 0.1 * predictions  # 10% confidence interval for demonstration
        future_dates = pd.date_range(start=df['date'].max() + pd.Timedelta(days=1), periods=future_days, freq='D')
        predicted_data = [{'date': date.strftime('%Y-%m-%d'), 'predicted_cost': float(pred), 'confidence_lower': float(pred - conf), 'confidence_upper': float(pred + conf)} 
                         for date, pred, conf in zip(future_dates, predictions, confidence)]
        return predicted_data, "Prediction successful"

    def analyze_patterns(self, data: List[Dict[str, Any]]) -> Tuple[Optional[Dict[str, Any]], str]:
        """Analyze data for recurring patterns or anomalies"""
        df = self.prepare_data(data)
        if len(df) < 3:
            return None, "Insufficient data for pattern analysis"

        # Simple moving average for trend detection
        df['moving_avg'] = df['cost'].rolling(window=3).mean()
        df['deviation'] = abs(df['cost'] - df['moving_avg'])
        
        # Detect anomalies (values deviating more than 1 std from moving average)
        threshold = df['deviation'].std()
        anomalies = df[df['deviation'] > threshold]
        anomaly_dates = anomalies['date'].dt.strftime('%Y-%m-%d').tolist()
        
        return {'anomalies': anomaly_dates}, "Pattern analysis completed"
