import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

logger = logging.getLogger(__name__)

class SelfLearningAI:
    def __init__(self, model_dir: str = 'ai_models', data_dir: str = 'ai_data', config_path: str = 'self_learning_config.json'):
        """
        Initialize Self-Learning AI module for system optimization
        """
        self.model_dir = model_dir
        self.data_dir = data_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.performance_data = {}
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        logger.info("Self-Learning AI module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load self-learning AI configuration from file or create default if not exists
        """
        default_config = {
            "learning": {
                "enabled": True,
                "learning_rate": 0.01,
                "training_interval_hours": 24,
                "model_types": {
                    "performance_optimization": "random_forest",
                    "resource_allocation": "random_forest",
                    "user_behavior": "random_forest"
                },
                "data_retention_days": 90,
                "performance_metrics": [
                    "response_time_ms",
                    "cpu_usage_percent",
                    "memory_usage_mb",
                    "request_throughput",
                    "error_rate"
                ],
                "optimization_targets": {
                    "response_time_ms": {"target": 100, "weight": 0.3, "direction": "minimize"},
                    "cpu_usage_percent": {"target": 70, "weight": 0.2, "direction": "minimize"},
                    "memory_usage_mb": {"target": 500, "weight": 0.2, "direction": "minimize"},
                    "request_throughput": {"target": 1000, "weight": 0.2, "direction": "maximize"},
                    "error_rate": {"target": 0.01, "weight": 0.1, "direction": "minimize"}
                }
            },
            "adaptation": {
                "enabled": True,
                "adaptation_frequency_hours": 6,
                "adaptation_threshold": 0.1,  # 10% deviation triggers adaptation
                "max_adaptation_attempts": 3,
                "adaptation_cooldown_minutes": 30,
                "adaptation_strategies": {
                    "performance": ["adjust_cache_size", "tune_thread_pool", "optimize_query", "scale_resources"],
                    "resource": ["reallocate_cpu", "reallocate_memory", "adjust_priorities"],
                    "behavior": ["update_recommendations", "adjust_ui", "personalize_content"]
                }
            },
            "monitoring": {
                "enabled": True,
                "collection_interval_seconds": 60,
                "reporting_interval_minutes": 60,
                "alert_thresholds": {
                    "response_time_ms": 200,
                    "cpu_usage_percent": 90,
                    "memory_usage_mb": 800,
                    "error_rate": 0.05
                },
                "alert_cooldown_minutes": 10
            },
            "model_storage": {
                "max_model_versions": 5,
                "model_compression": True,
                "backup_frequency_hours": 168  # Weekly
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded self-learning AI configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading self-learning config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default self-learning AI configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default self-learning config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved self-learning AI configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving self-learning config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def collect_performance_data(self, metrics: Dict[str, float], timestamp: datetime = None) -> Dict[str, Any]:
        """
        Collect system performance data for learning
        Args:
            metrics: Dictionary of metric names and their values
            timestamp: Timestamp of data collection, defaults to now
        Returns:
            Dictionary with collection status
        """
        try:
            if not self.config['monitoring']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Performance monitoring is disabled"
                }

            if timestamp is None:
                timestamp = datetime.now()

            data_point = {
                "timestamp": timestamp.isoformat(),
                "metrics": metrics
            }

            date_str = timestamp.strftime("%Y%m%d")
            data_file = os.path.join(self.data_dir, f"performance_data_{date_str}.jsonl")

            with open(data_file, 'a') as f:
                json.dump(data_point, f)
                f.write('\n')

            # Store in memory for quick access
            date_key = timestamp.strftime("%Y-%m-%d")
            if date_key not in self.performance_data:
                self.performance_data[date_key] = []
            self.performance_data[date_key].append(data_point)

            logger.info(f"Collected performance data at {timestamp.isoformat()}")
            return {
                "status": "success",
                "timestamp": timestamp.isoformat(),
                "metrics_collected": list(metrics.keys())
            }
        except Exception as e:
            logger.error(f"Error collecting performance data: {e}")
            return {"status": "error", "message": str(e)}

    def train_model(self, model_type: str, data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Train a self-learning model for optimization
        Args:
            model_type: Type of model to train ('performance_optimization', 'resource_allocation', 'user_behavior')
            data: Optional training data, if None will load from stored performance data
        Returns:
            Dictionary with training status and metrics
        """
        try:
            if not self.config['learning']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Self-learning is disabled"
                }

            if model_type not in self.config['learning']['model_types']:
                return {
                    "status": "error",
                    "message": f"Unknown model type: {model_type}"
                }

            model_algorithm = self.config['learning']['model_types'][model_type]
            if model_algorithm != "random_forest":
                return {
                    "status": "error",
                    "message": f"Unsupported model algorithm {model_algorithm} for {model_type}"
                }

            # Load data if not provided
            if data is None:
                data = []
                # Load from performance data files
                for date_key in sorted(self.performance_data.keys(), reverse=True):
                    data.extend(self.performance_data[date_key])
                    if len(data) >= 1000:  # Limit to recent 1000 data points
                        break

                if not data:
                    # Load from disk if no in-memory data
                    data_files = sorted(
                        [f for f in os.listdir(self.data_dir) if f.startswith("performance_data_")],
                        reverse=True
                    )
                    for data_file in data_files[:7]:  # Last 7 days
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
            # Features are the performance metrics
            feature_names = self.config['learning']['performance_metrics']
            X = []
            y = []

            if model_type == "performance_optimization":
                # For performance optimization, predict a weighted optimization score
                for data_point in data:
                    metrics = data_point['metrics']
                    if all(metric in metrics for metric in feature_names):
                        X.append([metrics[metric] for metric in feature_names])
                        # Calculate a weighted score based on optimization targets
                        score = 0.0
                        for metric, target_info in self.config['learning']['optimization_targets'].items():
                            if metric in metrics:
                                metric_value = metrics[metric]
                                weight = target_info['weight']
                                direction = target_info['direction']
                                target = target_info['target']
                                # Normalize deviation from target
                                deviation = abs(metric_value - target) / max(target, 1.0)
                                # If we want to minimize, higher deviation is worse
                                if direction == 'minimize':
                                    score += weight * (1.0 - deviation)
                                else:
                                    score += weight * deviation
                        y.append(score)

            elif model_type == "resource_allocation":
                # For resource allocation, predict optimal CPU and memory usage
                for data_point in data:
                    metrics = data_point['metrics']
                    if all(metric in metrics for metric in feature_names):
                        X.append([metrics[metric] for metric in feature_names if metric not in ['cpu_usage_percent', 'memory_usage_mb']])
                        # Target is CPU and memory usage (for simulation; in real system, would be optimal allocation)
                        cpu_target = metrics.get('cpu_usage_percent', 0)
                        mem_target = metrics.get('memory_usage_mb', 0)
                        y.append([cpu_target, mem_target])

            elif model_type == "user_behavior":
                # For user behavior, predict user engagement or satisfaction (simulated)
                for data_point in data:
                    metrics = data_point['metrics']
                    if all(metric in metrics for metric in feature_names):
                        X.append([metrics[metric] for metric in feature_names])
                        # Simulated user engagement score based on response time and error rate
                        response_time = metrics.get('response_time_ms', 0)
                        error_rate = metrics.get('error_rate', 0)
                        engagement = max(0, 1.0 - (response_time / 1000.0) - error_rate * 10)
                        y.append(engagement)

            if not X or not y:
                return {
                    "status": "error",
                    "message": f"No valid training data prepared for {model_type} model"
                }

            # Convert to numpy arrays
            X = np.array(X)
            if model_type == "resource_allocation":
                y = np.array(y)  # Multi-output for resource allocation
            else:
                y = np.array(y)  # Single output for others

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train model
            if model_algorithm == "random_forest":
                if model_type == "resource_allocation":
                    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
                else:
                    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
                model.fit(X_train, y_train)

                # Evaluate model
                y_pred = model.predict(X_test)
                if model_type == "resource_allocation":
                    mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
                    r2 = r2_score(y_test, y_pred, multioutput='raw_values')
                    eval_metrics = {
                        "mse_cpu": mse[0],
                        "mse_memory": mse[1],
                        "r2_cpu": r2[0],
                        "r2_memory": r2[1]
                    }
                else:
                    mse = mean_squared_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    eval_metrics = {"mse": mse, "r2": r2}

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
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported model algorithm: {model_algorithm}"
                }
        except Exception as e:
            logger.error(f"Error training {model_type} model: {e}")
            return {"status": "error", "message": str(e)}

    def predict_optimization(self, model_type: str, input_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Make a prediction using a trained self-learning model
        Args:
            model_type: Type of model to use for prediction
            input_data: Dictionary of input metrics for prediction
        Returns:
            Dictionary with prediction results
        """
        try:
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
            if model_type == "performance_optimization":
                feature_names = self.config['learning']['performance_metrics']
                if not all(name in input_data for name in feature_names):
                    missing = [name for name in feature_names if name not in input_data]
                    return {
                        "status": "error",
                        "message": f"Missing required input metrics for {model_type}: {missing}"
                    }
                input_array = np.array([[input_data[name] for name in feature_names]])

                # Make prediction
                prediction = model.predict(input_array)[0]

                return {
                    "status": "success",
                    "model_type": model_type,
                    "version": latest_model_info['version'],
                    "prediction": {
                        "optimization_score": float(prediction)
                    },
                    "timestamp": datetime.now().isoformat(),
                    "input_data": input_data
                }

            elif model_type == "resource_allocation":
                feature_names = [name for name in self.config['learning']['performance_metrics'] 
                               if name not in ['cpu_usage_percent', 'memory_usage_mb']]
                if not all(name in input_data for name in feature_names):
                    missing = [name for name in feature_names if name not in input_data]
                    return {
                        "status": "error",
                        "message": f"Missing required input metrics for {model_type}: {missing}"
                    }
                input_array = np.array([[input_data[name] for name in feature_names]])

                # Make prediction
                prediction = model.predict(input_array)[0]

                return {
                    "status": "success",
                    "model_type": model_type,
                    "version": latest_model_info['version'],
                    "prediction": {
                        "optimal_cpu_usage_percent": float(prediction[0]),
                        "optimal_memory_usage_mb": float(prediction[1])
                    },
                    "timestamp": datetime.now().isoformat(),
                    "input_data": input_data
                }

            elif model_type == "user_behavior":
                feature_names = self.config['learning']['performance_metrics']
                if not all(name in input_data for name in feature_names):
                    missing = [name for name in feature_names if name not in input_data]
                    return {
                        "status": "error",
                        "message": f"Missing required input metrics for {model_type}: {missing}"
                    }
                input_array = np.array([[input_data[name] for name in feature_names]])

                # Make prediction
                prediction = model.predict(input_array)[0]

                return {
                    "status": "success",
                    "model_type": model_type,
                    "version": latest_model_info['version'],
                    "prediction": {
                        "user_engagement_score": float(prediction)
                    },
                    "timestamp": datetime.now().isoformat(),
                    "input_data": input_data
                }

            else:
                return {
                    "status": "error",
                    "message": f"Unsupported model type for prediction: {model_type}"
                }
        except Exception as e:
            logger.error(f"Error making prediction with {model_type} model: {e}")
            return {"status": "error", "message": str(e)}

    def adapt_system(self, adaptation_type: str, current_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Adapt system configuration based on learned optimizations
        Args:
            adaptation_type: Type of adaptation ('performance', 'resource', 'behavior')
            current_metrics: Current system metrics for adaptation decision
        Returns:
            Dictionary with adaptation status and actions taken
        """
        try:
            if not self.config['adaptation']['enabled']:
                return {
                    "status": "skipped",
                    "message": "System adaptation is disabled"
                }

            if adaptation_type not in self.config['adaptation']['adaptation_strategies']:
                return {
                    "status": "error",
                    "message": f"Unknown adaptation type: {adaptation_type}"
                }

            model_type_map = {
                "performance": "performance_optimization",
                "resource": "resource_allocation",
                "behavior": "user_behavior"
            }

            model_type = model_type_map.get(adaptation_type)
            if model_type not in self.models or not self.models[model_type]:
                return {
                    "status": "error",
                    "message": f"No trained model available for {model_type} adaptation"
                }

            # Get prediction for optimal settings
            prediction_result = self.predict_optimization(model_type, current_metrics)
            if prediction_result['status'] != 'success':
                return prediction_result

            # Determine if adaptation is needed based on threshold
            adaptation_threshold = self.config['adaptation']['adaptation_threshold']
            strategies = self.config['adaptation']['adaptation_strategies'][adaptation_type]
            actions_taken = []

            if adaptation_type == "performance":
                current_score = 0.0
                predicted_score = prediction_result['prediction']['optimization_score']
                for metric, value in current_metrics.items():
                    if metric in self.config['learning']['optimization_targets']:
                        target_info = self.config['learning']['optimization_targets'][metric]
                        weight = target_info['weight']
                        target = target_info['target']
                        direction = target_info['direction']
                        deviation = abs(value - target) / max(target, 1.0)
                        if direction == 'minimize':
                            current_score += weight * (1.0 - deviation)
                        else:
                            current_score += weight * deviation

                if abs(predicted_score - current_score) > adaptation_threshold:
                    # Need to adapt
                    for strategy in strategies:
                        actions_taken.append({
                            "strategy": strategy,
                            "status": "simulated_applied",
                            "details": f"Applied {strategy} to improve performance score from {current_score:.2f} to predicted {predicted_score:.2f}"
                        })
                else:
                    actions_taken.append({
                        "strategy": "no_action",
                        "status": "skipped",
                        "details": f"Current performance score {current_score:.2f} within threshold of predicted {predicted_score:.2f}"
                    })

            elif adaptation_type == "resource":
                current_cpu = current_metrics.get("cpu_usage_percent", 0)
                current_memory = current_metrics.get("memory_usage_mb", 0)
                predicted_cpu = prediction_result['prediction']['optimal_cpu_usage_percent']
                predicted_memory = prediction_result['prediction']['optimal_memory_usage_mb']

                if abs(current_cpu - predicted_cpu) / max(current_cpu, 1.0) > adaptation_threshold:
                    actions_taken.append({
                        "strategy": "reallocate_cpu",
                        "status": "simulated_applied",
                        "details": f"Adjusted CPU allocation from {current_cpu:.1f}% to predicted optimal {predicted_cpu:.1f}%"
                    })
                else:
                    actions_taken.append({
                        "strategy": "reallocate_cpu",
                        "status": "skipped",
                        "details": f"Current CPU {current_cpu:.1f}% within threshold of predicted {predicted_cpu:.1f}%"
                    })

                if abs(current_memory - predicted_memory) / max(current_memory, 1.0) > adaptation_threshold:
                    actions_taken.append({
                        "strategy": "reallocate_memory",
                        "status": "simulated_applied",
                        "details": f"Adjusted memory allocation from {current_memory:.1f}MB to predicted optimal {predicted_memory:.1f}MB"
                    })
                else:
                    actions_taken.append({
                        "strategy": "reallocate_memory",
                        "status": "skipped",
                        "details": f"Current memory {current_memory:.1f}MB within threshold of predicted {predicted_memory:.1f}MB"
                    })

            elif adaptation_type == "behavior":
                current_engagement = 1.0 - (current_metrics.get("response_time_ms", 0) / 1000.0) - current_metrics.get("error_rate", 0) * 10
                current_engagement = max(0, current_engagement)
                predicted_engagement = prediction_result['prediction']['user_engagement_score']

                if abs(predicted_engagement - current_engagement) > adaptation_threshold:
                    for strategy in strategies:
                        actions_taken.append({
                            "strategy": strategy,
                            "status": "simulated_applied",
                            "details": f"Applied {strategy} to improve user engagement from {current_engagement:.2f} to predicted {predicted_engagement:.2f}"
                        })
                else:
                    actions_taken.append({
                        "strategy": "no_action",
                        "status": "skipped",
                        "details": f"Current engagement {current_engagement:.2f} within threshold of predicted {predicted_engagement:.2f}"
                    })

            logger.info(f"Adapted system for {adaptation_type} with actions: {[a['strategy'] for a in actions_taken]}")
            return {
                "status": "success",
                "adaptation_type": adaptation_type,
                "timestamp": datetime.now().isoformat(),
                "current_metrics": current_metrics,
                "prediction": prediction_result['prediction'],
                "actions_taken": actions_taken
            }
        except Exception as e:
            logger.error(f"Error adapting system for {adaptation_type}: {e}")
            return {"status": "error", "message": str(e)}

    def get_learning_status(self) -> Dict[str, Any]:
        """
        Get current status of self-learning AI system
        """
        try:
            model_status = {}
            for model_type in self.config['learning']['model_types']:
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

            data_points_by_date = {date: len(data_list) for date, data_list in self.performance_data.items()}
            total_data_points = sum(data_points_by_date.values())

            return {
                "status": "success",
                "learning_enabled": self.config['learning']['enabled'],
                "adaptation_enabled": self.config['adaptation']['enabled'],
                "monitoring_enabled": self.config['monitoring']['enabled'],
                "models": model_status,
                "data_points": {
                    "total": total_data_points,
                    "by_date": data_points_by_date
                },
                "training_interval_hours": self.config['learning']['training_interval_hours'],
                "adaptation_frequency_hours": self.config['adaptation']['adaptation_frequency_hours'],
                "collection_interval_seconds": self.config['monitoring']['collection_interval_seconds']
            }
        except Exception as e:
            logger.error(f"Error getting self-learning AI status: {e}")
            return {"status": "error", "message": str(e)}

# Global self-learning AI instance
self_learning_ai = SelfLearningAI()
