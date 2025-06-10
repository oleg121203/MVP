import pytest
import pandas as pd
import numpy as np

import sys
sys.path.append("../")
from backend.app.services.price_predictor import PricePredictor

@pytest.fixture
def predictor():
    return PricePredictor()

@pytest.mark.asyncio
async def test_load_data(predictor):
    predictor.load_data()
    assert isinstance(predictor.data, pd.DataFrame)
    assert not predictor.data.empty
    assert 'timestamp' in predictor.data.columns
    assert 'price' in predictor.data.columns

@pytest.mark.asyncio
async def test_prepare_features(predictor):
    predictor.load_data()
    features = predictor.prepare_features(predictor.data)
    assert isinstance(features, np.ndarray)
    assert features.shape[0] == len(predictor.data)
    assert features.shape[1] == 1  # Only 'days_since_start' feature

@pytest.mark.asyncio
async def test_train_model(predictor):
    predictor.load_data()
    predictor.train_model()
    # No direct assertion for training, but it should complete without errors

@pytest.mark.asyncio
async def test_predict(predictor):
    predictor.load_data()
    predictor.train_model()
    predictions = predictor.predict(future_days=7)
    assert isinstance(predictions, list)
    assert len(predictions) == 7
    assert all(isinstance(p, float) for p in predictions)

@pytest.mark.asyncio
async def test_evaluate_model(predictor):
    predictor.load_data()
    predictor.train_model()
    metrics = predictor.evaluate_model()
    assert isinstance(metrics, dict)
    assert 'mse' in metrics
    assert 'r2' in metrics
    assert isinstance(metrics['mse'], float)
    assert isinstance(metrics['r2'], float)
