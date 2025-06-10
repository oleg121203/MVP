import pytest
import pandas as pd
import sys
import os

# Add the parent directory to sys.path to find the app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.price_analyzer import PriceAnalyzer

@pytest.fixture
async def analyzer():
    return PriceAnalyzer()

@pytest.mark.asyncio
async def test_load_data(analyzer):
    data = analyzer.load_data(limit=10)
    assert isinstance(data, pd.DataFrame)

@pytest.mark.asyncio
async def test_calculate_basic_stats(analyzer):
    stats = analyzer.calculate_basic_stats()
    assert isinstance(stats, dict)
    if stats:
        assert 'mean_price' in stats
        assert 'median_price' in stats
        assert 'std_price' in stats
        assert 'min_price' in stats
        assert 'max_price' in stats
        assert 'count' in stats

@pytest.mark.asyncio
async def test_calculate_trends(analyzer):
    trends = analyzer.calculate_trends(window=3)
    assert isinstance(trends, pd.DataFrame)
    if not trends.empty:
        assert 'moving_average' in trends.columns
        assert 'trend' in trends.columns

@pytest.mark.asyncio
async def test_detect_outliers(analyzer):
    outliers = analyzer.detect_outliers(threshold=1.5)
    assert isinstance(outliers, pd.DataFrame)
    if not outliers.empty:
        assert 'is_outlier' in analyzer.data.columns
        assert all(analyzer.data.loc[outliers.index, 'is_outlier'])
