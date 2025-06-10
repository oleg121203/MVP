import numpy as np
import pandas as pd
from typing import List, Dict, Any
import logging

# Mock database session for testing
class MockSession:
    def __init__(self):
        self.bind = None

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceAnalyzer:
    def __init__(self):
        self.data = None
        self.db = MockSession()  # Use mock session for testing

    def load_data(self, limit: int = 1000) -> pd.DataFrame:
        """Load price data from the database or create mock data for testing."""
        try:
            # For testing, create mock data if database is not available
            self.data = pd.DataFrame({
                'id': range(10),
                'product_id': [f'prod_{i}' for i in range(10)],
                'price': np.random.uniform(10, 100, 10),
                'timestamp': pd.date_range(start='2025-06-01', periods=10, freq='D'),
                'source': ['mock_source'] * 10
            })
            logger.info(f"Loaded {len(self.data)} mock price data points for analysis")
            return self.data
        except Exception as e:
            logger.error(f"Error loading price data: {str(e)}")
            return pd.DataFrame()

    def calculate_basic_stats(self) -> Dict[str, Any]:
        """Calculate basic statistics for price data."""
        if self.data is None or self.data.empty:
            self.load_data()

        if not self.data.empty:
            stats = {
                'mean_price': self.data['price'].mean(),
                'median_price': self.data['price'].median(),
                'std_price': self.data['price'].std(),
                'min_price': self.data['price'].min(),
                'max_price': self.data['price'].max(),
                'count': len(self.data)
            }
            logger.info("Calculated basic statistics for price data")
            return stats
        else:
            logger.warning("No price data available for statistical analysis")
            return {}

    def calculate_trends(self, window: int = 7) -> pd.DataFrame:
        """Calculate moving averages and trends for price data."""
        if self.data is None or self.data.empty:
            self.load_data()

        if not self.data.empty:
            self.data['moving_average'] = self.data['price'].rolling(window=window).mean()
            self.data['trend'] = np.where(
                self.data['price'] > self.data['moving_average'],
                'Upward',
                np.where(self.data['price'] < self.data['moving_average'], 'Downward', 'Stable')
            )
            logger.info(f"Calculated trends with a {window}-day moving average")
            return self.data[['product_id', 'price', 'moving_average', 'trend', 'timestamp']]
        else:
            logger.warning("No price data available for trend analysis")
            return pd.DataFrame()

    def detect_outliers(self, threshold: float = 2.0) -> pd.DataFrame:
        """Detect outliers in price data using standard deviation method."""
        if self.data is None or self.data.empty:
            self.load_data()

        if not self.data.empty:
            mean_price = self.data['price'].mean()
            std_price = self.data['price'].std()
            self.data['is_outlier'] = abs(self.data['price'] - mean_price) > (threshold * std_price)
            outliers = self.data[self.data['is_outlier']]
            logger.info(f"Detected {len(outliers)} outliers in price data")
            return outliers[['product_id', 'price', 'timestamp', 'source']]
        else:
            logger.warning("No price data available for outlier detection")
            return pd.DataFrame()

# Usage example
def main():
    analyzer = PriceAnalyzer()
    stats = analyzer.calculate_basic_stats()
    if stats:
        print("Basic Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    trends = analyzer.calculate_trends()
    if not trends.empty:
        print("\nTrends (sample):")
        print(trends.head())

    outliers = analyzer.detect_outliers()
    if not outliers.empty:
        print("\nOutliers (sample):")
        print(outliers.head())

if __name__ == "__main__":
    main()
