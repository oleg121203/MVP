import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class PredictiveMaintenance:
    def __init__(self, maintenance_dir: str = 'maintenance_data', config_path: str = 'maintenance_config.json'):
        """
        Initialize AI-Driven Predictive Maintenance
        """
        self.maintenance_dir = maintenance_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.equipment = []
        os.makedirs(self.maintenance_dir, exist_ok=True)
        logger.info("Predictive Maintenance module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load predictive maintenance configuration from file or create default if not exists
        """
        default_config = {
            "predictive_maintenance": {
                "enabled": True,
                "prediction_modes": ["real_time", "batch", "on_demand", "hybrid"],
                "default_mode": "real_time",
                "prediction_frequency": "continuous",
                "prediction_time": "00:00",
                "equipment_domains": [
                    "manufacturing",
                    "transportation",
                    "energy",
                    "facilities",
                    "IT_infrastructure",
                    "medical"
                ],
                "prediction_levels": {
                    "manufacturing": "real_time",
                    "transportation": "hybrid",
                    "energy": "batch",
                    "facilities": "on_demand",
                    "IT_infrastructure": "hybrid",
                    "medical": "real_time"
                }
            },
            "models": {
                "enabled": True,
                "model_types": ["machine_learning", "statistical", "rule_based", "hybrid", "custom"],
                "default_model": "machine_learning",
                "model_validation": True
            },
            "prediction": {
                "enabled": True,
                "prediction_types": ["time_series", "anomaly_detection", "pattern_recognition", "predictive_modeling", "contextual"],
                "default_prediction": "time_series",
                "prediction_validation": True
            },
            "failure_classification": {
                "enabled": True,
                "severity_levels": ["low", "medium", "high", "critical"],
                "default_severity": "medium",
                "impact_areas": ["operations", "financial", "safety", "compliance", "productivity"],
                "default_impact": "operations",
                "time_horizons": ["immediate", "short_term", "medium_term", "long_term"],
                "default_horizon": "short_term"
            },
            "maintenance": {
                "enabled": True,
                "maintenance_strategies": ["preventive", "corrective", "condition_based", "predictive", "proactive"],
                "default_strategy": "predictive",
                "maintenance_validation": True,
                "resource_optimization": {
                    "enabled": True,
                    "optimization_strategies": ["cost", "time", "balanced"],
                    "default_strategy": "balanced",
                    "cost_alert_threshold": 1000,
                    "high_priority_alert_threshold": 5
                }
            },
            "reporting": {
                "enabled": True,
                "report_types": ["failure_prediction", "maintenance_schedule", "resource_allocation", "performance_metrics", "cost_analysis"],
                "default_report": "failure_prediction",
                "report_frequency": "weekly",
                "report_time": "08:00",
                "distribution_channels": ["email", "dashboard", "mobile_app"],
                "recipients": ["maintenance_team", "operations", "management", "equipment_owners"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["imminent_failure", "maintenance_due", "anomaly_detected", "prediction_confidence_low", "resource_shortage"],
                "alert_channels": ["email", "dashboard", "mobile_app", "sms", "phone"],
                "alert_escalation": True,
                "thresholds": {
                    "severity_threshold": "high",
                    "prediction_confidence": 0.7,
                    "time_to_failure_hours": 48,
                    "anomaly_score": 0.8
                }
            },
            "error_handling": {
                "enabled": True,
                "error_recovery": True,
                "recovery_attempts": 3,
                "recovery_delay_seconds": 30,
                "fallback_actions": ["notify_admin", "use_default_model", "log_only"],
                "default_fallback": "notify_admin",
                "error_logging": "detailed"
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded predictive maintenance configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading predictive maintenance config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default predictive maintenance configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default predictive maintenance config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved predictive maintenance configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving predictive maintenance config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_model(self, model_id: str, model_name: str, description: str, equipment_domain: str, model_type: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Define a new predictive maintenance model
        Args:
            model_id: Unique identifier for the model
            model_name: Name of the model
            description: Detailed description of the model
            equipment_domain: Target domain for predictive maintenance
            model_type: Type of model ('machine_learning', 'statistical', etc.)
            parameters: Model parameters and hyperparameters
        Returns:
            Dictionary with model definition status
        """
        try:
            if not self.config['predictive_maintenance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Predictive maintenance is disabled"
                }

            if model_id in self.models:
                return {
                    "status": "error",
                    "message": f"Model with ID {model_id} already exists"
                }

            if equipment_domain not in self.config['predictive_maintenance']['equipment_domains']:
                return {
                    "status": "error",
                    "message": f"Invalid equipment domain: {equipment_domain}. Must be one of {self.config['predictive_maintenance']['equipment_domains']}"
                }

            model_type = model_type or self.config['models']['default_model']
            if model_type not in self.config['models']['model_types']:
                return {
                    "status": "error",
                    "message": f"Invalid model type: {model_type}. Must be one of {self.config['models']['model_types']}"
                }

            model_info = {
                "model_id": model_id,
                "model_name": model_name,
                "description": description,
                "equipment_domain": equipment_domain,
                "model_type": model_type,
                "parameters": parameters or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "defined",
                "version": "1.0"
            }

            self.models[model_id] = model_info

            # Save model to file
            model_file = os.path.join(self.maintenance_dir, f"model_{model_id}.json")
            try:
                with open(model_file, 'w') as f:
                    json.dump(model_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving model data for {model_id}: {e}")

            logger.info(f"Defined predictive maintenance model {model_id} - {model_name} for {equipment_domain}")
            return {
                "status": "success",
                "model_id": model_id,
                "model_name": model_name,
                "equipment_domain": equipment_domain,
                "model_type": model_type,
                "parameters": parameters or {},
                "created_at": model_info['created_at'],
                "version": model_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining model {model_id}: {e}")
            return {"status": "error", "message": str(e)}

    def predict_failure(self, model_id: str, prediction_type: Optional[str] = None, equipment_ids: Optional[List[str]] = None, data_points: Optional[List[Dict[str, Any]]] = None, time_window: Optional[str] = None) -> Dict[str, Any]:
        """
        Predict equipment failures using the specified model
        Args:
            model_id: ID of model to use for failure prediction
            prediction_type: Type of prediction ('time_series', 'anomaly_detection', etc.)
            equipment_ids: List of equipment IDs to analyze
            data_points: List of data points for analysis [{'metric': str, 'value': float, 'timestamp': str, 'attributes': dict}]
            time_window: Time window for analysis (e.g., '1h', '1d', '1w')
        Returns:
            Dictionary with failure prediction status
        """
        try:
            if not self.config['predictive_maintenance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Predictive maintenance is disabled",
                    "prediction_id": "N/A"
                }

            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} not found",
                    "prediction_id": "N/A"
                }

            model_info = self.models[model_id]

            prediction_type = prediction_type or self.config['prediction']['default_prediction']
            if prediction_type not in self.config['prediction']['prediction_types']:
                return {
                    "status": "error",
                    "message": f"Invalid prediction type: {prediction_type}. Must be one of {self.config['prediction']['prediction_types']}",
                    "prediction_id": "N/A"
                }

            prediction_id = f"pred_{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated failure prediction - in real system, would run analysis
            prediction_start = datetime.now()
            prediction_info = {
                "prediction_id": prediction_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "equipment_domain": model_info['equipment_domain'],
                "prediction_type": prediction_type,
                "equipment_ids": equipment_ids or [],
                "data_points": data_points or [],
                "time_window": time_window or "default",
                "start_time": prediction_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "predicting",
                "failure_predictions": [],
                "alerts": []
            }

            # Use provided data points or generate simulated ones
            if data_points and len(data_points) > 0:
                data_to_analyze = data_points
            else:
                data_to_analyze = []
                for i in range(random.randint(10, 20)):
                    data_to_analyze.append({
                        "metric": f"metric_{i%5+1}",
                        "value": random.uniform(0, 100),
                        "timestamp": datetime.now().isoformat(),
                        "attributes": {
                            "source": random.choice(["sensor", "log", "user", "system", "maintenance"]),
                            "location": random.choice(["east", "west", "north", "south", "central"])
                        }
                    })

            # Use provided equipment IDs or generate simulated ones
            if equipment_ids and len(equipment_ids) > 0:
                eq_ids = equipment_ids
            else:
                eq_ids = [f"eq_{random.randint(1000, 9999)}" for _ in range(random.randint(3, 8))]

            # Analyze data points for failure predictions
            for eq_id in eq_ids:
                if random.random() < 0.3:  # 30% chance of predicting a failure
                    severity = random.choice(self.config['failure_classification']['severity_levels'])
                    impact_area = random.choice(self.config['failure_classification']['impact_areas'])
                    time_horizon = random.choice(self.config['failure_classification']['time_horizons'])
                    confidence = random.uniform(0.5, 0.95)
                    time_to_failure_hours = random.randint(1, 168)  # 1 hour to 1 week
                    
                    failure_prediction = {
                        "equipment_id": eq_id,
                        "prediction_id": f"fail_{prediction_id}_{eq_id}",
                        "severity": severity,
                        "impact_area": impact_area,
                        "time_horizon": time_horizon,
                        "time_to_failure_hours": time_to_failure_hours,
                        "confidence": confidence,
                        "description": f"Predicted {severity} failure in {impact_area} within {time_horizon} for equipment {eq_id}",
                        "timestamp": datetime.now().isoformat(),
                        "status": "predicted"
                    }
                    prediction_info['failure_predictions'].append(failure_prediction)

            # Check for alerts based on thresholds
            severity_threshold = self.config['alerts']['thresholds']['severity_threshold']
            high_severity_predictions = [pred for pred in prediction_info['failure_predictions'] 
                                       if pred['severity'] in (self.config['failure_classification']['severity_levels'][self.config['failure_classification']['severity_levels'].index(severity_threshold):])]
            if high_severity_predictions:
                prediction_info['alerts'].append({
                    "alert_type": "imminent_failure",
                    "equipment_domain": model_info['equipment_domain'],
                    "prediction_count": len(high_severity_predictions),
                    "severity_threshold": severity_threshold,
                    "message": f"High severity failure predictions in {model_info['equipment_domain']}: {len(high_severity_predictions)} predictions"
                })

            time_to_failure_threshold = self.config['alerts']['thresholds']['time_to_failure_hours']
            imminent_predictions = [pred for pred in prediction_info['failure_predictions'] 
                                  if pred['time_to_failure_hours'] <= time_to_failure_threshold]
            if imminent_predictions:
                prediction_info['alerts'].append({
                    "alert_type": "imminent_failure",
                    "equipment_domain": model_info['equipment_domain'],
                    "prediction_count": len(imminent_predictions),
                    "time_threshold_hours": time_to_failure_threshold,
                    "message": f"Imminent failure predictions in {model_info['equipment_domain']}: {len(imminent_predictions)} predictions within {time_to_failure_threshold} hours"
                })

            prediction_end = datetime.now()
            prediction_info['end_time'] = prediction_end.isoformat()
            prediction_info['duration_seconds'] = (prediction_end - prediction_start).total_seconds()
            prediction_info['status'] = "completed"

            # Save prediction results
            prediction_file = os.path.join(self.maintenance_dir, f"prediction_{prediction_id}.json")
            try:
                with open(prediction_file, 'w') as f:
                    json.dump(prediction_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving prediction data for {prediction_id}: {e}")

            # Add equipment to list if not already present
            for eq_id in eq_ids:
                if not any(eq['equipment_id'] == eq_id for eq in self.equipment):
                    self.equipment.append({
                        "equipment_id": eq_id,
                        "model_id": model_id,
                        "equipment_domain": model_info['equipment_domain'],
                        "status": "monitored",
                        "last_prediction_at": prediction_end.isoformat(),
                        "last_prediction_id": prediction_id
                    })

            logger.info(f"Completed failure prediction {prediction_id} using model {model_id}, found {len(prediction_info['failure_predictions'])} potential failures")
            return {
                "status": "success",
                "prediction_id": prediction_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "equipment_domain": model_info['equipment_domain'],
                "prediction_type": prediction_type,
                "equipment_count": len(eq_ids),
                "data_points_count": len(data_to_analyze),
                "start_time": prediction_info['start_time'],
                "end_time": prediction_info['end_time'],
                "duration_seconds": prediction_info['duration_seconds'],
                "prediction_status": prediction_info['status'],
                "failure_predictions_count": len(prediction_info['failure_predictions']),
                "alerts_count": len(prediction_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error predicting failures using model {model_id}: {e}")
            return {"status": "error", "message": str(e), "prediction_id": "N/A"}

    def schedule_maintenance(self, prediction_id: str, maintenance_strategy: Optional[str] = None) -> Dict[str, Any]:
        """
        Schedule maintenance based on failure predictions
        Args:
            prediction_id: ID of the prediction containing failure predictions
            maintenance_strategy: Strategy for maintenance ('preventive', 'corrective', etc.)
        Returns:
            Dictionary with maintenance scheduling status
        """
        try:
            if not self.config['predictive_maintenance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Predictive maintenance is disabled",
                    "schedule_id": "N/A"
                }

            if not self.config['maintenance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Maintenance scheduling is disabled",
                    "schedule_id": "N/A"
                }

            prediction_file = os.path.join(self.maintenance_dir, f"prediction_{prediction_id}.json")
            if not os.path.exists(prediction_file):
                return {
                    "status": "error",
                    "message": f"Prediction data for {prediction_id} not found",
                    "schedule_id": "N/A"
                }

            try:
                with open(prediction_file, 'r') as f:
                    prediction_info = json.load(f)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error loading prediction data for {prediction_id}: {str(e)}",
                    "schedule_id": "N/A"
                }

            model_id = prediction_info['model_id']
            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} for prediction {prediction_id} not found",
                    "schedule_id": "N/A"
                }

            model_info = self.models[model_id]

            maintenance_strategy = maintenance_strategy or self.config['maintenance']['default_strategy']
            if maintenance_strategy not in self.config['maintenance']['maintenance_strategies']:
                return {
                    "status": "error",
                    "message": f"Invalid maintenance strategy: {maintenance_strategy}. Must be one of {self.config['maintenance']['maintenance_strategies']}",
                    "schedule_id": "N/A"
                }

            schedule_id = f"sched_{prediction_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated maintenance scheduling - in real system, would optimize schedule
            scheduling_start = datetime.now()
            schedule_info = {
                "schedule_id": schedule_id,
                "prediction_id": prediction_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "equipment_domain": model_info['equipment_domain'],
                "maintenance_strategy": maintenance_strategy,
                "start_time": scheduling_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "scheduling",
                "maintenance_plans": [],
                "alerts": []
            }

            # Generate maintenance plans for predicted failures
            severity_threshold = self.config['alerts']['thresholds']['severity_threshold']
            time_to_failure_threshold = self.config['alerts']['thresholds']['time_to_failure_hours']

            for prediction in prediction_info['failure_predictions']:
                equipment_id = prediction['equipment_id']
                severity = prediction['severity']
                time_to_failure_hours = prediction['time_to_failure_hours']
                confidence = prediction['confidence']

                # Determine if maintenance should be scheduled based on severity and time to failure
                severity_index = self.config['failure_classification']['severity_levels'].index(severity)
                threshold_index = self.config['failure_classification']['severity_levels'].index(severity_threshold)
                is_high_severity = severity_index >= threshold_index
                is_imminent = time_to_failure_hours <= time_to_failure_threshold

                if is_high_severity or is_imminent:
                    # Schedule maintenance
                    maintenance_id = f"maint_{schedule_id}_{equipment_id}"
                    maintenance_start = datetime.now() + timedelta(hours=max(1, time_to_failure_hours - 24))
                    maintenance_duration_hours = random.randint(1, 4)
                    maintenance_end = maintenance_start + timedelta(hours=maintenance_duration_hours)

                    maintenance_plan = {
                        "maintenance_id": maintenance_id,
                        "equipment_id": equipment_id,
                        "prediction_id": prediction['prediction_id'],
                        "severity": severity,
                        "time_to_failure_hours": time_to_failure_hours,
                        "confidence": confidence,
                        "maintenance_strategy": maintenance_strategy,
                        "scheduled_start": maintenance_start.isoformat(),
                        "scheduled_end": maintenance_end.isoformat(),
                        "duration_hours": maintenance_duration_hours,
                        "status": "scheduled",
                        "description": f"Scheduled {maintenance_strategy} maintenance for equipment {equipment_id} due to {severity} failure prediction"
                    }
                    schedule_info['maintenance_plans'].append(maintenance_plan)

                    # Update equipment status
                    for eq in self.equipment:
                        if eq['equipment_id'] == equipment_id:
                            eq['status'] = "maintenance_scheduled"
                            eq['last_maintenance_scheduled_at'] = datetime.now().isoformat()
                            eq['last_maintenance_id'] = maintenance_id
                            break

            # Check for alerts based on scheduled maintenance
            if schedule_info['maintenance_plans']:
                high_severity_plans = [plan for plan in schedule_info['maintenance_plans'] 
                                     if plan['severity'] in self.config['failure_classification']['severity_levels'][self.config['failure_classification']['severity_levels'].index(severity_threshold):]]
                if high_severity_plans:
                    schedule_info['alerts'].append({
                        "alert_type": "maintenance_due",
                        "equipment_domain": model_info['equipment_domain'],
                        "maintenance_count": len(high_severity_plans),
                        "severity_threshold": severity_threshold,
                        "message": f"High severity maintenance scheduled in {model_info['equipment_domain']}: {len(high_severity_plans)} plans"
                    })

                imminent_plans = [plan for plan in schedule_info['maintenance_plans'] 
                                 if plan['time_to_failure_hours'] <= time_to_failure_threshold]
                if imminent_plans:
                    schedule_info['alerts'].append({
                        "alert_type": "maintenance_due",
                        "equipment_domain": model_info['equipment_domain'],
                        "maintenance_count": len(imminent_plans),
                        "time_threshold_hours": time_to_failure_threshold,
                        "message": f"Imminent maintenance scheduled in {model_info['equipment_domain']}: {len(imminent_plans)} plans within {time_to_failure_threshold} hours"
                    })

            scheduling_end = datetime.now()
            schedule_info['end_time'] = scheduling_end.isoformat()
            schedule_info['duration_seconds'] = (scheduling_end - scheduling_start).total_seconds()
            schedule_info['status'] = "completed"

            # Save schedule data
            schedule_file = os.path.join(self.maintenance_dir, f"schedule_{schedule_id}.json")
            try:
                with open(schedule_file, 'w') as f:
                    json.dump(schedule_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving schedule data for {schedule_id}: {e}")

            # Save updated equipment list
            equipment_file = os.path.join(self.maintenance_dir, "equipment.json")
            try:
                with open(equipment_file, 'w') as f:
                    json.dump(self.equipment, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving equipment list: {e}")

            logger.info(f"Completed maintenance scheduling {schedule_id} for prediction {prediction_id}, scheduled {len(schedule_info['maintenance_plans'])} maintenance plans")
            return {
                "status": "success",
                "schedule_id": schedule_id,
                "prediction_id": prediction_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "equipment_domain": model_info['equipment_domain'],
                "maintenance_strategy": maintenance_strategy,
                "start_time": schedule_info['start_time'],
                "end_time": schedule_info['end_time'],
                "duration_seconds": schedule_info['duration_seconds'],
                "schedule_status": schedule_info['status'],
                "maintenance_plans_count": len(schedule_info['maintenance_plans']),
                "alerts_count": len(schedule_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error scheduling maintenance for prediction {prediction_id}: {e}")
            return {"status": "error", "message": str(e), "schedule_id": "N/A"}

    def optimize_maintenance_resources(self, schedule_id: str, optimization_strategy: Optional[str] = None) -> Dict[str, Any]:
        """
        Optimize resource allocation for scheduled maintenance
        Args:
            schedule_id: ID of the maintenance schedule to optimize
            optimization_strategy: Strategy for resource optimization ('cost', 'time', 'balanced', etc.)
        Returns:
            Dictionary with resource optimization status
        """
        try:
            if not self.config['predictive_maintenance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Predictive maintenance is disabled",
                    "optimization_id": "N/A"
                }

            if not self.config['maintenance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Maintenance scheduling is disabled",
                    "optimization_id": "N/A"
                }

            if not self.config['maintenance']['resource_optimization']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Maintenance resource optimization is disabled",
                    "optimization_id": "N/A"
                }

            schedule_file = os.path.join(self.maintenance_dir, f"schedule_{schedule_id}.json")
            if not os.path.exists(schedule_file):
                return {
                    "status": "error",
                    "message": f"Schedule data for {schedule_id} not found",
                    "optimization_id": "N/A"
                }

            try:
                with open(schedule_file, 'r') as f:
                    schedule_info = json.load(f)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error loading schedule data for {schedule_id}: {str(e)}",
                    "optimization_id": "N/A"
                }

            optimization_strategy = optimization_strategy or self.config['maintenance']['resource_optimization']['default_strategy']
            if optimization_strategy not in self.config['maintenance']['resource_optimization']['optimization_strategies']:
                return {
                    "status": "error",
                    "message": f"Invalid optimization strategy: {optimization_strategy}. Must be one of {self.config['maintenance']['resource_optimization']['optimization_strategies']}",
                    "optimization_id": "N/A"
                }

            optimization_id = f"opt_{schedule_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated resource optimization - in real system, would use complex optimization algorithms
            optimization_start = datetime.now()
            optimization_info = {
                "optimization_id": optimization_id,
                "schedule_id": schedule_id,
                "prediction_id": schedule_info['prediction_id'],
                "model_id": schedule_info['model_id'],
                "model_name": schedule_info['model_name'],
                "equipment_domain": schedule_info['equipment_domain'],
                "optimization_strategy": optimization_strategy,
                "start_time": optimization_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "optimizing",
                "resource_allocations": [],
                "alerts": []
            }

            # Optimize resources for each maintenance plan
            for plan in schedule_info['maintenance_plans']:
                maintenance_id = plan['maintenance_id']
                equipment_id = plan['equipment_id']
                severity = plan['severity']

                # Simulated resource allocation based on strategy
                if optimization_strategy == "cost":
                    technician_level = "junior"
                    parts_quality = "standard"
                    priority = "normal"
                    estimated_cost = random.randint(100, 500)
                    duration_multiplier = 1.2  # Slower due to cheaper resources
                elif optimization_strategy == "time":
                    technician_level = "senior"
                    parts_quality = "premium"
                    priority = "high"
                    estimated_cost = random.randint(800, 1500)
                    duration_multiplier = 0.8  # Faster due to better resources
                else:  # balanced or other
                    technician_level = "standard"
                    parts_quality = "standard"
                    priority = "normal"
                    estimated_cost = random.randint(400, 1000)
                    duration_multiplier = 1.0  # Balanced approach

                # Adjust duration based on optimization strategy
                original_duration_hours = plan['duration_hours']
                optimized_duration_hours = max(1, int(original_duration_hours * duration_multiplier))
                maintenance_start = datetime.fromisoformat(plan['scheduled_start'])
                optimized_end = maintenance_start + timedelta(hours=optimized_duration_hours)

                # Update plan with optimized resources
                plan['technician_level'] = technician_level
                plan['parts_quality'] = parts_quality
                plan['priority'] = priority
                plan['estimated_cost'] = estimated_cost
                plan['optimized_duration_hours'] = optimized_duration_hours
                plan['scheduled_end'] = optimized_end.isoformat()
                plan['optimization_strategy'] = optimization_strategy
                plan['status'] = "optimized"

                # Record resource allocation
                allocation = {
                    "maintenance_id": maintenance_id,
                    "equipment_id": equipment_id,
                    "severity": severity,
                    "technician_level": technician_level,
                    "parts_quality": parts_quality,
                    "priority": priority,
                    "estimated_cost": estimated_cost,
                    "original_duration_hours": original_duration_hours,
                    "optimized_duration_hours": optimized_duration_hours,
                    "optimization_strategy": optimization_strategy
                }
                optimization_info['resource_allocations'].append(allocation)

                # Update equipment status
                for eq in self.equipment:
                    if eq['equipment_id'] == equipment_id:
                        eq['status'] = "maintenance_optimized"
                        eq['last_resource_optimization_at'] = datetime.now().isoformat()
                        eq['last_optimization_id'] = optimization_id
                        break

            # Check for alerts based on resource optimization
            if schedule_info['maintenance_plans']:
                high_cost_allocations = [alloc for alloc in optimization_info['resource_allocations'] 
                                       if alloc['estimated_cost'] > self.config['maintenance']['resource_optimization']['cost_alert_threshold']]
                if high_cost_allocations:
                    optimization_info['alerts'].append({
                        "alert_type": "high_cost_allocation",
                        "equipment_domain": schedule_info['equipment_domain'],
                        "allocation_count": len(high_cost_allocations),
                        "cost_threshold": self.config['maintenance']['resource_optimization']['cost_alert_threshold'],
                        "message": f"High cost resource allocations in {schedule_info['equipment_domain']}: {len(high_cost_allocations)} plans exceed cost threshold"
                    })

                high_priority_allocations = [alloc for alloc in optimization_info['resource_allocations'] 
                                           if alloc['priority'] == "high"]
                if len(high_priority_allocations) > self.config['maintenance']['resource_optimization']['high_priority_alert_threshold']:
                    optimization_info['alerts'].append({
                        "alert_type": "high_priority_allocation",
                        "equipment_domain": schedule_info['equipment_domain'],
                        "allocation_count": len(high_priority_allocations),
                        "priority_threshold": self.config['maintenance']['resource_optimization']['high_priority_alert_threshold'],
                        "message": f"High priority resource allocations in {schedule_info['equipment_domain']}: {len(high_priority_allocations)} plans with high priority"
                    })

            optimization_end = datetime.now()
            optimization_info['end_time'] = optimization_end.isoformat()
            optimization_info['duration_seconds'] = (optimization_end - optimization_start).total_seconds()
            optimization_info['status'] = "completed"

            # Save optimization data
            optimization_file = os.path.join(self.maintenance_dir, f"optimization_{optimization_id}.json")
            try:
                with open(optimization_file, 'w') as f:
                    json.dump(optimization_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving optimization data for {optimization_id}: {e}")

            # Update schedule with optimized plans
            try:
                with open(schedule_file, 'w') as f:
                    json.dump(schedule_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error updating schedule data for {schedule_id}: {e}")

            # Save updated equipment list
            equipment_file = os.path.join(self.maintenance_dir, "equipment.json")
            try:
                with open(equipment_file, 'w') as f:
                    json.dump(self.equipment, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving equipment list: {e}")

            logger.info(f"Completed resource optimization {optimization_id} for schedule {schedule_id}, optimized {len(optimization_info['resource_allocations'])} maintenance plans")
            return {
                "status": "success",
                "optimization_id": optimization_id,
                "schedule_id": schedule_id,
                "prediction_id": schedule_info['prediction_id'],
                "model_id": schedule_info['model_id'],
                "model_name": schedule_info['model_name'],
                "equipment_domain": schedule_info['equipment_domain'],
                "optimization_strategy": optimization_strategy,
                "start_time": optimization_info['start_time'],
                "end_time": optimization_info['end_time'],
                "duration_seconds": optimization_info['duration_seconds'],
                "optimization_status": optimization_info['status'],
                "resource_allocations_count": len(optimization_info['resource_allocations']),
                "alerts_count": len(optimization_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error optimizing resources for schedule {schedule_id}: {e}")
            return {"status": "error", "message": str(e), "optimization_id": "N/A"}

    def generate_maintenance_analytics(self, time_range: str = "all", report_type: str = "summary") -> Dict[str, Any]:
        """
        Generate analytics for predictive maintenance activities
        Args:
            time_range: Time range for analytics ("all", "last_24h", "last_7d", "last_30d")
            report_type: Type of report ("summary", "detailed", "trends", "equipment")
        Returns:
            Dictionary with maintenance analytics data
        """
        try:
            if not self.config['predictive_maintenance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Predictive maintenance is disabled",
                    "report_id": "N/A"
                }

            if not self.config['reporting']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Reporting is disabled",
                    "report_id": "N/A"
                }

            valid_time_ranges = ["all", "last_24h", "last_7d", "last_30d"]
            if time_range not in valid_time_ranges:
                return {
                    "status": "error",
                    "message": f"Invalid time range: {time_range}. Must be one of {valid_time_ranges}",
                    "report_id": "N/A"
                }

            valid_report_types = ["summary", "detailed", "trends", "equipment"]
            if report_type not in valid_report_types:
                return {
                    "status": "error",
                    "message": f"Invalid report type: {report_type}. Must be one of {valid_report_types}",
                    "report_id": "N/A"
                }

            report_id = f"report_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Calculate time filter
            now = datetime.now()
            if time_range == "last_24h":
                time_filter = now - timedelta(hours=24)
            elif time_range == "last_7d":
                time_filter = now - timedelta(days=7)
            elif time_range == "last_30d":
                time_filter = now - timedelta(days=30)
            else:  # all
                time_filter = None

            # Generate analytics based on stored data
            analytics_start = datetime.now()
            analytics_data = {
                "report_id": report_id,
                "time_range": time_range,
                "report_type": report_type,
                "start_time": analytics_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "generating",
                "predictions": {
                    "total_count": 0,
                    "by_domain": {},
                    "by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0},
                    "accuracy": 0.0
                },
                "maintenance_schedules": {
                    "total_count": 0,
                    "by_domain": {},
                    "by_strategy": {},
                    "effectiveness": 0.0
                },
                "resource_optimizations": {
                    "total_count": 0,
                    "by_domain": {},
                    "by_strategy": {},
                    "cost_savings": 0.0,
                    "time_savings": 0.0
                },
                "equipment_status": {
                    "total_count": len(self.equipment),
                    "by_domain": {},
                    "by_status": {}
                },
                "alerts": {
                    "total_count": 0,
                    "by_type": {},
                    "by_domain": {}
                },
                "trends": {
                    "prediction_accuracy_over_time": [],
                    "maintenance_effectiveness_over_time": [],
                    "equipment_downtime_over_time": []
                },
                "detailed_insights": []
            }

            # Process prediction data
            prediction_files = [f for f in os.listdir(self.maintenance_dir) if f.startswith("prediction_") and f.endswith(".json")]
            for pred_file in prediction_files:
                try:
                    file_path = os.path.join(self.maintenance_dir, pred_file)
                    with open(file_path, 'r') as f:
                        pred_data = json.load(f)

                    start_time = datetime.fromisoformat(pred_data['start_time'])
                    if time_filter and start_time < time_filter:
                        continue

                    analytics_data['predictions']['total_count'] += 1
                    domain = pred_data.get('equipment_domain', 'unknown')
                    analytics_data['predictions']['by_domain'][domain] = analytics_data['predictions']['by_domain'].get(domain, 0) + 1

                    for failure_pred in pred_data.get('failure_predictions', []):
                        severity = failure_pred.get('severity', 'unknown')
                        if severity in analytics_data['predictions']['by_severity']:
                            analytics_data['predictions']['by_severity'][severity] += 1

                    if report_type == "detailed":
                        analytics_data['detailed_insights'].append({
                            "type": "prediction",
                            "id": pred_data['prediction_id'],
                            "domain": domain,
                            "model": pred_data['model_name'],
                            "start_time": pred_data['start_time'],
                            "failure_count": len(pred_data.get('failure_predictions', [])),
                            "status": pred_data['status']
                        })
                except Exception as e:
                    logger.warning(f"Error processing prediction file {pred_file}: {e}")

            # Process schedule data
            schedule_files = [f for f in os.listdir(self.maintenance_dir) if f.startswith("schedule_") and f.endswith(".json")]
            for sched_file in schedule_files:
                try:
                    file_path = os.path.join(self.maintenance_dir, sched_file)
                    with open(file_path, 'r') as f:
                        sched_data = json.load(f)

                    start_time = datetime.fromisoformat(sched_data['start_time'])
                    if time_filter and start_time < time_filter:
                        continue

                    analytics_data['maintenance_schedules']['total_count'] += 1
                    domain = sched_data.get('equipment_domain', 'unknown')
                    strategy = sched_data.get('maintenance_strategy', 'unknown')
                    analytics_data['maintenance_schedules']['by_domain'][domain] = analytics_data['maintenance_schedules']['by_domain'].get(domain, 0) + 1
                    analytics_data['maintenance_schedules']['by_strategy'][strategy] = analytics_data['maintenance_schedules']['by_strategy'].get(strategy, 0) + 1

                    # Process alerts in schedules
                    for alert in sched_data.get('alerts', []):
                        alert_type = alert.get('alert_type', 'unknown')
                        analytics_data['alerts']['total_count'] += 1
                        analytics_data['alerts']['by_type'][alert_type] = analytics_data['alerts']['by_type'].get(alert_type, 0) + 1
                        analytics_data['alerts']['by_domain'][domain] = analytics_data['alerts']['by_domain'].get(domain, 0) + 1

                    if report_type == "detailed":
                        analytics_data['detailed_insights'].append({
                            "type": "schedule",
                            "id": sched_data['schedule_id'],
                            "domain": domain,
                            "strategy": strategy,
                            "start_time": sched_data['start_time'],
                            "plans_count": len(sched_data.get('maintenance_plans', [])),
                            "status": sched_data['status']
                        })
                except Exception as e:
                    logger.warning(f"Error processing schedule file {sched_file}: {e}")

            # Process optimization data
            optimization_files = [f for f in os.listdir(self.maintenance_dir) if f.startswith("optimization_") and f.endswith(".json")]
            for opt_file in optimization_files:
                try:
                    file_path = os.path.join(self.maintenance_dir, opt_file)
                    with open(file_path, 'r') as f:
                        opt_data = json.load(f)

                    start_time = datetime.fromisoformat(opt_data['start_time'])
                    if time_filter and start_time < time_filter:
                        continue

                    analytics_data['resource_optimizations']['total_count'] += 1
                    domain = opt_data.get('equipment_domain', 'unknown')
                    strategy = opt_data.get('optimization_strategy', 'unknown')
                    analytics_data['resource_optimizations']['by_domain'][domain] = analytics_data['resource_optimizations']['by_domain'].get(domain, 0) + 1
                    analytics_data['resource_optimizations']['by_strategy'][strategy] = analytics_data['resource_optimizations']['by_strategy'].get(strategy, 0) + 1

                    # Estimate savings (simulated)
                    total_allocations = len(opt_data.get('resource_allocations', []))
                    if strategy == "cost":
                        analytics_data['resource_optimizations']['cost_savings'] += total_allocations * random.uniform(50, 200)
                    elif strategy == "time":
                        analytics_data['resource_optimizations']['time_savings'] += total_allocations * random.uniform(2, 8)
                    else:  # balanced
                        analytics_data['resource_optimizations']['cost_savings'] += total_allocations * random.uniform(20, 100)
                        analytics_data['resource_optimizations']['time_savings'] += total_allocations * random.uniform(1, 4)

                    # Process alerts in optimizations
                    for alert in opt_data.get('alerts', []):
                        alert_type = alert.get('alert_type', 'unknown')
                        analytics_data['alerts']['total_count'] += 1
                        analytics_data['alerts']['by_type'][alert_type] = analytics_data['alerts']['by_type'].get(alert_type, 0) + 1
                        analytics_data['alerts']['by_domain'][domain] = analytics_data['alerts']['by_domain'].get(domain, 0) + 1

                    if report_type == "detailed":
                        analytics_data['detailed_insights'].append({
                            "type": "optimization",
                            "id": opt_data['optimization_id'],
                            "domain": domain,
                            "strategy": strategy,
                            "start_time": opt_data['start_time'],
                            "allocations_count": len(opt_data.get('resource_allocations', [])),
                            "status": opt_data['status']
                        })
                except Exception as e:
                    logger.warning(f"Error processing optimization file {opt_file}: {e}")

            # Process equipment status
            for eq in self.equipment:
                domain = eq.get('equipment_domain', 'unknown')
                status = eq.get('status', 'unknown')
                analytics_data['equipment_status']['by_domain'][domain] = analytics_data['equipment_status']['by_domain'].get(domain, 0) + 1
                analytics_data['equipment_status']['by_status'][status] = analytics_data['equipment_status']['by_status'].get(status, 0) + 1

                if report_type == "equipment":
                    analytics_data['detailed_insights'].append({
                        "type": "equipment",
                        "id": eq['equipment_id'],
                        "domain": domain,
                        "status": status,
                        "last_prediction": eq.get('last_prediction_at', 'N/A'),
                        "last_maintenance": eq.get('last_maintenance_scheduled_at', 'N/A'),
                        "last_optimization": eq.get('last_resource_optimization_at', 'N/A')
                    })

            # Generate simulated trends for report_type "trends"
            if report_type == "trends":
                # Simulated trend data - in real system, would use historical data
                for i in range(5):
                    day = (now - timedelta(days=4-i)).strftime("%Y-%m-%d")
                    analytics_data['trends']['prediction_accuracy_over_time'].append({
                        "date": day,
                        "accuracy": random.uniform(0.75, 0.95)
                    })
                    analytics_data['trends']['maintenance_effectiveness_over_time'].append({
                        "date": day,
                        "effectiveness": random.uniform(0.6, 0.9)
                    })
                    analytics_data['trends']['equipment_downtime_over_time'].append({
                        "date": day,
                        "downtime_hours": random.uniform(1.0, 5.0)
                    })

            # Calculate simulated metrics - in real system, would use actual data
            if analytics_data['predictions']['total_count'] > 0:
                analytics_data['predictions']['accuracy'] = random.uniform(0.75, 0.95)
            if analytics_data['maintenance_schedules']['total_count'] > 0:
                analytics_data['maintenance_schedules']['effectiveness'] = random.uniform(0.6, 0.9)

            analytics_end = datetime.now()
            analytics_data['end_time'] = analytics_end.isoformat()
            analytics_data['duration_seconds'] = (analytics_end - analytics_start).total_seconds()
            analytics_data['status'] = "completed"

            # Save analytics report
            report_file = os.path.join(self.maintenance_dir, f"report_{report_id}.json")
            try:
                with open(report_file, 'w') as f:
                    json.dump(analytics_data, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving analytics report {report_id}: {e}")

            logger.info(f"Generated predictive maintenance analytics report {report_id} for time range {time_range}, type {report_type}")
            return {
                "status": "success",
                "report_id": report_id,
                "time_range": time_range,
                "report_type": report_type,
                "start_time": analytics_data['start_time'],
                "end_time": analytics_data['end_time'],
                "duration_seconds": analytics_data['duration_seconds'],
                "report_status": analytics_data['status'],
                "prediction_count": analytics_data['predictions']['total_count'],
                "schedule_count": analytics_data['maintenance_schedules']['total_count'],
                "optimization_count": analytics_data['resource_optimizations']['total_count'],
                "equipment_count": analytics_data['equipment_status']['total_count'],
                "alert_count": analytics_data['alerts']['total_count'],
                "detailed_insights_count": len(analytics_data['detailed_insights'])
            }
        except Exception as e:
            logger.error(f"Error generating predictive maintenance analytics for time range {time_range}: {e}")
            return {"status": "error", "message": str(e), "report_id": "N/A"}

    def get_predictive_maintenance_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current predictive maintenance status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'models', 'equipment')
        Returns:
            Dictionary with predictive maintenance status information
        """
        try:
            models_summary = {
                "total_models": len(self.models),
                "models_by_domain": {},
                "models_by_type": {}
            }

            for m in self.models.values():
                models_summary['models_by_domain'][m['equipment_domain']] = models_summary['models_by_domain'].get(m['equipment_domain'], 0) + 1
                models_summary['models_by_type'][m['model_type']] = models_summary['models_by_type'].get(m['model_type'], 0) + 1

            equipment_summary = {
                "total_equipment": len(self.equipment),
                "equipment_by_domain": {},
                "equipment_by_status": {},
                "recent_equipment": sorted(
                    [
                        {
                            "equipment_id": eq['equipment_id'],
                            "model_id": eq['model_id'],
                            "equipment_domain": eq['equipment_domain'],
                            "status": eq['status'],
                            "last_prediction_at": eq.get('last_prediction_at', 'N/A'),
                            "last_prediction_id": eq.get('last_prediction_id', 'N/A')
                        }
                        for eq in self.equipment
                    ],
                    key=lambda x: x.get('last_prediction_at', ''),
                    reverse=True
                )[:5]
            }

            for eq in self.equipment:
                equipment_summary['equipment_by_domain'][eq['equipment_domain']] = equipment_summary['equipment_by_domain'].get(eq['equipment_domain'], 0) + 1
                equipment_summary['equipment_by_status'][eq['status']] = equipment_summary['equipment_by_status'].get(eq['status'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "predictive_maintenance_enabled": self.config['predictive_maintenance']['enabled'],
                    "default_mode": self.config['predictive_maintenance']['default_mode'],
                    "equipment_domains": self.config['predictive_maintenance']['equipment_domains'],
                    "models_summary": {
                        "total_models": models_summary['total_models']
                    },
                    "equipment_summary": {
                        "total_equipment": equipment_summary['total_equipment']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "predictive_maintenance": {
                        "enabled": self.config['predictive_maintenance']['enabled'],
                        "prediction_modes": self.config['predictive_maintenance']['prediction_modes'],
                        "default_mode": self.config['predictive_maintenance']['default_mode'],
                        "prediction_frequency": self.config['predictive_maintenance']['prediction_frequency'],
                        "prediction_time": self.config['predictive_maintenance']['prediction_time'],
                        "equipment_domains": self.config['predictive_maintenance']['equipment_domains'],
                        "prediction_levels": self.config['predictive_maintenance']['prediction_levels']
                    },
                    "models": {
                        "enabled": self.config['models']['enabled'],
                        "model_types": self.config['models']['model_types'],
                        "default_model": self.config['models']['default_model'],
                        "model_validation": self.config['models']['model_validation']
                    },
                    "prediction": {
                        "enabled": self.config['prediction']['enabled'],
                        "prediction_types": self.config['prediction']['prediction_types'],
                        "default_prediction": self.config['prediction']['default_prediction'],
                        "prediction_validation": self.config['prediction']['prediction_validation']
                    },
                    "failure_classification": {
                        "enabled": self.config['failure_classification']['enabled'],
                        "severity_levels": self.config['failure_classification']['severity_levels'],
                        "default_severity": self.config['failure_classification']['default_severity'],
                        "impact_areas": self.config['failure_classification']['impact_areas'],
                        "default_impact": self.config['failure_classification']['default_impact'],
                        "time_horizons": self.config['failure_classification']['time_horizons'],
                        "default_horizon": self.config['failure_classification']['default_horizon']
                    },
                    "maintenance": {
                        "enabled": self.config['maintenance']['enabled'],
                        "maintenance_strategies": self.config['maintenance']['maintenance_strategies'],
                        "default_strategy": self.config['maintenance']['default_strategy'],
                        "maintenance_validation": self.config['maintenance']['maintenance_validation']
                    },
                    "reporting": {
                        "enabled": self.config['reporting']['enabled'],
                        "report_types": self.config['reporting']['report_types'],
                        "default_report": self.config['reporting']['default_report'],
                        "report_frequency": self.config['reporting']['report_frequency'],
                        "report_time": self.config['reporting']['report_time'],
                        "distribution_channels": self.config['reporting']['distribution_channels'],
                        "recipients": self.config['reporting']['recipients']
                    },
                    "alerts": {
                        "enabled": self.config['alerts']['enabled'],
                        "alert_types": self.config['alerts']['alert_types'],
                        "alert_channels": self.config['alerts']['alert_channels'],
                        "alert_escalation": self.config['alerts']['alert_escalation'],
                        "thresholds": self.config['alerts']['thresholds']
                    },
                    "models_summary": models_summary,
                    "equipment_summary": equipment_summary
                }
            elif scope == "models":
                return {
                    "status": "success",
                    "models_summary": models_summary,
                    "models": [
                        {
                            "model_id": mid,
                            "model_name": m['model_name'],
                            "description": m['description'],
                            "equipment_domain": m['equipment_domain'],
                            "model_type": m['model_type'],
                            "parameters": m['parameters'],
                            "status": m['status'],
                            "version": m['version'],
                            "created_at": m['created_at'],
                            "updated_at": m['updated_at']
                        }
                        for mid, m in self.models.items()
                    ]
                }
            elif scope == "equipment":
                return {
                    "status": "success",
                    "equipment_summary": equipment_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting predictive maintenance status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global predictive maintenance instance
predictive_maintenance = PredictiveMaintenance()
