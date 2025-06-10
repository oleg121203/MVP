import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class RiskAssessment:
    def __init__(self, risk_dir: str = 'risk_data', config_path: str = 'risk_config.json'):
        """
        Initialize AI-Driven Risk Assessment and Mitigation
        """
        self.risk_dir = risk_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.models = {}
        self.assessments = []
        os.makedirs(self.risk_dir, exist_ok=True)
        logger.info("Risk Assessment module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load risk assessment configuration from file or create default if not exists
        """
        default_config = {
            "risk_assessment": {
                "enabled": True,
                "assessment_modes": ["proactive", "reactive", "continuous", "periodic"],
                "default_mode": "proactive",
                "assessment_frequency": "monthly",
                "assessment_time": "00:00",
                "risk_domains": [
                    "operational",
                    "financial",
                    "strategic",
                    "compliance",
                    "cybersecurity",
                    "market"
                ],
                "assessment_levels": {
                    "operational": "continuous",
                    "financial": "periodic",
                    "strategic": "proactive",
                    "compliance": "periodic",
                    "cybersecurity": "continuous",
                    "market": "reactive"
                }
            },
            "models": {
                "enabled": True,
                "model_types": ["probabilistic", "machine_learning", "bayesian", "scenario_based", "custom"],
                "default_model": "probabilistic",
                "model_validation": True
            },
            "data_sources": {
                "enabled": True,
                "source_types": ["historical", "real_time", "external_threat", "internal_audit", "market_data"],
                "default_source": "historical",
                "source_validation": True
            },
            "risk_factors": {
                "enabled": True,
                "factor_categories": ["internal", "external", "environmental", "technological", "human"],
                "default_category": "internal",
                "factor_validation": True
            },
            "mitigation": {
                "enabled": True,
                "strategy_types": ["avoidance", "transfer", "mitigation", "acceptance", "contingency"],
                "default_strategy": "mitigation",
                "strategy_validation": True,
                "effectiveness_levels": [0.6, 0.75, 0.9],
                "default_effectiveness": 0.75
            },
            "reporting": {
                "enabled": True,
                "report_types": ["summary", "detailed", "risk_heatmap", "mitigation_plan", "trend_analysis"],
                "default_report": "summary",
                "report_frequency": "monthly",
                "report_time": "06:00",
                "distribution_channels": ["email", "dashboard", "presentation"],
                "recipients": ["executives", "risk_team", "operations_team", "compliance_team"]
            },
            "alerts": {
                "enabled": True,
                "alert_types": ["high_risk", "emerging_threat", "mitigation_failure", "compliance_issue"],
                "alert_channels": ["email", "dashboard", "slack", "sms"],
                "alert_escalation": True,
                "thresholds": {
                    "risk_severity": 7,
                    "threat_probability": 0.7,
                    "mitigation_effectiveness": 0.5,
                    "compliance_impact": 8
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
                    logger.info("Loaded risk assessment configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading risk assessment config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default risk assessment configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default risk assessment config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved risk assessment configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving risk assessment config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_model(self, model_id: str, model_name: str, description: str, risk_domain: str, model_type: Optional[str] = None, data_sources: Optional[List[str]] = None, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Define a new risk assessment model
        Args:
            model_id: Unique identifier for the model
            model_name: Name of the model
            description: Detailed description of the model
            risk_domain: Target domain for risk assessment
            model_type: Type of model ('probabilistic', 'machine_learning', etc.)
            data_sources: Data sources for the model
            parameters: Model parameters and hyperparameters
        Returns:
            Dictionary with model definition status
        """
        try:
            if not self.config['risk_assessment']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Risk assessment is disabled"
                }

            if model_id in self.models:
                return {
                    "status": "error",
                    "message": f"Model with ID {model_id} already exists"
                }

            if risk_domain not in self.config['risk_assessment']['risk_domains']:
                return {
                    "status": "error",
                    "message": f"Invalid risk domain: {risk_domain}. Must be one of {self.config['risk_assessment']['risk_domains']}"
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
                "risk_domain": risk_domain,
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
            model_file = os.path.join(self.risk_dir, f"model_{model_id}.json")
            try:
                with open(model_file, 'w') as f:
                    json.dump(model_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving model data for {model_id}: {e}")

            logger.info(f"Defined risk assessment model {model_id} - {model_name} for {risk_domain}")
            return {
                "status": "success",
                "model_id": model_id,
                "model_name": model_name,
                "risk_domain": risk_domain,
                "model_type": model_type,
                "data_sources": data_sources,
                "parameters": parameters or {},
                "created_at": model_info['created_at'],
                "version": model_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining model {model_id}: {e}")
            return {"status": "error", "message": str(e)}

    def assess_risks(self, model_id: str, assessment_mode: Optional[str] = None, time_horizon: Optional[Dict[str, str]] = None, risk_factors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Assess risks using the specified model
        Args:
            model_id: ID of model to use for risk assessment
            assessment_mode: Mode of assessment ('proactive', 'reactive', 'continuous', 'periodic')
            time_horizon: Time horizon for assessment {'start': ISO_TIMESTAMP, 'end': ISO_TIMESTAMP}
            risk_factors: List of risk factors to assess [{'category': str, 'description': str, 'weight': float}]
        Returns:
            Dictionary with risk assessment status
        """
        try:
            if not self.config['risk_assessment']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Risk assessment is disabled",
                    "assessment_id": "N/A"
                }

            if model_id not in self.models:
                return {
                    "status": "error",
                    "message": f"Model {model_id} not found",
                    "assessment_id": "N/A"
                }

            model_info = self.models[model_id]

            assessment_mode = assessment_mode or self.config['risk_assessment']['assessment_levels'].get(model_info['risk_domain'], self.config['risk_assessment']['default_mode'])
            if assessment_mode not in self.config['risk_assessment']['assessment_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid assessment mode: {assessment_mode}. Must be one of {self.config['risk_assessment']['assessment_modes']}",
                    "assessment_id": "N/A"
                }

            if time_horizon and ('start' not in time_horizon or 'end' not in time_horizon):
                return {
                    "status": "error",
                    "message": "Time horizon must include 'start' and 'end' timestamps",
                    "assessment_id": "N/A"
                }

            if risk_factors:
                for factor in risk_factors:
                    if 'category' not in factor or factor['category'] not in self.config['risk_factors']['factor_categories']:
                        return {
                            "status": "error",
                            "message": f"Invalid risk factor category. Must be one of {self.config['risk_factors']['factor_categories']}",
                            "assessment_id": "N/A"
                        }

            assessment_id = f"risk_assmt_{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated risk assessment - in real system, would run model analysis
            assessment_start = datetime.now()
            assessment_info = {
                "assessment_id": assessment_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "risk_domain": model_info['risk_domain'],
                "assessment_mode": assessment_mode,
                "time_horizon": time_horizon or {},
                "risk_factors": risk_factors or [],
                "start_time": assessment_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "assessing",
                "risks": [],
                "insights": [],
                "alerts": []
            }

            # Use provided risk factors or generate simulated ones
            if risk_factors and len(risk_factors) > 0:
                factors_to_assess = risk_factors
            else:
                factors_to_assess = []
                default_categories = self.config['risk_factors']['factor_categories'][:3]  # Use first 3 categories
                for i, cat in enumerate(default_categories):
                    factors_to_assess.append({
                        "category": cat,
                        "description": f"Simulated {cat} risk factor {i+1} for {model_info['risk_domain']}",
                        "weight": random.uniform(0.1, 0.3)
                    })

            # Assess each risk factor
            for factor in factors_to_assess:
                risk = {
                    "risk_id": f"risk_{random.randint(1000,9999)}",
                    "category": factor['category'],
                    "description": factor.get('description', f"Assessed risk in {factor['category']} domain"),
                    "probability": random.uniform(0.2, 0.8),
                    "impact": random.uniform(0.3, 0.9),
                    "severity": 0.0,  # Calculated
                    "timeframe": random.choice(["immediate", "short_term", "medium_term", "long_term"]),
                    "mitigation_status": "unmitigated",
                    "mitigation_options": []
                }

                # Calculate severity as probability * impact * weight
                weight = factor.get('weight', 0.2)
                risk['severity'] = round(risk['probability'] * risk['impact'] * weight * 10, 2)

                # Generate mitigation options
                strategy_types = self.config['mitigation']['strategy_types']
                for i in range(random.randint(1, 3)):
                    strategy = random.choice(strategy_types)
                    effectiveness = random.choice(self.config['mitigation']['effectiveness_levels'])
                    mitigation = {
                        "option_id": f"mit_{i+1}",
                        "strategy": strategy,
                        "description": f"Apply {strategy} strategy to mitigate {risk['category']} risk",
                        "effectiveness": effectiveness,
                        "cost": random.uniform(0.1, 0.5),
                        "feasibility": random.uniform(0.4, 0.8),
                        "time_to_implement": random.choice(["immediate", "short_term", "medium_term"])
                    }
                    risk['mitigation_options'].append(mitigation)

                assessment_info['risks'].append(risk)

            # Generate insights based on risks
            assessment_info['insights'].append(f"Assessed risks in {model_info['risk_domain']} domain using {model_info['model_type']} model")
            if len(assessment_info['risks']) > 0:
                high_risks = [r for r in assessment_info['risks'] if r['severity'] > 5.0]
                if high_risks:
                    assessment_info['insights'].append(f"Identified {len(high_risks)} high-severity risks out of {len(assessment_info['risks'])} total risks")
                else:
                    assessment_info['insights'].append(f"No high-severity risks identified among {len(assessment_info['risks'])} total risks")

            # Check for alerts based on thresholds
            risk_severity_threshold = self.config['alerts']['thresholds']['risk_severity']
            for risk in assessment_info['risks']:
                if risk['severity'] > risk_severity_threshold:
                    assessment_info['alerts'].append({
                        "alert_type": "high_risk",
                        "risk_id": risk['risk_id'],
                        "category": risk['category'],
                        "severity": risk['severity'],
                        "probability": risk['probability'],
                        "impact": risk['impact'],
                        "threshold": risk_severity_threshold,
                        "message": f"High severity risk in {risk['category']}: severity {risk['severity']:.1f} (probability {risk['probability']:.2f}, impact {risk['impact']:.2f})"
                    })

            threat_probability_threshold = self.config['alerts']['thresholds']['threat_probability']
            for risk in assessment_info['risks']:
                if risk['probability'] > threat_probability_threshold and risk['timeframe'] in ["immediate", "short_term"]:
                    assessment_info['alerts'].append({
                        "alert_type": "emerging_threat",
                        "risk_id": risk['risk_id'],
                        "category": risk['category'],
                        "probability": risk['probability'],
                        "timeframe": risk['timeframe'],
                        "threshold": threat_probability_threshold,
                        "message": f"Emerging threat in {risk['category']}: high probability {risk['probability']:.2f} with {risk['timeframe']} timeframe"
                    })

            assessment_end = datetime.now()
            assessment_info['end_time'] = assessment_end.isoformat()
            assessment_info['duration_seconds'] = (assessment_end - assessment_start).total_seconds()
            assessment_info['status'] = "completed"

            # Save assessment
            assessment_file = os.path.join(self.risk_dir, f"assessment_{assessment_id}.json")
            try:
                with open(assessment_file, 'w') as f:
                    json.dump(assessment_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving risk assessment data for {assessment_id}: {e}")

            # Add to assessments list
            self.assessments.append({
                "assessment_id": assessment_id,
                "model_id": model_id,
                "risk_domain": model_info['risk_domain'],
                "assessment_mode": assessment_mode,
                "generated_at": assessment_end.isoformat(),
                "status": assessment_info['status']
            })

            logger.info(f"Generated risk assessment {assessment_id} using model {model_id}, status: {assessment_info['status']}")
            return {
                "status": "success",
                "assessment_id": assessment_id,
                "model_id": model_id,
                "model_name": model_info['model_name'],
                "risk_domain": model_info['risk_domain'],
                "assessment_mode": assessment_mode,
                "time_horizon": time_horizon or {},
                "risk_factors_count": len(factors_to_assess),
                "start_time": assessment_info['start_time'],
                "end_time": assessment_info['end_time'],
                "duration_seconds": assessment_info['duration_seconds'],
                "assessment_status": assessment_info['status'],
                "risks_count": len(assessment_info['risks']),
                "insights_count": len(assessment_info['insights']),
                "alerts_count": len(assessment_info['alerts'])
            }
        except Exception as e:
            logger.error(f"Error assessing risks using model {model_id}: {e}")
            return {"status": "error", "message": str(e), "assessment_id": "N/A"}

    def apply_mitigation_strategy(self, assessment_id: str, risk_id: str, option_id: str) -> Dict[str, Any]:
        """
        Apply a mitigation strategy to a specific risk from an assessment
        Args:
            assessment_id: ID of the risk assessment containing the risk
            risk_id: ID of the risk to mitigate
            option_id: ID of the mitigation option to apply
        Returns:
            Dictionary with mitigation application status
        """
        try:
            if not self.config['mitigation']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Risk mitigation is disabled",
                    "mitigation_id": "N/A"
                }

            # Find the assessment
            assessment = next((a for a in self.assessments if a['assessment_id'] == assessment_id), None)
            if not assessment:
                return {
                    "status": "error",
                    "message": f"Assessment {assessment_id} not found",
                    "mitigation_id": "N/A"
                }

            # Load full assessment data
            assessment_file = os.path.join(self.risk_dir, f"assessment_{assessment_id}.json")
            if not os.path.exists(assessment_file):
                return {
                    "status": "error",
                    "message": f"Assessment data file for {assessment_id} not found",
                    "mitigation_id": "N/A"
                }

            with open(assessment_file, 'r') as f:
                assessment_info = json.load(f)

            # Find the risk
            risk = next((r for r in assessment_info['risks'] if r['risk_id'] == risk_id), None)
            if not risk:
                return {
                    "status": "error",
                    "message": f"Risk {risk_id} not found in assessment {assessment_id}",
                    "mitigation_id": "N/A"
                }

            if risk['mitigation_status'] in ["mitigated", "in_progress"]:
                return {
                    "status": "error",
                    "message": f"Risk {risk_id} is already {risk['mitigation_status']}",
                    "mitigation_id": "N/A"
                }

            # Find the mitigation option
            mitigation_option = next((opt for opt in risk['mitigation_options'] if opt['option_id'] == option_id), None)
            if not mitigation_option:
                return {
                    "status": "error",
                    "message": f"Mitigation option {option_id} not found for risk {risk_id}",
                    "mitigation_id": "N/A"
                }

            mitigation_id = f"mit_{assessment_id}_{risk_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Apply mitigation - in real system, would trigger actions
            application_start = datetime.now()
            mitigation_result = {
                "mitigation_id": mitigation_id,
                "assessment_id": assessment_id,
                "risk_id": risk_id,
                "risk_category": risk['category'],
                "risk_description": risk['description'],
                "option_id": option_id,
                "strategy": mitigation_option['strategy'],
                "description": mitigation_option['description'],
                "start_time": application_start.isoformat(),
                "end_time": None,
                "duration_seconds": None,
                "status": "applying",
                "effectiveness": mitigation_option['effectiveness'],
                "cost": mitigation_option['cost'],
                "feasibility": mitigation_option['feasibility'],
                "time_to_implement": mitigation_option['time_to_implement'],
                "implementation_details": f"Initiated {mitigation_option['strategy']} strategy for {risk['category']} risk",
                "residual_risk": {
                    "probability": risk['probability'] * (1 - mitigation_option['effectiveness'] * 0.7),
                    "impact": risk['impact'] * (1 - mitigation_option['effectiveness'] * 0.3),
                    "severity": 0.0  # Calculated
                },
                "alerts": []
            }

            # Calculate residual severity
            mitigation_result['residual_risk']['severity'] = round(
                mitigation_result['residual_risk']['probability'] * 
                mitigation_result['residual_risk']['impact'] * 
                2.0,  # Assuming weight of 0.2 * 10
                2
            )

            # Check if residual risk is still high
            risk_severity_threshold = self.config['alerts']['thresholds']['risk_severity']
            if mitigation_result['residual_risk']['severity'] > risk_severity_threshold * 0.7:
                mitigation_result['alerts'].append({
                    "alert_type": "residual_risk",
                    "risk_id": risk_id,
                    "category": risk['category'],
                    "original_severity": risk['severity'],
                    "residual_severity": mitigation_result['residual_risk']['severity'],
                    "threshold": risk_severity_threshold * 0.7,
                    "message": f"Residual risk still significant after mitigation for {risk['category']}: reduced from {risk['severity']:.1f} to {mitigation_result['residual_risk']['severity']:.1f}"
                })

            application_end = datetime.now()
            mitigation_result['end_time'] = application_end.isoformat()
            mitigation_result['duration_seconds'] = (application_end - application_start).total_seconds()
            mitigation_result['status'] = "applied"

            # Update risk status in assessment
            risk['mitigation_status'] = "mitigated"
            risk['mitigation_applied'] = {
                "mitigation_id": mitigation_id,
                "strategy": mitigation_option['strategy'],
                "applied_at": application_end.isoformat(),
                "effectiveness": mitigation_option['effectiveness'],
                "residual_severity": mitigation_result['residual_risk']['severity']
            }

            # Save updated assessment
            try:
                with open(assessment_file, 'w') as f:
                    json.dump(assessment_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error updating assessment data for {assessment_id}: {e}")

            # Save mitigation result
            mitigation_file = os.path.join(self.risk_dir, f"mitigation_{mitigation_id}.json")
            try:
                with open(mitigation_file, 'w') as f:
                    json.dump(mitigation_result, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving mitigation data for {mitigation_id}: {e}")

            logger.info(f"Applied mitigation {mitigation_id} for risk {risk_id} in assessment {assessment_id}")
            return {
                "status": "success",
                "mitigation_id": mitigation_id,
                "assessment_id": assessment_id,
                "risk_id": risk_id,
                "risk_category": risk['category'],
                "strategy": mitigation_option['strategy'],
                "start_time": mitigation_result['start_time'],
                "end_time": mitigation_result['end_time'],
                "duration_seconds": mitigation_result['duration_seconds'],
                "mitigation_status": mitigation_result['status'],
                "effectiveness": mitigation_option['effectiveness'],
                "original_severity": risk['severity'],
                "residual_severity": mitigation_result['residual_risk']['severity'],
                "alerts_count": len(mitigation_result['alerts'])
            }
        except Exception as e:
            logger.error(f"Error applying mitigation for risk {risk_id} in assessment {assessment_id}: {e}")
            return {"status": "error", "message": str(e), "mitigation_id": "N/A"}

    def get_risk_assessment_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current risk assessment status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'models', 'assessments')
        Returns:
            Dictionary with risk assessment status information
        """
        try:
            models_summary = {
                "total_models": len(self.models),
                "models_by_domain": {},
                "models_by_type": {}
            }

            for m in self.models.values():
                models_summary['models_by_domain'][m['risk_domain']] = models_summary['models_by_domain'].get(m['risk_domain'], 0) + 1
                models_summary['models_by_type'][m['model_type']] = models_summary['models_by_type'].get(m['model_type'], 0) + 1

            assessments_summary = {
                "total_assessments": len(self.assessments),
                "assessments_by_domain": {},
                "recent_assessments": sorted(
                    [
                        {
                            "assessment_id": a['assessment_id'],
                            "model_id": a['model_id'],
                            "risk_domain": a['risk_domain'],
                            "assessment_mode": a['assessment_mode'],
                            "generated_at": a['generated_at'],
                            "status": a['status']
                        }
                        for a in self.assessments
                    ],
                    key=lambda x: x['generated_at'],
                    reverse=True
                )[:5]
            }

            for a in self.assessments:
                assessments_summary['assessments_by_domain'][a['risk_domain']] = assessments_summary['assessments_by_domain'].get(a['risk_domain'], 0) + 1

            if scope == "summary":
                return {
                    "status": "success",
                    "risk_assessment_enabled": self.config['risk_assessment']['enabled'],
                    "default_mode": self.config['risk_assessment']['default_mode'],
                    "risk_domains": self.config['risk_assessment']['risk_domains'],
                    "models_summary": {
                        "total_models": models_summary['total_models']
                    },
                    "assessments_summary": {
                        "total_assessments": assessments_summary['total_assessments']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "risk_assessment": {
                        "enabled": self.config['risk_assessment']['enabled'],
                        "assessment_modes": self.config['risk_assessment']['assessment_modes'],
                        "default_mode": self.config['risk_assessment']['default_mode'],
                        "assessment_frequency": self.config['risk_assessment']['assessment_frequency'],
                        "assessment_time": self.config['risk_assessment']['assessment_time'],
                        "risk_domains": self.config['risk_assessment']['risk_domains'],
                        "assessment_levels": self.config['risk_assessment']['assessment_levels']
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
                    "risk_factors": {
                        "enabled": self.config['risk_factors']['enabled'],
                        "factor_categories": self.config['risk_factors']['factor_categories'],
                        "default_category": self.config['risk_factors']['default_category'],
                        "factor_validation": self.config['risk_factors']['factor_validation']
                    },
                    "mitigation": {
                        "enabled": self.config['mitigation']['enabled'],
                        "strategy_types": self.config['mitigation']['strategy_types'],
                        "default_strategy": self.config['mitigation']['default_strategy'],
                        "strategy_validation": self.config['mitigation']['strategy_validation'],
                        "effectiveness_levels": self.config['mitigation']['effectiveness_levels'],
                        "default_effectiveness": self.config['mitigation']['default_effectiveness']
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
                    "assessments_summary": assessments_summary
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
                            "risk_domain": m['risk_domain'],
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
            elif scope == "assessments":
                return {
                    "status": "success",
                    "assessments_summary": assessments_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting risk assessment status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global risk assessment instance
risk_assessment = RiskAssessment()
