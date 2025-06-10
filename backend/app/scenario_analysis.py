import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class ScenarioAnalysis:
    def __init__(self, scenario_dir: str = 'scenario_data', config_path: str = 'scenario_config.json'):
        """
        Initialize Scenario Analysis for Strategic Planning
        """
        self.scenario_dir = scenario_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.scenarios = []
        os.makedirs(self.scenario_dir, exist_ok=True)
        logger.info("Scenario Analysis module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load scenario analysis configuration from file or create default if not exists
        """
        default_config = {
            "scenario_analysis": {
                "enabled": True,
                "analysis_modes": ["exploratory", "predictive", "prescriptive", "comparative"],
                "default_mode": "exploratory",
                "analysis_frequency": "quarterly",
                "analysis_time": "00:00",
                "planning_areas": [
                    "market_expansion",
                    "product_development",
                    "operational_scaling",
                    "financial_strategy",
                    "competitive_response"
                ],
                "analysis_levels": {
                    "market_expansion": "exploratory",
                    "product_development": "predictive",
                    "operational_scaling": "prescriptive",
                    "financial_strategy": "comparative",
                    "competitive_response": "exploratory"
                }
            },
            "models": {
                "enabled": True,
                "model_types": ["monte_carlo", "system_dynamics", "agent_based", "scenario_tree", "custom"],
                "default_model": "monte_carlo",
                "model_validation": True
            },
            "data_sources": {
                "enabled": True,
                "source_types": ["historical", "forecast", "market_data", "expert_input", "simulated"],
                "default_source": "historical",
                "source_validation": True
            },
            "scenarios": {
                "enabled": True,
                "scenario_types": ["base_case", "best_case", "worst_case", "disruptive", "transformative", "custom"],
                "default_scenario_set": ["base_case", "best_case", "worst_case"],
                "scenario_validation": True,
                "max_scenarios": 6
            },
            "outcomes": {
                "enabled": True,
                "outcome_types": ["financial", "operational", "market", "strategic", "risk"],
                "default_outcome": "financial",
                "outcome_validation": True
            },
            "reporting": {
                "enabled": True,
                "report_types": ["summary", "detailed", "comparative", "sensitivity", "decision_impact"],
                "default_report": "summary",
                "report_frequency": "quarterly",
                "report_time": "06:00",
                "distribution_channels": ["email", "dashboard", "presentation"],
                "recipients": ["executives", "strategy_team", "operations_team"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["critical_divergence", "strategic_opportunity", "major_risk", "scenario_trigger"],
                "alert_channels": ["email", "dashboard", "slack", "sms"],
                "alert_escalation": True,
                "thresholds": {
                    "divergence_level": 15,
                    "opportunity_potential": 20,
                    "risk_impact": 25,
                    "trigger_proximity": 5
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
                    logger.info("Loaded scenario analysis configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading scenario analysis config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default scenario analysis configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default scenario analysis config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved scenario analysis configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving scenario analysis config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_model(self, model_id: str, model_name: str, description: str, planning_area: str, model_type: Optional[str] = None, data_sources: Optional[List[str]] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Define a new scenario analysis model
        Args:
            model_id: Unique identifier for the model
            model_name: Name of the model
            description: Detailed description of the model
            planning_area: Target area for scenario analysis
            model_type: Type of model ('monte_carlo', 'system_dynamics', etc.)
            data_sources: Data sources for the model
            parameters: Model parameters and hyperparameters
        Returns:
            Dictionary with model definition status
        """
        try:
            if not self.config['scenario_analysis']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Scenario analysis is disabled"
                }

            if model_id in self.models:
                return {
                    "status": "error",
                    "message": f"Model with ID {model_id} already exists"
                }

            if planning_area not in self.config['scenario_analysis']['planning_areas']:
                return {
                    "status": "error",
                    "message": f"Invalid planning area: {planning_area}. Must be one of {self.config['scenario_analysis']['planning_areas']}"
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
                "planning_area": planning_area,
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
            model_file = os.path.join(self.scenario_dir, f"model_{model_id}.json")
            try:
                with open(model_file, 'w') as f:
                    json.dump(model_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving model data for {model_id}: {e}")

            logger.info(f"Defined scenario analysis model {model_id} - {model_name} for {planning_area}")
            return {
                "status": "success",
                "model_id": model_id,
                "model_name": model_name,
                "planning_area": planning_area,
                "model_type": model_type,
                "data_sources": data_sources,
                "parameters": parameters or {},
                "created_at": model_info['created_at'],
                "version": model_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining model {model_id}: {e}")
            return {"status": "error", "message": str(e)}

    def generate_scenario_analysis(self, model_id: str, analysis_mode: Optional[str] = None, time_horizon: Optional[Dict[str, str]] = None, scenario_set: Optional[List[str]] = None, outcome_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate a scenario analysis using the specified model
        Args:
            model_id: ID of model to use for scenario analysis
            analysis_mode: Mode of analysis ('exploratory', 'predictive', 'prescriptive', 'comparative')
            time_horizon: Time horizon for analysis {'start': ISO_TIMESTAMP, 'end': ISO_TIMESTAMP}
            scenario_set: Set of scenarios to analyze ('base_case', 'best_case', 'worst_case', etc.)
            outcome_types: Types of outcomes to evaluate ('financial', 'operational', 'market', etc.)
        Returns:
            Dictionary with scenario analysis generation status
        """
        try:
            if not self.config['scenario_analysis']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Scenario analysis is disabled",
                    "analysis_id": "N/A"
                }

            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} not found",
                    "analysis_id": "N/A"
                }

            model_info = self.models[model_id]

            analysis_mode = analysis_mode or self.config['scenario_analysis']['analysis_levels'].get(model_info['planning_area'], self.config['scenario_analysis']['default_mode'])
            if analysis_mode not in self.config['scenario_analysis']['analysis_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid analysis mode: {analysis_mode}. Must be one of {self.config['scenario_analysis']['analysis_modes']}",
                    "analysis_id": "N/A"
                }

            if time_horizon and ('start' not in time_horizon or 'end' not in time_horizon):
                return {
                    "status": "error",
                    "message": "Time horizon must include 'start' and 'end' timestamps",
                    "analysis_id": "N/A"
                }

            scenario_set = scenario_set or self.config['scenarios']['default_scenario_set']
            invalid_scenarios = [s for s in scenario_set if s not in self.config['scenarios']['scenario_types']]
            if invalid_scenarios:
                return {
                    "status": "error",
                    "message": f"Invalid scenarios: {invalid_scenarios}. Must be subset of {self.config['scenarios']['scenario_types']}",
                    "analysis_id": "N/A"
                }

            if len(scenario_set) > self.config['scenarios']['max_scenarios']:
                return {
                    "status": "error",
                    "message": f"Too many scenarios: {len(scenario_set)}. Maximum allowed is {self.config['scenarios']['max_scenarios']}",
                    "analysis_id": "N/A"
                }

            outcome_types = outcome_types or [self.config['outcomes']['default_outcome']]
            invalid_outcomes = [o for o in outcome_types if o not in self.config['outcomes']['outcome_types']]
            if invalid_outcomes:
                return {
                    "status": "error",
                    "message": f"Invalid outcome types: {invalid_outcomes}. Must be subset of {self.config['outcomes']['outcome_types']}",
                    "analysis_id": "N/A"
                }

            analysis_id = f"scn_anl_{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated scenario analysis generation - in real system, would run model simulations
            generation_start = datetime.now()
            analysis_info = {
                "analysis_id": analysis_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "planning_area": model_info['planning_area'],
                "analysis_mode": analysis_mode,
                "time_horizon": time_horizon or {},
                "scenario_set": scenario_set,
                "outcome_types": outcome_types,
                "start_time": generation_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "generating",
                "scenario_results": [],
                "insights": [],
                "alerts": []
            }

            # Simulate results for each scenario
            for scenario in scenario_set:
                scenario_result = {
                    "scenario": scenario,
                    "scenario_label": scenario.replace('_', ' ').title(),
                    "probability": round(random.uniform(0.1, 0.5 if scenario == 'base_case' else 0.3), 2),
                    "outcomes": [],
                    "key_drivers": []
                }

                # Generate outcomes for each type
                for outcome_type in outcome_types:
                    base_value = random.uniform(100, 1000)
                    outcome = {
                        "outcome_type": outcome_type,
                        "value": base_value,
                        "range": {
                            "low": base_value * 0.8 if scenario != 'best_case' else base_value * 0.9,
                            "high": base_value * 1.2 if scenario != 'worst_case' else base_value * 1.1
                        },
                        "impact": random.uniform(0.3, 0.8) + (0.2 if scenario == 'best_case' else -0.2 if scenario == 'worst_case' else 0),
                        "confidence": random.uniform(0.7, 0.9)
                    }
                    scenario_result['outcomes'].append(outcome)

                # Add key drivers
                for i in range(random.randint(2, 4)):
                    driver = {
                        "driver_id": f"drv_{i+1}",
                        "description": f"Key driver {i+1} for {scenario} in {model_info['planning_area']}",
                        "impact": random.uniform(0.2, 0.6) + (0.1 if scenario == 'best_case' else -0.1 if scenario == 'worst_case' else 0),
                        "controllability": random.uniform(0.3, 0.7)
                    }
                    scenario_result['key_drivers'].append(driver)

                analysis_info['scenario_results'].append(scenario_result)

            # Generate insights based on scenario results
            analysis_info['insights'].append(f"Generated scenario analysis for {model_info['planning_area']} using {model_info['model_type']} model")
            analysis_info['insights'].append(f"Analyzed {len(scenario_set)} scenarios: {', '.join([s.replace('_', ' ').title() for s in scenario_set])}")
            if len(outcome_types) > 1:
                analysis_info['insights'].append(f"Evaluated {len(outcome_types)} outcome dimensions: {', '.join(outcome_types)}")

            # Check for alerts based on thresholds
            if len(analysis_info['scenario_results']) >= 2:
                base_scenario = next((s for s in analysis_info['scenario_results'] if s['scenario'] == 'base_case'), analysis_info['scenario_results'][0])
                other_scenarios = [s for s in analysis_info['scenario_results'] if s != base_scenario]

                for other_scenario in other_scenarios:
                    for idx, outcome in enumerate(other_scenario['outcomes']):
                        base_outcome = base_scenario['outcomes'][idx]
                        divergence = abs(outcome['value'] - base_outcome['value']) / base_outcome['value'] * 100
                        divergence_threshold = self.config['alerts']['thresholds']['divergence_level']

                        if divergence > divergence_threshold:
                            analysis_info['alerts'].append({
                                "alert_type": "critical_divergence",
                                "scenario": other_scenario['scenario_label'],
                                "metric": outcome['outcome_type'],
                                "base_value": base_outcome['value'],
                                "scenario_value": outcome['value'],
                                "divergence_percent": round(divergence, 1),
                                "threshold": divergence_threshold,
                                "message": f"Critical divergence in {outcome['outcome_type']} between Base Case ({base_outcome['value']:.1f}) and {other_scenario['scenario_label']} ({outcome['value']:.1f}): {divergence:.1f}%"
                            })

            generation_end = datetime.now()
            analysis_info['end_time'] = generation_end.isoformat()
            analysis_info['duration_seconds'] = (generation_end - generation_start).total_seconds()
            analysis_info['status'] = "completed"

            # Save analysis
            analysis_file = os.path.join(self.scenario_dir, f"analysis_{analysis_id}.json")
            try:
                with open(analysis_file, 'w') as f:
                    json.dump(analysis_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving scenario analysis data for {analysis_id}: {e}")

            # Add to scenarios list
            self.scenarios.append({
                "analysis_id": analysis_id,
                "model_id": model_id,
                "planning_area": model_info['planning_area'],
                "analysis_mode": analysis_mode,
                "generated_at": generation_end.isoformat(),
                "status": analysis_info['status']
            })

            logger.info(f"Generated scenario analysis {analysis_id} using model {model_id}, status: {analysis_info['status']}")
            return {
                "status": "success",
                "analysis_id": analysis_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "planning_area": model_info['planning_area'],
                "analysis_mode": analysis_mode,
                "time_horizon": time_horizon or {},
                "scenario_set": scenario_set,
                "outcome_types": outcome_types,
                "start_time": analysis_info['start_time'],
                "end_time": analysis_info['end_time'],
                "duration_seconds": analysis_info['duration_seconds'],
                "analysis_status": analysis_info['status'],
                "scenarios_count": len(analysis_info['scenario_results']),
                "insights_count": len(analysis_info['insights']),
                "alerts_count": len(analysis_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error generating scenario analysis using model {model_id}: {e}")
            return {"status": "error", "message": str(e), "analysis_id": "N/A"}

    def get_scenario_analysis_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current scenario analysis status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'models', 'analyses')
        Returns:
            Dictionary with scenario analysis status information
        """
        try:
            models_summary = {
                "total_models": len(self.models),
                "models_by_area": {},
                "models_by_type": {}
            }

            for m in self.models.values():
                models_summary['models_by_area'][m['planning_area']] = models_summary['models_by_area'].get(m['planning_area'], 0) + 1
                models_summary['models_by_type'][m['model_type']] = models_summary['models_by_type'].get(m['model_type'], 0) + 1

            analyses_summary = {
                "total_analyses": len(self.scenarios),
                "analyses_by_area": {},
                "recent_analyses": sorted(
                    [
                        {
                            "analysis_id": s['analysis_id'],
                            "model_id": s['model_id'],
                            "planning_area": s['planning_area'],
                            "analysis_mode": s['analysis_mode'],
                            "generated_at": s['generated_at'],
                            "status": s['status']
                        }
                        for s in self.scenarios
                    ],
                    key=lambda x: x['generated_at'],
                    reverse=True
                )[:5]
            }

            for s in self.scenarios:
                analyses_summary['analyses_by_area'][s['planning_area']] = analyses_summary['analyses_by_area'].get(s['planning_area'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "scenario_analysis_enabled": self.config['scenario_analysis']['enabled'],
                    "default_mode": self.config['scenario_analysis']['default_mode'],
                    "planning_areas": self.config['scenario_analysis']['planning_areas'],
                    "models_summary": {
                        "total_models": models_summary['total_models']
                    },
                    "analyses_summary": {
                        "total_analyses": analyses_summary['total_analyses']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "scenario_analysis": {
                        "enabled": self.config['scenario_analysis']['enabled'],
                        "analysis_modes": self.config['scenario_analysis']['analysis_modes'],
                        "default_mode": self.config['scenario_analysis']['default_mode'],
                        "analysis_frequency": self.config['scenario_analysis']['analysis_frequency'],
                        "analysis_time": self.config['scenario_analysis']['analysis_time'],
                        "planning_areas": self.config['scenario_analysis']['planning_areas'],
                        "analysis_levels": self.config['scenario_analysis']['analysis_levels']
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
                    "scenarios": {
                        "enabled": self.config['scenarios']['enabled'],
                        "scenario_types": self.config['scenarios']['scenario_types'],
                        "default_scenario_set": self.config['scenarios']['default_scenario_set'],
                        "scenario_validation": self.config['scenarios']['scenario_validation'],
                        "max_scenarios": self.config['scenarios']['max_scenarios']
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
                    "models_summary": models_summary,
                    "analyses_summary": analyses_summary
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
                            "planning_area": m['planning_area'],
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
            elif scope == "analyses":
                return {
                    "status": "success",
                    "analyses_summary": analyses_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting scenario analysis status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global scenario analysis instance
scenario_analysis = ScenarioAnalysis()
