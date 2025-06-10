import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class EnterpriseIntegration:
    def __init__(self, integration_dir: str = 'integration_data', config_path: str = 'integration_config.json'):
        """
        Initialize Enterprise Integration with AI-Driven Workflows
        """
        self.integration_dir = integration_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.workflows = {}
        self.integration_logs = []
        os.makedirs(self.integration_dir, exist_ok=True)
        logger.info("Enterprise Integration module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load integration configuration from file or create default if not exists
        """
        default_config = {
            "integration": {
                "enabled": True,
                "integration_modes": ["real_time", "batch", "hybrid"],
                "default_mode": "real_time",
                "integration_frequency": "hourly",
                "integration_time": "00:00",
                "target_systems": [
                    "erp",
                    "crm",
                    "hris",
                    "finance",
                    "supply_chain"
                ],
                "integration_levels": {
                    "erp": "real_time",
                    "crm": "real_time",
                    "hris": "batch",
                    "finance": "hybrid",
                    "supply_chain": "batch"
                }
            },
            "data_mapping": {
                "enabled": True,
                "mapping_types": ["direct", "transformed", "aggregated", "custom"],
                "default_mapping": "direct",
                "mapping_validation": True
            },
            "workflows": {
                "enabled": True,
                "workflow_types": ["data_sync", "process_automation", "event_driven", "user_triggered"],
                "default_workflow": "data_sync",
                "workflow_validation": True
            },
            "connectors": {
                "enabled": True,
                "connector_types": ["api", "database", "file", "message_queue", "custom"],
                "default_connector": "api",
                "connector_validation": True,
                "connector_retries": 3,
                "retry_delay_seconds": 10,
                "connector_timeout_seconds": 300
            },
            "actions": {
                "enabled": True,
                "action_types": ["data_transfer", "process_initiation", "notification", "data_update", "system_sync"],
                "action_validation": True,
                "action_retries": 3,
                "retry_delay_seconds": 10,
                "action_timeout_seconds": 300
            },
            "monitoring": {
                "enabled": True,
                "metrics": [
                    "integration_time",
                    "success_rate",
                    "error_rate",
                    "data_volume",
                    "system_coverage"
                ],
                "alert_thresholds": {
                    "integration_time": 300,
                    "success_rate": 95,
                    "error_rate": 5,
                    "data_volume": 1000000,
                    "system_coverage": 90
                },
                "alert_channels": ["email", "dashboard", "slack"],
                "alert_escalation": True
            },
            "error_handling": {
                "enabled": True,
                "error_recovery": True,
                "recovery_attempts": 3,
                "recovery_delay_seconds": 30,
                "fallback_actions": ["notify_admin", "switch_to_manual", "log_only"],
                "default_fallback": "notify_admin",
                "error_logging": "detailed"
            },
            "reporting": {
                "enabled": True,
                "report_types": ["summary", "detailed", "exception", "performance"],
                "report_frequency": "daily",
                "report_time": "06:00",
                "distribution_channels": ["email", "dashboard"],
                "recipients": ["operations_team", "it_admin", "executives"]
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded integration configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading integration config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default integration configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default integration config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved integration configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving integration config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_workflow(self, workflow_id: str, workflow_name: str, description: str, target_system: str, workflow_type: Optional[str] = None, integration_mode: Optional[str] = None, connectors: Optional[List[str]] = None, actions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Define a new integration workflow
        Args:
            workflow_id: Unique identifier for the workflow
            workflow_name: Name of the workflow
            description: Detailed description of the workflow
            target_system: Target enterprise system for integration
            workflow_type: Type of workflow ('data_sync', 'process_automation', etc.)
            integration_mode: Mode of integration ('real_time', 'batch', 'hybrid')
            connectors: Connector types for system integration
            actions: Action types for workflow execution
        Returns:
            Dictionary with workflow definition status
        """
        try:
            if not self.config['integration']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Integration is disabled"
                }

            if workflow_id in self.workflows:
                return {
                    "status": "error",
                    "message": f"Workflow with ID {workflow_id} already exists"
                }

            if target_system not in self.config['integration']['target_systems']:
                return {
                    "status": "error",
                    "message": f"Invalid target system: {target_system}. Must be one of {self.config['integration']['target_systems']}"
                }

            workflow_type = workflow_type or self.config['workflows']['default_workflow']
            if workflow_type not in self.config['workflows']['workflow_types']:
                return {
                    "status": "error",
                    "message": f"Invalid workflow type: {workflow_type}. Must be one of {self.config['workflows']['workflow_types']}"
                }

            integration_mode = integration_mode or self.config['integration']['integration_levels'].get(target_system, self.config['integration']['default_mode'])
            if integration_mode not in self.config['integration']['integration_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid integration mode: {integration_mode}. Must be one of {self.config['integration']['integration_modes']}"
                }

            connectors = connectors or [self.config['connectors']['default_connector']]
            invalid_connectors = [c for c in connectors if c not in self.config['connectors']['connector_types']]
            if invalid_connectors:
                return {
                    "status": "error",
                    "message": f"Invalid connectors: {invalid_connectors}. Must be subset of {self.config['connectors']['connector_types']}"
                }

            actions = actions or []
            invalid_actions = [a for a in actions if a not in self.config['actions']['action_types']]
            if invalid_actions:
                return {
                    "status": "error",
                    "message": f"Invalid actions: {invalid_actions}. Must be subset of {self.config['actions']['action_types']}"
                }

            workflow_info = {
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "description": description,
                "target_system": target_system,
                "workflow_type": workflow_type,
                "integration_mode": integration_mode,
                "connectors": connectors,
                "actions": actions,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "defined",
                "version": "1.0"
            }

            self.workflows[workflow_id] = workflow_info

            # Save workflow to file
            workflow_file = os.path.join(self.integration_dir, f"workflow_{workflow_id}.json")
            try:
                with open(workflow_file, 'w') as f:
                    json.dump(workflow_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving workflow data for {workflow_id}: {e}")

            logger.info(f"Defined integration workflow {workflow_id} - {workflow_name} for {target_system}")
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "workflow_name": workflow_name,
                "target_system": target_system,
                "workflow_type": workflow_type,
                "integration_mode": integration_mode,
                "connectors": connectors,
                "actions": actions,
                "created_at": workflow_info['created_at'],
                "version": workflow_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining workflow {workflow_id}: {e}")
            return {"status": "error", "message": str(e)}

    def execute_workflow(self, workflow_id: str, trigger_type: str, trigger_details: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute an integration workflow
        Args:
            workflow_id: ID of workflow to execute
            trigger_type: Type of trigger initiating execution
            trigger_details: Details about the trigger event
        Returns:
            Dictionary with workflow execution status
        """
        try:
            if not self.config['integration']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Integration is disabled",
                    "execution_id": "N/A"
                }

            if workflow_id not in self.workflows:
                return {
                    "status": "error",
                    "message": f"Workflow {workflow_id} not found",
                    "execution_id": "N/A"
                }

            workflow_info = self.workflows[workflow_id]

            if trigger_type not in self.config['triggers']['trigger_types']:
                return {
                    "status": "error",
                    "message": f"Invalid trigger type: {trigger_type}. Must be one of {self.config['triggers']['trigger_types']}",
                    "execution_id": "N/A"
                }

            execution_id = f"exec_{workflow_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated workflow execution - in real system, would execute actual actions
            execution_start = datetime.now()
            execution_info = {
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "workflow_name": workflow_info['workflow_name'],
                "target_system": workflow_info['target_system'],
                "integration_mode": workflow_info['integration_mode'],
                "trigger_type": trigger_type,
                "trigger_details": trigger_details or {},
                "start_time": execution_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "running",
                "actions_executed": [],
                "results": [],
                "errors": []
            }

            # Simulate action execution based on integration mode
            actions_to_execute = workflow_info['actions']
            success_chance = {
                "real_time": 0.85,
                "hybrid": 0.75,
                "batch": 0.9
            }.get(workflow_info['integration_mode'], 0.8)

            for action in actions_to_execute:
                action_result = {
                    "action_type": action,
                    "start_time": datetime.now().isoformat(),
                    "end_time": None,
                    "status": "running",
                    "result": None,
                    "error": None
                }

                # Simulate action outcome
                if random.random() < success_chance:
                    action_result['status'] = "success"
                    action_result['result'] = f"Simulated successful {action} for {workflow_info['target_system']}"
                else:
                    action_result['status'] = "failed"
                    action_result['error'] = f"Simulated failure in {action} for {workflow_info['target_system']}"

                action_result['end_time'] = datetime.now().isoformat()
                execution_info['actions_executed'].append(action_result)

                if action_result['status'] == "success":
                    execution_info['results'].append(action_result['result'])
                else:
                    execution_info['errors'].append(action_result['error'])

            execution_end = datetime.now()
            execution_info['end_time'] = execution_end.isoformat()
            execution_info['duration_seconds'] = (execution_end - execution_start).total_seconds()
            execution_info['status'] = "completed" if not execution_info['errors'] else "completed_with_errors"

            # Log execution
            self.integration_logs.append(execution_info)

            # Save execution log
            execution_file = os.path.join(self.integration_dir, f"execution_{execution_id}.json")
            try:
                with open(execution_file, 'w') as f:
                    json.dump(execution_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving execution data for {execution_id}: {e}")

            logger.info(f"Executed integration workflow {workflow_id} with execution ID {execution_id}, status: {execution_info['status']}")
            return {
                "status": "success",
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "workflow_name": workflow_info['workflow_name'],
                "target_system": workflow_info['target_system'],
                "integration_mode": workflow_info['integration_mode'],
                "trigger_type": trigger_type,
                "start_time": execution_info['start_time'],
                "end_time": execution_info['end_time'],
                "duration_seconds": execution_info['duration_seconds'],
                "execution_status": execution_info['status'],
                "actions_count": len(execution_info['actions_executed']),
                "success_count": len([a for a in execution_info['actions_executed'] if a['status'] == "success"]),
                "error_count": len(execution_info['errors'])
            }
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_id}: {e}")
            return {"status": "error", "message": str(e), "execution_id": "N/A"}

    def get_integration_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current integration status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'workflows', 'executions')
        Returns:
            Dictionary with integration status information
        """
        try:
            workflow_summary = {
                "total_workflows": len(self.workflows),
                "workflows_by_system": {},
                "workflows_by_mode": {"real_time": 0, "batch": 0, "hybrid": 0}
            }

            for w in self.workflows.values():
                workflow_summary['workflows_by_system'][w['target_system']] = workflow_summary['workflows_by_system'].get(w['target_system'], 0) + 1
                workflow_summary['workflows_by_mode'][w['integration_mode']] += 1

            execution_summary = {
                "total_executions": len(self.integration_logs),
                "successful_executions": len([e for e in self.integration_logs if e['status'] == "completed"]),
                "executions_with_errors": len([e for e in self.integration_logs if e['status'] == "completed_with_errors"]),
                "executions_by_workflow": {},
                "recent_executions": sorted(
                    [
                        {
                            "execution_id": e['execution_id'],
                            "workflow_id": e['workflow_id'],
                            "workflow_name": e['workflow_name'],
                            "target_system": e['target_system'],
                            "start_time": e['start_time'],
                            "status": e['status']
                        }
                        for e in self.integration_logs
                    ],
                    key=lambda x: x['start_time'],
                    reverse=True
                )[:5]
            }

            for e in self.integration_logs:
                execution_summary['executions_by_workflow'][e['workflow_id']] = execution_summary['executions_by_workflow'].get(e['workflow_id'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "integration_enabled": self.config['integration']['enabled'],
                    "default_mode": self.config['integration']['default_mode'],
                    "target_systems": self.config['integration']['target_systems'],
                    "workflow_summary": {
                        "total_workflows": workflow_summary['total_workflows']
                    },
                    "execution_summary": {
                        "total_executions": execution_summary['total_executions'],
                        "successful_executions": execution_summary['successful_executions'],
                        "executions_with_errors": execution_summary['executions_with_errors']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "integration": {
                        "enabled": self.config['integration']['enabled'],
                        "integration_modes": self.config['integration']['integration_modes'],
                        "default_mode": self.config['integration']['default_mode'],
                        "integration_frequency": self.config['integration']['integration_frequency'],
                        "integration_time": self.config['integration']['integration_time'],
                        "target_systems": self.config['integration']['target_systems'],
                        "integration_levels": self.config['integration']['integration_levels']
                    },
                    "data_mapping": {
                        "enabled": self.config['data_mapping']['enabled'],
                        "mapping_types": self.config['data_mapping']['mapping_types'],
                        "default_mapping": self.config['data_mapping']['default_mapping'],
                        "mapping_validation": self.config['data_mapping']['mapping_validation']
                    },
                    "workflows": {
                        "enabled": self.config['workflows']['enabled'],
                        "workflow_types": self.config['workflows']['workflow_types'],
                        "default_workflow": self.config['workflows']['default_workflow'],
                        "workflow_validation": self.config['workflows']['workflow_validation']
                    },
                    "connectors": {
                        "enabled": self.config['connectors']['enabled'],
                        "connector_types": self.config['connectors']['connector_types'],
                        "default_connector": self.config['connectors']['default_connector'],
                        "connector_validation": self.config['connectors']['connector_validation'],
                        "connector_retries": self.config['connectors']['connector_retries'],
                        "retry_delay_seconds": self.config['connectors']['retry_delay_seconds'],
                        "connector_timeout_seconds": self.config['connectors']['connector_timeout_seconds']
                    },
                    "actions": {
                        "enabled": self.config['actions']['enabled'],
                        "action_types": self.config['actions']['action_types'],
                        "action_validation": self.config['actions']['action_validation'],
                        "action_retries": self.config['actions']['action_retries'],
                        "retry_delay_seconds": self.config['actions']['retry_delay_seconds'],
                        "action_timeout_seconds": self.config['actions']['action_timeout_seconds']
                    },
                    "monitoring": {
                        "enabled": self.config['monitoring']['enabled'],
                        "metrics": self.config['monitoring']['metrics'],
                        "alert_thresholds": self.config['monitoring']['alert_thresholds'],
                        "alert_channels": self.config['monitoring']['alert_channels'],
                        "alert_escalation": self.config['monitoring']['alert_escalation']
                    },
                    "error_handling": {
                        "enabled": self.config['error_handling']['enabled'],
                        "error_recovery": self.config['error_handling']['error_recovery'],
                        "recovery_attempts": self.config['error_handling']['recovery_attempts'],
                        "recovery_delay_seconds": self.config['error_handling']['recovery_delay_seconds'],
                        "fallback_actions": self.config['error_handling']['fallback_actions'],
                        "default_fallback": self.config['error_handling']['default_fallback'],
                        "error_logging": self.config['error_handling']['error_logging']
                    },
                    "workflow_summary": workflow_summary,
                    "execution_summary": execution_summary
                }
            elif scope == "workflows":
                return {
                    "status": "success",
                    "workflow_summary": workflow_summary,
                    "workflows": [
                        {
                            "workflow_id": wid,
                            "workflow_name": w['workflow_name'],
                            "description": w['description'],
                            "target_system": w['target_system'],
                            "workflow_type": w['workflow_type'],
                            "integration_mode": w['integration_mode'],
                            "connectors": w['connectors'],
                            "actions": w['actions'],
                            "status": w['status'],
                            "version": w['version'],
                            "created_at": w['created_at'],
                            "updated_at": w['updated_at']
                        }
                        for wid, w in self.workflows.items()
                    ]
                }
            elif scope == "executions":
                return {
                    "status": "success",
                    "execution_summary": execution_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting integration status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global enterprise integration instance
integration = EnterpriseIntegration()
