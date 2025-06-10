from sqlalchemy.orm import Session
from typing import Dict, Any, List
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import logging

from .financial_models import FinancialProject, FinancialTransaction, FinancialForecast

logger = logging.getLogger(__name__)

class BudgetForecaster:
    def __init__(self, db: Session):
        self.db = db
        self.linear_model = LinearRegression()
        self.rf_model = RandomForestRegressor(n_estimators=50, random_state=42)
    
    def create_long_term_forecast(self, project_id: int, months: int = 12, forecast_type: str = 'baseline') -> Dict[str, Any]:
        """
        Create a long-term budget forecast for a project using ensemble methods.
        Returns detailed monthly forecasts for the specified number of months.
        
        Args:
            project_id: ID of the project to forecast for
            months: Number of months to forecast into the future (default 12)
            forecast_type: Type of forecast - 'baseline', 'optimistic', or 'pessimistic'
        """
        project = self.db.query(FinancialProject).filter(FinancialProject.id == project_id).first()
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id
        ).order_by(FinancialTransaction.date).all()
        
        if not project or not transactions or len(transactions) < 6:
            return {
                "status": "no_data",
                "message": "Insufficient data for long-term forecasting. Need at least 6 months of transactions.",
                "project_id": project_id,
                "forecast": [],
                "confidence": 0.0,
                "forecast_type": forecast_type
            }
        
        # Prepare historical data
        dates = [t.date for t in transactions if t.date]
        amounts = [t.amount for t in transactions if t.date]
        
        if len(dates) < 6:
            return {
                "status": "no_data",
                "message": "Insufficient dated transactions for forecasting.",
                "project_id": project_id,
                "forecast": [],
                "confidence": 0.0,
                "forecast_type": forecast_type
            }
        
        # Aggregate by month for more stable trends
        monthly_data = {}
        min_date, max_date = min(dates), max(dates)
        current_date = min_date.replace(day=1)
        while current_date <= max_date:
            next_date = (current_date + timedelta(days=32)).replace(day=1)
            monthly_sum = sum(
                t.amount for i, t in enumerate(transactions) 
                if t.date and current_date <= t.date < next_date
            )
            monthly_data[current_date] = monthly_sum
            current_date = next_date
        
        # Prepare data for models
        hist_dates = sorted(monthly_data.keys())
        hist_values = [monthly_data[d] for d in hist_dates]
        date_nums = np.array([(d - hist_dates[0]).days for d in hist_dates]).reshape(-1, 1)
        
        # Train ensemble models
        try:
            self.linear_model.fit(date_nums, hist_values)
            linear_r2 = self.linear_model.score(date_nums, hist_values)
            
            # Prepare features for Random Forest (including temporal features)
            rf_features = np.array([
                [(d - hist_dates[0]).days, d.month, d.year] 
                for d in hist_dates
            ])
            self.rf_model.fit(rf_features, hist_values)
            rf_r2 = self.rf_model.score(rf_features, hist_values)
            
            # Weighted confidence based on model performance
            total_r2 = linear_r2 + rf_r2
            if total_r2 > 0:
                linear_weight = linear_r2 / total_r2
                rf_weight = rf_r2 / total_r2
            else:
                linear_weight = rf_weight = 0.5
            
            confidence = min(max(linear_r2, rf_r2), 0.9) if max(linear_r2, rf_r2) > 0 else 0.2
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            confidence = 0.1
            linear_weight = rf_weight = 0.5
            # Fallback to average
            avg_cost = sum(hist_values) / len(hist_values)
            self.linear_model.coef_ = np.array([0.0])
            self.linear_model.intercept_ = avg_cost
            self.rf_model = lambda x: np.array([avg_cost] * len(x))
        
        # Create forecast
        last_date = hist_dates[-1]
        forecast = []
        for i in range(months):
            forecast_date = (last_date + timedelta(days=30 * (i + 1))).replace(day=1)
            days_diff = (forecast_date - hist_dates[0]).days
            
            # Linear prediction
            linear_pred = max(0.0, float(self.linear_model.predict(np.array([[days_diff]]))[0]))
            
            # RF prediction
            rf_features = np.array([[days_diff, forecast_date.month, forecast_date.year]])
            rf_pred = max(0.0, float(self.rf_model.predict(rf_features)[0]))
            
            # Ensemble prediction (weighted average)
            predicted = (linear_pred * linear_weight) + (rf_pred * rf_weight)
            
            # Adjust based on forecast type
            if forecast_type == 'optimistic':
                predicted *= 0.85  # Assume lower costs
                adj_confidence = confidence * 0.8
            elif forecast_type == 'pessimistic':
                predicted *= 1.15  # Assume higher costs
                adj_confidence = confidence * 0.8
            else:  # baseline
                adj_confidence = confidence
            
            # Further adjust confidence based on time horizon (further out = less confident)
            horizon_factor = max(0.5, 1.0 - (i * 0.05))
            final_confidence = adj_confidence * horizon_factor
            
            forecast.append({
                "date": forecast_date.strftime("%Y-%m-%d"),
                "amount": round(predicted, 2),
                "type": forecast_type,
                "confidence": round(final_confidence, 2),
                "period": f"Month {i+1}",
                "components": {
                    "linear": round(linear_pred, 2),
                    "random_forest": round(rf_pred, 2)
                }
            })
        
        return {
            "status": "forecasted",
            "message": f"Long-term {forecast_type} budget forecast for next {months} months",
            "project_id": project_id,
            "forecast": forecast,
            "confidence": round(confidence, 2),
            "forecast_type": forecast_type,
            "historical_months": len(hist_dates),
            "model_weights": {
                "linear": round(linear_weight, 2),
                "random_forest": round(rf_weight, 2)
            }
        }
    
    def save_forecast_to_db(self, project_id: int, forecast_data: Dict[str, Any]) -> List[int]:
        """
        Save forecast results to database for historical tracking and reporting.
        Returns list of IDs for saved forecast records.
        """
        if forecast_data.get('status') != 'forecasted':
            logger.warning(f"Invalid forecast data status for project {project_id}: {forecast_data.get('status')}")
            return []
        
        forecast_type = forecast_data.get('forecast_type', 'baseline')
        saved_ids = []
        
        for entry in forecast_data['forecast']:
            try:
                forecast_date = datetime.strptime(entry['date'], '%Y-%m-%d')
                db_forecast = FinancialForecast(
                    project_id=project_id,
                    forecast_date=forecast_date,
                    period=entry['period'],
                    forecast_amount=entry['amount'],
                    confidence_score=entry['confidence'],
                    forecast_type=forecast_type
                )
                self.db.add(db_forecast)
                self.db.flush()  # Flush to get ID
                saved_ids.append(db_forecast.id)
            except Exception as e:
                logger.error(f"Failed to save forecast entry for {entry['date']}: {e}")
                continue
        
        self.db.commit()
        logger.info(f"Saved {len(saved_ids)} forecast entries for project {project_id}, type {forecast_type}")
        return saved_ids
    
    def get_historical_forecasts(self, project_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve historical forecasts for a project, ordered by forecast date descending.
        Returns list of past forecast records.
        """
        forecasts = self.db.query(FinancialForecast).filter(
            FinancialForecast.project_id == project_id
        ).order_by(FinancialForecast.forecast_date.desc()).limit(limit).all()
        
        return [{
            "id": f.id,
            "forecast_date": f.forecast_date.strftime("%Y-%m-%d") if f.forecast_date else "N/A",
            "period": f.period,
            "amount": f.forecast_amount,
            "confidence": f.confidence_score,
            "type": f.forecast_type
        } for f in forecasts]
    
    def evaluate_forecast_accuracy(self, project_id: int, past_months: int = 12) -> Dict[str, Any]:
        """
        Evaluate accuracy of past forecasts by comparing to actual spending.
        Returns accuracy metrics for forecast performance.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * past_months)
        
        # Get historical forecasts
        forecasts = self.db.query(FinancialForecast).filter(
            FinancialForecast.project_id == project_id,
            FinancialForecast.forecast_date >= start_date,
            FinancialForecast.forecast_date <= end_date
        ).order_by(FinancialForecast.forecast_date).all()
        
        # Get actual transactions
        transactions = self.db.query(FinancialTransaction).filter(
            FinancialTransaction.project_id == project_id,
            FinancialTransaction.date >= start_date,
            FinancialTransaction.date <= end_date
        ).all()
        
        if not forecasts or not transactions:
            return {
                "status": "no_data",
                "message": "Insufficient forecast or transaction data to evaluate accuracy",
                "project_id": project_id,
                "accuracy_metrics": {},
                "data_points": 0
            }
        
        # Aggregate transactions by month for comparison
        actuals = {}
        for t in transactions:
            if t.date:
                month_key = t.date.replace(day=1)
                actuals[month_key] = actuals.get(month_key, 0.0) + t.amount
        
        # Compare forecasts to actuals
        comparisons = []
        for f in forecasts:
            if f.forecast_date:
                forecast_month = f.forecast_date.replace(day=1)
                if forecast_month in actuals:
                    comparisons.append({
                        "month": forecast_month.strftime("%Y-%m"),
                        "forecast": f.forecast_amount,
                        "actual": actuals[forecast_month],
                        "type": f.forecast_type,
                        "error": abs(f.forecast_amount - actuals[forecast_month]),
                        "percent_error": abs(f.forecast_amount - actuals[forecast_month]) / actuals[forecast_month] if actuals[forecast_month] > 0 else 0.0
                    })
        
        if not comparisons:
            return {
                "status": "no_data",
                "message": "No overlapping forecast and actual data points for comparison",
                "project_id": project_id,
                "accuracy_metrics": {},
                "data_points": 0
            }
        
        # Calculate metrics
        errors = [c['error'] for c in comparisons]
        pct_errors = [c['percent_error'] for c in comparisons]
        
        return {
            "status": "evaluated",
            "message": f"Forecast accuracy evaluated over {len(comparisons)} data points",
            "project_id": project_id,
            "accuracy_metrics": {
                "mean_absolute_error": round(np.mean(errors), 2),
                "median_absolute_error": round(np.median(errors), 2),
                "mean_percent_error": round(np.mean(pct_errors) * 100, 1),
                "accuracy_score": round(max(0.0, 1.0 - np.mean(pct_errors)), 2)
            },
            "data_points": len(comparisons),
            "detailed_comparison": comparisons
        }
