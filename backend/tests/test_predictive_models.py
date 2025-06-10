import pytest
import sys
import os

# Add the parent directory to sys.path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from analytics.predictive_models import PredictiveAnalytics
except ImportError:
    # Fallback for different directory structure
    from backend.analytics.predictive_models import PredictiveAnalytics

# Mock data for testing
mock_data = [
    {'date': '2025-06-01', 'cost': 1000, 'performance': 80, 'efficiency': 75},
    {'date': '2025-06-02', 'cost': 1200, 'performance': 85, 'efficiency': 78},
    {'date': '2025-06-03', 'cost': 1100, 'performance': 82, 'efficiency': 77},
    {'date': '2025-06-04', 'cost': 1300, 'performance': 88, 'efficiency': 80},
    {'date': '2025-06-05', 'cost': 900, 'performance': 78, 'efficiency': 73},
]

def test_prepare_data():
    analytics = PredictiveAnalytics()
    df = analytics.prepare_data(mock_data)
    assert 'days' in df.columns
    assert len(df) == len(mock_data)

def test_train_model():
    analytics = PredictiveAnalytics()
    success, message = analytics.train_model(mock_data, target_column='cost')
    assert success is True
    assert message == "Model trained successfully"
    assert analytics.is_trained is True

def test_train_model_insufficient_data():
    analytics = PredictiveAnalytics()
    success, message = analytics.train_model([mock_data[0]], target_column='cost')
    assert success is False
    assert message == "Insufficient data for training"
    assert analytics.is_trained is False

def test_predict_trend_not_trained():
    analytics = PredictiveAnalytics()
    result, message = analytics.predict_trend(mock_data)
    assert result is None
    assert message == "Model not trained yet"

def test_predict_trend_no_data():
    analytics = PredictiveAnalytics()
    analytics.is_trained = True  # Manually set to trained for testing
    result, message = analytics.predict_trend([])
    assert result is None
    assert message == "No data provided for prediction"

def test_predict_trend_success():
    analytics = PredictiveAnalytics()
    analytics.train_model(mock_data, target_column='cost')
    result, message = analytics.predict_trend(mock_data, future_days=3)
    assert result is not None
    assert len(result) == 3
    assert message == "Prediction successful"
    assert 'date' in result[0]
    assert 'predicted_cost' in result[0]

def test_analyze_patterns_insufficient_data():
    analytics = PredictiveAnalytics()
    result, message = analytics.analyze_patterns([mock_data[0]])
    assert result is None
    assert message == "Insufficient data for pattern analysis"

def test_analyze_patterns_success():
    analytics = PredictiveAnalytics()
    result, message = analytics.analyze_patterns(mock_data)
    assert result is not None
    assert 'anomalies' in result
    assert message == "Pattern analysis completed"
