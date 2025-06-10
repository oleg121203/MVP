import logging
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from datetime import datetime, timedelta
import joblib
import os

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, model_dir: str = 'anomaly_models'):
        """
        Initialize Anomaly Detection module with machine learning capabilities
        """
        self.model_dir = model_dir
        self.models = {
            'isolation_forest': None,
            'dbscan': None
        }
        self.scaler = StandardScaler()
        self.last_training = None
        os.makedirs(self.model_dir, exist_ok=True)
        logger.info("Anomaly Detection module initialized")

    def load_models(self) -> bool:
        """
        Load trained anomaly detection models from disk if available
        Returns True if at least one model was loaded successfully
        """
        loaded = False
        try:
            if_path = os.path.join(self.model_dir, 'isolation_forest_model.joblib')
            if os.path.exists(if_path):
                self.models['isolation_forest'] = joblib.load(if_path)
                logger.info("Loaded Isolation Forest model")
                loaded = True

            dbscan_path = os.path.join(self.model_dir, 'dbscan_model.joblib')
            if os.path.exists(dbscan_path):
                self.models['dbscan'] = joblib.load(dbscan_path)
                logger.info("Loaded DBSCAN model")
                loaded = True

            scaler_path = os.path.join(self.model_dir, 'scaler.joblib')
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info("Loaded feature scaler")

            last_training_path = os.path.join(self.model_dir, 'last_training.txt')
            if os.path.exists(last_training_path):
                with open(last_training_path, 'r') as f:
                    self.last_training = f.read().strip()
                logger.info(f"Last training timestamp loaded: {self.last_training}")

            return loaded
        except Exception as e:
            logger.error(f"Error loading anomaly detection models: {e}")
            return False

    def save_models(self) -> bool:
        """
        Save trained anomaly detection models and scaler to disk
        Returns True if save was successful
        """
        try:
            if self.models['isolation_forest'] is not None:
                joblib.dump(self.models['isolation_forest'], os.path.join(self.model_dir, 'isolation_forest_model.joblib'))
                logger.info("Saved Isolation Forest model")

            if self.models['dbscan'] is not None:
                joblib.dump(self.models['dbscan'], os.path.join(self.model_dir, 'dbscan_model.joblib'))
                logger.info("Saved DBSCAN model")

            joblib.dump(self.scaler, os.path.join(self.model_dir, 'scaler.joblib'))
            logger.info("Saved feature scaler")

            self.last_training = datetime.now().isoformat()
            with open(os.path.join(self.model_dir, 'last_training.txt'), 'w') as f:
                f.write(self.last_training)
            logger.info(f"Updated last training timestamp: {self.last_training}")

            return True
        except Exception as e:
            logger.error(f"Error saving anomaly detection models: {e}")
            return False

    def train_models(self, data: pd.DataFrame, feature_columns: List[str], contamination: float = 0.1, 
                     eps: float = 0.5, min_samples: int = 5) -> Dict[str, Any]:
        """
        Train anomaly detection models
        Args:
            data: DataFrame containing the training data
            feature_columns: List of column names to use as features
            contamination: Expected proportion of anomalies in the data for Isolation Forest
            eps: The maximum distance between two samples for DBSCAN
            min_samples: The number of samples in a neighborhood for a point to be considered as a core point for DBSCAN
        Returns:
            Dictionary with training results and metrics
        """
        try:
            logger.info(f"Starting anomaly detection model training")
            X = data[feature_columns]

            # Scale features
            X_scaled = self.scaler.fit_transform(X)

            # Train Isolation Forest
            if_model = IsolationForest(contamination=contamination, random_state=42, n_jobs=-1)
            if_model.fit(X_scaled)
            if_labels = if_model.predict(X_scaled)
            if_anomaly_count = np.sum(if_labels == -1)
            logger.info(f"Isolation Forest - Detected {if_anomaly_count} anomalies")

            # Train DBSCAN
            dbscan_model = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
            dbscan_labels = dbscan_model.fit_predict(X_scaled)
            dbscan_anomaly_count = np.sum(dbscan_labels == -1)
            logger.info(f"DBSCAN - Detected {dbscan_anomaly_count} anomalies")

            # Store models
            self.models['isolation_forest'] = if_model
            self.models['dbscan'] = dbscan_model

            # Save models
            self.save_models()

            return {
                "status": "success",
                "message": "Anomaly detection models trained successfully",
                "training_time": datetime.now().isoformat(),
                "data_shape": {
                    "total_samples": len(data),
                    "features": len(feature_columns)
                },
                "isolation_forest": {
                    "anomaly_count": int(if_anomaly_count),
                    "anomaly_percentage": round(if_anomaly_count / len(data) * 100, 2)
                },
                "dbscan": {
                    "anomaly_count": int(dbscan_anomaly_count),
                    "anomaly_percentage": round(dbscan_anomaly_count / len(data) * 100, 2)
                }
            }
        except Exception as e:
            logger.error(f"Error training anomaly detection models: {e}")
            return {"status": "error", "message": str(e)}

    def detect_anomalies(self, data: pd.DataFrame, feature_columns: List[str], 
                         model_type: str = 'isolation_forest') -> Dict[str, Any]:
        """
        Detect anomalies in the provided data using the specified model
        Args:
            data: DataFrame with features for anomaly detection
            feature_columns: List of column names to use as features
            model_type: Type of model to use ('isolation_forest' or 'dbscan')
        Returns:
            Dictionary with anomaly detection results
        """
        try:
            if model_type not in self.models or self.models[model_type] is None:
                # Try to load models if not loaded
                if not self.load_models() or self.models[model_type] is None:
                    return {
                        "status": "error",
                        "message": f"Anomaly detection model {model_type} not trained or loaded"
                    }

            # Ensure all expected feature columns are present
            expected_features = feature_columns
            missing_features = [f for f in expected_features if f not in data.columns]
            if missing_features:
                logger.warning(f"Missing features in input data: {missing_features}")
                # Fill missing features with zeros or appropriate default
                for f in missing_features:
                    data[f] = 0

            # Scale input data
            X = data[feature_columns]
            X_scaled = self.scaler.transform(X)

            # Detect anomalies
            if model_type == 'isolation_forest':
                labels = self.models[model_type].predict(X_scaled)
                scores = self.models[model_type].decision_function(X_scaled)
            else:  # dbscan
                labels = self.models[model_type].fit_predict(X_scaled)
                scores = None  # DBSCAN doesn't provide anomaly scores directly

            anomaly_indices = np.where(labels == -1)[0].tolist()
            anomaly_count = len(anomaly_indices)

            # Prepare anomaly details
            anomaly_details = []
            for idx in anomaly_indices:
                detail = {
                    "index": int(idx),
                    "data_row": data.iloc[idx].to_dict()
                }
                if scores is not None and len(scores) > idx:
                    detail["anomaly_score"] = float(scores[idx])
                anomaly_details.append(detail)

            return {
                "status": "success",
                "model_used": model_type,
                "anomaly_count": anomaly_count,
                "total_samples": len(data),
                "anomaly_percentage": round(anomaly_count / len(data) * 100, 2) if len(data) > 0 else 0.0,
                "anomaly_indices": anomaly_indices,
                "anomaly_details": anomaly_details
            }
        except Exception as e:
            logger.error(f"Error detecting anomalies with {model_type}: {e}")
            return {"status": "error", "message": str(e)}

    def detect_financial_anomalies(self, financial_data: pd.DataFrame, 
                                  feature_columns: List[str] = None) -> Dict[str, Any]:
        """
        Detect anomalies in financial data using the Isolation Forest model
        Args:
            financial_data: DataFrame with financial data for anomaly detection
            feature_columns: List of column names to use as features, defaults to common financial metrics
        Returns:
            Dictionary with financial anomaly detection results
        """
        try:
            logger.info(f"Detecting financial anomalies in dataset of size {len(financial_data)}")

            if feature_columns is None:
                feature_columns = [col for col in financial_data.columns if col in 
                                  ['amount', 'transaction_value', 'cost', 'expense', 'revenue', 
                                   'transaction_frequency', 'avg_transaction_size']]

            if not feature_columns:
                return {
                    "status": "error",
                    "message": "No suitable feature columns provided or found for anomaly detection"
                }

            # Remove rows with NaN in feature columns
            initial_size = len(financial_data)
            analysis_data = financial_data.dropna(subset=feature_columns)
            if len(analysis_data) < initial_size:
                logger.warning(f"Dropped {initial_size - len(analysis_data)} rows with NaN values in feature columns")

            if len(analysis_data) == 0:
                return {
                    "status": "error",
                    "message": "No data available after removing rows with NaN values"
                }

            result = self.detect_anomalies(analysis_data, feature_columns, model_type='isolation_forest')

            if result['status'] == 'success':
                # Add context about time period if available
                time_info = {}
                if 'date' in financial_data.columns:
                    try:
                        financial_data['date'] = pd.to_datetime(financial_data['date'])
                        time_info['data_start_date'] = financial_data['date'].min().strftime('%Y-%m-%d')
                        time_info['data_end_date'] = financial_data['date'].max().strftime('%Y-%m-%d')
                        # Check if anomalies are concentrated in a specific time period
                        anomaly_dates = financial_data.iloc[result['anomaly_indices']]['date']
                        if not anomaly_dates.empty:
                            time_info['anomaly_start_date'] = anomaly_dates.min().strftime('%Y-%m-%d')
                            time_info['anomaly_end_date'] = anomaly_dates.max().strftime('%Y-%m-%d')
                    except Exception as e:
                        logger.warning(f"Could not process date information: {e}")

                result['financial_context'] = {
                    "feature_columns_used": feature_columns,
                    "time_period": time_info
                }

            return result
        except Exception as e:
            logger.error(f"Error detecting financial anomalies: {e}")
            return {"status": "error", "message": str(e)}

    def detect_project_anomalies(self, project_data: pd.DataFrame, 
                                feature_columns: List[str] = None) -> Dict[str, Any]:
        """
        Detect anomalies in project data using the Isolation Forest model
        Args:
            project_data: DataFrame with project data for anomaly detection
            feature_columns: List of column names to use as features, defaults to common project metrics
        Returns:
            Dictionary with project anomaly detection results
        """
        try:
            logger.info(f"Detecting project anomalies in dataset of size {len(project_data)}")

            if feature_columns is None:
                feature_columns = [col for col in project_data.columns if col in 
                                  ['budget', 'actual_cost', 'completion_percentage', 'duration_days', 
                                   'team_size', 'risk_score', 'cost_per_day', 'budget_utilization']]

            if not feature_columns:
                return {
                    "status": "error",
                    "message": "No suitable feature columns provided or found for anomaly detection"
                }

            # Remove rows with NaN in feature columns
            initial_size = len(project_data)
            analysis_data = project_data.dropna(subset=feature_columns)
            if len(analysis_data) < initial_size:
                logger.warning(f"Dropped {initial_size - len(analysis_data)} rows with NaN values in feature columns")

            if len(analysis_data) == 0:
                return {
                    "status": "error",
                    "message": "No data available after removing rows with NaN values"
                }

            result = self.detect_anomalies(analysis_data, feature_columns, model_type='isolation_forest')

            if result['status'] == 'success':
                result['project_context'] = {
                    "feature_columns_used": feature_columns
                }

            return result
        except Exception as e:
            logger.error(f"Error detecting project anomalies: {e}")
            return {"status": "error", "message": str(e)}

    def get_model_status(self) -> Dict[str, Any]:
        """
        Get current status of anomaly detection models
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

# Global anomaly detector instance
anomaly_detector = AnomalyDetector()
