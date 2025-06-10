import logging
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AIPredictiveAnalytics:
    def __init__(self, model_dir: str = 'ai_models'):
        """
        Initialize AI Predictive Analytics module for financial forecasting
        """
        self.model_dir = model_dir
        self.models = {
            'linear_regression': None,
            'random_forest': None
        }
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.last_training = None
        os.makedirs(self.model_dir, exist_ok=True)
        logger.info("AI Predictive Analytics initialized")

    def load_models(self) -> bool:
        """
        Load trained models from disk if available
        Returns True if at least one model was loaded successfully
        """
        loaded = False
        try:
            lr_path = os.path.join(self.model_dir, 'linear_regression_model.joblib')
            if os.path.exists(lr_path):
                self.models['linear_regression'] = joblib.load(lr_path)
                logger.info("Loaded Linear Regression model")
                loaded = True

            rf_path = os.path.join(self.model_dir, 'random_forest_model.joblib')
            if os.path.exists(rf_path):
                self.models['random_forest'] = joblib.load(rf_path)
                logger.info("Loaded Random Forest model")
                loaded = True

            scaler_X_path = os.path.join(self.model_dir, 'scaler_X.joblib')
            if os.path.exists(scaler_X_path):
                self.scaler_X = joblib.load(scaler_X_path)
                logger.info("Loaded feature scaler")

            scaler_y_path = os.path.join(self.model_dir, 'scaler_y.joblib')
            if os.path.exists(scaler_y_path):
                self.scaler_y = joblib.load(scaler_y_path)
                logger.info("Loaded target scaler")

            last_training_path = os.path.join(self.model_dir, 'last_training.txt')
            if os.path.exists(last_training_path):
                with open(last_training_path, 'r') as f:
                    self.last_training = f.read().strip()
                logger.info(f"Last training timestamp loaded: {self.last_training}")

            return loaded
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False

    def save_models(self) -> bool:
        """
        Save trained models and scalers to disk
        Returns True if save was successful
        """
        try:
            if self.models['linear_regression'] is not None:
                joblib.dump(self.models['linear_regression'], os.path.join(self.model_dir, 'linear_regression_model.joblib'))
                logger.info("Saved Linear Regression model")

            if self.models['random_forest'] is not None:
                joblib.dump(self.models['random_forest'], os.path.join(self.model_dir, 'random_forest_model.joblib'))
                logger.info("Saved Random Forest model")

            joblib.dump(self.scaler_X, os.path.join(self.model_dir, 'scaler_X.joblib'))
            logger.info("Saved feature scaler")

            joblib.dump(self.scaler_y, os.path.join(self.model_dir, 'scaler_y.joblib'))
            logger.info("Saved target scaler")

            self.last_training = datetime.now().isoformat()
            with open(os.path.join(self.model_dir, 'last_training.txt'), 'w') as f:
                f.write(self.last_training)
            logger.info(f"Updated last training timestamp: {self.last_training}")

            return True
        except Exception as e:
            logger.error(f"Error saving models: {e}")
            return False

    def train_models(self, data: pd.DataFrame, target_column: str, feature_columns: List[str], 
                     test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
        """
        Train AI models for predictive analytics
        Args:
            data: DataFrame containing the training data
            target_column: Name of the column to predict
            feature_columns: List of column names to use as features
            test_size: Fraction of data to use for testing
            random_state: Random seed for reproducibility
        Returns:
            Dictionary with training results and metrics
        """
        try:
            logger.info(f"Starting model training for target: {target_column}")
            X = data[feature_columns]
            y = data[target_column]

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )

            # Scale features and target
            X_train_scaled = self.scaler_X.fit_transform(X_train)
            X_test_scaled = self.scaler_X.transform(X_test)
            y_train_scaled = self.scaler_y.fit_transform(y_train.values.reshape(-1, 1)).ravel()
            y_test_scaled = self.scaler_y.transform(y_test.values.reshape(-1, 1)).ravel()

            # Train Linear Regression
            lr_model = LinearRegression()
            lr_model.fit(X_train_scaled, y_train_scaled)
            lr_train_pred = lr_model.predict(X_train_scaled)
            lr_test_pred = lr_model.predict(X_test_scaled)
            lr_train_mse = mean_squared_error(y_train_scaled, lr_train_pred)
            lr_test_mse = mean_squared_error(y_test_scaled, lr_test_pred)
            lr_train_r2 = r2_score(y_train_scaled, lr_train_pred)
            lr_test_r2 = r2_score(y_test_scaled, lr_test_pred)
            logger.info(f"Linear Regression - Train MSE: {lr_train_mse:.4f}, Test MSE: {lr_test_mse:.4f}")
            logger.info(f"Linear Regression - Train R2: {lr_train_r2:.4f}, Test R2: {lr_test_r2:.4f}")

            # Train Random Forest
            rf_model = RandomForestRegressor(n_estimators=100, random_state=random_state, n_jobs=-1)
            rf_model.fit(X_train_scaled, y_train_scaled)
            rf_train_pred = rf_model.predict(X_train_scaled)
            rf_test_pred = rf_model.predict(X_test_scaled)
            rf_train_mse = mean_squared_error(y_train_scaled, rf_train_pred)
            rf_test_mse = mean_squared_error(y_test_scaled, rf_test_pred)
            rf_train_r2 = r2_score(y_train_scaled, rf_train_pred)
            rf_test_r2 = r2_score(y_test_scaled, rf_test_pred)
            logger.info(f"Random Forest - Train MSE: {rf_train_mse:.4f}, Test MSE: {rf_test_mse:.4f}")
            logger.info(f"Random Forest - Train R2: {rf_train_r2:.4f}, Test R2: {rf_test_r2:.4f}")

            # Store models
            self.models['linear_regression'] = lr_model
            self.models['random_forest'] = rf_model

            # Save models
            self.save_models()

            return {
                "status": "success",
                "message": "Models trained successfully",
                "training_time": datetime.now().isoformat(),
                "data_shape": {
                    "total_samples": len(data),
                    "training_samples": len(X_train),
                    "testing_samples": len(X_test),
                    "features": len(feature_columns)
                },
                "linear_regression": {
                    "train_mse": lr_train_mse,
                    "test_mse": lr_test_mse,
                    "train_r2": lr_train_r2,
                    "test_r2": lr_test_r2
                },
                "random_forest": {
                    "train_mse": rf_train_mse,
                    "test_mse": rf_test_mse,
                    "train_r2": rf_train_r2,
                    "test_r2": rf_test_r2
                }
            }
        except Exception as e:
            logger.error(f"Error training models: {e}")
            return {"status": "error", "message": str(e)}

    def predict(self, data: pd.DataFrame, model_type: str = 'random_forest') -> Dict[str, Any]:
        """
        Make predictions using the specified model
        Args:
            data: DataFrame with features for prediction
            model_type: Type of model to use ('linear_regression' or 'random_forest')
        Returns:
            Dictionary with predictions and confidence metrics if available
        """
        try:
            if model_type not in self.models or self.models[model_type] is None:
                # Try to load models if not loaded
                if not self.load_models() or self.models[model_type] is None:
                    return {
                        "status": "error",
                        "message": f"Model {model_type} not trained or loaded"
                    }

            # Ensure all expected feature columns are present
            expected_features = getattr(self.models[model_type], 'feature_names_in_', None)
            if expected_features is not None:
                missing_features = [f for f in expected_features if f not in data.columns]
                if missing_features:
                    logger.warning(f"Missing features in input data: {missing_features}")
                    # Fill missing features with zeros or appropriate default
                    for f in missing_features:
                        data[f] = 0

            # Scale input data
            X_scaled = self.scaler_X.transform(data)

            # Make predictions
            predictions_scaled = self.models[model_type].predict(X_scaled)

            # Inverse transform predictions
            predictions = self.scaler_y.inverse_transform(predictions_scaled.reshape(-1, 1)).ravel()

            # Calculate confidence intervals (simplified for Random Forest)
            confidence_intervals = None
            if model_type == 'random_forest':
                # Use tree predictions for confidence interval (simplified approach)
                tree_predictions = np.array([tree.predict(X_scaled) for tree in self.models[model_type].estimators_])
                if tree_predictions.shape[0] > 0:
                    ci_lower_scaled = np.percentile(tree_predictions, 2.5, axis=0)
                    ci_upper_scaled = np.percentile(tree_predictions, 97.5, axis=0)
                    ci_lower = self.scaler_y.inverse_transform(ci_lower_scaled.reshape(-1, 1)).ravel()
                    ci_upper = self.scaler_y.inverse_transform(ci_upper_scaled.reshape(-1, 1)).ravel()
                    confidence_intervals = list(zip(ci_lower, ci_upper))

            return {
                "status": "success",
                "predictions": predictions.tolist(),
                "model_used": model_type,
                "confidence_intervals": confidence_intervals if confidence_intervals else "Not available",
                "prediction_count": len(predictions)
            }
        except Exception as e:
            logger.error(f"Error making predictions with {model_type}: {e}")
            return {"status": "error", "message": str(e)}

    def predict_ensemble(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Make predictions using an ensemble of available models
        Args:
            data: DataFrame with features for prediction
        Returns:
            Dictionary with ensemble predictions and model agreement metrics
        """
        try:
            # Get predictions from all available models
            predictions = {}
            for model_type in self.models:
                if self.models[model_type] is not None:
                    result = self.predict(data, model_type=model_type)
                    if result['status'] == 'success':
                        predictions[model_type] = result['predictions']

            if not predictions:
                # Try loading models if none are loaded
                if not self.load_models():
                    return {
                        "status": "error",
                        "message": "No trained models available for ensemble prediction"
                    }
                # Retry after load attempt
                for model_type in self.models:
                    if self.models[model_type] is not None:
                        result = self.predict(data, model_type=model_type)
                        if result['status'] == 'success':
                            predictions[model_type] = result['predictions']

                if not predictions:
                    return {
                        "status": "error",
                        "message": "Failed to load or predict with any model"
                    }

            # Calculate ensemble prediction as weighted average
            # For simplicity, equal weights if both models are present
            model_count = len(predictions)
            ensemble_predictions = np.zeros(len(data))
            for model_type, preds in predictions.items():
                weight = 1.0 / model_count
                ensemble_predictions += np.array(preds) * weight

            # Calculate model agreement (simplified as standard deviation across model predictions)
            if model_count > 1:
                all_predictions = np.array(list(predictions.values()))
                model_agreement = np.std(all_predictions, axis=0).tolist()
            else:
                model_agreement = [0.0] * len(data)

            return {
                "status": "success",
                "ensemble_predictions": ensemble_predictions.tolist(),
                "model_agreement": model_agreement,
                "models_used": list(predictions.keys()),
                "individual_predictions": {k: v for k, v in predictions.items()},
                "prediction_count": len(ensemble_predictions)
            }
        except Exception as e:
            logger.error(f"Error making ensemble predictions: {e}")
            return {"status": "error", "message": str(e)}

    def forecast_financial_trends(self, historical_data: pd.DataFrame, periods: int = 12, 
                                 frequency: str = 'M', model_type: str = 'ensemble') -> Dict[str, Any]:
        """
        Forecast financial trends based on historical data
        Args:
            historical_data: DataFrame with historical financial data, must include 'date' and value columns
            periods: Number of future periods to forecast
            frequency: Frequency of forecast ('D' for daily, 'W' for weekly, 'M' for monthly, 'Q' for quarterly)
            model_type: Model to use for forecasting ('ensemble', 'linear_regression', or 'random_forest')
        Returns:
            Dictionary with forecast results and confidence metrics if available
        """
        try:
            logger.info(f"Forecasting financial trends for {periods} {frequency} periods using {model_type}")

            # Extract features from date
            if 'date' not in historical_data.columns:
                return {"status": "error", "message": "Historical data must contain 'date' column"}

            historical_data = historical_data.copy()
            historical_data['date'] = pd.to_datetime(historical_data['date'])
            historical_data.set_index('date', inplace=True)

            # Create time-based features
            historical_data['year'] = historical_data.index.year
            historical_data['month'] = historical_data.index.month
            historical_data['quarter'] = historical_data.index.quarter
            historical_data['day_of_year'] = historical_data.index.dayofyear
            historical_data['day_of_month'] = historical_data.index.day
            historical_data['week_of_year'] = historical_data.index.isocalendar().week

            # Identify target and feature columns
            target_column = [col for col in historical_data.columns if col not in 
                            ['year', 'month', 'quarter', 'day_of_year', 'day_of_month', 'week_of_year']][0]
            feature_columns = ['year', 'month', 'quarter', 'day_of_year', 'day_of_month', 'week_of_year']

            # Train models if not already trained or data is newer
            if self.models.get('random_forest') is None or self.last_training is None:
                self.train_models(historical_data, target_column, feature_columns)
            else:
                last_training_dt = datetime.fromisoformat(self.last_training)
                last_data_date = historical_data.index.max()
                if last_data_date > last_training_dt:
                    logger.info("New data detected, retraining models")
                    self.train_models(historical_data, target_column, feature_columns)

            # Generate future dates
            last_date = historical_data.index.max()
            if frequency == 'D':
                future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=periods, freq='D')
            elif frequency == 'W':
                future_dates = pd.date_range(start=last_date + timedelta(days=7), periods=periods, freq='W')
            elif frequency == 'M':
                future_dates = pd.date_range(start=last_date + timedelta(days=30), periods=periods, freq='M')
            elif frequency == 'Q':
                future_dates = pd.date_range(start=last_date + timedelta(days=90), periods=periods, freq='Q')
            else:
                return {"status": "error", "message": f"Unsupported frequency: {frequency}"}

            # Create future DataFrame with features
            future_df = pd.DataFrame(index=future_dates)
            future_df['year'] = future_df.index.year
            future_df['month'] = future_df.index.month
            future_df['quarter'] = future_df.index.quarter
            future_df['day_of_year'] = future_df.index.dayofyear
            future_df['day_of_month'] = future_df.index.day
            future_df['week_of_year'] = future_df.index.isocalendar().week

            # Make predictions
            if model_type == 'ensemble':
                result = self.predict_ensemble(future_df[feature_columns])
                if result['status'] != 'success':
                    return result
                predictions = result['ensemble_predictions']
                model_agreement = result['model_agreement']
                confidence_intervals = None  # Ensemble doesn't provide CI directly in this implementation
            else:
                result = self.predict(future_df[feature_columns], model_type=model_type)
                if result['status'] != 'success':
                    return result
                predictions = result['predictions']
                confidence_intervals = result['confidence_intervals'] if model_type == 'random_forest' else None
                model_agreement = None

            # Format results
            forecast = []
            for date, pred in zip(future_dates, predictions):
                entry = {
                    "date": date.strftime('%Y-%m-%d'),
                    "forecast": float(pred)
                }
                if confidence_intervals and isinstance(confidence_intervals, list):
                    idx = len(forecast)
                    if idx < len(confidence_intervals) and isinstance(confidence_intervals[idx], (list, tuple)):
                        entry['confidence_lower'] = float(confidence_intervals[idx][0])
                        entry['confidence_upper'] = float(confidence_intervals[idx][1])
                if model_agreement and isinstance(model_agreement, list):
                    idx = len(forecast)
                    if idx < len(model_agreement):
                        entry['model_disagreement'] = float(model_agreement[idx])
                forecast.append(entry)

            return {
                "status": "success",
                "forecast": forecast,
                "model_type": model_type,
                "target": target_column,
                "periods_forecasted": len(forecast),
                "frequency": frequency,
                "historical_data_range": {
                    "start": historical_data.index.min().strftime('%Y-%m-%d'),
                    "end": historical_data.index.max().strftime('%Y-%m-%d'),
                    "records": len(historical_data)
                }
            }
        except Exception as e:
            logger.error(f"Error forecasting financial trends: {e}")
            return {"status": "error", "message": str(e)}

    def forecast_project_outcomes(self, project_data: pd.DataFrame, outcome_metric: str, 
                                 periods: int = 6, frequency: str = 'M') -> Dict[str, Any]:
        """
        Forecast project outcomes based on historical project metrics
        Args:
            project_data: DataFrame with historical project metrics, must include 'date' and outcome metric
            outcome_metric: Specific metric to forecast (e.g., 'completion_percentage', 'cost')
            periods: Number of future periods to forecast
            frequency: Frequency of forecast ('D' for daily, 'W' for weekly, 'M' for monthly, 'Q' for quarterly)
        Returns:
            Dictionary with forecast results for project outcomes
        """
        try:
            logger.info(f"Forecasting project outcome {outcome_metric} for {periods} {frequency} periods")

            if 'date' not in project_data.columns or outcome_metric not in project_data.columns:
                return {
                    "status": "error",
                    "message": f"Project data must contain 'date' and '{outcome_metric}' columns"
                }

            # Use the financial trend forecasting logic
            return self.forecast_financial_trends(
                historical_data=project_data.rename(columns={outcome_metric: 'value'}),
                periods=periods,
                frequency=frequency,
                model_type='ensemble'
            )
        except Exception as e:
            logger.error(f"Error forecasting project outcomes: {e}")
            return {"status": "error", "message": str(e)}

    def get_model_status(self) -> Dict[str, Any]:
        """
        Get current status of AI models
        """
        # Attempt to load models if not already loaded
        if not any(self.models.values()):
            self.load_models()

        return {
            "models_loaded": {
                model_type: model is not None for model_type, model in self.models.items()
            },
            "last_training": self.last_training if self.last_training else "Never trained",
            "model_dir": self.model_dir
        }

# Global AI predictive analytics instance
ai_analytics = AIPredictiveAnalytics()
