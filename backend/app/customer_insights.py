import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
import joblib
import random

logger = logging.getLogger(__name__)

class CustomerInsights:
    def __init__(self, model_dir: str = 'customer_models', data_dir: str = 'customer_data', config_path: str = 'customer_insights_config.json'):
        """
        Initialize Customer Insights module for AI-driven customer analysis
        """
        self.model_dir = model_dir
        self.data_dir = data_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.customer_data = {}
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        logger.info("Customer Insights module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load customer insights configuration from file or create default if not exists
        """
        default_config = {
            "data_collection": {
                "enabled": True,
                "collection_interval_hours": 24,
                "data_retention_days": 365,
                "anonymization_enabled": True,
                "metrics": [
                    "purchase_frequency",
                    "average_order_value",
                    "customer_tenure_days",
                    "support_tickets_count",
                    "website_visits",
                    "app_usage_minutes",
                    "email_engagement_rate",
                    "social_media_interactions",
                    "product_categories_viewed",
                    "cart_abandonment_rate"
                ]
            },
            "analysis": {
                "enabled": True,
                "analysis_frequency_hours": 12,
                "segmentation": {
                    "enabled": True,
                    "min_segment_size": 100,
                    "max_segments": 10,
                    "segmentation_criteria": ["behavioral", "demographic", "value_based"]
                },
                "churn_prediction": {
                    "enabled": True,
                    "churn_window_days": 30,
                    "churn_probability_threshold": 0.7,
                    "confidence_threshold": 0.75
                },
                "lifetime_value": {
                    "enabled": True,
                    "prediction_horizon_months": 12,
                    "confidence_threshold": 0.7
                },
                "recommendation": {
                    "enabled": True,
                    "recommendation_types": ["product", "content", "service"],
                    "max_recommendations": 5,
                    "confidence_threshold": 0.6
                }
            },
            "modeling": {
                "enabled": True,
                "training_interval_days": 7,
                "model_types": {
                    "churn_prediction": "random_forest_classifier",
                    "lifetime_value": "random_forest_regressor",
                    "behavior_segmentation": "random_forest_classifier",
                    "recommendation_engine": "random_forest_classifier"
                }
            },
            "personalization": {
                "enabled": True,
                "delivery_channels": ["email", "app", "website", "sms"],
                "delivery_frequency_hours": 24,
                "max_personalized_messages_per_day": 3,
                "opt_out_handling": True
            },
            "reporting": {
                "enabled": True,
                "report_frequency_hours": 24,
                "report_types": ["segment_analysis", "churn_risk", "customer_value", "engagement_metrics"],
                "distribution_channels": ["email", "dashboard"],
                "recipients": ["marketing_team", "executives"]
            },
            "model_storage": {
                "max_model_versions": 5,
                "model_compression": True,
                "backup_frequency_days": 30
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded customer insights configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading customer insights config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default customer insights configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default customer insights config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved customer insights configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving customer insights config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def collect_customer_data(self, customer_id: str, metrics: Dict[str, float], timestamp: datetime = None, additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Collect customer data for analysis and modeling
        Args:
            customer_id: Unique identifier for the customer
            metrics: Dictionary of metric names and their values
            timestamp: Timestamp of data collection, defaults to now
            additional_data: Additional non-metric data about the customer
        Returns:
            Dictionary with collection status
        """
        try:
            if not self.config['data_collection']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Customer data collection is disabled"
                }

            if timestamp is None:
                timestamp = datetime.now()

            data_point = {
                "customer_id": customer_id,
                "timestamp": timestamp.isoformat(),
                "metrics": metrics,
                "additional_data": additional_data if additional_data else {}
            }

            date_str = timestamp.strftime("%Y%m%d")
            data_file = os.path.join(self.data_dir, f"customer_data_{date_str}.jsonl")

            with open(data_file, 'a') as f:
                json.dump(data_point, f)
                f.write('\n')

            # Store in memory for quick access
            date_key = timestamp.strftime("%Y-%m-%d")
            if date_key not in self.customer_data:
                self.customer_data[date_key] = []
            self.customer_data[date_key].append(data_point)

            logger.info(f"Collected customer data for {customer_id} at {timestamp.isoformat()}")
            return {
                "status": "success",
                "customer_id": customer_id,
                "timestamp": timestamp.isoformat(),
                "metrics_collected": list(metrics.keys()),
                "additional_data": additional_data if additional_data else {}
            }
        except Exception as e:
            logger.error(f"Error collecting customer data for {customer_id}: {e}")
            return {"status": "error", "message": str(e)}

    def train_model(self, model_type: str, data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Train a customer insights model for prediction or segmentation
        Args:
            model_type: Type of model to train ('churn_prediction', 'lifetime_value', 'behavior_segmentation', 'recommendation_engine')
            data: Optional training data, if None will load from stored customer data
        Returns:
            Dictionary with training status and metrics
        """
        try:
            if not self.config['modeling']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Customer insights modeling is disabled"
                }

            if model_type not in self.config['modeling']['model_types']:
                return {
                    "status": "error",
                    "message": f"Unknown model type: {model_type}"
                }

            model_algorithm = self.config['modeling']['model_types'][model_type]
            if model_algorithm not in ["random_forest_classifier", "random_forest_regressor"]:
                return {
                    "status": "error",
                    "message": f"Unsupported model algorithm {model_algorithm} for {model_type}"
                }

            # Load data if not provided
            if data is None:
                data = []
                # Load from customer data files
                for date_key in sorted(self.customer_data.keys(), reverse=True):
                    data.extend(self.customer_data[date_key])
                    if len(data) >= 1000:  # Limit to recent 1000 data points
                        break

                if not data:
                    # Load from disk if no in-memory data
                    data_files = sorted(
                        [f for f in os.listdir(self.data_dir) if f.startswith("customer_data_")],
                        reverse=True
                    )
                    for data_file in data_files[:30]:  # Last 30 days
                        file_path = os.path.join(self.data_dir, data_file)
                        try:
                            with open(file_path, 'r') as f:
                                for line in f:
                                    if line.strip():
                                        data_point = json.loads(line)
                                        data.append(data_point)
                                        if len(data) >= 1000:
                                            break
                        except Exception as e:
                            logger.warning(f"Error reading data file {data_file}: {e}")

            if len(data) < 10:
                return {
                    "status": "error",
                    "message": f"Insufficient data for training {model_type} model. Need at least 10 data points, have {len(data)}"
                }

            # Prepare data for training
            feature_names = self.config['data_collection']['metrics']
            X = []
            y = []

            if model_type == "churn_prediction":
                # For churn prediction, target is whether customer churned
                for data_point in data:
                    metrics = data_point['metrics']
                    additional_data = data_point.get('additional_data', {})
                    if all(metric in metrics for metric in feature_names):
                        X.append([metrics[metric] for metric in feature_names])
                        # Label: 1 if customer churned, 0 otherwise (simulated if no label)
                        if 'churned' in additional_data:
                            y.append(1 if additional_data['churned'] else 0)
                        else:
                            # Simulated label based on low engagement
                            if metrics.get('purchase_frequency', 0) < 0.1 and metrics.get('website_visits', 0) < 5:
                                y.append(1 if random.random() > 0.7 else 0)
                            else:
                                y.append(0)

            elif model_type == "lifetime_value":
                # For lifetime value prediction, target is future value (regression)
                for data_point in data:
                    metrics = data_point['metrics']
                    additional_data = data_point.get('additional_data', {})
                    if all(metric in metrics for metric in feature_names):
                        X.append([metrics[metric] for metric in feature_names])
                        # Target: simulated future value based on current metrics if no real data
                        if 'lifetime_value' in additional_data:
                            y.append(float(additional_data['lifetime_value']))
                        else:
                            # Simulated value based on purchase frequency and order value
                            simulated_value = metrics.get('purchase_frequency', 0) * metrics.get('average_order_value', 0) * 12  # rough annual value
                            y.append(simulated_value * random.uniform(0.8, 1.2))  # add some randomness

            elif model_type == "behavior_segmentation":
                # For behavior segmentation, target is segment label (simulated as clusters)
                for data_point in data:
                    metrics = data_point['metrics']
                    additional_data = data_point.get('additional_data', {})
                    if all(metric in metrics for metric in feature_names):
                        X.append([metrics[metric] for metric in feature_names])
                        # Label: simulated segment based on engagement level
                        if 'segment_id' in additional_data:
                            y.append(int(additional_data['segment_id']))
                        else:
                            # Simulated segment based on engagement metrics
                            engagement_score = metrics.get('website_visits', 0) + metrics.get('app_usage_minutes', 0) + metrics.get('email_engagement_rate', 0)
                            if engagement_score > 50:
                                y.append(0)  # High engagement segment
                            elif engagement_score > 10:
                                y.append(1)  # Medium engagement
                            else:
                                y.append(2)  # Low engagement

            elif model_type == "recommendation_engine":
                # For recommendation engine, target is likelihood to engage with recommendation
                for data_point in data:
                    metrics = data_point['metrics']
                    additional_data = data_point.get('additional_data', {})
                    if all(metric in metrics for metric in feature_names):
                        X.append([metrics[metric] for metric in feature_names])
                        # Label: 1 if likely to engage with recommendation, 0 otherwise
                        if 'recommendation_engaged' in additional_data:
                            y.append(1 if additional_data['recommendation_engaged'] else 0)
                        else:
                            # Simulated label based on email engagement and purchase frequency
                            if metrics.get('email_engagement_rate', 0) > 0.5 and metrics.get('purchase_frequency', 0) > 0.2:
                                y.append(1 if random.random() > 0.6 else 0)
                            else:
                                y.append(0)

            if not X or not y:
                return {
                    "status": "error",
                    "message": f"No valid training data prepared for {model_type} model"
                }

            # Convert to numpy arrays
            X = np.array(X)
            y = np.array(y)

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train model
            if model_algorithm == "random_forest_classifier":
                model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight='balanced')
                model.fit(X_train, y_train)

                # Evaluate model
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

                eval_metrics = {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1
                }

            elif model_algorithm == "random_forest_regressor":
                model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
                model.fit(X_train, y_train)

                # Evaluate model
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)

                eval_metrics = {
                    "mean_squared_error": mse,
                    "r2_score": r2
                }

            # Save model
            version = datetime.now().strftime("%Y%m%d%H%M%S")
            model_filename = os.path.join(self.model_dir, f"{model_type}_{version}.joblib")
            joblib.dump(model, model_filename, compress=3 if self.config['model_storage']['model_compression'] else 0)

            # Update model registry
            if model_type not in self.models:
                self.models[model_type] = []
            self.models[model_type].append({
                "version": version,
                "filename": model_filename,
                "trained_at": datetime.now().isoformat(),
                "training_data_points": len(data),
                "evaluation": eval_metrics
            })

            # Keep only the latest versions based on max_model_versions
            max_versions = self.config['model_storage'].get('max_model_versions', 5)
            if len(self.models[model_type]) > max_versions:
                # Sort by trained_at descending
                self.models[model_type].sort(key=lambda x: x['trained_at'], reverse=True)
                # Remove oldest models
                for old_model in self.models[model_type][max_versions:]:
                    try:
                        if os.path.exists(old_model['filename']):
                            os.remove(old_model['filename'])
                            logger.info(f"Removed old model version: {old_model['filename']}")
                    except Exception as e:
                        logger.warning(f"Error removing old model {old_model['filename']}: {e}")
                self.models[model_type] = self.models[model_type][:max_versions]

            logger.info(f"Trained {model_type} model version {version} with {len(data)} data points")
            return {
                "status": "success",
                "model_type": model_type,
                "version": version,
                "algorithm": model_algorithm,
                "trained_at": datetime.now().isoformat(),
                "training_data_points": len(data),
                "evaluation_metrics": eval_metrics,
                "model_file": model_filename
            }
        except Exception as e:
            logger.error(f"Error training {model_type} model: {e}")
            return {"status": "error", "message": str(e)}

    def predict_churn(self, customer_id: str, input_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Predict customer churn probability
        Args:
            customer_id: Unique identifier for the customer
            input_data: Dictionary of input metrics for prediction
        Returns:
            Dictionary with churn prediction results
        """
        try:
            model_type = "churn_prediction"
            if model_type not in self.models or not self.models[model_type]:
                return {
                    "status": "error",
                    "message": f"No trained model available for {model_type}"
                }

            # Get the latest model for this type
            latest_model_info = max(self.models[model_type], key=lambda x: x['trained_at'])
            model_filename = latest_model_info['filename']

            if not os.path.exists(model_filename):
                return {
                    "status": "error",
                    "message": f"Model file not found: {model_filename}"
                }

            # Load the model
            model = joblib.load(model_filename)

            # Prepare input data
            feature_names = self.config['data_collection']['metrics']
            if not all(name in input_data for name in feature_names):
                missing = [name for name in feature_names if name not in input_data]
                return {
                    "status": "error",
                    "message": f"Missing required input metrics for {model_type}: {missing}"
                }
            input_array = np.array([[input_data[name] for name in feature_names]])

            # Make prediction
            prediction = model.predict(input_array)[0]
            prediction_proba = model.predict_proba(input_array)[0]
            confidence = float(max(prediction_proba))

            churn_predicted = bool(prediction == 1)
            churn_probability = float(prediction_proba[1])

            # Determine time window for churn prediction
            churn_window_days = self.config['analysis']['churn_prediction']['churn_window_days']

            return {
                "status": "success",
                "model_type": model_type,
                "version": latest_model_info['version'],
                "customer_id": customer_id,
                "prediction": {
                    "churn_predicted": churn_predicted,
                    "churn_probability": churn_probability,
                    "confidence": confidence,
                    "churn_window_days": churn_window_days
                },
                "timestamp": datetime.now().isoformat(),
                "input_data": input_data
            }
        except Exception as e:
            logger.error(f"Error predicting churn for customer {customer_id}: {e}")
            return {"status": "error", "message": str(e)}

    def predict_lifetime_value(self, customer_id: str, input_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Predict customer lifetime value
        Args:
            customer_id: Unique identifier for the customer
            input_data: Dictionary of input metrics for prediction
        Returns:
            Dictionary with lifetime value prediction results
        """
        try:
            model_type = "lifetime_value"
            if model_type not in self.models or not self.models[model_type]:
                return {
                    "status": "error",
                    "message": f"No trained model available for {model_type}"
                }

            # Get the latest model for this type
            latest_model_info = max(self.models[model_type], key=lambda x: x['trained_at'])
            model_filename = latest_model_info['filename']

            if not os.path.exists(model_filename):
                return {
                    "status": "error",
                    "message": f"Model file not found: {model_filename}"
                }

            # Load the model
            model = joblib.load(model_filename)

            # Prepare input data
            feature_names = self.config['data_collection']['metrics']
            if not all(name in input_data for name in feature_names):
                missing = [name for name in feature_names if name not in input_data]
                return {
                    "status": "error",
                    "message": f"Missing required input metrics for {model_type}: {missing}"
                }
            input_array = np.array([[input_data[name] for name in feature_names]])

            # Make prediction
            predicted_value = float(model.predict(input_array)[0])
            feature_importance = dict(zip(feature_names, model.feature_importances_))

            # Determine prediction horizon
            prediction_horizon_months = self.config['analysis']['lifetime_value']['prediction_horizon_months']

            return {
                "status": "success",
                "model_type": model_type,
                "version": latest_model_info['version'],
                "customer_id": customer_id,
                "prediction": {
                    "lifetime_value": predicted_value,
                    "prediction_horizon_months": prediction_horizon_months,
                    "feature_importance": feature_importance
                },
                "timestamp": datetime.now().isoformat(),
                "input_data": input_data
            }
        except Exception as e:
            logger.error(f"Error predicting lifetime value for customer {customer_id}: {e}")
            return {"status": "error", "message": str(e)}

    def get_customer_segment(self, customer_id: str, input_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Determine customer segment based on behavior and characteristics
        Args:
            customer_id: Unique identifier for the customer
            input_data: Dictionary of input metrics for segmentation
        Returns:
            Dictionary with customer segment information
        """
        try:
            model_type = "behavior_segmentation"
            if model_type not in self.models or not self.models[model_type]:
                return {
                    "status": "error",
                    "message": f"No trained model available for {model_type}"
                }

            # Get the latest model for this type
            latest_model_info = max(self.models[model_type], key=lambda x: x['trained_at'])
            model_filename = latest_model_info['filename']

            if not os.path.exists(model_filename):
                return {
                    "status": "error",
                    "message": f"Model file not found: {model_filename}"
                }

            # Load the model
            model = joblib.load(model_filename)

            # Prepare input data
            feature_names = self.config['data_collection']['metrics']
            if not all(name in input_data for name in feature_names):
                missing = [name for name in feature_names if name not in input_data]
                return {
                    "status": "error",
                    "message": f"Missing required input metrics for {model_type}: {missing}"
                }
            input_array = np.array([[input_data[name] for name in feature_names]])

            # Predict segment
            segment_id = int(model.predict(input_array)[0])
            segment_probabilities = model.predict_proba(input_array)[0].tolist()
            confidence = float(max(segment_probabilities))

            # Map segment ID to descriptive name (simulated mapping, in real system would be configured)
            segment_names = {
                0: "High Engagement - Frequent Buyer",
                1: "Medium Engagement - Occasional Buyer",
                2: "Low Engagement - At Risk"
            }
            segment_name = segment_names.get(segment_id, f"Segment {segment_id}")

            # Segment characteristics (simulated, in real system based on data analysis)
            segment_characteristics = {
                0: {
                    "engagement_level": "high",
                    "purchase_frequency": "weekly",
                    "value_category": "high_value",
                    "loyalty": "strong"
                },
                1: {
                    "engagement_level": "medium",
                    "purchase_frequency": "monthly",
                    "value_category": "medium_value",
                    "loyalty": "moderate"
                },
                2: {
                    "engagement_level": "low",
                    "purchase_frequency": "rare",
                    "value_category": "low_value",
                    "loyalty": "weak"
                }
            }
            characteristics = segment_characteristics.get(segment_id, {
                "engagement_level": "unknown",
                "purchase_frequency": "unknown",
                "value_category": "unknown",
                "loyalty": "unknown"
            })

            return {
                "status": "success",
                "model_type": model_type,
                "version": latest_model_info['version'],
                "customer_id": customer_id,
                "segment": {
                    "segment_id": segment_id,
                    "segment_name": segment_name,
                    "confidence": confidence,
                    "segment_probabilities": segment_probabilities,
                    "characteristics": characteristics
                },
                "timestamp": datetime.now().isoformat(),
                "input_data": input_data
            }
        except Exception as e:
            logger.error(f"Error determining customer segment for {customer_id}: {e}")
            return {"status": "error", "message": str(e)}

    def generate_recommendations(self, customer_id: str, input_data: Dict[str, float], recommendation_type: str = "product") -> Dict[str, Any]:
        """
        Generate personalized recommendations for a customer
        Args:
            customer_id: Unique identifier for the customer
            input_data: Dictionary of input metrics for recommendation
            recommendation_type: Type of recommendation ('product', 'content', 'service')
        Returns:
            Dictionary with recommendation results
        """
        try:
            model_type = "recommendation_engine"
            if model_type not in self.models or not self.models[model_type]:
                return {
                    "status": "error",
                    "message": f"No trained model available for {model_type}"
                }

            if recommendation_type not in self.config['analysis']['recommendation']['recommendation_types']:
                return {
                    "status": "error",
                    "message": f"Unsupported recommendation type: {recommendation_type}"
                }

            # Get the latest model for this type
            latest_model_info = max(self.models[model_type], key=lambda x: x['trained_at'])
            model_filename = latest_model_info['filename']

            if not os.path.exists(model_filename):
                return {
                    "status": "error",
                    "message": f"Model file not found: {model_filename}"
                }

            # Load the model
            model = joblib.load(model_filename)

            # Prepare input data
            feature_names = self.config['data_collection']['metrics']
            if not all(name in input_data for name in feature_names):
                missing = [name for name in feature_names if name not in input_data]
                return {
                    "status": "error",
                    "message": f"Missing required input metrics for {model_type}: {missing}"
                }
            input_array = np.array([[input_data[name] for name in feature_names]])

            # Predict recommendation engagement likelihood
            engagement_pred = model.predict(input_array)[0]
            engagement_proba = model.predict_proba(input_array)[0]
            confidence = float(max(engagement_proba))

            will_engage = bool(engagement_pred == 1)
            engagement_probability = float(engagement_proba[1])

            # Generate recommendations if likely to engage
            recommendations = []
            if will_engage and confidence >= self.config['analysis']['recommendation']['confidence_threshold']:
                max_recommendations = self.config['analysis']['recommendation']['max_recommendations']
                # Simulated recommendations - in real system, would be based on product/content catalog and customer history
                if recommendation_type == "product":
                    product_categories = ["Electronics", "Clothing", "Home Goods", "Books", "Beauty"]
                    for i in range(min(max_recommendations, len(product_categories))):
                        category = product_categories[i]
                        recommendations.append({
                            "recommendation_id": f"rec_prod_{i}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                            "type": "product",
                            "item": f"Featured {category} Product",
                            "description": f"A popular item in our {category} category based on your interests",
                            "relevance_score": random.uniform(0.6, 0.95),
                            "category": category,
                            "action": "view_product",
                            "priority": i + 1
                        })
                elif recommendation_type == "content":
                    content_types = ["Blog Post", "Video Tutorial", "Case Study", "Newsletter", "Webinar"]
                    for i in range(min(max_recommendations, len(content_types))):
                        content_type = content_types[i]
                        recommendations.append({
                            "recommendation_id": f"rec_cont_{i}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                            "type": "content",
                            "item": f"Latest {content_type}",
                            "description": f"A {content_type.lower()} about topics you follow",
                            "relevance_score": random.uniform(0.5, 0.9),
                            "content_type": content_type,
                            "action": "view_content",
                            "priority": i + 1
                        })
                elif recommendation_type == "service":
                    services = ["Premium Support", "Extended Warranty", "Installation Service", "Personal Consultation", "Custom Solution"]
                    for i in range(min(max_recommendations, len(services))):
                        service = services[i]
                        recommendations.append({
                            "recommendation_id": f"rec_serv_{i}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                            "type": "service",
                            "item": service,
                            "description": f"Enhance your experience with our {service}",
                            "relevance_score": random.uniform(0.5, 0.85),
                            "service_type": service,
                            "action": "learn_more",
                            "priority": i + 1
                        })

                # Sort by relevance score descending
                recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)

            return {
                "status": "success",
                "model_type": model_type,
                "version": latest_model_info['version'],
                "customer_id": customer_id,
                "recommendation_type": recommendation_type,
                "engagement": {
                    "will_engage": will_engage,
                    "engagement_probability": engagement_probability,
                    "confidence": confidence
                },
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat(),
                "input_data": input_data
            }
        except Exception as e:
            logger.error(f"Error generating {recommendation_type} recommendations for customer {customer_id}: {e}")
            return {"status": "error", "message": str(e)}

    def get_insights_status(self) -> Dict[str, Any]:
        """
        Get current status of customer insights system
        """
        try:
            model_status = {}
            for model_type in self.config['modeling']['model_types']:
                if model_type in self.models and self.models[model_type]:
                    model_status[model_type] = [
                        {
                            "version": m['version'],
                            "trained_at": m['trained_at'],
                            "data_points": m['training_data_points'],
                            "evaluation": m['evaluation']
                        }
                        for m in sorted(self.models[model_type], key=lambda x: x['trained_at'], reverse=True)
                    ]
                else:
                    model_status[model_type] = []

            data_points_by_date = {date: len(data_list) for date, data_list in self.customer_data.items()}
            total_data_points = sum(data_points_by_date.values())

            return {
                "status": "success",
                "data_collection_enabled": self.config['data_collection']['enabled'],
                "analysis_enabled": self.config['analysis']['enabled'],
                "modeling_enabled": self.config['modeling']['enabled'],
                "personalization_enabled": self.config['personalization']['enabled'],
                "reporting_enabled": self.config['reporting']['enabled'],
                "models": model_status,
                "data_points": {
                    "total": total_data_points,
                    "by_date": data_points_by_date
                },
                "training_interval_days": self.config['modeling']['training_interval_days'],
                "analysis_frequency_hours": self.config['analysis']['analysis_frequency_hours'],
                "report_frequency_hours": self.config['reporting']['report_frequency_hours']
            }
        except Exception as e:
            logger.error(f"Error getting customer insights status: {e}")
            return {"status": "error", "message": str(e)}

# Global customer insights instance
customer_insights = CustomerInsights()
