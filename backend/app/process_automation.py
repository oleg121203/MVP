import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class ProcessAutomation:
    def __init__(self, automation_dir: str = 'automation_data', config_path: str = 'automation_config.json'):
        """
        Initialize AI-Driven Process Automation
        """
        self.automation_dir = automation_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.processes = {}
        self.executions = []
        os.makedirs(self.automation_dir, exist_ok=True)
        logger.info("Process Automation module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load process automation configuration from file or create default if not exists
        """
        default_config = {
            "process_automation": {
                "enabled": True,
                "automation_modes": ["scheduled", "event_driven", "on_demand", "continuous"],
                "default_mode": "scheduled",
                "execution_frequency": "daily",
                "execution_time": "02:00",
                "process_domains": [
                    "customer_support",
                    "sales_marketing",
                    "operations",
                    "finance",
                    "human_resources",
                    "it_services"
                ],
                "automation_levels": {
                    "customer_support": "event_driven",
                    "sales_marketing": "scheduled",
                    "operations": "continuous",
                    "finance": "scheduled",
                    "human_resources": "on_demand",
                    "it_services": "event_driven"
                }
            },
            "processes": {
                "enabled": True,
                "process_types": ["workflow", "decision_tree", "rule_based", "ai_driven", "custom"],
                "default_process": "workflow",
                "process_validation": True
            },
            "triggers": {
                "enabled": True,
                "trigger_types": ["time_based", "event_based", "condition_based", "manual", "system_alert"],
                "default_trigger": "time_based",
                "trigger_validation": True
            },
            "actions": {
                "enabled": True,
                "action_categories": ["notification", "data_update", "service_call", "report_generation", "escalation"],
                "default_category": "notification",
                "action_validation": True
            },
            "outcomes": {
                "enabled": True,
                "outcome_types": ["success", "partial_success", "failure", "escalated", "deferred"],
                "default_outcome": "success",
                "outcome_validation": True
            },
            "reporting": {
                "enabled": True,
                "report_types": ["summary", "detailed", "performance", "exception", "trend_analysis"],
                "default_report": "summary",
                "report_frequency": "weekly",
                "report_time": "06:00",
                "distribution_channels": ["email", "dashboard", "slack"],
                "recipients": ["operations_team", "management", "it_team"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["execution_failure", "performance_issue", "escalation_needed", "anomaly_detected"],
                "alert_channels": ["email", "dashboard", "slack", "sms"],
                "alert_escalation": True,
                "thresholds": {
                    "failure_rate": 0.1,
                    "performance_degradation": 0.2,
                    "escalation_priority": 7,
                    "anomaly_confidence": 0.8
                }
            },
            "error_handling": {
                "enabled": True,
                "error_recovery": True,
                "recovery_attempts": 3,
                "recovery_delay_seconds": 30,
                "fallback_actions": ["notify_admin", "use_alternative_process", "log_only"],
                "default_fallback": "notify_admin",
                "error_logging": "detailed"
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded process automation configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading process automation config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default process automation configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default process automation config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved process automation configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving process automation config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_process(self, process_id: str, process_name: str, description: str, process_domain: str, process_type: Optional[str] = None, steps: Optional[List[Dict[str, Any]]] = None, triggers: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Define a new automated process
        Args:
            process_id: Unique identifier for the process
            process_name: Name of the process
            description: Detailed description of the process
            process_domain: Target domain for process automation
            process_type: Type of process ('workflow', 'decision_tree', etc.)
            steps: List of steps in the process [{'step_id': str, 'action': str, 'parameters': dict, 'dependencies': list}]
            triggers: List of triggers for the process [{'trigger_type': str, 'condition': str, 'parameters': dict}]
        Returns:
            Dictionary with process definition status
        """
        try:
            if not self.config['process_automation']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Process automation is disabled"
                }

            if process_id in self.processes:
                return {
                    "status": "error",
                    "message": f"Process with ID {process_id} already exists"
                }

            if process_domain not in self.config['process_automation']['process_domains']:
                return {
                    "status": "error",
                    "message": f"Invalid process domain: {process_domain}. Must be one of {self.config['process_automation']['process_domains']}"
                }

            process_type = process_type or self.config['processes']['default_process']
            if process_type not in self.config['processes']['process_types']:
                return {
                    "status": "error",
                    "message": f"Invalid process type: {process_type}. Must be one of {self.config['processes']['process_types']}"
                }

            if triggers:
                for trigger in triggers:
                    if 'trigger_type' not in trigger or trigger['trigger_type'] not in self.config['triggers']['trigger_types']:
                        return {
                            "status": "error",
                            "message": f"Invalid trigger type. Must be one of {self.config['triggers']['trigger_types']}"
                        }

            if steps:
                for step in steps:
                    if 'action' not in step or step.get('action_category', self.config['actions']['default_category']) not in self.config['actions']['action_categories']:
                        return {
                            "status": "error",
                            "message": f"Invalid action category in step. Must be one of {self.config['actions']['action_categories']}"
                        }

            process_info = {
                "process_id": process_id,
                "process_name": process_name,
                "description": description,
                "process_domain": process_domain,
                "process_type": process_type,
                "steps": steps or [],
                "triggers": triggers or [],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "defined",
                "version": "1.0"
            }

            self.processes[process_id] = process_info

            # Save process to file
            process_file = os.path.join(self.automation_dir, f"process_{process_id}.json")
            try:
                with open(process_file, 'w') as f:
                    json.dump(process_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving process data for {process_id}: {e}")

            logger.info(f"Defined automation process {process_id} - {process_name} for {process_domain}")
            return {
                "status": "success",
                "process_id": process_id,
                "process_name": process_name,
                "process_domain": process_domain,
                "process_type": process_type,
                "steps_count": len(steps or []),
                "triggers_count": len(triggers or []),
                "created_at": process_info['created_at'],
                "version": process_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining process {process_id}: {e}")
            return {"status": "error", "message": str(e)}

    def execute_process(self, process_id: str, automation_mode: Optional[str] = None, trigger_info: Optional[Dict[str, Any]] = None, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the specified automated process
        Args:
            process_id: ID of process to execute
            automation_mode: Mode of automation ('scheduled', 'event_driven', 'on_demand', 'continuous')
            trigger_info: Information about the trigger causing execution {'trigger_type': str, 'event': str, 'timestamp': ISO_TIMESTAMP}
            context_data: Contextual data for the process execution
        Returns:
            Dictionary with process execution status
        """
        try:
            if not self.config['process_automation']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Process automation is disabled",
                    "execution_id": "N/A"
                }

            if process_id not in self.processes:
                return {
                    "status": "error",
                    "message": f"Process {process_id} not found",
                    "execution_id": "N/A"
                }

            process_info = self.processes[process_id]

            automation_mode = automation_mode or self.config['process_automation']['automation_levels'].get(process_info['process_domain'], self.config['process_automation']['default_mode'])
            if automation_mode not in self.config['process_automation']['automation_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid automation mode: {automation_mode}. Must be one of {self.config['process_automation']['automation_modes']}",
                    "execution_id": "N/A"
                }

            if trigger_info and 'trigger_type' in trigger_info:
                if trigger_info['trigger_type'] not in self.config['triggers']['trigger_types']:
                    return {
                        "status": "error",
                        "message": f"Invalid trigger type: {trigger_info['trigger_type']}. Must be one of {self.config['triggers']['trigger_types']}",
                        "execution_id": "N/A"
                    }

            execution_id = f"exec_{process_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated process execution - in real system, would run process steps
            execution_start = datetime.now()
            execution_info = {
                "execution_id": execution_id,
                "process_id": process_id,
                "process_name": process_info['process_name'],
                "process_domain": process_info['process_domain'],
                "automation_mode": automation_mode,
                "trigger_info": trigger_info or {},
                "context_data": context_data or {},
                "start_time": execution_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "executing",
                "steps_results": [],
                "outcome": None,
                "alerts": []
            }

            # Execute steps if defined, else create simulated steps
            if process_info['steps'] and len(process_info['steps']) > 0:
                steps_to_execute = process_info['steps']
            else:
                steps_to_execute = []
                default_actions = self.config['actions']['action_categories'][:3]  # Use first 3 categories
                for i, action_cat in enumerate(default_actions):
                    steps_to_execute.append({
                        "step_id": f"step_{i+1}",
                        "action": f"Perform {action_cat}",
                        "action_category": action_cat,
                        "parameters": {},
                        "dependencies": []
                    })

            # Execute each step
            for step in steps_to_execute:
                step_result = {
                    "step_id": step['step_id'],
                    "action": step['action'],
                    "action_category": step.get('action_category', self.config['actions']['default_category']),
                    "parameters": step.get('parameters', {}),
                    "start_time": datetime.now().isoformat(),
                    "end_time": None,
                    "duration_seconds": None,
                    "status": "executing",
                    "output": None,
                    "errors": []
                }

                # Simulated execution result
                step_start = datetime.now()
                success_chance = random.uniform(0, 1)
                step_end = datetime.now()

                step_result['end_time'] = step_end.isoformat()
                step_result['duration_seconds'] = (step_end - step_start).total_seconds()

                if success_chance > 0.8:
                    step_result['status'] = "failed"
                    step_result['errors'] = [f"Failed to execute {step['action']}: simulated error"]
                    step_result['output'] = None
                else:
                    step_result['status'] = "completed"
                    step_result['output'] = f"Successfully executed {step['action']}"

                execution_info['steps_results'].append(step_result)

            # Determine overall outcome
            failed_steps = [s for s in execution_info['steps_results'] if s['status'] == "failed"]
            if len(failed_steps) == len(execution_info['steps_results']):
                execution_info['outcome'] = "failure"
            elif len(failed_steps) > 0:
                execution_info['outcome'] = "partial_success"
            else:
                execution_info['outcome'] = "success"

            # Check for alerts based on thresholds
            failure_rate_threshold = self.config['alerts']['thresholds']['failure_rate']
            failure_rate = len(failed_steps) / len(execution_info['steps_results']) if execution_info['steps_results'] else 0
            if failure_rate > failure_rate_threshold:
                execution_info['alerts'].append({
                    "alert_type": "execution_failure",
                    "process_id": process_id,
                    "execution_id": execution_id,
                    "failure_rate": failure_rate,
                    "failed_steps": len(failed_steps),
                    "total_steps": len(execution_info['steps_results']),
                    "threshold": failure_rate_threshold,
                    "message": f"High failure rate in process execution: {failure_rate:.2%} of steps failed ({len(failed_steps)}/{len(execution_info['steps_results'])})",
                })

            execution_end = datetime.now()
            execution_info['end_time'] = execution_end.isoformat()
            execution_info['duration_seconds'] = (execution_end - execution_start).total_seconds()
            execution_info['status'] = "completed"

            # Save execution
            execution_file = os.path.join(self.automation_dir, f"execution_{execution_id}.json")
            try:
                with open(execution_file, 'w') as f:
                    json.dump(execution_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving execution data for {execution_id}: {e}")

            # Add to executions list
            self.executions.append({
                "execution_id": execution_id,
                "process_id": process_id,
                "process_domain": process_info['process_domain'],
                "automation_mode": automation_mode,
                "executed_at": execution_end.isoformat(),
                "status": execution_info['status'],
                "outcome": execution_info['outcome']
            })

            logger.info(f"Executed process {execution_id} for process {process_id}, outcome: {execution_info['outcome']}")
            return {
                "status": "success",
                "execution_id": execution_id,
                "process_id": process_id,
                "process_name": process_info['process_name'],
                "process_domain": process_info['process_domain'],
                "automation_mode": automation_mode,
                "trigger_info": trigger_info or {},
                "start_time": execution_info['start_time'],
                "end_time": execution_info['end_time'],
                "duration_seconds": execution_info['duration_seconds'],
                "execution_status": execution_info['status'],
                "outcome": execution_info['outcome'],
                "steps_count": len(execution_info['steps_results']),
                "successful_steps": len([s for s in execution_info['steps_results'] if s['status'] == "completed"]),
                "failed_steps": len([s for s in execution_info['steps_results'] if s['status'] == "failed"]),
                "alerts_count": len(execution_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error executing process {process_id}: {e}")
            return {"status": "error", "message": str(e), "execution_id": "N/A"}

    def get_process_automation_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current process automation status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'processes', 'executions')
        Returns:
            Dictionary with process automation status information
        """
        try:
            processes_summary = {
                "total_processes": len(self.processes),
                "processes_by_domain": {},
                "processes_by_type": {}
            }

            for p in self.processes.values():
                processes_summary['processes_by_domain'][p['process_domain']] = processes_summary['processes_by_domain'].get(p['process_domain'], 0) + 1
                processes_summary['processes_by_type'][p['process_type']] = processes_summary['processes_by_type'].get(p['process_type'], 0) + 1

            executions_summary = {
                "total_executions": len(self.executions),
                "executions_by_domain": {},
                "executions_by_outcome": {},
                "recent_executions": sorted(
                    [
                        {
                            "execution_id": e['execution_id'],
                            "process_id": e['process_id'],
                            "process_domain": e['process_domain'],
                            "automation_mode": e['automation_mode'],
                            "executed_at": e['executed_at'],
                            "status": e['status'],
                            "outcome": e['outcome']
                        }
                        for e in self.executions
                    ],
                    key=lambda x: x['executed_at'],
                    reverse=True
                )[:5]
            }

            for e in self.executions:
                executions_summary['executions_by_domain'][e['process_domain']] = executions_summary['executions_by_domain'].get(e['process_domain'], 0) + 1
                executions_summary['executions_by_outcome'][e['outcome']] = executions_summary['executions_by_outcome'].get(e['outcome'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "process_automation_enabled": self.config['process_automation']['enabled'],
                    "default_mode": self.config['process_automation']['default_mode'],
                    "process_domains": self.config['process_automation']['process_domains'],
                    "processes_summary": {
                        "total_processes": processes_summary['total_processes']
                    },
                    "executions_summary": {
                        "total_executions": executions_summary['total_executions']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "process_automation": {
                        "enabled": self.config['process_automation']['enabled'],
                        "automation_modes": self.config['process_automation']['automation_modes'],
                        "default_mode": self.config['process_automation']['default_mode'],
                        "execution_frequency": self.config['process_automation']['execution_frequency'],
                        "execution_time": self.config['process_automation']['execution_time'],
                        "process_domains": self.config['process_automation']['process_domains'],
                        "automation_levels": self.config['process_automation']['automation_levels']
                    },
                    "processes": {
                        "enabled": self.config['processes']['enabled'],
                        "process_types": self.config['processes']['process_types'],
                        "default_process": self.config['processes']['default_process'],
                        "process_validation": self.config['processes']['process_validation']
                    },
                    "triggers": {
                        "enabled": self.config['triggers']['enabled'],
                        "trigger_types": self.config['triggers']['trigger_types'],
                        "default_trigger": self.config['triggers']['default_trigger'],
                        "trigger_validation": self.config['triggers']['trigger_validation']
                    },
                    "actions": {
                        "enabled": self.config['actions']['enabled'],
                        "action_categories": self.config['actions']['action_categories'],
                        "default_category": self.config['actions']['default_category'],
                        "action_validation": self.config['actions']['action_validation']
                    },
                    "outcomes": {
                        "enabled": self.config['outcomes']['enabled'],
                        "outcome_types": self.config['outcomes']['outcome_types'],
                        "default_outcome": self.config['outcomes']['default_outcome'],
                        "outcome_validation": self.config['outcomes']['outcome_validation']
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
                    "processes_summary": processes_summary,
                    "executions_summary": executions_summary
                }
            elif scope == "processes":
                return {
                    "status": "success",
                    "processes_summary": processes_summary,
                    "processes": [
                        {
                            "process_id": pid,
                            "process_name": p['process_name'],
                            "description": p['description'],
                            "process_domain": p['process_domain'],
                            "process_type": p['process_type'],
                            "steps_count": len(p['steps']),
                            "triggers_count": len(p['triggers']),
                            "status": p['status'],
                            "version": p['version'],
                            "created_at": p['created_at'],
                            "updated_at": p['updated_at']
                        }
                        for pid, p in self.processes.items()
                    ]
                }
            elif scope == "executions":
                return {
                    "status": "success",
                    "executions_summary": executions_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting process automation status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global process automation instance
process_automation = ProcessAutomation()
