import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class AIGovernance:
    def __init__(self, governance_dir: str = 'ai_governance_data', config_path: str = 'ai_governance_config.json'):
        """
        Initialize AI Governance and Ethics Framework
        """
        self.governance_dir = governance_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.policies = {}
        self.audit_logs = []
        os.makedirs(self.governance_dir, exist_ok=True)
        logger.info("AI Governance module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load AI governance configuration from file or create default if not exists
        """
        default_config = {
            "governance": {
                "enabled": True,
                "policy_enforcement": ["development", "training", "deployment", "monitoring", "maintenance"],
                "compliance_standards": ["gdpr", "ccpa", "hipaa", "iso_27001", "soc2", "eu_ai_act"],
                "ethics_principles": [
                    "transparency",
                    "accountability",
                    "fairness",
                    "privacy",
                    "safety",
                    "human_oversight"
                ],
                "default_policy_strictness": "medium",
                "policy_strictness_levels": ["low", "medium", "high"]
            },
            "approval_workflow": {
                "enabled": True,
                "required_for": [
                    "model_training",
                    "model_deployment",
                    "data_usage",
                    "third_party_integration",
                    "high_risk_use_case"
                ],
                "approval_levels": ["team_lead", "ai_governance_board", "ethics_committee", "executive"],
                "default_approvers": {
                    "model_training": ["team_lead"],
                    "model_deployment": ["team_lead", "ai_governance_board"],
                    "data_usage": ["team_lead"],
                    "third_party_integration": ["ai_governance_board"],
                    "high_risk_use_case": ["ai_governance_board", "ethics_committee", "executive"]
                },
                "approval_deadline_days": 7
            },
            "risk_assessment": {
                "enabled": True,
                "assessment_frequency_days": 30,
                "risk_categories": [
                    "bias_and_fairness",
                    "privacy_violation",
                    "safety_risk",
                    "security_vulnerability",
                    "regulatory_non_compliance",
                    "reputational_risk"
                ],
                "risk_levels": ["low", "medium", "high", "critical"],
                "default_risk_threshold": "medium",
                "mitigation_requirements": {
                    "low": "document_only",
                    "medium": "mitigation_plan",
                    "high": "immediate_action",
                    "critical": "halt_operations"
                }
            },
            "audit_and_monitoring": {
                "enabled": True,
                "audit_frequency_hours": 24,
                "audit_types": [
                    "model_behavior",
                    "data_usage",
                    "decision_log",
                    "compliance_status",
                    "ethics_violation"
                ],
                "retention_days": 365,
                "alert_on_violation": True,
                "automatic_escalation": True
            },
            "training_and_education": {
                "enabled": True,
                "mandatory_training": ["ai_ethics", "data_privacy", "model_bias", "regulatory_compliance"],
                "training_frequency_days": 180,
                "certification_required": True,
                "target_audiences": ["developers", "data_scientists", "managers", "executives"]
            },
            "reporting": {
                "enabled": True,
                "report_frequency_hours": 24,
                "report_types": [
                    "compliance_summary",
                    "risk_assessment",
                    "audit_findings",
                    "ethics_violations",
                    "policy_adherence"
                ],
                "distribution_channels": ["email", "dashboard"],
                "recipients": ["ai_governance_team", "compliance_officer", "executives", "ethics_committee"]
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded AI governance configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading AI governance config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default AI governance configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default AI governance config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved AI governance configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving AI governance config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def define_policy(self, policy_id: str, policy_name: str, description: str, principles: List[str], enforcement_areas: List[str], strictness: Optional[str] = None, compliance_standards: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Define a new AI governance policy
        Args:
            policy_id: Unique identifier for the policy
            policy_name: Name of the policy
            description: Detailed description of the policy
            principles: AI ethics principles addressed by this policy
            enforcement_areas: Areas where policy is enforced ('development', 'training', etc.)
            strictness: Strictness level of policy enforcement ('low', 'medium', 'high')
            compliance_standards: Compliance standards this policy helps meet
        Returns:
            Dictionary with policy creation status
        """
        try:
            if not self.config['governance']['enabled']:
                return {
                    "status": "skipped",
                    "message": "AI governance is disabled"
                }

            if policy_id in self.policies:
                return {
                    "status": "error",
                    "message": f"Policy with ID {policy_id} already exists"
                }

            strictness = strictness or self.config['governance']['default_policy_strictness']
            if strictness not in self.config['governance']['policy_strictness_levels']:
                return {
                    "status": "error",
                    "message": f"Invalid strictness level: {strictness}. Must be one of {self.config['governance']['policy_strictness_levels']}"
                }

            invalid_principles = [p for p in principles if p not in self.config['governance']['ethics_principles']]
            if invalid_principles:
                return {
                    "status": "error",
                    "message": f"Invalid ethics principles: {invalid_principles}. Must be subset of {self.config['governance']['ethics_principles']}"
                }

            invalid_areas = [a for a in enforcement_areas if a not in self.config['governance']['policy_enforcement']]
            if invalid_areas:
                return {
                    "status": "error",
                    "message": f"Invalid enforcement areas: {invalid_areas}. Must be subset of {self.config['governance']['policy_enforcement']}"
                }

            compliance_standards = compliance_standards or []
            invalid_standards = [s for s in compliance_standards if s not in self.config['governance']['compliance_standards']]
            if invalid_standards:
                return {
                    "status": "error",
                    "message": f"Invalid compliance standards: {invalid_standards}. Must be subset of {self.config['governance']['compliance_standards']}"
                }

            policy_info = {
                "policy_id": policy_id,
                "policy_name": policy_name,
                "description": description,
                "principles": principles,
                "enforcement_areas": enforcement_areas,
                "strictness": strictness,
                "compliance_standards": compliance_standards,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "active",
                "version": "1.0"
            }

            self.policies[policy_id] = policy_info

            # Save policy to file
            policy_file = os.path.join(self.governance_dir, f"policy_{policy_id}.json")
            try:
                with open(policy_file, 'w') as f:
                    json.dump(policy_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving policy data for {policy_id}: {e}")

            logger.info(f"Defined AI governance policy {policy_id} - {policy_name}")
            return {
                "status": "success",
                "policy_id": policy_id,
                "policy_name": policy_name,
                "principles": principles,
                "enforcement_areas": enforcement_areas,
                "strictness": strictness,
                "compliance_standards": compliance_standards,
                "created_at": policy_info['created_at'],
                "version": policy_info['version']
            }
        except Exception as e:
            logger.error(f"Error defining policy {policy_id}: {e}")
            return {"status": "error", "message": str(e)}

    def request_approval(self, request_type: str, request_details: Dict[str, Any], requester: str, associated_model: Optional[str] = None, associated_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Request approval for AI-related activity
        Args:
            request_type: Type of approval request ('model_training', 'model_deployment', etc.)
            request_details: Details of the request
            requester: Identifier of the requesting entity
            associated_model: ID of associated model if applicable
            associated_data: ID of associated dataset if applicable
        Returns:
            Dictionary with approval request status
        """
        try:
            if not self.config['approval_workflow']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Approval workflow is disabled",
                    "request_id": "N/A"
                }

            if request_type not in self.config['approval_workflow']['required_for']:
                return {
                    "status": "error",
                    "message": f"Invalid request type: {request_type}. Must be one of {self.config['approval_workflow']['required_for']}",
                    "request_id": "N/A"
                }

            approvers = self.config['approval_workflow']['default_approvers'].get(request_type, ["team_lead"])

            request_id = f"approval_{request_type}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            request_info = {
                "request_id": request_id,
                "request_type": request_type,
                "request_details": request_details,
                "requester": requester,
                "associated_model": associated_model,
                "associated_data": associated_data,
                "requested_at": datetime.now().isoformat(),
                "approvers": approvers,
                "approval_status": "pending",
                "approval_history": [],
                "deadline": (datetime.now() + pd.Timedelta(days=self.config['approval_workflow']['approval_deadline_days'])).isoformat()
            }

            # Simulated approval request submission - in real system, would notify approvers
            # For simulation, auto-approve after short delay if strictness is low
            strictness = self.config['governance']['default_policy_strictness']
            if strictness == "low":
                request_info['approval_status'] = "approved"
                request_info['approval_history'].append({
                    "approver": "auto_approval_simulated",
                    "action": "approved",
                    "timestamp": datetime.now().isoformat(),
                    "comments": "Auto-approved due to low strictness in simulation"
                })
            else:
                # Simulated pending state
                request_info['approval_history'].append({
                    "approver": "system",
                    "action": "submitted",
                    "timestamp": datetime.now().isoformat(),
                    "comments": f"Submitted for approval to {', '.join(approvers)}"
                })

            # Log request as audit event
            audit_event = {
                "event_id": f"audit_{request_id}",
                "event_type": "approval_request",
                "event_category": "governance",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "request_type": request_type,
                    "requester": requester,
                    "associated_model": associated_model,
                    "associated_data": associated_data,
                    "status": request_info['approval_status']
                },
                "compliance_relevance": self.config['governance']['compliance_standards']
            }
            self.audit_logs.append(audit_event)

            # Save audit log
            audit_file = os.path.join(self.governance_dir, f"audit_log_{datetime.now().strftime('%Y%m%d')}.jsonl")
            try:
                with open(audit_file, 'a') as f:
                    json.dump(audit_event, f)
                    f.write('\n')
            except Exception as e:
                logger.warning(f"Error saving audit log for approval request {request_id}: {e}")

            # Save request data
            request_file = os.path.join(self.governance_dir, f"request_{request_id}.json")
            try:
                with open(request_file, 'w') as f:
                    json.dump(request_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving approval request data for {request_id}: {e}")

            logger.info(f"Submitted approval request {request_id} for {request_type} by {requester}")
            return {
                "status": "success",
                "request_id": request_id,
                "request_type": request_type,
                "requester": requester,
                "requested_at": request_info['requested_at'],
                "approval_status": request_info['approval_status'],
                "approvers": approvers,
                "deadline": request_info['deadline']
            }
        except Exception as e:
            logger.error(f"Error submitting approval request for {request_type}: {e}")
            return {"status": "error", "message": str(e), "request_id": "N/A"}

    def assess_risk(self, assessment_target: str, target_type: str, details: Dict[str, Any], assessor: str) -> Dict[str, Any]:
        """
        Assess risk for an AI system component or use case
        Args:
            assessment_target: Identifier of the item being assessed (model ID, use case ID, etc.)
            target_type: Type of target ('model', 'use_case', 'dataset', 'system')
            details: Details about the target and assessment context
            assessor: Identifier of the assessing entity
        Returns:
            Dictionary with risk assessment results
        """
        try:
            if not self.config['risk_assessment']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Risk assessment is disabled",
                    "assessment_id": "N/A"
                }

            assessment_id = f"risk_assessment_{target_type}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

            # Simulated risk assessment - in real system, would use detailed analysis
            risk_scores = {}
            overall_risk_level = "low"
            highest_risk_score = 0.0

            for category in self.config['risk_assessment']['risk_categories']:
                # Simulated risk score
                risk_score = random.random()
                risk_scores[category] = {
                    "score": risk_score,
                    "level": self._map_score_to_risk_level(risk_score),
                    "details": f"Simulated risk assessment for {category}",
                    "mitigation_recommendation": self._get_mitigation_recommendation(category, risk_score)
                }

                if risk_score > highest_risk_score:
                    highest_risk_score = risk_score
                    overall_risk_level = self._map_score_to_risk_level(risk_score)

            assessment_info = {
                "assessment_id": assessment_id,
                "target": assessment_target,
                "target_type": target_type,
                "assessor": assessor,
                "assessment_date": datetime.now().isoformat(),
                "risk_scores": risk_scores,
                "overall_risk_level": overall_risk_level,
                "overall_risk_score": highest_risk_score,
                "details": details,
                "status": "completed",
                "mitigation_required": overall_risk_level in ["medium", "high", "critical"],
                "mitigation_deadline": (datetime.now() + pd.Timedelta(days=14 if overall_risk_level == "medium" else 7 if overall_risk_level == "high" else 1)).isoformat()
            }

            # Log assessment as audit event
            audit_event = {
                "event_id": f"audit_{assessment_id}",
                "event_type": "risk_assessment",
                "event_category": "governance",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "target": assessment_target,
                    "target_type": target_type,
                    "assessor": assessor,
                    "overall_risk_level": overall_risk_level,
                    "overall_risk_score": highest_risk_score
                },
                "compliance_relevance": self.config['governance']['compliance_standards']
            }
            self.audit_logs.append(audit_event)

            # Save audit log
            audit_file = os.path.join(self.governance_dir, f"audit_log_{datetime.now().strftime('%Y%m%d')}.jsonl")
            try:
                with open(audit_file, 'a') as f:
                    json.dump(audit_event, f)
                    f.write('\n')
            except Exception as e:
                logger.warning(f"Error saving audit log for risk assessment {assessment_id}: {e}")

            # Save assessment data
            assessment_file = os.path.join(self.governance_dir, f"assessment_{assessment_id}.json")
            try:
                with open(assessment_file, 'w') as f:
                    json.dump(assessment_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving risk assessment data for {assessment_id}: {e}")

            logger.info(f"Completed risk assessment {assessment_id} for {target_type} {assessment_target} with overall risk level {overall_risk_level}")
            return {
                "status": "success",
                "assessment_id": assessment_id,
                "target": assessment_target,
                "target_type": target_type,
                "assessment_date": assessment_info['assessment_date'],
                "overall_risk_level": overall_risk_level,
                "overall_risk_score": highest_risk_score,
                "mitigation_required": assessment_info['mitigation_required'],
                "mitigation_deadline": assessment_info['mitigation_deadline'],
                "risk_categories": {k: v['level'] for k, v in risk_scores.items()}
            }
        except Exception as e:
            logger.error(f"Error assessing risk for {target_type} {assessment_target}: {e}")
            return {"status": "error", "message": str(e), "assessment_id": "N/A"}

    def _map_score_to_risk_level(self, score: float) -> str:
        """
        Map numerical risk score to risk level
        """
        if score >= 0.9:
            return "critical"
        elif score >= 0.7:
            return "high"
        elif score >= 0.4:
            return "medium"
        else:
            return "low"

    def _get_mitigation_recommendation(self, category: str, score: float) -> str:
        """
        Get mitigation recommendation based on risk category and score
        """
        risk_level = self._map_score_to_risk_level(score)
        mitigation_action = self.config['risk_assessment']['mitigation_requirements'].get(risk_level, "document_only")

        recommendations = {
            "bias_and_fairness": {
                "document_only": "Document potential bias sources and monitor outcomes",
                "mitigation_plan": "Develop bias mitigation plan and diverse training data strategy",
                "immediate_action": "Implement bias correction techniques and re-evaluate model",
                "halt_operations": "Halt model operation until bias is mitigated and independently audited"
            },
            "privacy_violation": {
                "document_only": "Document data usage and privacy safeguards",
                "mitigation_plan": "Develop enhanced data anonymization and consent processes",
                "immediate_action": "Implement strict access controls and data minimization",
                "halt_operations": "Halt data processing until privacy compliance is verified"
            },
            "safety_risk": {
                "document_only": "Document safety considerations and usage constraints",
                "mitigation_plan": "Develop safety protocols and fail-safe mechanisms",
                "immediate_action": "Implement strict usage controls and monitoring",
                "halt_operations": "Halt operation in safety-critical contexts until risks are eliminated"
            },
            "security_vulnerability": {
                "document_only": "Document security measures protecting AI system",
                "mitigation_plan": "Develop enhanced security and adversarial defense plan",
                "immediate_action": "Implement immediate security patches and hardening",
                "halt_operations": "Halt exposed systems until security is independently verified"
            },
            "regulatory_non_compliance": {
                "document_only": "Document regulatory requirements and current compliance status",
                "mitigation_plan": "Develop compliance achievement plan with legal team",
                "immediate_action": "Implement required changes to achieve compliance",
                "halt_operations": "Halt non-compliant operations until regulatory approval"
            },
            "reputational_risk": {
                "document_only": "Document potential reputational concerns",
                "mitigation_plan": "Develop communication and transparency plan",
                "immediate_action": "Implement proactive disclosure and stakeholder engagement",
                "halt_operations": "Halt controversial operations until stakeholder consensus"
            }
        }

        category_recommendations = recommendations.get(category, {})
        return category_recommendations.get(mitigation_action, f"Take appropriate {mitigation_action} action for {category} risk")

    def get_governance_status(self, scope: str = "summary") -> Dict[str, Any]:
        """
        Get current AI governance status
        Args:
            scope: Scope of status report ('summary', 'detailed', 'policies', 'approvals', 'risks', 'audits')
        Returns:
            Dictionary with governance status information
        """
        try:
            policy_summary = {
                "total_policies": len(self.policies),
                "active_policies": sum(1 for p in self.policies.values() if p['status'] == "active"),
                "policy_areas": list(set(area for p in self.policies.values() for area in p['enforcement_areas'])),
                "policy_principles": list(set(principle for p in self.policies.values() for principle in p['principles']))
            }

            approval_summary = {
                "total_requests": 0,  # Would be calculated from request files in real system
                "pending_requests": 0,
                "approved_requests": 0,
                "rejected_requests": 0,
                "recent_requests": []
            }

            risk_summary = {
                "total_assessments": 0,  # Would be calculated from assessment files in real system
                "risk_distribution": {"low": 0, "medium": 0, "high": 0, "critical": 0},
                "mitigation_required": 0,
                "recent_assessments": []
            }

            audit_summary = {
                "total_audit_events": len(self.audit_logs),
                "audit_categories": list(set(event['event_category'] for event in self.audit_logs)),
                "audit_types": list(set(event['event_type'] for event in self.audit_logs)),
                "recent_audit_events": sorted(
                    [
                        {
                            "event_id": event['event_id'],
                            "event_type": event['event_type'],
                            "timestamp": event['timestamp'],
                            "category": event['event_category']
                        }
                        for event in self.audit_logs
                    ],
                    key=lambda x: x['timestamp'],
                    reverse=True
                )[:5]
            }

            if scope == "summary":
                return {
                    "status": "success",
                    "governance_enabled": self.config['governance']['enabled'],
                    "policy_enforcement_areas": self.config['governance']['policy_enforcement'],
                    "compliance_standards": self.config['governance']['compliance_standards'],
                    "ethics_principles": self.config['governance']['ethics_principles'],
                    "policy_summary": {
                        "total_policies": policy_summary['total_policies'],
                        "active_policies": policy_summary['active_policies']
                    },
                    "approval_summary": {
                        "total_requests": approval_summary['total_requests'],
                        "pending_requests": approval_summary['pending_requests']
                    },
                    "risk_summary": {
                        "total_assessments": risk_summary['total_assessments'],
                        "mitigation_required": risk_summary['mitigation_required']
                    },
                    "audit_summary": {
                        "total_audit_events": audit_summary['total_audit_events']
                    }
                }
            elif scope == "detailed":
                return {
                    "status": "success",
                    "governance": {
                        "enabled": self.config['governance']['enabled'],
                        "policy_enforcement": self.config['governance']['policy_enforcement'],
                        "compliance_standards": self.config['governance']['compliance_standards'],
                        "ethics_principles": self.config['governance']['ethics_principles'],
                        "default_policy_strictness": self.config['governance']['default_policy_strictness']
                    },
                    "approval_workflow": {
                        "enabled": self.config['approval_workflow']['enabled'],
                        "required_for": self.config['approval_workflow']['required_for'],
                        "approval_levels": self.config['approval_workflow']['approval_levels'],
                        "approval_deadline_days": self.config['approval_workflow']['approval_deadline_days']
                    },
                    "risk_assessment": {
                        "enabled": self.config['risk_assessment']['enabled'],
                        "assessment_frequency_days": self.config['risk_assessment']['assessment_frequency_days'],
                        "risk_categories": self.config['risk_assessment']['risk_categories'],
                        "risk_levels": self.config['risk_assessment']['risk_levels'],
                        "default_risk_threshold": self.config['risk_assessment']['default_risk_threshold'],
                        "mitigation_requirements": self.config['risk_assessment']['mitigation_requirements']
                    },
                    "audit_and_monitoring": {
                        "enabled": self.config['audit_and_monitoring']['enabled'],
                        "audit_frequency_hours": self.config['audit_and_monitoring']['audit_frequency_hours'],
                        "audit_types": self.config['audit_and_monitoring']['audit_types'],
                        "retention_days": self.config['audit_and_monitoring']['retention_days'],
                        "alert_on_violation": self.config['audit_and_monitoring']['alert_on_violation'],
                        "automatic_escalation": self.config['audit_and_monitoring']['automatic_escalation']
                    },
                    "training_and_education": {
                        "enabled": self.config['training_and_education']['enabled'],
                        "mandatory_training": self.config['training_and_education']['mandatory_training'],
                        "training_frequency_days": self.config['training_and_education']['training_frequency_days'],
                        "certification_required": self.config['training_and_education']['certification_required'],
                        "target_audiences": self.config['training_and_education']['target_audiences']
                    },
                    "policy_summary": policy_summary,
                    "approval_summary": approval_summary,
                    "risk_summary": risk_summary,
                    "audit_summary": audit_summary
                }
            elif scope == "policies":
                return {
                    "status": "success",
                    "policy_summary": policy_summary,
                    "policies": [
                        {
                            "policy_id": pid,
                            "policy_name": p['policy_name'],
                            "description": p['description'],
                            "principles": p['principles'],
                            "enforcement_areas": p['enforcement_areas'],
                            "strictness": p['strictness'],
                            "status": p['status'],
                            "version": p['version'],
                            "created_at": p['created_at'],
                            "updated_at": p['updated_at']
                        }
                        for pid, p in self.policies.items()
                    ]
                }
            elif scope == "approvals":
                return {
                    "status": "success",
                    "approval_summary": approval_summary
                }
            elif scope == "risks":
                return {
                    "status": "success",
                    "risk_summary": risk_summary
                }
            elif scope == "audits":
                return {
                    "status": "success",
                    "audit_summary": audit_summary
                }
            else:
                return {
                    "status": "error",
                    "message": f"Invalid status scope: {scope}"
                }
        except Exception as e:
            logger.error(f"Error getting AI governance status for scope {scope}: {e}")
            return {"status": "error", "message": str(e)}

# Global AI governance instance
ai_governance = AIGovernance()
