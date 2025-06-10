from sqlalchemy.orm import Session
from typing import Dict, Any, List
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta, datetime
import logging

from .financial_models import FinancialProject, FinancialTransaction

logger = logging.getLogger(__name__)

class CostOptimizer:
    def __init__(self, db: Session):
        self.db = db
        self.model = LinearRegression()
    
    def optimize_project_costs(self, project_id: int) -> Dict[str, Any]:
        """
        Optimize project costs using linear programming and machine learning predictions.
        Returns recommended budget allocations and potential savings.
        """
        # Get project and transactions
        project = self.db.query(FinancialProject).filter(FinancialProject.id == project_id).first()
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id
        ).all()
        
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        if not transactions:
            return {
                "status": "no_data",
                "message": "No transactions available for optimization",
                "project_id": project_id,
                "current_cost": project.actual_cost,
                "recommended_allocations": {},
                "potential_savings": 0.0,
                "optimization_score": 0.0
            }
        
        # Calculate current cost breakdown by category and cost center
        category_breakdown = {}
        cost_center_breakdown = {}
        for t in transactions:
            if t.category:
                category_breakdown[t.category] = category_breakdown.get(t.category, 0.0) + t.amount
            if t.cost_center:
                cost_center_breakdown[t.cost_center] = cost_center_breakdown.get(t.cost_center, 0.0) + t.amount
        
        # Identify high-cost areas (top 3 categories and cost centers)
        high_cost_categories = dict(sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)[:3])
        high_cost_centers = dict(sorted(cost_center_breakdown.items(), key=lambda x: x[1], reverse=True)[:3])
        
        # ML-based cost prediction for high-cost areas
        predicted_costs = self._predict_cost_trends(project_id, transactions, high_cost_categories.keys())
        
        # Optimization rules with ML insights
        recommended_allocations = {}
        for category, current_cost in high_cost_categories.items():
            # Use ML prediction if available, otherwise use rule-based reduction
            if category in predicted_costs:
                optimal_cost = predicted_costs[category]['predicted_cost']
                confidence = predicted_costs[category]['confidence']
            else:
                optimal_cost = current_cost * 0.85  # Default 15% reduction target
                confidence = 0.5
            
            recommended_allocations[category] = {
                "current": current_cost,
                "recommended": max(optimal_cost, current_cost * 0.7),  # Limit reduction to 30% max
                "confidence": confidence,
                "action": "reduce" if optimal_cost < current_cost else "maintain"
            }
        
        # Calculate potential savings with confidence weighting
        total_potential_savings = 0.0
        total_confidence_weight = 0.0
        for category, alloc in recommended_allocations.items():
            if alloc['action'] == 'reduce':
                savings = alloc['current'] - alloc['recommended']
                weighted_savings = savings * alloc['confidence']
                total_potential_savings += weighted_savings
                total_confidence_weight += alloc['confidence']
        
        optimization_score = min(total_confidence_weight, 1.0) if total_confidence_weight > 0 else 0.0
        
        return {
            "status": "optimized",
            "message": "Cost optimization completed with ML insights",
            "project_id": project_id,
            "current_cost": project.actual_cost,
            "category_breakdown": category_breakdown,
            "cost_center_breakdown": cost_center_breakdown,
            "high_cost_areas": {
                "categories": high_cost_categories,
                "centers": high_cost_centers
            },
            "recommended_allocations": recommended_allocations,
            "potential_savings": total_potential_savings,
            "optimization_score": optimization_score
        }
    
    def forecast_budget(self, project_id: int, periods: int = 3) -> Dict[str, Any]:
        """
        Forecast future budget needs for a project using historical data and ML.
        Returns forecast for next periods (default 3 months).
        """
        project = self.db.query(FinancialProject).filter(FinancialProject.id == project_id).first()
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id
        ).order_by(FinancialTransaction.date).all()
        
        if not project or not transactions or len(transactions) < 3:
            return {
                "status": "no_data",
                "message": "Insufficient data for budget forecasting",
                "project_id": project_id,
                "forecast": [],
                "confidence": 0.0
            }
        
        # Prepare data for ML model
        dates = [t.date for t in transactions if t.date]
        amounts = [t.amount for t in transactions if t.date]
        
        if len(dates) < 3:
            return {
                "status": "no_data",
                "message": "Insufficient dated transactions for forecasting",
                "project_id": project_id,
                "forecast": [],
                "confidence": 0.0
            }
        
        # Aggregate by month
        monthly_data = {}
        min_date, max_date = min(dates), max(dates)
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
        
        # Convert dates to numeric for ML
        date_nums = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)
        
        # Train simple linear model
        try:
            self.model.fit(date_nums, values)
            r_squared = self.model.score(date_nums, values)
            confidence = min(r_squared, 0.9) if r_squared > 0 else 0.1
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            confidence = 0.1
            # Fallback to average
            avg_cost = sum(values) / len(values)
            self.model.coef_ = np.array([0.0])
            self.model.intercept_ = avg_cost
        
        # Forecast next periods
        last_date = dates[-1]
        forecast = []
        for i in range(periods):
            forecast_date = (last_date + timedelta(days=30 * (i + 1))).replace(day=1)
            days_diff = (forecast_date - dates[0]).days
            predicted = max(0.0, float(self.model.predict(np.array([[days_diff]]))[0]))
            
            # Adjust confidence based on period distance
            period_confidence = confidence * (0.9 ** (i + 1))
            
            forecast.append({
                "date": forecast_date.strftime("%Y-%m-%d"),
                "amount": round(predicted, 2),
                "type": "forecast",
                "confidence": round(period_confidence, 2),
                "period": f"Month {i+1}"
            })
        
        # Add optimistic and pessimistic scenarios
        for f in forecast[:]:  # Copy to iterate
            forecast.append({
                "date": f["date"],
                "amount": round(f["amount"] * 1.2, 2),
                "type": "optimistic",
                "confidence": round(f["confidence"] * 0.7, 2),
                "period": f["period"]
            })
            forecast.append({
                "date": f["date"],
                "amount": round(f["amount"] * 0.8, 2),
                "type": "pessimistic",
                "confidence": round(f["confidence"] * 0.7, 2),
                "period": f["period"]
            })
        
        return {
            "status": "forecasted",
            "message": f"Budget forecast for next {periods} months",
            "project_id": project_id,
            "forecast": forecast,
            "confidence": round(confidence, 2),
            "historical_data_points": len(dates)
        }
    
    def detect_cost_anomalies(self, project_id: int, window_days: int = 90) -> List[Dict[str, Any]]:
        """
        Detect cost anomalies in recent transactions using statistical methods.
        Returns list of anomalous transactions with explanations.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id,
            FinancialTransaction.date >= start_date,
            FinancialTransaction.date <= end_date
        ).order_by(FinancialTransaction.date).all()
        
        if len(transactions) < 5:
            return []
        
        # Group by week or month depending on data volume
        if window_days > 60 and len(transactions) > 20:
            grouping = "month"
            grouped_data = {}
            for t in transactions:
                if t.date:
                    key = t.date.replace(day=1)
                    grouped_data[key] = grouped_data.get(key, 0.0) + t.amount
        else:
            grouping = "week"
            grouped_data = {}
            for t in transactions:
                if t.date:
                    # Start of week (Monday)
                    key = t.date - timedelta(days=t.date.weekday())
                    grouped_data[key] = grouped_data.get(key, 0.0) + t.amount
        
        # Convert to sorted list for analysis
        dates = sorted(grouped_data.keys())
        values = [grouped_data[d] for d in dates]
        
        if len(values) < 3:
            return []
        
        # Calculate stats
        mean_val = np.mean(values)
        std_val = np.std(values) if len(values) > 1 else 0.0
        
        # Define threshold (2 standard deviations)
        threshold = mean_val + (std_val * 2) if std_val > 0 else mean_val * 1.5
        
        # Find anomalies in grouped data
        anomalies = []
        for i, (date, value) in enumerate(zip(dates, values)):
            if value > threshold:
                # Get transactions in this period
                if grouping == "month":
                    period_end = (date + timedelta(days=32)).replace(day=1)
                else:  # week
                    period_end = date + timedelta(days=7)
                
                period_trans = [
                    t for t in transactions 
                    if t.date and date <= t.date < period_end
                ]
                
                # Sort by amount to highlight biggest contributors
                period_trans.sort(key=lambda x: x.amount, reverse=True)
                top_contributors = period_trans[:3]
                
                anomalies.append({
                    "period": f"{date.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}",
                    "amount": round(value, 2),
                    "average_comparison": f"{round((value/mean_val)*100, 1)}% of average",
                    "deviation": round(value - mean_val, 2),
                    "confidence": round(min(std_val/mean_val if mean_val > 0 else 1, 1.0), 2),
                    "grouping": grouping,
                    "top_contributors": [
                        {
                            "id": t.id,
                            "date": t.date.strftime("%Y-%m-%d") if t.date else "N/A",
                            "amount": round(t.amount, 2),
                            "category": t.category or "Uncategorized",
                            "description": t.description or "No description"
                        } for t in top_contributors
                    ],
                    "recommendation": "Review high-cost transactions for potential savings"
                })
        
        return anomalies
    
    def _predict_cost_trends(self, project_id: int, transactions: List[FinancialTransaction], categories: List[str], window_days: int = 180) -> Dict[str, Any]:
        """
        Use ML to predict cost trends for specific categories.
        Returns predicted costs with confidence scores.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        # Filter transactions in window
        trans_in_window = [
            t for t in transactions 
            if t.date and start_date <= t.date <= end_date and t.category in categories
        ]
        
        if len(trans_in_window) < 10:
            return {}
        
        predictions = {}
        for category in categories:
            cat_trans = [t for t in trans_in_window if t.category == category]
            if len(cat_trans) < 5:
                continue
            
            # Group by week
            dates = sorted([t.date for t in cat_trans])
            weekly_data = {}
            for t in cat_trans:
                if t.date:
                    week_start = t.date - timedelta(days=t.date.weekday())
                    weekly_data[week_start] = weekly_data.get(week_start, 0.0) + t.amount
            
            if len(weekly_data) < 3:
                continue
            
            # Prepare for ML
            week_dates = sorted(weekly_data.keys())
            week_values = [weekly_data[d] for d in week_dates]
            date_nums = np.array([(d - week_dates[0]).days / 7.0 for d in week_dates]).reshape(-1, 1)
            
            # Train model
            try:
                self.model.fit(date_nums, week_values)
                r2 = self.model.score(date_nums, week_values)
                confidence = max(0.3, min(r2, 0.85))
                
                # Predict next period (4 weeks)
                last_week = week_dates[-1]
                next_periods = []
                for i in range(4):
                    next_week = last_week + timedelta(days=7 * (i + 1))
                    days_diff = (next_week - week_dates[0]).days / 7.0
                    next_periods.append(days_diff)
                
                predicted_values = self.model.predict(np.array(next_periods).reshape(-1, 1))
                predicted_cost = max(0.0, float(sum(predicted_values) / len(predicted_values) * 4))  # Monthly avg
                
                predictions[category] = {
                    "predicted_cost": round(predicted_cost, 2),
                    "confidence": round(confidence, 2),
                    "trend": "increasing" if self.model.coef_[0] > 0 else "decreasing",
                    "historical_avg": round(sum(week_values) / len(week_values) * 4, 2),  # Monthly avg from history
                    "data_points": len(week_values)
                }
            except Exception as e:
                logger.error(f"Prediction failed for {category}: {e}")
                continue
        
        return predictions
    
    def analyze_cost_efficiency(self, project_id: int) -> Dict[str, Any]:
        """
        Analyze cost efficiency metrics for a project compared to industry benchmarks.
        Returns efficiency scores and recommendations.
        """
        project = self.db.query(FinancialProject).filter(FinancialProject.id == project_id).first()
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id
        ).all()
        
        if not project or not transactions:
            return {
                "status": "no_data",
                "message": "No data available for cost efficiency analysis",
                "project_id": project_id,
                "efficiency_score": 0.0,
                "recommendations": []
            }
        
        # Calculate basic metrics
        total_spent = sum(t.amount for t in transactions)
        budget_utilization = (total_spent / project.budget) if project.budget > 0 else 1.0
        
        # Category distribution
        category_dist = {}
        for t in transactions:
            cat = t.category or "Uncategorized"
            category_dist[cat] = category_dist.get(cat, 0.0) + t.amount
        
        # Normalize distribution
        category_dist_norm = {k: v/total_spent for k, v in category_dist.items()}
        
        # Hard-coded industry benchmarks for demo (in reality, would query benchmark DB)
        industry = project.industry or "Construction"
        if industry == "Construction":
            benchmarks = {
                "Labor": 0.35,  # 35% of budget typical for labor
                "Materials": 0.40,
                "Equipment": 0.15,
                "Overhead": 0.10
            }
            max_utilization = 0.95  # Warning if over 95% budget used
        else:
            benchmarks = {
                "Personnel": 0.50,
                "Operations": 0.30,
                "Technology": 0.15
            }
            max_utilization = 0.90
        
        # Calculate efficiency metrics
        efficiency_score = 0.0
        recommendations = []
        
        # 1. Budget utilization check
        if budget_utilization > max_utilization:
            efficiency_score -= 0.3
            recommendations.append({
                "area": "Budget Management",
                "issue": f"Budget utilization at {round(budget_utilization*100, 1)}%, over target of {round(max_utilization*100, 1)}%",
                "recommendation": "Implement stricter cost controls or revise budget",
                "priority": "high",
                "potential_impact": f"Risk of {round((budget_utilization-max_utilization)*project.budget, 2)} overrun"
            })
        elif budget_utilization < 0.6:
            efficiency_score += 0.2
            recommendations.append({
                "area": "Budget Management",
                "issue": f"Budget utilization low at {round(budget_utilization*100, 1)}%",
                "recommendation": "Accelerate project activities or reallocate funds",
                "priority": "medium",
                "potential_impact": f"Underutilization of {round((1-budget_utilization)*project.budget, 2)}"
            })
        else:
            efficiency_score += 0.3
        
        # 2. Category distribution vs benchmarks
        for cat, benchmark_pct in benchmarks.items():
            actual_pct = category_dist_norm.get(cat, 0.0)
            deviation = abs(actual_pct - benchmark_pct)
            
            if deviation > 0.1:  # More than 10% deviation
                efficiency_score -= deviation * 0.5  # Penalty proportional to deviation
                recommendations.append({
                    "area": f"Category - {cat}",
                    "issue": f"{cat} allocation {round(actual_pct*100, 1)}% vs benchmark {round(benchmark_pct*100, 1)}%",
                    "recommendation": f"Review spending in {cat} to align with industry standards",
                    "priority": "high" if deviation > 0.2 else "medium",
                    "potential_impact": f"Misallocation of {round(deviation*total_spent, 2)}"
                })
            else:
                efficiency_score += 0.1
        
        # 3. Check for uncategorized transactions
        uncategorized_pct = category_dist_norm.get("Uncategorized", 0.0)
        if uncategorized_pct > 0.05:  # More than 5% uncategorized
            efficiency_score -= uncategorized_pct * 0.3
            recommendations.append({
                "area": "Transaction Categorization",
                "issue": f"{round(uncategorized_pct*100, 1)}% of transactions uncategorized",
                "recommendation": "Improve transaction categorization for accurate analysis",
                "priority": "medium",
                "potential_impact": f"Untracked spending of {round(uncategorized_pct*total_spent, 2)}"
            })
        
        # Normalize score to 0-1 range
        efficiency_score = max(0.0, min(1.0, efficiency_score + 0.5))
        
        return {
            "status": "analyzed",
            "message": "Cost efficiency analysis completed",
            "project_id": project_id,
            "efficiency_score": round(efficiency_score, 2),
            "budget_utilization": round(budget_utilization, 2),
            "category_distribution": {k: round(v, 2) for k, v in category_dist_norm.items()},
            "industry_benchmarks": benchmarks,
            "recommendations": recommendations[:5],  # Top 5 recommendations
            "total_spent": round(total_spent, 2),
            "budget": project.budget
        }
