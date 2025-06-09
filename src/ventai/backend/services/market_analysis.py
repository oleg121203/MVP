from typing import List, Dict
import pandas as pd
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class MarketAnalysisService:
    """Core service for price intelligence and supplier analysis"""
    
    def __init__(self):
        self.price_history = pd.DataFrame(columns=[
            'supplier_id', 'product_id', 'price', 'timestamp'
        ])
    
    def add_price_data(self, supplier_id: str, product_id: str, price: float) -> None:
        """Record new price data point"""
        new_data = pd.DataFrame([{
            'supplier_id': supplier_id,
            'product_id': product_id,
            'price': price,
            'timestamp': datetime.now(timezone.utc)
        }])
        
        self.price_history = pd.concat(
            [self.price_history, new_data], 
            ignore_index=True
        )
        logger.info(f"Added price data for {product_id} from {supplier_id}")
    
    def get_price_trends(self, product_id: str) -> Dict:
        """Analyze price trends for a product"""
        product_data = self.price_history[
            self.price_history['product_id'] == product_id
        ]
        
        if product_data.empty:
            return {
                "current_price": None,
                "min_price": None,
                "price_difference": None,
                "supplier_count": 0,
                "trend": "no_data"
            }
            
        latest = product_data.iloc[-1]
        min_price = product_data['price'].min()
        
        return {
            "current_price": latest['price'],
            "min_price": min_price,
            "price_difference": latest['price'] - min_price,
            "supplier_count": product_data['supplier_id'].nunique(),
            "trend": self._calculate_trend(product_data)
        }
    
    def _calculate_trend(self, data: pd.DataFrame) -> str:
        """Determine price trend (upward/downward/stable)"""
        # Simple trend analysis - can be enhanced with ML
        if len(data) < 2:
            return "stable"
            
        recent = data.iloc[-10:]  # Last 10 data points
        slope = (recent['price'].iloc[-1] - recent['price'].iloc[0]) / len(recent)
        
        if slope > 0.05:
            return "upward"
        elif slope < -0.05:
            return "downward"
        return "stable"
    
    def get_cost_saving_recommendations(self, product_ids: List[str]) -> Dict:
        """Generate cost-saving recommendations for products"""
        recommendations = {}
        
        for pid in product_ids:
            trends = self.get_price_trends(pid)
            if trends["trend"] == "no_data":
                continue
                
            if trends["price_difference"] and trends["price_difference"] > 0:
                recommendations[pid] = {
                    "potential_savings": trends["price_difference"],
                    "recommendation": "Consider switching suppliers"
                }
            elif trends["trend"] == "upward":
                recommendations[pid] = {
                    "potential_savings": None,
                    "recommendation": "Prices rising - consider bulk purchase"
                }
        
        return recommendations
