import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import numpy as np
import random

logger = logging.getLogger(__name__)

class AISecurity:
    def __init__(self, security_dir: str = 'ai_security_data', config_path: str = 'ai_security_config.json'):
        """
        Initialize AI Security module with adversarial defense mechanisms
        """
        self.security_dir = security_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.threat_logs = []
        self.defense_models = {}
        os.makedirs(self.security_dir, exist_ok=True)
        logger.info("AI Security module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load AI security configuration from file or create default if not exists
        """
        default_config = {
            "threat_detection": {
                "enabled": True,
                "detection_frequency_minutes": 5,
                "threat_types": [
                    "adversarial_attack",
                    "data_poisoning",
                    "model_inversion",
                    "membership_inference",
                    "model_stealing",
                    "bias_exploitation"
                ],
                "sensitivity_levels": ["low", "medium", "high"],
                "default_sensitivity": "medium",
                "anomaly_thresholds": {
                    "input_anomaly_score": 0.8,
                    "output_anomaly_score": 0.7,
                    "prediction_confidence_deviation": 0.5,
                    "data_distribution_shift": 0.6
                }
            },
            "defense_mechanisms": {
                "enabled": True,
                "active_defenses": [
                    "input_perturbation",
                    "output_smoothing",
                    "adversarial_training",
                    "model_regularization",
                    "data_augmentation",
                    "certified_defenses"
                ],
                "defense_strength_levels": ["low", "medium", "high"],
                "default_defense_strength": "medium",
                "defense_update_interval_days": 7
            },
            "model_monitoring": {
                "enabled": True,
                "monitoring_frequency_minutes": 10,
                "monitored_metrics": [
                    "prediction_confidence",
                    "input_distribution",
                    "output_distribution",
                    "feature_importance_stability",
                    "model_gradient_norm",
                    "inference_latency"
                ],
                "alert_thresholds": {
                    "confidence_drop_percent": 20.0,
                    "distribution_shift": 0.3,
                    "gradient_norm_spike": 2.0,
                    "latency_increase_percent": 50.0
                }
            },
            "countermeasures": {
                "enabled": True,
                "automatic_response": True,
                "response_types": [
                    "model_retraining",
                    "input_filtering",
                    "output_filtering",
                    "temporary_model_freeze",
                    "fallback_to_robust_model",
                    "alert_only"
                ],
                "default_response": "alert_only",
                "escalation_protocols": {
                    "low_threat": ["alert_only"],
                    "medium_threat": ["input_filtering", "alert_only"],
                    "high_threat": ["fallback_to_robust_model", "temporary_model_freeze", "alert_only"],
                    "critical_threat": ["temporary_model_freeze", "model_retraining", "alert_only"]
                }
            },
            "auditing": {
                "enabled": True,
                "audit_frequency_hours": 24,
                "audit_types": ["threat_log", "defense_effectiveness", "model_vulnerability", "compliance_check"],
                "retention_days": 365,
                "compliance_standards": ["gdpr", "ccpa", "hipaa", "iso_27001", "soc2"]
            },
            "reporting": {
                "enabled": True,
                "report_frequency_hours": 12,
                "report_types": ["threat_summary", "defense_status", "vulnerability_assessment", "compliance_report"],
                "distribution_channels": ["email", "dashboard"],
                "recipients": ["security_team", "ai_team", "compliance_officer", "executives"]
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded AI security configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading AI security config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default AI security configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default AI security config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved AI security configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving AI security config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def detect_threat(self, model_id: str, input_data: Dict[str, Any], output_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Detect potential adversarial threats to AI model
        Args:
            model_id: Identifier of the model being evaluated
            input_data: Input data to the model
            output_data: Output data from the model
            context: Additional context about the request (user, session, etc.)
        Returns:
            Dictionary with threat detection results
        """
        try:
            if not self.config['threat_detection']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Threat detection is disabled"
                }

            threat_type = None
            threat_level = "none"
            threat_score = 0.0
            detection_details = {}

            # Simulated threat detection logic - in real system, would use sophisticated anomaly detection
            input_anomaly_score = random.random()
            output_anomaly_score = random.random()
            confidence_deviation = random.random()
            distribution_shift = random.random()

            detection_details = {
                "input_anomaly_score": input_anomaly_score,
                "output_anomaly_score": output_anomaly_score,
                "confidence_deviation": confidence_deviation,
                "distribution_shift": distribution_shift,
                "thresholds": self.config['threat_detection']['anomaly_thresholds']
            }

            if input_anomaly_score > self.config['threat_detection']['anomaly_thresholds']['input_anomaly_score']:
                threat_type = "adversarial_attack"
                threat_score = input_anomaly_score
                threat_level = "high" if threat_score > 0.9 else "medium"
            elif output_anomaly_score > self.config['threat_detection']['anomaly_thresholds']['output_anomaly_score']:
                threat_type = "model_inversion"
                threat_score = output_anomaly_score
                threat_level = "high" if threat_score > 0.9 else "medium"
            elif confidence_deviation > self.config['threat_detection']['anomaly_thresholds']['prediction_confidence_deviation']:
                threat_type = "data_poisoning"
                threat_score = confidence_deviation
                threat_level = "medium" if threat_score > 0.7 else "low"
            elif distribution_shift > self.config['threat_detection']['anomaly_thresholds']['data_distribution_shift']:
                threat_type = "bias_exploitation"
                threat_score = distribution_shift
                threat_level = "medium" if threat_score > 0.7 else "low"

            threat_info = {
                "threat_id": f"threat_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "model_id": model_id,
                "threat_type": threat_type or "none",
                "threat_level": threat_level,
                "threat_score": threat_score,
                "detection_time": datetime.now().isoformat(),
                "detection_details": detection_details,
                "context": context or {},
                "mitigation": "none",
                "status": "detected"
            }

            if threat_type is not None:
                self.threat_logs.append(threat_info)

                # Save threat log
                threat_log_file = os.path.join(self.security_dir, f"threat_log_{datetime.now().strftime('%Y%m%d')}.jsonl")
                try:
                    with open(threat_log_file, 'a') as f:
                        json.dump(threat_info, f)
                        f.write('\n')
                except Exception as e:
                    logger.warning(f"Error saving threat log: {e}")

                # Trigger automatic countermeasures if enabled
                if self.config['countermeasures']['enabled'] and self.config['countermeasures']['automatic_response']:
                    countermeasure_result = self.trigger_countermeasure(threat_info['threat_id'], threat_level)
                    threat_info['mitigation'] = countermeasure_result.get('response_type', 'none')
                    threat_info['status'] = countermeasure_result.get('status', 'detected')

                logger.info(f"Detected {threat_level} level {threat_type} threat to model {model_id} with score {threat_score}")
            else:
                logger.debug(f"No threat detected for model {model_id}")

            return {
                "status": "success",
                "model_id": model_id,
                "threat_detected": threat_type is not None,
                "threat_type": threat_type or "none",
                "threat_level": threat_level,
                "threat_score": threat_score,
                "threat_id": threat_info['threat_id'],
                "detection_time": threat_info['detection_time'],
                "mitigation": threat_info['mitigation'],
                "details": detection_details
            }
        except Exception as e:
            logger.error(f"Error detecting threat for model {model_id}: {e}")
            return {"status": "error", "message": str(e)}

    def trigger_countermeasure(self, threat_id: str, threat_level: str) -> Dict[str, Any]:
        """
        Trigger countermeasures against detected threat
        Args:
            threat_id: Identifier of the detected threat
            threat_level: Level of the threat ('low', 'medium', 'high', 'critical')
        Returns:
            Dictionary with countermeasure results
        """
        try:
            if not self.config['countermeasures']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Countermeasures are disabled",
                    "response_type": "none"
                }

            threat_info = next((t for t in self.threat_logs if t['threat_id'] == threat_id), None)
            if threat_info is None:
                return {
                    "status": "error",
                    "message": f"Threat {threat_id} not found in logs",
                    "response_type": "none"
                }

            # Determine appropriate response based on threat level
            escalation_map = {
                "low": "low_threat",
                "medium": "medium_threat",
                "high": "high_threat",
                "critical": "critical_threat"
            }
            threat_category = escalation_map.get(threat_level, "low_threat")
            possible_responses = self.config['countermeasures']['escalation_protocols'].get(
                threat_category, self.config['countermeasures']['escalation_protocols']['low_threat']
            )

            # Select the most appropriate response - for simulation, just pick first non-alert response if available
            response_type = self.config['countermeasures']['default_response']
            for resp in possible_responses:
                if resp != "alert_only":
                    response_type = resp
                    break

            # Execute the countermeasure - simulated
            response_details = {
                "initiated_at": datetime.now().isoformat(),
                "response_type": response_type,
                "effectiveness": random.uniform(0.5, 1.0),
                "side_effects": "none",
                "recovery_time_seconds": random.randint(1, 300)
            }

            # Update threat log
            threat_info['mitigation'] = response_type
            threat_info['status'] = "mitigated" if response_details['effectiveness'] > 0.7 else "partially_mitigated"
            threat_info['mitigation_details'] = response_details

            # Save updated threat log
            threat_log_file = os.path.join(self.security_dir, f"threat_log_{datetime.now().strftime('%Y%m%d')}.jsonl")
            try:
                with open(threat_log_file, 'a') as f:
                    json.dump(threat_info, f)
                    f.write('\n')
            except Exception as e:
                logger.warning(f"Error saving updated threat log: {e}")

            logger.info(f"Triggered {response_type} countermeasure for threat {threat_id} at level {threat_level}")
            return {
                "status": "success",
                "threat_id": threat_id,
                "threat_type": threat_info['threat_type'],
                "threat_level": threat_level,
                "response_type": response_type,
                "initiated_at": response_details['initiated_at'],
                "effectiveness": response_details['effectiveness'],
                "details": response_details
            }
        except Exception as e:
            logger.error(f"Error triggering countermeasure for threat {threat_id}: {e}")
            return {"status": "error", "message": str(e), "response_type": "none"}

    def update_defense_model(self, defense_type: str, strength: Optional[str] = None) -> Dict[str, Any]:
        """
        Update or retrain defense model
        Args:
            defense_type: Type of defense to update ('input_perturbation', 'output_smoothing', 'adversarial_training', etc.)
            strength: Strength level of the defense ('low', 'medium', 'high')
        Returns:
            Dictionary with update status
        """
        try:
            if not self.config['defense_mechanisms']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Defense mechanisms are disabled"
                }

            if defense_type not in self.config['defense_mechanisms']['active_defenses']:
                return {
                    "status": "error",
                    "message": f"Unknown defense type: {defense_type}. Must be one of {self.config['defense_mechanisms']['active_defenses']}"
                }

            strength = strength or self.config['defense_mechanisms']['default_defense_strength']
            if strength not in self.config['defense_mechanisms']['defense_strength_levels']:
                return {
                    "status": "error",
                    "message": f"Invalid defense strength: {strength}. Must be one of {self.config['defense_mechanisms']['defense_strength_levels']}"
                }

            # Simulated defense model update - in real system, would retrain or adjust defense parameters
            update_result = {
                "defense_type": defense_type,
                "strength": strength,
                "updated_at": datetime.now().isoformat(),
                "update_duration_seconds": random.randint(10, 300),
                "performance_impact_percent": random.uniform(0.5, 5.0),
                "defense_effectiveness": random.uniform(0.6, 0.95),
                "version": f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }

            # Update defense model registry
            self.defense_models[defense_type] = update_result

            # Save defense model info
            defense_file = os.path.join(self.security_dir, f"defense_{defense_type}.json")
            try:
                with open(defense_file, 'w') as f:
                    json.dump(update_result, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving defense model data for {defense_type}: {e}")

            logger.info(f"Updated defense model {defense_type} to strength {strength}")
            return {
                "status": "success",
                "defense_type": defense_type,
                "strength": strength,
                "version": update_result['version'],
                "updated_at": update_result['updated_at'],
                "effectiveness": update_result['defense_effectiveness'],
                "performance_impact_percent": update_result['performance_impact_percent']
            }
        except Exception as e:
            logger.error(f"Error updating defense model {defense_type}: {e}")
            return {"status": "error", "message": str(e)}

    def get_security_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current AI security status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'threats_only', 'defenses_only')
        Returns:
            Dictionary with security status information
        """
        try:
            threat_summary = {
                "total_threats": len(self.threat_logs),
                "threats_by_type": {},
                "threats_by_level": {"low": 0, "medium": 0, "high": 0, "critical": 0},
                "threats_by_status": {"detected": 0, "mitigated": 0, "partially_mitigated": 0, "unresolved": 0},
                "recent_threats": []
            }

            for threat in self.threat_logs:
                threat_type = threat['threat_type']
                threat_level = threat['threat_level']
                threat_status = threat['status']

                threat_summary['threats_by_type'][threat_type] = threat_summary['threats_by_type'].get(threat_type, 0) + 1
                if threat_level in threat_summary['threats_by_level']:
                    threat_summary['threats_by_level'][threat_level] += 1
                if threat_status in threat_summary['threats_by_status']:
                    threat_summary['threats_by_status'][threat_status] += 1

            # Get recent threats (last 5, sorted by time descending)
            sorted_threats = sorted(self.threat_logs, key=lambda x: x['detection_time'], reverse=True)
            threat_summary['recent_threats'] = [
                {
                    "threat_id": t['threat_id'],
                    "threat_type": t['threat_type'],
                    "threat_level": t['threat_level'],
                    "detection_time": t['detection_time'],
                    "status": t['status'],
                    "mitigation": t.get('mitigation', 'none')
                }
                for t in sorted_threats[:5]
            ]

            defense_summary = {
                "active_defenses": list(self.defense_models.keys()),
                "defense_status": [
                    {
                        "defense_type": dtype,
                        "strength": dmodel['strength'],
                        "version": dmodel['version'],
                        "updated_at": dmodel['updated_at'],
                        "effectiveness": dmodel['defense_effectiveness'],
                        "performance_impact_percent": dmodel['performance_impact_percent']
                    }
                    for dtype, dmodel in self.defense_models.items()
                ]
            }

            if scope == "summary":
                return {
                    "status": "success",
                    "threat_detection_enabled": self.config['threat_detection']['enabled'],
                    "defense_mechanisms_enabled": self.config['defense_mechanisms']['enabled'],
                    "model_monitoring_enabled": self.config['model_monitoring']['enabled'],
                    "countermeasures_enabled": self.config['countermeasures']['enabled'],
                    "automatic_response": self.config['countermeasures']['automatic_response'],
                    "threat_summary": {
                        "total_threats": threat_summary['total_threats'],
                        "threats_by_level": threat_summary['threats_by_level'],
                        "threats_by_status": threat_summary['threats_by_status']
                    },
                    "defense_summary": {
                        "active_defense_count": len(defense_summary['active_defenses'])
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "threat_detection": {
                        "enabled": self.config['threat_detection']['enabled'],
                        "frequency_minutes": self.config['threat_detection']['detection_frequency_minutes'],
                        "sensitivity": self.config['threat_detection']['default_sensitivity'],
                        "threat_types": self.config['threat_detection']['threat_types'],
                        "anomaly_thresholds": self.config['threat_detection']['anomaly_thresholds']
                    },
                    "defense_mechanisms": {
                        "enabled": self.config['defense_mechanisms']['enabled'],
                        "active_defenses": self.config['defense_mechanisms']['active_defenses'],
                        "default_strength": self.config['defense_mechanisms']['default_defense_strength'],
                        "update_interval_days": self.config['defense_mechanisms']['defense_update_interval_days'],
                        "defense_status": defense_summary['defense_status']
                    },
                    "model_monitoring": {
                        "enabled": self.config['model_monitoring']['enabled'],
                        "frequency_minutes": self.config['model_monitoring']['monitoring_frequency_minutes'],
                        "monitored_metrics": self.config['model_monitoring']['monitored_metrics'],
                        "alert_thresholds": self.config['model_monitoring']['alert_thresholds']
                    },
                    "countermeasures": {
                        "enabled": self.config['countermeasures']['enabled'],
                        "automatic_response": self.config['countermeasures']['automatic_response'],
                        "response_types": self.config['countermeasures']['response_types'],
                        "default_response": self.config['countermeasures']['default_response'],
                        "escalation_protocols": self.config['countermeasures']['escalation_protocols']
                    },
                    "threat_summary": threat_summary
                }
            elif scope == "threats_only":
                return {
                    "status": "success",
                    "threat_summary": threat_summary
                }
            elif scope == "defenses_only":
                return {
                    "status": "success",
                    "defense_summary": defense_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting AI security status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global AI security instance
ai_security = AISecurity()
