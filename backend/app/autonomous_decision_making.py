import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class AutonomousDecisionMaking:
    def __init__(self, config_path: str = 'autonomous_decision_config.json', rules_dir: str = 'decision_rules'):
        """
        Initialize Autonomous Decision-Making module for automated system operations
        """
        self.config_path = config_path
        self.rules_dir = rules_dir
        self.config = self.load_config()
        os.makedirs(self.rules_dir, exist_ok=True)
        logger.info("Autonomous Decision-Making module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load autonomous decision-making configuration from file or create default if not exists
        """
        default_config = {
            "decision_engine": {
                "enabled": True,
                "decision_frequency_minutes": 5,
                "confidence_threshold": 0.75,
                "max_decision_attempts": 3,
                "decision_cooldown_minutes": 10,
                "default_action": "monitor",
                "decision_modes": {
                    "performance": {
                        "mode": "automatic",
                        "triggers": ["high_cpu", "high_memory", "slow_response", "high_error_rate"],
                        "actions": ["scale_up", "scale_down", "restart_service", "optimize_query", "clear_cache"],
                        "escalation_path": ["notify_ops", "page_oncall", "emergency_shutdown"]
                    },
                    "security": {
                        "mode": "automatic",
                        "triggers": ["brute_force_attempt", "anomaly_detected", "unauthorized_access", "ddos_attack"],
                        "actions": ["block_ip", "lock_account", "increase_logging", "enforce_mfa", "temporary_shutdown"],
                        "escalation_path": ["notify_security", "page_security_team", "full_system_lockdown"]
                    },
                    "resource": {
                        "mode": "semi_automatic",
                        "triggers": ["low_disk_space", "high_bandwidth", "resource_contention", "quota_exceeded"],
                        "actions": ["allocate_more_disk", "throttle_bandwidth", "rebalance_resources", "notify_user"],
                        "escalation_path": ["notify_ops", "request_manual_intervention"]
                    },
                    "user_experience": {
                        "mode": "semi_automatic",
                        "triggers": ["low_engagement", "high_bounce_rate", "negative_feedback", "usage_spike"],
                        "actions": ["adjust_ui", "personalize_content", "send_notification", "trigger_survey"],
                        "escalation_path": ["notify_product_team", "schedule_user_research"]
                    },
                    "maintenance": {
                        "mode": "scheduled",
                        "triggers": ["predictive_failure", "scheduled_maintenance", "component_degradation"],
                        "actions": ["initiate_backup", "run_diagnostics", "replace_component", "schedule_downtime"],
                        "escalation_path": ["notify_maintenance_team", "emergency_repair"]
                    }
                }
            },
            "rules_engine": {
                "enabled": True,
                "ruleset_update_frequency_hours": 24,
                "custom_rules_allowed": True,
                "rule_priority": {
                    "security": 1,
                    "performance": 2,
                    "resource": 3,
                    "maintenance": 4,
                    "user_experience": 5
                },
                "conflict_resolution": "highest_priority",
                "default_rule_file": "default_rules.json"
            },
            "learning_integration": {
                "enabled": True,
                "ai_feedback_loop": True,
                "decision_improvement_threshold": 0.1,  # 10% improvement needed to update rules
                "historical_analysis_days": 30
            },
            "monitoring": {
                "enabled": True,
                "decision_logging": True,
                "log_directory": "decision_logs",
                "retention_days": 90,
                "alert_on_decision_failure": True,
                "alert_cooldown_minutes": 15
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded autonomous decision-making configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading decision-making config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default decision-making configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default decision-making config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved autonomous decision-making configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving decision-making config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def load_default_rules(self) -> Dict[str, Any]:
        """
        Load or create default decision rules
        """
        default_rules_file = os.path.join(self.rules_dir, self.config['rules_engine'].get('default_rule_file', 'default_rules.json'))
        default_rules = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "rules": {
                "performance": [
                    {
                        "id": "high_cpu_response",
                        "trigger": "cpu_usage_percent > 85",
                        "condition": "duration_minutes >= 5",
                        "action": "scale_up",
                        "parameters": {"scale_factor": 1.2, "max_instances": 10},
                        "priority": 2,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 15,
                            "action": "notify_ops",
                            "repeat_every_minutes": 10
                        }
                    },
                    {
                        "id": "slow_response_time",
                        "trigger": "response_time_ms > 200",
                        "condition": "duration_minutes >= 3 AND error_rate < 0.1",
                        "action": "optimize_query",
                        "parameters": {"optimization_level": "moderate"},
                        "priority": 3,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 10,
                            "action": "scale_up",
                            "repeat_every_minutes": 0  # One-time escalation
                        }
                    },
                    {
                        "id": "high_error_rate",
                        "trigger": "error_rate > 0.05",
                        "condition": "duration_minutes >= 2",
                        "action": "restart_service",
                        "parameters": {"service": "api", "restart_mode": "rolling"},
                        "priority": 1,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 5,
                            "action": "page_oncall",
                            "repeat_every_minutes": 5
                        }
                    }
                ],
                "security": [
                    {
                        "id": "brute_force_detection",
                        "trigger": "failed_login_attempts > 5",
                        "condition": "duration_minutes < 10 AND same_ip == True",
                        "action": "block_ip",
                        "parameters": {"block_duration_hours": 24, "notify_security": True},
                        "priority": 1,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 30,
                            "action": "full_system_scan",
                            "repeat_every_minutes": 0
                        }
                    },
                    {
                        "id": "unauthorized_access_attempt",
                        "trigger": "access_denied_count > 3",
                        "condition": "duration_minutes < 5 AND same_user == True",
                        "action": "lock_account",
                        "parameters": {"lock_duration_minutes": 30, "notify_user": True},
                        "priority": 2,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 10,
                            "action": "notify_security",
                            "repeat_every_minutes": 0
                        }
                    },
                    {
                        "id": "anomaly_detected",
                        "trigger": "anomaly_score > 0.9",
                        "condition": "duration_minutes >= 1",
                        "action": "increase_logging",
                        "parameters": {"log_level": "debug", "duration_hours": 24},
                        "priority": 3,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 15,
                            "action": "temporary_shutdown",
                            "repeat_every_minutes": 0
                        }
                    }
                ],
                "resource": [
                    {
                        "id": "low_disk_space",
                        "trigger": "disk_usage_percent > 90",
                        "condition": "duration_minutes >= 10",
                        "action": "allocate_more_disk",
                        "parameters": {"additional_space_gb": 10, "notify_ops": True},
                        "priority": 1,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 30,
                            "action": "emergency_cleanup",
                            "repeat_every_minutes": 0
                        }
                    },
                    {
                        "id": "quota_exceeded",
                        "trigger": "tenant_resource_usage > tenant_quota",
                        "condition": "duration_minutes >= 5",
                        "action": "notify_user",
                        "parameters": {"message": "Resource quota exceeded. Please upgrade plan or reduce usage.", "severity": "warning"},
                        "priority": 2,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 1440,  # 24 hours
                            "action": "throttle_resources",
                            "repeat_every_minutes": 0
                        }
                    }
                ],
                "maintenance": [
                    {
                        "id": "predictive_component_failure",
                        "trigger": "failure_prediction_score > 0.8",
                        "condition": "predicted_failure_window_hours < 48",
                        "action": "schedule_downtime",
                        "parameters": {"window_hours": 24, "notify_users": True, "notification_lead_time_hours": 12},
                        "priority": 1,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 720,  # 12 hours if not scheduled
                            "action": "emergency_repair",
                            "repeat_every_minutes": 60
                        }
                    },
                    {
                        "id": "component_degradation",
                        "trigger": "performance_degradation_percent > 20",
                        "condition": "duration_hours >= 6",
                        "action": "run_diagnostics",
                        "parameters": {"diagnostic_level": "full", "notify_maintenance": True},
                        "priority": 2,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 120,
                            "action": "replace_component",
                            "repeat_every_minutes": 0
                        }
                    }
                ],
                "user_experience": [
                    {
                        "id": "low_user_engagement",
                        "trigger": "engagement_score < 0.5",
                        "condition": "duration_days >= 3 AND user_segment == 'active'",
                        "action": "personalize_content",
                        "parameters": {"personalization_type": "recommendations", "test_group_percent": 20},
                        "priority": 1,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 4320,  # 3 days
                            "action": "send_notification",
                            "repeat_every_minutes": 0
                        }
                    },
                    {
                        "id": "negative_user_feedback",
                        "trigger": "feedback_sentiment_score < 0.3",
                        "condition": "feedback_count >= 5 AND duration_hours < 24",
                        "action": "trigger_survey",
                        "parameters": {"survey_type": "issue_specific", "target_users": "recent_negative_feedback"},
                        "priority": 2,
                        "enabled": True,
                        "escalation": {
                            "after_minutes": 1440,  # 24 hours
                            "action": "notify_product_team",
                            "repeat_every_minutes": 0
                        }
                    }
                ]
            }
        }

        if os.path.exists(default_rules_file):
            try:
                with open(default_rules_file, 'r') as f:
                    rules = json.load(f)
                    logger.info("Loaded default decision rules from file")
                    return rules
            except Exception as e:
                logger.error(f"Error loading default rules: {e}")
                # Save default rules to file
                try:
                    with open(default_rules_file, 'w') as f:
                        json.dump(default_rules, f, indent=2)
                    logger.info(f"Created default rules file at {default_rules_file}")
                except Exception as e2:
                    logger.error(f"Error creating default rules file: {e2}")
                return default_rules
        else:
            # Save default rules to file
            try:
                with open(default_rules_file, 'w') as f:
                    json.dump(default_rules, f, indent=2)
                logger.info(f"Created default rules file at {default_rules_file}")
            except Exception as e:
                logger.error(f"Error creating default rules file: {e}")
            return default_rules

    def evaluate_triggers(self, domain: str, current_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate triggers for a specific decision domain based on current metrics
        Args:
            domain: Decision domain to evaluate ('performance', 'security', etc.)
            current_metrics: Current system metrics and events
        Returns:
            List of triggered rules with associated actions
        """
        try:
            if domain not in self.config['decision_engine']['decision_modes']:
                return []

            domain_config = self.config['decision_engine']['decision_modes'][domain]
            if domain_config['mode'] == 'disabled':
                return []

            rules = self.load_default_rules().get('rules', {}).get(domain, [])
            triggered_rules = []

            for rule in [r for r in rules if r.get('enabled', False)]:
                # Simple trigger evaluation - in a real system, this would be a full expression parser
                trigger_active = False
                trigger = rule.get('trigger', '')

                # Parse trigger condition - very simplified parsing for simulation
                if '>' in trigger:
                    metric, threshold = trigger.split('>')
                    metric = metric.strip()
                    try:
                        threshold = float(threshold.strip())
                        if metric in current_metrics and float(current_metrics[metric]) > threshold:
                            trigger_active = True
                    except ValueError:
                        pass
                elif '<' in trigger:
                    metric, threshold = trigger.split('<')
                    metric = metric.strip()
                    try:
                        threshold = float(threshold.strip())
                        if metric in current_metrics and float(current_metrics[metric]) < threshold:
                            trigger_active = True
                    except ValueError:
                        pass

                if trigger_active:
                    # Check condition if present - simplified evaluation
                    condition = rule.get('condition', '')
                    if condition:
                        # Very basic condition check for simulation
                        if 'duration_minutes >=' in condition:
                            try:
                                duration_part = condition.split('duration_minutes >=')[1].strip()
                                duration_threshold = float(duration_part.split(' ')[0])
                                # In simulation, assume duration is met for high severity
                                if random.random() > 0.3:  # 70% chance condition met for demo
                                    trigger_active = True
                                else:
                                    trigger_active = False
                            except Exception:
                                pass  # Default to active if parsing fails

                    if trigger_active:
                        triggered_rules.append({
                            "rule_id": rule['id'],
                            "domain": domain,
                            "trigger": trigger,
                            "action": rule['action'],
                            "parameters": rule.get('parameters', {}),
                            "priority": rule.get('priority', 999),
                            "escalation": rule.get('escalation', {}),
                            "confidence": random.uniform(0.6, 0.95)  # Simulated confidence
                        })

            # Sort by priority
            triggered_rules.sort(key=lambda x: x['priority'])
            return triggered_rules
        except Exception as e:
            logger.error(f"Error evaluating triggers for {domain}: {e}")
            return []

    def make_decision(self, domain: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an autonomous decision for a specific domain based on current metrics
        Args:
            domain: Decision domain ('performance', 'security', etc.)
            current_metrics: Current system metrics and events
        Returns:
            Dictionary with decision status and actions to take
        """
        try:
            if not self.config['decision_engine']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Autonomous decision engine is disabled"
                }

            if domain not in self.config['decision_engine']['decision_modes']:
                return {
                    "status": "error",
                    "message": f"Unknown decision domain: {domain}"
                }

            domain_config = self.config['decision_engine']['decision_modes'][domain]
            mode = domain_config['mode']

            if mode == 'disabled':
                return {
                    "status": "skipped",
                    "domain": domain,
                    "message": f"Decision mode for {domain} is disabled"
                }

            # Evaluate triggers and get potential actions
            triggered_rules = self.evaluate_triggers(domain, current_metrics)
            if not triggered_rules:
                return {
                    "status": "no_action",
                    "domain": domain,
                    "message": f"No triggers activated for {domain}",
                    "metrics": current_metrics
                }

            # Select highest priority rule above confidence threshold
            confidence_threshold = self.config['decision_engine']['confidence_threshold']
            selected_rule = None
            for rule in triggered_rules:
                if rule['confidence'] >= confidence_threshold:
                    selected_rule = rule
                    break

            if not selected_rule:
                return {
                    "status": "no_action",
                    "domain": domain,
                    "message": f"No rules met confidence threshold of {confidence_threshold} for {domain}",
                    "triggered_rules": triggered_rules,
                    "confidence_threshold": confidence_threshold
                }

            # Make decision based on mode
            decision_id = f"dec_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            if mode == 'automatic':
                # In automatic mode, execute the action
                decision_result = {
                    "status": "action_scheduled",
                    "decision_id": decision_id,
                    "domain": domain,
                    "mode": mode,
                    "rule_id": selected_rule['rule_id'],
                    "action": selected_rule['action'],
                    "parameters": selected_rule['parameters'],
                    "confidence": selected_rule['confidence'],
                    "priority": selected_rule['priority'],
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Scheduled action {selected_rule['action']} for {domain} trigger {selected_rule['trigger']}",
                    "escalation": selected_rule['escalation'],
                    "metrics": current_metrics
                }
            elif mode == 'semi_automatic':
                # In semi-automatic mode, recommend action but require approval
                decision_result = {
                    "status": "action_recommended",
                    "decision_id": decision_id,
                    "domain": domain,
                    "mode": mode,
                    "rule_id": selected_rule['rule_id'],
                    "action": selected_rule['action'],
                    "parameters": selected_rule['parameters'],
                    "confidence": selected_rule['confidence'],
                    "priority": selected_rule['priority'],
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Recommended action {selected_rule['action']} for {domain} trigger {selected_rule['trigger']} - awaiting approval",
                    "escalation": selected_rule['escalation'],
                    "metrics": current_metrics
                }
            elif mode == 'scheduled':
                # In scheduled mode, schedule the action for a maintenance window
                decision_result = {
                    "status": "action_scheduled_maintenance",
                    "decision_id": decision_id,
                    "domain": domain,
                    "mode": mode,
                    "rule_id": selected_rule['rule_id'],
                    "action": selected_rule['action'],
                    "parameters": selected_rule['parameters'],
                    "confidence": selected_rule['confidence'],
                    "priority": selected_rule['priority'],
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Scheduled action {selected_rule['action']} for {domain} trigger {selected_rule['trigger']} during maintenance window",
                    "escalation": selected_rule['escalation'],
                    "metrics": current_metrics
                }
            else:
                decision_result = {
                    "status": "error",
                    "domain": domain,
                    "message": f"Unknown decision mode {mode} for domain {domain}"
                }

            # Log the decision if logging is enabled
            if self.config['monitoring']['decision_logging']:
                log_dir = self.config['monitoring'].get('log_directory', 'decision_logs')
                os.makedirs(log_dir, exist_ok=True)
                date_str = datetime.now().strftime("%Y%m%d")
                log_file = os.path.join(log_dir, f"decision_log_{date_str}.jsonl")

                log_entry = {
                    "decision_id": decision_id,
                    "timestamp": datetime.now().isoformat(),
                    "domain": domain,
                    "status": decision_result['status'],
                    "rule_id": selected_rule['rule_id'],
                    "action": selected_rule['action'],
                    "confidence": selected_rule['confidence'],
                    "priority": selected_rule['priority'],
                    "metrics": current_metrics
                }

                try:
                    with open(log_file, 'a') as f:
                        json.dump(log_entry, f)
                        f.write('\n')
                except Exception as e:
                    logger.warning(f"Error logging decision: {e}")

            logger.info(f"Made {mode} decision {decision_id} for {domain}: {decision_result['status']}")
            return decision_result
        except Exception as e:
            logger.error(f"Error making decision for {domain}: {e}")
            return {"status": "error", "message": str(e)}

    def get_decision_status(self) -> Dict[str, Any]:
        """
        Get current status of autonomous decision-making system
        """
        try:
            decision_modes = {}
            for domain, config in self.config['decision_engine']['decision_modes'].items():
                decision_modes[domain] = {
                    "mode": config['mode'],
                    "triggers": config['triggers'],
                    "actions": config['actions']
                }

            return {
                "status": "success",
                "decision_engine_enabled": self.config['decision_engine']['enabled'],
                "rules_engine_enabled": self.config['rules_engine']['enabled'],
                "learning_integration_enabled": self.config['learning_integration']['enabled'],
                "monitoring_enabled": self.config['monitoring']['enabled'],
                "decision_frequency_minutes": self.config['decision_engine']['decision_frequency_minutes'],
                "confidence_threshold": self.config['decision_engine']['confidence_threshold'],
                "decision_modes": decision_modes,
                "rule_priorities": self.config['rules_engine']['rule_priority']
            }
        except Exception as e:
            logger.error(f"Error getting decision-making status: {e}")
            return {"status": "error", "message": str(e)}

# Global autonomous decision-making instance
autonomous_decision_making = AutonomousDecisionMaking()
