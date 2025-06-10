import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class DecisionSupport:
    def __init__(self, decision_dir: str = 'decision_data', config_path: str = 'decision_config.json'):
        """
        Initialize AI-Assisted Decision Support System
        """
        self.decision_dir = decision_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.decisions = []
        os.makedirs(self.decision_dir, exist_ok=True)
        logger.info("Decision Support module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load decision support configuration from file or create default if not exists
        """
        default_config = {
            "decision_making": {
                "enabled": True,
                "decision_modes": ["automatic", "semi_automatic", "advisory"],
                "default_mode": "advisory",
                "decision_frequency": "as_needed",
                "decision_time": "00:00",
                "decision_areas": [
                    "strategic_planning",
                    "resource_allocation",
                    "risk_management",
                    "operational_optimization",
                    "market_strategy"
                ],
                "decision_levels": {
                    "strategic_planning": "semi_automatic",
                    "resource_allocation": "advisory",
                    "risk_management": "semi_automatic",
                    "operational_optimization": "automatic",
                    "market_strategy": "advisory"
                }
            },
            "models": {
                "enabled": True,
                "model_types": ["decision_tree", "bayesian", "neural_network", "simulation", "custom"],
                "default_model": "decision_tree",
                "model_validation": True
            },
            "data_sources": {
                "enabled": True,
                "source_types": ["historical", "real_time", "forecast", "external", "user_input"],
                "default_source": "historical",
                "source_validation": True
            },
            "criteria": {
                "enabled": True,
                "criteria_types": ["financial", "operational", "strategic", "risk", "custom"],
                "default_criteria": "financial",
                "criteria_validation": True
            },
            "recommendations": {
                "enabled": True,
                "recommendation_types": ["single_best", "ranked_options", "scenario_analysis", "sensitivity_analysis"],
                "default_recommendation": "single_best",
                "recommendation_validation": True,
                "confidence_levels": [0.8, 0.9, 0.95],
                "default_confidence": 0.9
            },
            "reporting": {
                "enabled": True,
                "report_types": ["summary", "detailed", "comparative", "decision_rationale"],
                "default_report": "summary",
                "report_frequency": "as_needed",
                "report_time": "06:00",
                "distribution_channels": ["email", "dashboard", "presentation"],
                "recipients": ["executives", "decision_makers", "operations_team"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["urgent_decision", "opportunity", "risk", "conflict"],
                "alert_channels": ["email", "dashboard", "slack", "sms"],
                "alert_escalation": True,
                "thresholds": {
                    "urgency_level": 8,
                    "opportunity_potential": 15,
                    "risk_impact": 20,
                    "conflict_severity": 7
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
                    logger.info("Loaded decision support configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading decision support config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default decision support configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default decision support config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved decision support configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving decision support config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_model(self, model_id: str, model_name: str, description: str, decision_area: str, model_type: Optional[str] = None, data_sources: Optional[List[str]] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Define a new decision support model
        Args:
            model_id: Unique identifier for the model
            model_name: Name of the model
            description: Detailed description of the model
            decision_area: Target area for decision making
            model_type: Type of model ('decision_tree', 'bayesian', etc.)
            data_sources: Data sources for the model
            parameters: Model parameters and hyperparameters
        Returns:
            Dictionary with model definition status
        """
        try:
            if not self.config['decision_making']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Decision making is disabled"
                }

            if model_id in self.models:
                return {
                    "status": "error",
                    "message": f"Model with ID {model_id} already exists"
                }

            if decision_area not in self.config['decision_making']['decision_areas']:
                return {
                    "status": "error",
                    "message": f"Invalid decision area: {decision_area}. Must be one of {self.config['decision_making']['decision_areas']}"
                }

            model_type = model_type or self.config['models']['default_model']
            if model_type not in self.config['models']['model_types']:
                return {
                    "status": "error",
                    "message": f"Invalid model type: {model_type}. Must be one of {self.config['models']['model_types']}"
                }

            data_sources = data_sources or [self.config['data_sources']['default_source']]
            invalid_sources = [s for s in data_sources if s not in self.config['data_sources']['source_types']]
            if invalid_sources:
                return {
                    "status": "error",
                    "message": f"Invalid data sources: {invalid_sources}. Must be subset of {self.config['data_sources']['source_types']}"
                }

            model_info = {
                "model_id": model_id,
                "model_name": model_name,
                "description": description,
                "decision_area": decision_area,
                "model_type": model_type,
                "data_sources": data_sources,
                "parameters": parameters or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "defined",
                "version": "1.0"
            }

            self.models[model_id] = model_info

            # Save model to file
            model_file = os.path.join(self.decision_dir, f"model_{model_id}.json")
            try:
                with open(model_file, 'w') as f:
                    json.dump(model_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving model data for {model_id}: {e}")

            logger.info(f"Defined decision support model {model_id} - {model_name} for {decision_area}")
            return {
                "status": "success",
                "model_id": model_id,
                "model_name": model_name,
                "decision_area": decision_area,
                "model_type": model_type,
                "data_sources": data_sources,
                "parameters": parameters or {},
                "created_at": model_info['created_at'],
                "version": model_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining model {model_id}: {e}")
            return {"status": "error", "message": str(e)}

    def generate_recommendation(self, model_id: str, decision_mode: Optional[str] = None, decision_context: Optional[Dict[str, Any]] = None, criteria: Optional[List[str]] = None, recommendation_type: Optional[str] = None, confidence_level: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate a decision recommendation using the specified model
        Args:
            model_id: ID of model to use for decision making
            decision_mode: Mode of decision making ('automatic', 'semi_automatic', 'advisory')
            decision_context: Contextual data for decision {'context_data': {...}}
            criteria: Decision criteria ('financial', 'operational', etc.)
            recommendation_type: Type of recommendation ('single_best', 'ranked_options', etc.)
            confidence_level: Confidence level for recommendations (0.8, 0.9, 0.95)
        Returns:
            Dictionary with recommendation generation status
        """
        try:
            if not self.config['decision_making']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Decision making is disabled",
                    "recommendation_id": "N/A"
                }

            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} not found",
                    "recommendation_id": "N/A"
                }

            model_info = self.models[model_id]

            decision_mode = decision_mode or self.config['decision_making']['decision_levels'].get(model_info['decision_area'], self.config['decision_making']['default_mode'])
            if decision_mode not in self.config['decision_making']['decision_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid decision mode: {decision_mode}. Must be one of {self.config['decision_making']['decision_modes']}",
                    "recommendation_id": "N/A"
                }

            criteria = criteria or [self.config['criteria']['default_criteria']]
            invalid_criteria = [c for c in criteria if c not in self.config['criteria']['criteria_types']]
            if invalid_criteria:
                return {
                    "status": "error",
                    "message": f"Invalid criteria: {invalid_criteria}. Must be subset of {self.config['criteria']['criteria_types']}",
                    "recommendation_id": "N/A"
                }

            recommendation_type = recommendation_type or self.config['recommendations']['default_recommendation']
            if recommendation_type not in self.config['recommendations']['recommendation_types']:
                return {
                    "status": "error",
                    "message": f"Invalid recommendation type: {recommendation_type}. Must be one of {self.config['recommendations']['recommendation_types']}",
                    "recommendation_id": "N/A"
                }

            confidence_level = confidence_level or self.config['recommendations']['default_confidence']
            if confidence_level not in self.config['recommendations']['confidence_levels']:
                return {
                    "status": "error",
                    "message": f"Invalid confidence level: {confidence_level}. Must be one of {self.config['recommendations']['confidence_levels']}",
                    "recommendation_id": "N/A"
                }

            recommendation_id = f"rec_{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated recommendation generation - in real system, would run model analysis
            generation_start = datetime.now()
            recommendation_info = {
                "recommendation_id": recommendation_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "decision_area": model_info['decision_area'],
                "decision_mode": decision_mode,
                "decision_context": decision_context or {},
                "criteria": criteria,
                "recommendation_type": recommendation_type,
                "confidence_level": confidence_level,
                "start_time": generation_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "generating",
                "recommendations": [],
                "rationale": [],
                "alerts": []
            }

            # Simulate recommendations based on type
            if recommendation_type == "single_best":
                recommendation = {
                    "option_id": "opt_1",
                    "description": f"Best option for {model_info['decision_area']}",
                    "confidence": confidence_level,
                    "impact": random.uniform(0.7, 0.9),
                    "feasibility": random.uniform(0.6, 0.8),
                    "risk": random.uniform(0.1, 0.3),
                    "recommended_action": f"Implement strategy for {model_info['decision_area']}"
                }
                recommendation_info['recommendations'].append(recommendation)
            elif recommendation_type == "ranked_options":
                for i in range(3):
                    recommendation = {
                        "option_id": f"opt_{i+1}",
                        "description": f"Option {i+1} for {model_info['decision_area']}",
                        "confidence": confidence_level - (i * 0.05),
                        "impact": random.uniform(0.5, 0.9) - (i * 0.1),
                        "feasibility": random.uniform(0.4, 0.8) - (i * 0.1),
                        "risk": random.uniform(0.1, 0.4) + (i * 0.05),
                        "recommended_action": f"Consider strategy {i+1} for {model_info['decision_area']}"
                    }
                    recommendation_info['recommendations'].append(recommendation)
            elif recommendation_type == "scenario_analysis":
                scenarios = ["base_case", "best_case", "worst_case"]
                for i, scenario in enumerate(scenarios):
                    recommendation = {
                        "option_id": f"scn_{i+1}",
                        "description": f"{scenario.replace('_', ' ').title()} scenario for {model_info['decision_area']}",
                        "confidence": confidence_level,
                        "impact": random.uniform(0.3, 0.9) + (0.2 if scenario == 'best_case' else -0.2 if scenario == 'worst_case' else 0),
                        "feasibility": random.uniform(0.3, 0.8),
                        "risk": random.uniform(0.1, 0.5) + (0.2 if scenario == 'worst_case' else 0),
                        "recommended_action": f"Plan for {scenario.replace('_', ' ').title()} in {model_info['decision_area']}"
                    }
                    recommendation_info['recommendations'].append(recommendation)
            else:  # sensitivity_analysis
                factors = ["factor_1", "factor_2", "factor_3"]
                for i, factor in enumerate(factors):
                    recommendation = {
                        "option_id": f"sen_{i+1}",
                        "description": f"Sensitivity to {factor} in {model_info['decision_area']}",
                        "confidence": confidence_level,
                        "impact": random.uniform(0.4, 0.8),
                        "feasibility": random.uniform(0.5, 0.7),
                        "risk": random.uniform(0.2, 0.4),
                        "sensitivity": random.uniform(0.1, 0.5),
                        "recommended_action": f"Analyze impact of {factor} on {model_info['decision_area']}"
                    }
                    recommendation_info['recommendations'].append(recommendation)

            # Generate rationale based on recommendations
            recommendation_info['rationale'].append(f"Generated decision support for {model_info['decision_area']} using {model_info['model_type']} model")
            if len(recommendation_info['recommendations']) > 1:
                recommendation_info['rationale'].append(f"Provided {len(recommendation_info['recommendations'])} options for consideration")

            # Check for alerts based on thresholds
            if recommendation_info['recommendations']:
                primary_option = recommendation_info['recommendations'][0]
                urgency_threshold = self.config['alerts']['thresholds']['urgency_level']
                if primary_option.get('impact', 0) > urgency_threshold / 10:
                    recommendation_info['alerts'].append({
                        "alert_type": "urgent_decision",
                        "metric": model_info['decision_area'],
                        "value": primary_option.get('impact', 0),
                        "threshold": urgency_threshold,
                        "message": f"Urgent decision needed for {model_info['decision_area']}: high impact {primary_option.get('impact', 0):.2f}"
                    })

                opportunity_threshold = self.config['alerts']['thresholds']['opportunity_potential']
                if primary_option.get('impact', 0) > opportunity_threshold / 20:
                    recommendation_info['alerts'].append({
                        "alert_type": "opportunity",
                        "metric": model_info['decision_area'],
                        "value": primary_option.get('impact', 0),
                        "threshold": opportunity_threshold,
                        "message": f"Significant opportunity in {model_info['decision_area']}: impact {primary_option.get('impact', 0):.2f}"
                    })

            generation_end = datetime.now()
            recommendation_info['end_time'] = generation_end.isoformat()
            recommendation_info['duration_seconds'] = (generation_end - generation_start).total_seconds()
            recommendation_info['status'] = "completed"

            # Save recommendation
            recommendation_file = os.path.join(self.decision_dir, f"recommendation_{recommendation_id}.json")
            try:
                with open(recommendation_file, 'w') as f:
                    json.dump(recommendation_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving recommendation data for {recommendation_id}: {e}")

            # Add to decisions list
            self.decisions.append({
                "recommendation_id": recommendation_id,
                "model_id": model_id,
                "decision_area": model_info['decision_area'],
                "decision_mode": decision_mode,
                "generated_at": generation_end.isoformat(),
                "status": recommendation_info['status']
            })

            logger.info(f"Generated recommendation {recommendation_id} using model {model_id}, status: {recommendation_info['status']}")
            return {
                "status": "success",
                "recommendation_id": recommendation_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "decision_area": model_info['decision_area'],
                "decision_mode": decision_mode,
                "decision_context": decision_context or {},
                "criteria": criteria,
                "recommendation_type": recommendation_type,
                "confidence_level": confidence_level,
                "start_time": recommendation_info['start_time'],
                "end_time": recommendation_info['end_time'],
                "duration_seconds": recommendation_info['duration_seconds'],
                "recommendation_status": recommendation_info['status'],
                "recommendations_count": len(recommendation_info['recommendations']),
                "rationale_count": len(recommendation_info['rationale']),
                "alerts_count": len(recommendation_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error generating recommendation using model {model_id}: {e}")
            return {"status": "error", "message": str(e), "recommendation_id": "N/A"}

    def get_decision_support_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current decision support status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'models', 'decisions')
        Returns:
            Dictionary with decision support status information
        """
        try:
            models_summary = {
                "total_models": len(self.models),
                "models_by_area": {},
                "models_by_type": {}
            }

            for m in self.models.values():
                models_summary['models_by_area'][m['decision_area']] = models_summary['models_by_area'].get(m['decision_area'], 0) + 1
                models_summary['models_by_type'][m['model_type']] = models_summary['models_by_type'].get(m['model_type'], 0) + 1

            decisions_summary = {
                "total_decisions": len(self.decisions),
                "decisions_by_area": {},
                "recent_decisions": sorted(
                    [
                        {
                            "recommendation_id": d['recommendation_id'],
                            "model_id": d['model_id'],
                            "decision_area": d['decision_area'],
                            "decision_mode": d['decision_mode'],
                            "generated_at": d['generated_at'],
                            "status": d['status']
                        }
                        for d in self.decisions
                    ],
                    key=lambda x: x['generated_at'],
                    reverse=True
                )[:5]
            }

            for d in self.decisions:
                decisions_summary['decisions_by_area'][d['decision_area']] = decisions_summary['decisions_by_area'].get(d['decision_area'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "decision_making_enabled": self.config['decision_making']['enabled'],
                    "default_mode": self.config['decision_making']['default_mode'],
                    "decision_areas": self.config['decision_making']['decision_areas'],
                    "models_summary": {
                        "total_models": models_summary['total_models']
                    },
                    "decisions_summary": {
                        "total_decisions": decisions_summary['total_decisions']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "decision_making": {
                        "enabled": self.config['decision_making']['enabled'],
                        "decision_modes": self.config['decision_making']['decision_modes'],
                        "default_mode": self.config['decision_making']['default_mode'],
                        "decision_frequency": self.config['decision_making']['decision_frequency'],
                        "decision_time": self.config['decision_making']['decision_time'],
                        "decision_areas": self.config['decision_making']['decision_areas'],
                        "decision_levels": self.config['decision_making']['decision_levels']
                    },
                    "models": {
                        "enabled": self.config['models']['enabled'],
                        "model_types": self.config['models']['model_types'],
                        "default_model": self.config['models']['default_model'],
                        "model_validation": self.config['models']['model_validation']
                    },
                    "data_sources": {
                        "enabled": self.config['data_sources']['enabled'],
                        "source_types": self.config['data_sources']['source_types'],
                        "default_source": self.config['data_sources']['default_source'],
                        "source_validation": self.config['data_sources']['source_validation']
                    },
                    "criteria": {
                        "enabled": self.config['criteria']['enabled'],
                        "criteria_types": self.config['criteria']['criteria_types'],
                        "default_criteria": self.config['criteria']['default_criteria'],
                        "criteria_validation": self.config['criteria']['criteria_validation']
                    },
                    "recommendations": {
                        "enabled": self.config['recommendations']['enabled'],
                        "recommendation_types": self.config['recommendations']['recommendation_types'],
                        "default_recommendation": self.config['recommendations']['default_recommendation'],
                        "recommendation_validation": self.config['recommendations']['recommendation_validation'],
                        "confidence_levels": self.config['recommendations']['confidence_levels'],
                        "default_confidence": self.config['recommendations']['default_confidence']
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
                    "decisions_summary": decisions_summary
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
                            "decision_area": m['decision_area'],
                            "model_type": m['model_type'],
                            "data_sources": m['data_sources'],
                            "parameters": m['parameters'],
                            "status": m['status'],
                            "version": m['version'],
                            "created_at": m['created_at'],
                            "updated_at": m['updated_at']
                        }
                        for mid, m in self.models.items()
                    ]
                }
            elif scope == "decisions":
                return {
                    "status": "success",
                    "decisions_summary": decisions_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting decision support status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global decision support instance
decision_support = DecisionSupport()
