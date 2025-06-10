from typing import List, Dict, Any
import numpy as np
from scipy.optimize import linprog
from .financial_models import FinancialProject, FinancialTransaction
from .database import get_db
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class CostOptimizer:
    def __init__(self, db: Session = next(get_db())):
        self.db = db
    
    def optimize_project_costs(self, project_id: int) -> Dict[str, Any]:
        """
        Optimize project costs using linear programming
        Returns recommended budget allocations and potential savings
        """
        # Get project and transactions
        project = self.db.query(FinancialProject).filter(FinancialProject.id == project_id).first()
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id
        ).all()
        
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Prepare optimization inputs
        categories = list(set(t.category for t in transactions if t.category))
        if not categories:
            return {"status": "no_categories", "message": "No transaction categories found"}
        
        # Cost coefficients (current spending per category)
        c = np.array([
            sum(t.amount for t in transactions if t.category == category)
            for category in categories
        ])
        
        # Budget constraint (total available budget)
        A_ub = np.ones((1, len(categories)))
        b_ub = np.array([project.budget * 1.1])  # Allow 10% over budget for optimization
        
        # Run linear programming optimization
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(0, None))
        
        if not res.success:
            return {"status": "optimization_failed", "message": res.message}
        
        # Prepare results
        recommended_allocation = dict(zip(categories, res.x))
        potential_savings = sum(c) - sum(res.x)
        
        return {
            "status": "success",
            "current_spending": dict(zip(categories, c)),
            "recommended_allocation": recommended_allocation,
            "potential_savings": potential_savings,
            "optimization_status": res.message
        }

    def detect_cost_anomalies(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Detect anomalous transactions using z-score analysis
        Returns list of transactions with high deviation from category norms
        """
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id
        ).all()
        
        if not transactions:
            return []
        
        # Group transactions by category
        categories = {}
        for t in transactions:
            if t.category not in categories:
                categories[t.category] = []
            categories[t.category].append(t.amount)
        
        # Calculate z-scores for each transaction
        anomalies = []
        for t in transactions:
            if t.category and len(categories[t.category]) > 1:
                amounts = np.array(categories[t.category])
                mean = np.mean(amounts)
                std = np.std(amounts)
                if std > 0:
                    z_score = abs((t.amount - mean) / std)
                    if z_score > 2:  # 2 standard deviations
                        anomalies.append({
                            "transaction_id": t.id,
                            "amount": t.amount,
                            "category": t.category,
                            "z_score": z_score,
                            "date": t.date,
                            "description": t.description
                        })
        
        return sorted(anomalies, key=lambda x: x["z_score"], reverse=True)

    def forecast_budget(self, project_id: int, periods: int = 3) -> Dict[str, Any]:
        """
        Forecast future budget needs using time series analysis
        periods: number of future periods to forecast (weeks/months)
        """
        project = self.db.query(FinancialProject).filter(FinancialProject.id == project_id).first()
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id
        ).order_by(FinancialTransaction.date).all()
        
        if not project or not transactions:
            return {"status": "insufficient_data", "message": "Not enough transaction history"}
        
        # Prepare time series data
        dates = [t.date for t in transactions if t.date]
        min_date, max_date = min(dates), max(dates)
        
        # Aggregate by month
        monthly_data = {}
        current_date = min_date.replace(day=1)
        while current_date <= max_date:
            next_date = (current_date + timedelta(days=32)).replace(day=1)
            monthly_sum = sum(
                t.amount for t in transactions 
                if t.date and current_date <= t.date < next_date
            )
            monthly_data[current_date] = monthly_sum
            current_date = next_date
        
        # Prepare data for forecasting
        dates = sorted(monthly_data.keys())
        values = [monthly_data[d] for d in dates]
        
        if len(values) < 3:
            return {"status": "insufficient_data", "message": "Need at least 3 months of data"}
        
        # Fit Holt-Winters model
        try:
            model = ExponentialSmoothing(
                values,
                trend='add',
                seasonal='add',
                seasonal_periods=4
            ).fit()
            forecast = model.forecast(periods)
        except Exception as e:
            return {"status": "forecast_failed", "message": str(e)}
        
        # Prepare forecast dates
        last_date = dates[-1]
        forecast_dates = [
            (last_date + timedelta(days=30*i)).replace(day=1) 
            for i in range(1, periods+1)
        ]
        
        return {
            "status": "success",
            "historical": {
                "dates": dates,
                "values": values
            },
            "forecast": {
                "dates": forecast_dates,
                "values": forecast.tolist()
            },
            "model_summary": str(model)
        }
