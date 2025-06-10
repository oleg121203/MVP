import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class ResourceAllocation:
    def __init__(self, allocation_dir: str = 'allocation_data', config_path: str = 'allocation_config.json'):
        """
        Initialize AI-Assisted Resource Allocation
        """
        self.allocation_dir = allocation_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.allocations = []
        os.makedirs(self.allocation_dir, exist_ok=True)
        logger.info("Resource Allocation module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load resource allocation configuration from file or create default if not exists
        """
        default_config = {
            "resource_allocation": {
                "enabled": True,
                "allocation_modes": ["predictive", "reactive", "scheduled", "on_demand"],
                "default_mode": "predictive",
                "allocation_frequency": "daily",
                "allocation_time": "01:00",
                "resource_domains": [
                    "human_resources",
                    "computing_resources",
                    "financial_resources",
                    "inventory",
                    "facilities",
                    "equipment"
                ],
                "allocation_levels": {
                    "human_resources": "predictive",
                    "computing_resources": "reactive",
                    "financial_resources": "scheduled",
                    "inventory": "on_demand",
                    "facilities": "scheduled",
                    "equipment": "reactive"
                }
            },
            "models": {
                "enabled": True,
                "model_types": ["optimization", "machine_learning", "heuristic", "simulation", "custom"],
                "default_model": "optimization",
                "model_validation": True
            },
            "constraints": {
                "enabled": True,
                "constraint_types": ["budget", "capacity", "time", "skill", "location", "priority"],
                "default_constraint": "budget",
                "constraint_validation": True
            },
            "objectives": {
                "enabled": True,
                "objective_categories": ["cost_minimization", "efficiency_maximization", "service_level", "risk_reduction", "sustainability"],
                "default_objective": "efficiency_maximization",
                "objective_validation": True
            },
            "reporting": {
                "enabled": True,
                "report_types": ["summary", "detailed", "utilization", "forecast", "optimization_analysis"],
                "default_report": "summary",
                "report_frequency": "weekly",
                "report_time": "07:00",
                "distribution_channels": ["email", "dashboard", "slack"],
                "recipients": ["operations_team", "management", "finance_team"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["resource_shortage", "overallocation", "constraint_violation", "optimization_failure"],
                "alert_channels": ["email", "dashboard", "slack", "sms"],
                "alert_escalation": True,
                "thresholds": {
                    "shortage_level": 0.2,
                    "overallocation_level": 0.1,
                    "constraint_violation_severity": 5,
                    "optimization_confidence": 0.7
                }
            },
            "error_handling": {
                "enabled": True,
                "error_recovery": True,
                "recovery_attempts": 3,
                "recovery_delay_seconds": 30,
                "fallback_actions": ["notify_admin", "use_default_allocation", "log_only"],
                "default_fallback": "notify_admin",
                "error_logging": "detailed"
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded resource allocation configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading resource allocation config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default resource allocation configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default resource allocation config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved resource allocation configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving resource allocation config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_model(self, model_id: str, model_name: str, description: str, resource_domain: str, model_type: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Define a new resource allocation model
        Args:
            model_id: Unique identifier for the model
            model_name: Name of the model
            description: Detailed description of the model
            resource_domain: Target domain for resource allocation
            model_type: Type of model ('optimization', 'machine_learning', etc.)
            parameters: Model parameters and hyperparameters
        Returns:
            Dictionary with model definition status
        """
        try:
            if not self.config['resource_allocation']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Resource allocation is disabled"
                }

            if model_id in self.models:
                return {
                    "status": "error",
                    "message": f"Model with ID {model_id} already exists"
                }

            if resource_domain not in self.config['resource_allocation']['resource_domains']:
                return {
                    "status": "error",
                    "message": f"Invalid resource domain: {resource_domain}. Must be one of {self.config['resource_allocation']['resource_domains']}"
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
                "resource_domain": resource_domain,
                "model_type": model_type,
                "parameters": parameters or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "defined",
                "version": "1.0"
            }

            self.models[model_id] = model_info

            # Save model to file
            model_file = os.path.join(self.allocation_dir, f"model_{model_id}.json")
            try:
                with open(model_file, 'w') as f:
                    json.dump(model_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving model data for {model_id}: {e}")

            logger.info(f"Defined resource allocation model {model_id} - {model_name} for {resource_domain}")
            return {
                "status": "success",
                "model_id": model_id,
                "model_name": model_name,
                "resource_domain": resource_domain,
                "model_type": model_type,
                "parameters": parameters or {},
                "created_at": model_info['created_at'],
                "version": model_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining model {model_id}: {e}")
            return {"status": "error", "message": str(e)}

    def allocate_resources(self, model_id: str, allocation_mode: Optional[str] = None, resources: Optional[List[Dict[str, Any]]] = None, demands: Optional[List[Dict[str, Any]]] = None, constraints: Optional[List[Dict[str, Any]]] = None, objectives: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Allocate resources using the specified model
        Args:
            model_id: ID of model to use for resource allocation
            allocation_mode: Mode of allocation ('predictive', 'reactive', 'scheduled', 'on_demand')
            resources: List of resources to allocate [{'resource_id': str, 'type': str, 'quantity': float, 'attributes': dict}]
            demands: List of demands for resources [{'demand_id': str, 'type': str, 'quantity': float, 'priority': float, 'attributes': dict}]
            constraints: List of constraints for allocation [{'constraint_type': str, 'value': Any, 'weight': float}]
            objectives: List of objectives for allocation [{'objective_category': str, 'weight': float, 'parameters': dict}]
        Returns:
            Dictionary with resource allocation status
        """
        try:
            if not self.config['resource_allocation']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Resource allocation is disabled",
                    "allocation_id": "N/A"
                }

            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} not found",
                    "allocation_id": "N/A"
                }

            model_info = self.models[model_id]

            allocation_mode = allocation_mode or self.config['resource_allocation']['allocation_levels'].get(model_info['resource_domain'], self.config['resource_allocation']['default_mode'])
            if allocation_mode not in self.config['resource_allocation']['allocation_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid allocation mode: {allocation_mode}. Must be one of {self.config['resource_allocation']['allocation_modes']}",
                    "allocation_id": "N/A"
                }

            if constraints:
                for constraint in constraints:
                    if 'constraint_type' not in constraint or constraint['constraint_type'] not in self.config['constraints']['constraint_types']:
                        return {
                            "status": "error",
                            "message": f"Invalid constraint type. Must be one of {self.config['constraints']['constraint_types']}",
                            "allocation_id": "N/A"
                        }

            if objectives:
                for objective in objectives:
                    if 'objective_category' not in objective or objective['objective_category'] not in self.config['objectives']['objective_categories']:
                        return {
                            "status": "error",
                            "message": f"Invalid objective category. Must be one of {self.config['objectives']['objective_categories']}",
                            "allocation_id": "N/A"
                        }

            allocation_id = f"alloc_{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated resource allocation - in real system, would run optimization
            allocation_start = datetime.now()
            allocation_info = {
                "allocation_id": allocation_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "resource_domain": model_info['resource_domain'],
                "allocation_mode": allocation_mode,
                "resources": resources or [],
                "demands": demands or [],
                "constraints": constraints or [],
                "objectives": objectives or [],
                "start_time": allocation_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "allocating",
                "allocations": [],
                "metrics": {},
                "alerts": []
            }

            # Use provided resources or generate simulated ones
            if resources and len(resources) > 0:
                resources_to_allocate = resources
            else:
                resources_to_allocate = []
                for i in range(random.randint(3, 6)):
                    resources_to_allocate.append({
                        "resource_id": f"res_{i+1}",
                        "type": f"{model_info['resource_domain']}_type_{i%3+1}",
                        "quantity": random.uniform(5, 50),
                        "attributes": {
                            "location": random.choice(["east", "west", "north", "south", "central"]),
                            "cost_per_unit": random.uniform(10, 100)
                        }
                    })

            # Use provided demands or generate simulated ones
            if demands and len(demands) > 0:
                demands_to_satisfy = demands
            else:
                demands_to_satisfy = []
                for i in range(random.randint(2, 5)):
                    demands_to_satisfy.append({
                        "demand_id": f"dem_{i+1}",
                        "type": f"{model_info['resource_domain']}_type_{i%3+1}",
                        "quantity": random.uniform(2, 20),
                        "priority": random.uniform(0.5, 1.0),
                        "attributes": {
                            "location": random.choice(["east", "west", "north", "south", "central"]),
                            "deadline": (datetime.now().isoformat() if i%2==0 else None)
                        }
                    })

            # Allocate resources to demands
            for demand in demands_to_satisfy:
                matching_resources = [r for r in resources_to_allocate if r['type'] == demand['type']]
                if not matching_resources:
                    allocation = {
                        "demand_id": demand['demand_id'],
                        "resource_id": None,
                        "allocated_quantity": 0,
                        "allocation_efficiency": 0,
                        "status": "unfulfilled",
                        "reason": f"No matching resources of type {demand['type']}"
                    }
                    allocation_info['allocations'].append(allocation)
                    continue

                # Sort by location match if applicable, else random
                matching_resources.sort(key=lambda r: 0 if r['attributes'].get('location') == demand['attributes'].get('location') else 1)

                total_available = sum(r['quantity'] for r in matching_resources)
                if total_available < demand['quantity']:
                    allocation = {
                        "demand_id": demand['demand_id'],
                        "resource_id": matching_resources[0]['resource_id'] if matching_resources else None,
                        "allocated_quantity": total_available,
                        "allocation_efficiency": total_available / demand['quantity'] if demand['quantity'] > 0 else 0,
                        "status": "partial",
                        "reason": f"Insufficient quantity: needed {demand['quantity']}, allocated {total_available}"
                    }
                    # Update resource quantities
                    remaining = total_available
                    for res in matching_resources:
                        if remaining <= 0:
                            break
                        allocated_from_this = min(res['quantity'], remaining)
                        res['quantity'] -= allocated_from_this
                        remaining -= allocated_from_this
                else:
                    allocation = {
                        "demand_id": demand['demand_id'],
                        "resource_id": matching_resources[0]['resource_id'] if matching_resources else None,
                        "allocated_quantity": demand['quantity'],
                        "allocation_efficiency": 1.0,
                        "status": "fulfilled",
                        "reason": "Demand fully met"
                    }
                    # Update resource quantities
                    remaining_demand = demand['quantity']
                    for res in matching_resources:
                        if remaining_demand <= 0:
                            break
                        allocated_from_this = min(res['quantity'], remaining_demand)
                        res['quantity'] -= allocated_from_this
                        remaining_demand -= allocated_from_this

                allocation_info['allocations'].append(allocation)

            # Calculate metrics
            fulfilled_demands = [a for a in allocation_info['allocations'] if a['status'] == "fulfilled"]
            partial_demands = [a for a in allocation_info['allocations'] if a['status'] == "partial"]
            unfulfilled_demands = [a for a in allocation_info['allocations'] if a['status'] == "unfulfilled"]

            allocation_info['metrics'] = {
                "total_demands": len(allocation_info['allocations']),
                "fulfilled_demands": len(fulfilled_demands),
                "partial_demands": len(partial_demands),
                "unfulfilled_demands": len(unfulfilled_demands),
                "fulfillment_rate": len(fulfilled_demands) / len(allocation_info['allocations']) if allocation_info['allocations'] else 0,
                "average_efficiency": sum(a['allocation_efficiency'] for a in allocation_info['allocations']) / len(allocation_info['allocations']) if allocation_info['allocations'] else 0,
                "resource_utilization": 1.0 - sum(r['quantity'] for r in resources_to_allocate) / sum(r['quantity'] for r in resources) if resources else 0
            }

            # Check for alerts based on thresholds
            shortage_threshold = self.config['alerts']['thresholds']['shortage_level']
            if allocation_info['metrics']['unfulfilled_demands'] / allocation_info['metrics']['total_demands'] > shortage_threshold:
                allocation_info['alerts'].append({
                    "alert_type": "resource_shortage",
                    "resource_domain": model_info['resource_domain'],
                    "unfulfilled_rate": allocation_info['metrics']['unfulfilled_demands'] / allocation_info['metrics']['total_demands'],
                    "unfulfilled_count": allocation_info['metrics']['unfulfilled_demands'],
                    "total_demands": allocation_info['metrics']['total_demands'],
                    "threshold": shortage_threshold,
                    "message": f"Significant resource shortage in {model_info['resource_domain']}: {allocation_info['metrics']['unfulfilled_demands']} of {allocation_info['metrics']['total_demands']} demands unfulfilled"
                })

            overallocation_threshold = self.config['alerts']['thresholds']['overallocation_level']
            if allocation_info['metrics']['resource_utilization'] > 1 + overallocation_threshold:
                allocation_info['alerts'].append({
                    "alert_type": "overallocation",
                    "resource_domain": model_info['resource_domain'],
                    "utilization_rate": allocation_info['metrics']['resource_utilization'],
                    "threshold": 1 + overallocation_threshold,
                    "message": f"Overallocation detected in {model_info['resource_domain']}: utilization at {allocation_info['metrics']['resource_utilization']:.2%}"
                })

            allocation_end = datetime.now()
            allocation_info['end_time'] = allocation_end.isoformat()
            allocation_info['duration_seconds'] = (allocation_end - allocation_start).total_seconds()
            allocation_info['status'] = "completed"

            # Save allocation
            allocation_file = os.path.join(self.allocation_dir, f"allocation_{allocation_id}.json")
            try:
                with open(allocation_file, 'w') as f:
                    json.dump(allocation_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving allocation data for {allocation_id}: {e}")

            # Add to allocations list
            self.allocations.append({
                "allocation_id": allocation_id,
                "model_id": model_id,
                "resource_domain": model_info['resource_domain'],
                "allocation_mode": allocation_mode,
                "generated_at": allocation_end.isoformat(),
                "status": allocation_info['status']
            })

            logger.info(f"Generated resource allocation {allocation_id} using model {model_id}, status: {allocation_info['status']}")
            return {
                "status": "success",
                "allocation_id": allocation_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "resource_domain": model_info['resource_domain'],
                "allocation_mode": allocation_mode,
                "resources_count": len(resources_to_allocate),
                "demands_count": len(demands_to_satisfy),
                "start_time": allocation_info['start_time'],
                "end_time": allocation_info['end_time'],
                "duration_seconds": allocation_info['duration_seconds'],
                "allocation_status": allocation_info['status'],
                "fulfilled_demands": allocation_info['metrics']['fulfilled_demands'],
                "partial_demands": allocation_info['metrics']['partial_demands'],
                "unfulfilled_demands": allocation_info['metrics']['unfulfilled_demands'],
                "fulfillment_rate": allocation_info['metrics']['fulfillment_rate'],
                "average_efficiency": allocation_info['metrics']['average_efficiency'],
                "resource_utilization": allocation_info['metrics']['resource_utilization'],
                "alerts_count": len(allocation_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error allocating resources using model {model_id}: {e}")
            return {"status": "error", "message": str(e), "allocation_id": "N/A"}

    def get_resource_allocation_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current resource allocation status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'models', 'allocations')
        Returns:
            Dictionary with resource allocation status information
        """
        try:
            models_summary = {
                "total_models": len(self.models),
                "models_by_domain": {},
                "models_by_type": {}
            }

            for m in self.models.values():
                models_summary['models_by_domain'][m['resource_domain']] = models_summary['models_by_domain'].get(m['resource_domain'], 0) + 1
                models_summary['models_by_type'][m['model_type']] = models_summary['models_by_type'].get(m['model_type'], 0) + 1

            allocations_summary = {
                "total_allocations": len(self.allocations),
                "allocations_by_domain": {},
                "recent_allocations": sorted(
                    [
                        {
                            "allocation_id": a['allocation_id'],
                            "model_id": a['model_id'],
                            "resource_domain": a['resource_domain'],
                            "allocation_mode": a['allocation_mode'],
                            "generated_at": a['generated_at'],
                            "status": a['status']
                        }
                        for a in self.allocations
                    ],
                    key=lambda x: x['generated_at'],
                    reverse=True
                )[:5]
            }

            for a in self.allocations:
                allocations_summary['allocations_by_domain'][a['resource_domain']] = allocations_summary['allocations_by_domain'].get(a['resource_domain'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "resource_allocation_enabled": self.config['resource_allocation']['enabled'],
                    "default_mode": self.config['resource_allocation']['default_mode'],
                    "resource_domains": self.config['resource_allocation']['resource_domains'],
                    "models_summary": {
                        "total_models": models_summary['total_models']
                    },
                    "allocations_summary": {
                        "total_allocations": allocations_summary['total_allocations']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "resource_allocation": {
                        "enabled": self.config['resource_allocation']['enabled'],
                        "allocation_modes": self.config['resource_allocation']['allocation_modes'],
                        "default_mode": self.config['resource_allocation']['default_mode'],
                        "allocation_frequency": self.config['resource_allocation']['allocation_frequency'],
                        "allocation_time": self.config['resource_allocation']['allocation_time'],
                        "resource_domains": self.config['resource_allocation']['resource_domains'],
                        "allocation_levels": self.config['resource_allocation']['allocation_levels']
                    },
                    "models": {
                        "enabled": self.config['models']['enabled'],
                        "model_types": self.config['models']['model_types'],
                        "default_model": self.config['models']['default_model'],
                        "model_validation": self.config['models']['model_validation']
                    },
                    "constraints": {
                        "enabled": self.config['constraints']['enabled'],
                        "constraint_types": self.config['constraints']['constraint_types'],
                        "default_constraint": self.config['constraints']['default_constraint'],
                        "constraint_validation": self.config['constraints']['constraint_validation']
                    },
                    "objectives": {
                        "enabled": self.config['objectives']['enabled'],
                        "objective_categories": self.config['objectives']['objective_categories'],
                        "default_objective": self.config['objectives']['default_objective'],
                        "objective_validation": self.config['objectives']['objective_validation']
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
                    "allocations_summary": allocations_summary
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
                            "resource_domain": m['resource_domain'],
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
            elif scope == "allocations":
                return {
                    "status": "success",
                    "allocations_summary": allocations_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting resource allocation status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global resource allocation instance
resource_allocation = ResourceAllocation()
