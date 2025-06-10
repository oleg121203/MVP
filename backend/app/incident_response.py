import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class IncidentResponse:
    def __init__(self, incident_dir: str = 'incident_data', config_path: str = 'incident_config.json'):
        """
        Initialize AI-Driven Incident Response
        """
        self.incident_dir = incident_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.incidents = []
        os.makedirs(self.incident_dir, exist_ok=True)
        logger.info("Incident Response module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load incident response configuration from file or create default if not exists
        """
        default_config = {
            "incident_response": {
                "enabled": True,
                "response_modes": ["automated", "assisted", "manual", "hybrid"],
                "default_mode": "automated",
                "detection_frequency": "continuous",
                "detection_time": "00:00",
                "incident_domains": [
                    "system_operations",
                    "security",
                    "customer_service",
                    "financial",
                    "compliance",
                    "employee_relations"
                ],
                "response_levels": {
                    "system_operations": "automated",
                    "security": "hybrid",
                    "customer_service": "assisted",
                    "financial": "manual",
                    "compliance": "hybrid",
                    "employee_relations": "assisted"
                }
            },
            "models": {
                "enabled": True,
                "model_types": ["rule_based", "machine_learning", "statistical", "hybrid", "custom"],
                "default_model": "rule_based",
                "model_validation": True
            },
            "detection": {
                "enabled": True,
                "detection_types": ["anomaly_detection", "signature_based", "behavioral", "predictive", "contextual"],
                "default_detection": "anomaly_detection",
                "detection_validation": True
            },
            "classification": {
                "enabled": True,
                "severity_levels": ["low", "medium", "high", "critical"],
                "default_severity": "medium",
                "impact_areas": ["operations", "financial", "reputation", "compliance", "safety"],
                "default_impact": "operations",
                "urgency_levels": ["low", "medium", "high", "immediate"],
                "default_urgency": "medium"
            },
            "response": {
                "enabled": True,
                "response_strategies": ["containment", "mitigation", "recovery", "communication", "prevention"],
                "default_strategy": "containment",
                "response_validation": True
            },
            "reporting": {
                "enabled": True,
                "report_types": ["incident_summary", "detailed_analysis", "response_effectiveness", "trend_analysis", "compliance_report"],
                "default_report": "incident_summary",
                "report_frequency": "as_needed",
                "report_time": "08:00",
                "distribution_channels": ["email", "dashboard", "slack"],
                "recipients": ["incident_response_team", "management", "affected_departments", "compliance_team"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["new_incident", "severity_escalation", "response_delay", "recurring_incident", "compliance_violation"],
                "alert_channels": ["email", "dashboard", "slack", "sms", "phone"],
                "alert_escalation": True,
                "thresholds": {
                    "severity_threshold": "high",
                    "response_time_minutes": 30,
                    "recurrence_count": 3,
                    "impact_threshold": 0.5
                }
            },
            "error_handling": {
                "enabled": True,
                "error_recovery": True,
                "recovery_attempts": 3,
                "recovery_delay_seconds": 30,
                "fallback_actions": ["notify_admin", "use_manual_response", "log_only"],
                "default_fallback": "notify_admin",
                "error_logging": "detailed"
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded incident response configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading incident response config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default incident response configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default incident response config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved incident response configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving incident response config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_model(self, model_id: str, model_name: str, description: str, incident_domain: str, model_type: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Define a new incident response model
        Args:
            model_id: Unique identifier for the model
            model_name: Name of the model
            description: Detailed description of the model
            incident_domain: Target domain for incident response
            model_type: Type of model ('rule_based', 'machine_learning', etc.)
            parameters: Model parameters and hyperparameters
        Returns:
            Dictionary with model definition status
        """
        try:
            if not self.config['incident_response']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Incident response is disabled"
                }

            if model_id in self.models:
                return {
                    "status": "error",
                    "message": f"Model with ID {model_id} already exists"
                }

            if incident_domain not in self.config['incident_response']['incident_domains']:
                return {
                    "status": "error",
                    "message": f"Invalid incident domain: {incident_domain}. Must be one of {self.config['incident_response']['incident_domains']}"
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
                "incident_domain": incident_domain,
                "model_type": model_type,
                "parameters": parameters or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "defined",
                "version": "1.0"
            }

            self.models[model_id] = model_info

            # Save model to file
            model_file = os.path.join(self.incident_dir, f"model_{model_id}.json")
            try:
                with open(model_file, 'w') as f:
                    json.dump(model_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving model data for {model_id}: {e}")

            logger.info(f"Defined incident response model {model_id} - {model_name} for {incident_domain}")
            return {
                "status": "success",
                "model_id": model_id,
                "model_name": model_name,
                "incident_domain": incident_domain,
                "model_type": model_type,
                "parameters": parameters or {},
                "created_at": model_info['created_at'],
                "version": model_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining model {model_id}: {e}")
            return {"status": "error", "message": str(e)}

    def detect_incident(self, model_id: str, detection_type: Optional[str] = None, data_points: Optional[List[Dict[str, Any]]] = None, time_window: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect incidents using the specified model
        Args:
            model_id: ID of model to use for incident detection
            detection_type: Type of detection ('anomaly_detection', 'signature_based', etc.)
            data_points: List of data points for analysis [{'metric': str, 'value': float, 'timestamp': str, 'attributes': dict}]
            time_window: Time window for analysis (e.g., '1h', '1d', '1w')
        Returns:
            Dictionary with incident detection status
        """
        try:
            if not self.config['incident_response']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Incident response is disabled",
                    "detection_id": "N/A"
                }

            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} not found",
                    "detection_id": "N/A"
                }

            model_info = self.models[model_id]

            detection_type = detection_type or self.config['detection']['default_detection']
            if detection_type not in self.config['detection']['detection_types']:
                return {
                    "status": "error",
                    "message": f"Invalid detection type: {detection_type}. Must be one of {self.config['detection']['detection_types']}",
                    "detection_id": "N/A"
                }

            detection_id = f"det_{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated incident detection - in real system, would run analysis
            detection_start = datetime.now()
            detection_info = {
                "detection_id": detection_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "incident_domain": model_info['incident_domain'],
                "detection_type": detection_type,
                "data_points": data_points or [],
                "time_window": time_window or "default",
                "start_time": detection_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "detecting",
                "potential_incidents": [],
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
                            "source": random.choice(["system", "user", "sensor", "log", "transaction"]),
                            "location": random.choice(["east", "west", "north", "south", "central"])
                        }
                    })

            # Analyze data points for potential incidents
            for i, dp in enumerate(data_to_analyze):
                if random.random() < 0.2:  # 20% chance of detecting a potential incident
                    severity = random.choice(self.config['classification']['severity_levels'])
                    impact_area = random.choice(self.config['classification']['impact_areas'])
                    urgency = random.choice(self.config['classification']['urgency_levels'])
                    confidence = random.uniform(0.5, 0.95)
                    
                    potential_incident = {
                        "incident_id": f"inc_{detection_id}_{i}",
                        "metric": dp['metric'],
                        "value": dp['value'],
                        "timestamp": dp.get('timestamp', datetime.now().isoformat()),
                        "severity": severity,
                        "impact_area": impact_area,
                        "urgency": urgency,
                        "confidence": confidence,
                        "description": f"Potential {severity} incident in {impact_area} detected with {confidence:.2%} confidence",
                        "attributes": dp.get('attributes', {}),
                        "status": "detected"
                    }
                    detection_info['potential_incidents'].append(potential_incident)

            # Check for alerts based on thresholds
            severity_threshold = self.config['alerts']['thresholds']['severity_threshold']
            high_severity_incidents = [inc for inc in detection_info['potential_incidents'] 
                                     if inc['severity'] in (self.config['classification']['severity_levels'][self.config['classification']['severity_levels'].index(severity_threshold):])]
            if high_severity_incidents:
                detection_info['alerts'].append({
                    "alert_type": "new_incident",
                    "incident_domain": model_info['incident_domain'],
                    "incident_count": len(high_severity_incidents),
                    "severity_threshold": severity_threshold,
                    "message": f"High severity incidents detected in {model_info['incident_domain']}: {len(high_severity_incidents)} incidents"
                })

            detection_end = datetime.now()
            detection_info['end_time'] = detection_end.isoformat()
            detection_info['duration_seconds'] = (detection_end - detection_start).total_seconds()
            detection_info['status'] = "completed"

            # Save detection results
            detection_file = os.path.join(self.incident_dir, f"detection_{detection_id}.json")
            try:
                with open(detection_file, 'w') as f:
                    json.dump(detection_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving detection data for {detection_id}: {e}")

            # Add potential incidents to incidents list if any
            for incident in detection_info['potential_incidents']:
                self.incidents.append({
                    "incident_id": incident['incident_id'],
                    "model_id": model_id,
                    "incident_domain": model_info['incident_domain'],
                    "severity": incident['severity'],
                    "impact_area": incident['impact_area'],
                    "urgency": incident['urgency'],
                    "detected_at": incident['timestamp'],
                    "status": "detected"
                })

            logger.info(f"Completed incident detection {detection_id} using model {model_id}, found {len(detection_info['potential_incidents'])} potential incidents")
            return {
                "status": "success",
                "detection_id": detection_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "incident_domain": model_info['incident_domain'],
                "detection_type": detection_type,
                "data_points_count": len(data_to_analyze),
                "start_time": detection_info['start_time'],
                "end_time": detection_info['end_time'],
                "duration_seconds": detection_info['duration_seconds'],
                "detection_status": detection_info['status'],
                "potential_incidents_count": len(detection_info['potential_incidents']),
                "alerts_count": len(detection_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error detecting incidents using model {model_id}: {e}")
            return {"status": "error", "message": str(e), "detection_id": "N/A"}

    def respond_to_incident(self, incident_id: str, response_mode: Optional[str] = None, response_strategies: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Respond to a detected incident
        Args:
            incident_id: ID of the incident to respond to
            response_mode: Mode of response ('automated', 'assisted', 'manual', 'hybrid')
            response_strategies: List of strategies to apply ('containment', 'mitigation', etc.)
        Returns:
            Dictionary with incident response status
        """
        try:
            if not self.config['incident_response']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Incident response is disabled",
                    "response_id": "N/A"
                }

            target_incident = None
            for inc in self.incidents:
                if inc['incident_id'] == incident_id:
                    target_incident = inc
                    break

            if target_incident is None:
                return {
                    "status": "error",
                    "message": f"Incident {incident_id} not found",
                    "response_id": "N/A"
                }

            model_id = target_incident['model_id']
            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} for incident {incident_id} not found",
                    "response_id": "N/A"
                }

            model_info = self.models[model_id]

            response_mode = response_mode or self.config['incident_response']['response_levels'].get(model_info['incident_domain'], self.config['incident_response']['default_mode'])
            if response_mode not in self.config['incident_response']['response_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid response mode: {response_mode}. Must be one of {self.config['incident_response']['response_modes']}",
                    "response_id": "N/A"
                }

            if response_strategies:
                for strategy in response_strategies:
                    if strategy not in self.config['response']['response_strategies']:
                        return {
                            "status": "error",
                            "message": f"Invalid response strategy: {strategy}. Must be one of {self.config['response']['response_strategies']}",
                            "response_id": "N/A"
                        }
            else:
                response_strategies = [self.config['response']['default_strategy']]

            response_id = f"resp_{incident_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated incident response - in real system, would execute response actions
            response_start = datetime.now()
            response_info = {
                "response_id": response_id,
                "incident_id": incident_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "incident_domain": model_info['incident_domain'],
                "response_mode": response_mode,
                "response_strategies": response_strategies,
                "start_time": response_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "responding",
                "response_actions": [],
                "effectiveness": None,
                "alerts": []
            }

            # Generate simulated response actions based on strategies
            for strategy in response_strategies:
                action_count = random.randint(1, 3)
                for i in range(action_count):
                    action = {
                        "strategy": strategy,
                        "action_id": f"act_{strategy}_{i+1}",
                        "description": f"Execute {strategy} action {i+1} for incident {incident_id}",
                        "status": random.choice(["planned", "in_progress", "completed", "failed"]),
                        "effectiveness": random.uniform(0.5, 1.0) if random.random() < 0.8 else random.uniform(0.0, 0.5),
                        "timestamp": datetime.now().isoformat(),
                        "details": {
                            "target_component": random.choice(["system", "process", "user", "data", "access"]),
                            "action_type": random.choice(["update", "restart", "rollback", "notify", "isolate", "patch", "reconfigure"])
                        }
                    }
                    response_info['response_actions'].append(action)

            # Calculate overall effectiveness based on actions
            completed_actions = [a for a in response_info['response_actions'] if a['status'] == "completed"]
            if completed_actions:
                response_info['effectiveness'] = sum(a['effectiveness'] for a in completed_actions) / len(completed_actions)
            else:
                response_info['effectiveness'] = 0.0

            # Check for alerts based on thresholds
            response_time_threshold = self.config['alerts']['thresholds']['response_time_minutes']
            incident_age_minutes = (datetime.now() - datetime.fromisoformat(target_incident['detected_at'])).total_seconds() / 60.0
            if incident_age_minutes > response_time_threshold and target_incident['status'] not in ["resolved", "closed"]:
                response_info['alerts'].append({
                    "alert_type": "response_delay",
                    "incident_id": incident_id,
                    "incident_domain": model_info['incident_domain'],
                    "delay_minutes": incident_age_minutes,
                    "threshold_minutes": response_time_threshold,
                    "message": f"Response delay for incident {incident_id} in {model_info['incident_domain']}: {incident_age_minutes:.1f} minutes"
                })

            severity_threshold = self.config['alerts']['thresholds']['severity_threshold']
            if target_incident['severity'] in self.config['classification']['severity_levels'][self.config['classification']['severity_levels'].index(severity_threshold):] and target_incident['status'] not in ["resolved", "closed"]:
                response_info['alerts'].append({
                    "alert_type": "severity_escalation",
                    "incident_id": incident_id,
                    "incident_domain": model_info['incident_domain'],
                    "severity": target_incident['severity'],
                    "threshold": severity_threshold,
                    "message": f"High severity incident {incident_id} in {model_info['incident_domain']}: severity {target_incident['severity']}"
                })

            response_end = datetime.now()
            response_info['end_time'] = response_end.isoformat()
            response_info['duration_seconds'] = (response_end - response_start).total_seconds()
            response_info['status'] = "completed"

            # Update incident status based on response effectiveness
            if response_info['effectiveness'] > 0.8:
                target_incident['status'] = "resolved"
            elif response_info['effectiveness'] > 0.4:
                target_incident['status'] = "partially_resolved"
            else:
                target_incident['status'] = "unresolved"

            target_incident['last_response_at'] = response_end.isoformat()
            target_incident['last_response_id'] = response_id

            # Save response data
            response_file = os.path.join(self.incident_dir, f"response_{response_id}.json")
            try:
                with open(response_file, 'w') as f:
                    json.dump(response_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving response data for {response_id}: {e}")

            # Save updated incidents list
            incidents_file = os.path.join(self.incident_dir, "incidents.json")
            try:
                with open(incidents_file, 'w') as f:
                    json.dump(self.incidents, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving incidents list: {e}")

            logger.info(f"Completed incident response {response_id} for incident {incident_id}, effectiveness: {response_info['effectiveness']:.2%}")
            return {
                "status": "success",
                "response_id": response_id,
                "incident_id": incident_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "incident_domain": model_info['incident_domain'],
                "response_mode": response_mode,
                "strategies_count": len(response_strategies),
                "actions_count": len(response_info['response_actions']),
                "start_time": response_info['start_time'],
                "end_time": response_info['end_time'],
                "duration_seconds": response_info['duration_seconds'],
                "response_status": response_info['status'],
                "effectiveness": response_info['effectiveness'],
                "incident_status": target_incident['status'],
                "alerts_count": len(response_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error responding to incident {incident_id}: {e}")
            return {"status": "error", "message": str(e), "response_id": "N/A"}

    def get_incident_response_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current incident response status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'models', 'incidents')
        Returns:
            Dictionary with incident response status information
        """
        try:
            models_summary = {
                "total_models": len(self.models),
                "models_by_domain": {},
                "models_by_type": {}
            }

            for m in self.models.values():
                models_summary['models_by_domain'][m['incident_domain']] = models_summary['models_by_domain'].get(m['incident_domain'], 0) + 1
                models_summary['models_by_type'][m['model_type']] = models_summary['models_by_type'].get(m['model_type'], 0) + 1

            incidents_summary = {
                "total_incidents": len(self.incidents),
                "incidents_by_domain": {},
                "incidents_by_status": {},
                "recent_incidents": sorted(
                    [
                        {
                            "incident_id": inc['incident_id'],
                            "model_id": inc['model_id'],
                            "incident_domain": inc['incident_domain'],
                            "severity": inc.get('severity', 'N/A'),
                            "impact_area": inc.get('impact_area', 'N/A'),
                            "urgency": inc.get('urgency', 'N/A'),
                            "detected_at": inc['detected_at'],
                            "status": inc['status']
                        }
                        for inc in self.incidents
                    ],
                    key=lambda x: x['detected_at'],
                    reverse=True
                )[:5]
            }

            for inc in self.incidents:
                incidents_summary['incidents_by_domain'][inc['incident_domain']] = incidents_summary['incidents_by_domain'].get(inc['incident_domain'], 0) + 1
                incidents_summary['incidents_by_status'][inc['status']] = incidents_summary['incidents_by_status'].get(inc['status'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "incident_response_enabled": self.config['incident_response']['enabled'],
                    "default_mode": self.config['incident_response']['default_mode'],
                    "incident_domains": self.config['incident_response']['incident_domains'],
                    "models_summary": {
                        "total_models": models_summary['total_models']
                    },
                    "incidents_summary": {
                        "total_incidents": incidents_summary['total_incidents']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "incident_response": {
                        "enabled": self.config['incident_response']['enabled'],
                        "response_modes": self.config['incident_response']['response_modes'],
                        "default_mode": self.config['incident_response']['default_mode'],
                        "detection_frequency": self.config['incident_response']['detection_frequency'],
                        "detection_time": self.config['incident_response']['detection_time'],
                        "incident_domains": self.config['incident_response']['incident_domains'],
                        "response_levels": self.config['incident_response']['response_levels']
                    },
                    "models": {
                        "enabled": self.config['models']['enabled'],
                        "model_types": self.config['models']['model_types'],
                        "default_model": self.config['models']['default_model'],
                        "model_validation": self.config['models']['model_validation']
                    },
                    "detection": {
                        "enabled": self.config['detection']['enabled'],
                        "detection_types": self.config['detection']['detection_types'],
                        "default_detection": self.config['detection']['default_detection'],
                        "detection_validation": self.config['detection']['detection_validation']
                    },
                    "classification": {
                        "enabled": self.config['classification']['enabled'],
                        "severity_levels": self.config['classification']['severity_levels'],
                        "default_severity": self.config['classification']['default_severity'],
                        "impact_areas": self.config['classification']['impact_areas'],
                        "default_impact": self.config['classification']['default_impact'],
                        "urgency_levels": self.config['classification']['urgency_levels'],
                        "default_urgency": self.config['classification']['default_urgency']
                    },
                    "response": {
                        "enabled": self.config['response']['enabled'],
                        "response_strategies": self.config['response']['response_strategies'],
                        "default_strategy": self.config['response']['default_strategy'],
                        "response_validation": self.config['response']['response_validation']
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
                    "incidents_summary": incidents_summary
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
                            "incident_domain": m['incident_domain'],
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
            elif scope == "incidents":
                return {
                    "status": "success",
                    "incidents_summary": incidents_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting incident response status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global incident response instance
incident_response = IncidentResponse()
