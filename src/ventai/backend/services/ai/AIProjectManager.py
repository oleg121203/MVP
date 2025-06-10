"""
AI Project Manager Assistant
Provides intelligent project management capabilities with automated decision making
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ProjectPhase(Enum):
    INITIATION = "initiation"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    CLOSURE = "closure"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ProjectInsight:
    """AI-generated project insight"""
    type: str
    title: str
    description: str
    priority: str
    impact_score: float
    confidence: float
    recommendations: List[str]
    generated_at: datetime

@dataclass
class ProjectRisk:
    """Identified project risk"""
    id: str
    title: str
    description: str
    category: str
    probability: float
    impact: float
    risk_score: float
    level: RiskLevel
    mitigation_strategies: List[str]
    identified_at: datetime

class AIProjectManager:
    """AI-powered project management assistant"""
    
    def __init__(self):
        self.project_templates = self._load_project_templates()
        self.risk_patterns = self._load_risk_patterns()
        self.performance_metrics = {}
    
    def _load_project_templates(self) -> Dict[str, Any]:
        """Load project management templates"""
        return {
            "hvac_commercial": {
                "name": "Commercial HVAC Project",
                "phases": [
                    {
                        "name": "Site Assessment",
                        "duration_days": 7,
                        "tasks": [
                            "Site survey and measurements",
                            "Existing system evaluation",
                            "Load calculation analysis",
                            "Code compliance review"
                        ],
                        "deliverables": [
                            "Site assessment report",
                            "Load calculation summary",
                            "Compliance checklist"
                        ]
                    },
                    {
                        "name": "Design Phase",
                        "duration_days": 14,
                        "tasks": [
                            "System design and specifications",
                            "Equipment selection",
                            "Drawing preparation",
                            "Cost estimation"
                        ],
                        "deliverables": [
                            "Technical drawings",
                            "Equipment specifications",
                            "Cost estimate",
                            "Project timeline"
                        ]
                    },
                    {
                        "name": "Implementation",
                        "duration_days": 21,
                        "tasks": [
                            "Equipment procurement",
                            "Installation coordination",
                            "System commissioning",
                            "Testing and verification"
                        ],
                        "deliverables": [
                            "Installation documentation",
                            "Commissioning report",
                            "Test results",
                            "User manual"
                        ]
                    }
                ],
                "risk_factors": [
                    "Weather delays",
                    "Equipment delivery delays",
                    "Site access restrictions",
                    "Code compliance issues"
                ]
            },
            "hvac_residential": {
                "name": "Residential HVAC Project",
                "phases": [
                    {
                        "name": "Home Assessment",
                        "duration_days": 3,
                        "tasks": [
                            "Home energy audit",
                            "Existing system inspection",
                            "Insulation evaluation",
                            "Ductwork assessment"
                        ],
                        "deliverables": [
                            "Energy audit report",
                            "Upgrade recommendations",
                            "Cost-benefit analysis"
                        ]
                    },
                    {
                        "name": "System Design",
                        "duration_days": 7,
                        "tasks": [
                            "Load calculation",
                            "Equipment sizing",
                            "Ductwork design",
                            "Permit applications"
                        ],
                        "deliverables": [
                            "System design",
                            "Equipment list",
                            "Installation plan"
                        ]
                    },
                    {
                        "name": "Installation",
                        "duration_days": 5,
                        "tasks": [
                            "Equipment installation",
                            "Ductwork installation",
                            "System startup",
                            "Customer training"
                        ],
                        "deliverables": [
                            "Installation certificate",
                            "Warranty documentation",
                            "Maintenance schedule"
                        ]
                    }
                ],
                "risk_factors": [
                    "Access limitations",
                    "Structural modifications needed",
                    "Electrical upgrades required"
                ]
            }
        }
    
    def _load_risk_patterns(self) -> Dict[str, Any]:
        """Load common risk patterns and indicators"""
        return {
            "schedule_overrun": {
                "indicators": [
                    "Task completion rate < 80%",
                    "Multiple deadline extensions",
                    "Resource unavailability",
                    "Scope creep detected"
                ],
                "probability_factors": {
                    "complex_project": 0.3,
                    "new_team": 0.2,
                    "tight_deadline": 0.4,
                    "unclear_requirements": 0.5
                }
            },
            "budget_overrun": {
                "indicators": [
                    "Material cost increases > 10%",
                    "Unplanned scope changes",
                    "Inefficient resource utilization",
                    "Extended project duration"
                ],
                "probability_factors": {
                    "material_price_volatility": 0.25,
                    "scope_changes": 0.4,
                    "inexperienced_contractor": 0.3
                }
            },
            "quality_issues": {
                "indicators": [
                    "Test failures > 15%",
                    "Rework requests increasing",
                    "Client complaints",
                    "Inspection failures"
                ],
                "probability_factors": {
                    "rushed_schedule": 0.35,
                    "inadequate_supervision": 0.3,
                    "substandard_materials": 0.4
                }
            }
        }
    
    async def analyze_project_status(self, project_data: Dict[str, Any]) -> List[ProjectInsight]:
        """Analyze project status and generate AI insights"""
        insights = []
        
        try:
            # Analyze schedule performance
            schedule_insight = await self._analyze_schedule_performance(project_data)
            if schedule_insight:
                insights.append(schedule_insight)
            
            # Analyze budget performance
            budget_insight = await self._analyze_budget_performance(project_data)
            if budget_insight:
                insights.append(budget_insight)
            
            # Analyze resource utilization
            resource_insight = await self._analyze_resource_utilization(project_data)
            if resource_insight:
                insights.append(resource_insight)
            
            # Analyze quality metrics
            quality_insight = await self._analyze_quality_metrics(project_data)
            if quality_insight:
                insights.append(quality_insight)
            
            # Analyze stakeholder satisfaction
            stakeholder_insight = await self._analyze_stakeholder_satisfaction(project_data)
            if stakeholder_insight:
                insights.append(stakeholder_insight)
            
            logger.info(f"Generated {len(insights)} insights for project {project_data.get('id', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Error analyzing project status: {str(e)}")
        
        return insights
    
    async def _analyze_schedule_performance(self, project_data: Dict[str, Any]) -> Optional[ProjectInsight]:
        """Analyze project schedule performance"""
        try:
            planned_completion = datetime.fromisoformat(project_data.get("planned_completion", ""))
            actual_progress = project_data.get("completion_percentage", 0)
            current_date = datetime.now()
            
            # Calculate expected progress based on time elapsed
            total_duration = (planned_completion - datetime.fromisoformat(project_data.get("start_date", ""))).days
            elapsed_duration = (current_date - datetime.fromisoformat(project_data.get("start_date", ""))).days
            expected_progress = min((elapsed_duration / total_duration) * 100, 100)
            
            schedule_variance = actual_progress - expected_progress
            
            if schedule_variance < -10:  # Behind schedule
                return ProjectInsight(
                    type="schedule_alert",
                    title="Project Behind Schedule",
                    description=f"Project is {abs(schedule_variance):.1f}% behind schedule. "
                              f"Expected: {expected_progress:.1f}%, Actual: {actual_progress:.1f}%",
                    priority="high",
                    impact_score=0.8,
                    confidence=0.9,
                    recommendations=[
                        "Review and optimize critical path activities",
                        "Consider additional resources for bottleneck tasks",
                        "Implement daily progress tracking",
                        "Reassess project timeline and communicate with stakeholders"
                    ],
                    generated_at=datetime.now()
                )
            elif schedule_variance > 5:  # Ahead of schedule
                return ProjectInsight(
                    type="schedule_success",
                    title="Project Ahead of Schedule",
                    description=f"Project is {schedule_variance:.1f}% ahead of schedule. Excellent progress!",
                    priority="info",
                    impact_score=0.3,
                    confidence=0.9,
                    recommendations=[
                        "Maintain current pace",
                        "Consider early delivery benefits",
                        "Review resource allocation for other projects"
                    ],
                    generated_at=datetime.now()
                )
        except Exception as e:
            logger.error(f"Error analyzing schedule performance: {str(e)}")
        
        return None
    
    async def _analyze_budget_performance(self, project_data: Dict[str, Any]) -> Optional[ProjectInsight]:
        """Analyze project budget performance"""
        try:
            total_budget = project_data.get("total_budget", 0)
            spent_amount = project_data.get("spent_amount", 0)
            completion_percentage = project_data.get("completion_percentage", 0)
            
            if total_budget == 0:
                return None
            
            budget_utilization = (spent_amount / total_budget) * 100
            expected_utilization = completion_percentage
            
            budget_variance = budget_utilization - expected_utilization
            
            if budget_variance > 15:  # Over budget
                return ProjectInsight(
                    type="budget_alert",
                    title="Budget Overrun Risk",
                    description=f"Budget utilization ({budget_utilization:.1f}%) exceeds project progress "
                              f"({completion_percentage:.1f}%) by {budget_variance:.1f}%",
                    priority="high",
                    impact_score=0.9,
                    confidence=0.85,
                    recommendations=[
                        "Conduct detailed cost analysis",
                        "Review and approve all pending expenses",
                        "Identify cost reduction opportunities",
                        "Update budget forecast and communicate with stakeholders"
                    ],
                    generated_at=datetime.now()
                )
            elif budget_variance < -10:  # Under budget
                return ProjectInsight(
                    type="budget_efficiency",
                    title="Efficient Budget Utilization",
                    description=f"Project is running {abs(budget_variance):.1f}% under budget",
                    priority="info",
                    impact_score=0.4,
                    confidence=0.8,
                    recommendations=[
                        "Maintain cost discipline",
                        "Consider quality enhancements within budget",
                        "Document cost-saving practices for future projects"
                    ],
                    generated_at=datetime.now()
                )
        except Exception as e:
            logger.error(f"Error analyzing budget performance: {str(e)}")
        
        return None
    
    async def _analyze_resource_utilization(self, project_data: Dict[str, Any]) -> Optional[ProjectInsight]:
        """Analyze resource utilization efficiency"""
        try:
            team_members = project_data.get("team_members", [])
            if not team_members:
                return None
            
            total_utilization = 0
            overutilized_members = 0
            underutilized_members = 0
            
            for member in team_members:
                utilization = member.get("utilization_percentage", 0)
                total_utilization += utilization
                
                if utilization > 90:
                    overutilized_members += 1
                elif utilization < 60:
                    underutilized_members += 1
            
            avg_utilization = total_utilization / len(team_members)
            
            if overutilized_members > 0:
                return ProjectInsight(
                    type="resource_alert",
                    title="Team Overutilization Detected",
                    description=f"{overutilized_members} team member(s) are over 90% utilized. "
                              f"Average team utilization: {avg_utilization:.1f}%",
                    priority="medium",
                    impact_score=0.7,
                    confidence=0.8,
                    recommendations=[
                        "Redistribute workload among team members",
                        "Consider additional resources for critical tasks",
                        "Monitor team burnout indicators",
                        "Review task assignments and priorities"
                    ],
                    generated_at=datetime.now()
                )
            elif avg_utilization < 70:
                return ProjectInsight(
                    type="resource_optimization",
                    title="Resource Optimization Opportunity",
                    description=f"Average team utilization is {avg_utilization:.1f}%. "
                              f"Potential for resource optimization.",
                    priority="low",
                    impact_score=0.4,
                    confidence=0.7,
                    recommendations=[
                        "Evaluate task distribution",
                        "Consider parallel task execution",
                        "Assess if resources can be allocated to other projects",
                        "Review project scope for additional value-add activities"
                    ],
                    generated_at=datetime.now()
                )
        except Exception as e:
            logger.error(f"Error analyzing resource utilization: {str(e)}")
        
        return None
    
    async def _analyze_quality_metrics(self, project_data: Dict[str, Any]) -> Optional[ProjectInsight]:
        """Analyze project quality metrics"""
        try:
            quality_metrics = project_data.get("quality_metrics", {})
            if not quality_metrics:
                return None
            
            defect_rate = quality_metrics.get("defect_rate", 0)
            rework_percentage = quality_metrics.get("rework_percentage", 0)
            client_satisfaction = quality_metrics.get("client_satisfaction_score", 0)
            
            quality_issues = []
            if defect_rate > 5:
                quality_issues.append(f"High defect rate: {defect_rate}%")
            if rework_percentage > 10:
                quality_issues.append(f"High rework rate: {rework_percentage}%")
            if client_satisfaction < 7:
                quality_issues.append(f"Low client satisfaction: {client_satisfaction}/10")
            
            if quality_issues:
                return ProjectInsight(
                    type="quality_alert",
                    title="Quality Issues Detected",
                    description=f"Quality concerns identified: {', '.join(quality_issues)}",
                    priority="high",
                    impact_score=0.85,
                    confidence=0.8,
                    recommendations=[
                        "Implement additional quality control measures",
                        "Conduct root cause analysis for defects",
                        "Increase inspection frequency",
                        "Provide additional training to team members",
                        "Review and update quality standards"
                    ],
                    generated_at=datetime.now()
                )
            elif defect_rate < 2 and rework_percentage < 5 and client_satisfaction >= 8:
                return ProjectInsight(
                    type="quality_excellence",
                    title="Excellent Quality Performance",
                    description="Project demonstrates exceptional quality metrics across all areas",
                    priority="info",
                    impact_score=0.3,
                    confidence=0.9,
                    recommendations=[
                        "Document quality best practices",
                        "Share success factors with other projects",
                        "Consider this project as a benchmark",
                        "Maintain current quality standards"
                    ],
                    generated_at=datetime.now()
                )
        except Exception as e:
            logger.error(f"Error analyzing quality metrics: {str(e)}")
        
        return None
    
    async def _analyze_stakeholder_satisfaction(self, project_data: Dict[str, Any]) -> Optional[ProjectInsight]:
        """Analyze stakeholder satisfaction and communication"""
        try:
            stakeholders = project_data.get("stakeholders", [])
            if not stakeholders:
                return None
            
            satisfaction_scores = []
            communication_issues = 0
            
            for stakeholder in stakeholders:
                satisfaction = stakeholder.get("satisfaction_score", 0)
                satisfaction_scores.append(satisfaction)
                
                last_contact = stakeholder.get("last_contact_days_ago", 0)
                if last_contact > 7:  # No contact for more than a week
                    communication_issues += 1
            
            avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
            
            if avg_satisfaction < 7 or communication_issues > 0:
                return ProjectInsight(
                    type="stakeholder_alert",
                    title="Stakeholder Engagement Issues",
                    description=f"Average satisfaction: {avg_satisfaction:.1f}/10. "
                              f"{communication_issues} stakeholder(s) need communication attention.",
                    priority="medium",
                    impact_score=0.6,
                    confidence=0.8,
                    recommendations=[
                        "Schedule stakeholder check-in meetings",
                        "Improve communication frequency",
                        "Address specific stakeholder concerns",
                        "Provide regular project updates",
                        "Implement stakeholder feedback system"
                    ],
                    generated_at=datetime.now()
                )
            elif avg_satisfaction >= 8.5:
                return ProjectInsight(
                    type="stakeholder_success",
                    title="High Stakeholder Satisfaction",
                    description=f"Excellent stakeholder satisfaction: {avg_satisfaction:.1f}/10",
                    priority="info",
                    impact_score=0.2,
                    confidence=0.9,
                    recommendations=[
                        "Maintain current communication practices",
                        "Document successful engagement strategies",
                        "Consider stakeholder testimonials",
                        "Continue regular updates"
                    ],
                    generated_at=datetime.now()
                )
        except Exception as e:
            logger.error(f"Error analyzing stakeholder satisfaction: {str(e)}")
        
        return None
    
    async def identify_project_risks(self, project_data: Dict[str, Any]) -> List[ProjectRisk]:
        """Identify potential project risks using AI analysis"""
        risks = []
        
        try:
            # Analyze schedule risks
            schedule_risks = await self._analyze_schedule_risks(project_data)
            risks.extend(schedule_risks)
            
            # Analyze budget risks
            budget_risks = await self._analyze_budget_risks(project_data)
            risks.extend(budget_risks)
            
            # Analyze technical risks
            technical_risks = await self._analyze_technical_risks(project_data)
            risks.extend(technical_risks)
            
            # Analyze resource risks
            resource_risks = await self._analyze_resource_risks(project_data)
            risks.extend(resource_risks)
            
            logger.info(f"Identified {len(risks)} risks for project {project_data.get('id', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Error identifying project risks: {str(e)}")
        
        return risks
    
    async def _analyze_schedule_risks(self, project_data: Dict[str, Any]) -> List[ProjectRisk]:
        """Analyze schedule-related risks"""
        risks = []
        
        try:
            completion_percentage = project_data.get("completion_percentage", 0)
            planned_completion = datetime.fromisoformat(project_data.get("planned_completion", ""))
            days_remaining = (planned_completion - datetime.now()).days
            
            if days_remaining < 30 and completion_percentage < 80:
                risk_score = min(((80 - completion_percentage) / 80) * 0.8 + 0.2, 1.0)
                
                risks.append(ProjectRisk(
                    id=f"schedule_risk_{int(datetime.now().timestamp())}",
                    title="Schedule Compression Risk",
                    description=f"Only {days_remaining} days remaining with {completion_percentage}% completion",
                    category="schedule",
                    probability=0.8,
                    impact=0.9,
                    risk_score=risk_score,
                    level=RiskLevel.HIGH if risk_score > 0.7 else RiskLevel.MEDIUM,
                    mitigation_strategies=[
                        "Fast-track critical path activities",
                        "Add resources to bottleneck tasks",
                        "Consider scope reduction if possible",
                        "Implement crash program with overtime"
                    ],
                    identified_at=datetime.now()
                ))
        except Exception as e:
            logger.error(f"Error analyzing schedule risks: {str(e)}")
        
        return risks
    
    async def _analyze_budget_risks(self, project_data: Dict[str, Any]) -> List[ProjectRisk]:
        """Analyze budget-related risks"""
        risks = []
        
        try:
            total_budget = project_data.get("total_budget", 0)
            spent_amount = project_data.get("spent_amount", 0)
            completion_percentage = project_data.get("completion_percentage", 0)
            
            if total_budget > 0:
                spend_rate = spent_amount / total_budget
                progress_rate = completion_percentage / 100
                
                if spend_rate > progress_rate + 0.15:  # Spending faster than progress
                    risk_score = min((spend_rate - progress_rate) * 2, 1.0)
                    
                    risks.append(ProjectRisk(
                        id=f"budget_risk_{int(datetime.now().timestamp())}",
                        title="Budget Overrun Risk",
                        description=f"Spend rate ({spend_rate:.1%}) exceeds progress rate ({progress_rate:.1%})",
                        category="budget",
                        probability=0.7,
                        impact=0.8,
                        risk_score=risk_score,
                        level=RiskLevel.HIGH if risk_score > 0.7 else RiskLevel.MEDIUM,
                        mitigation_strategies=[
                            "Implement strict cost controls",
                            "Review all pending expenses",
                            "Renegotiate vendor contracts",
                            "Seek budget increase approval if justified"
                        ],
                        identified_at=datetime.now()
                    ))
        except Exception as e:
            logger.error(f"Error analyzing budget risks: {str(e)}")
        
        return risks
    
    async def _analyze_technical_risks(self, project_data: Dict[str, Any]) -> List[ProjectRisk]:
        """Analyze technical risks"""
        risks = []
        
        try:
            complexity_score = project_data.get("complexity_score", 0)
            team_experience = project_data.get("team_experience_score", 0)
            technology_maturity = project_data.get("technology_maturity_score", 0)
            
            if complexity_score > 7 and team_experience < 6:
                risk_score = (complexity_score - team_experience) / 10
                
                risks.append(ProjectRisk(
                    id=f"technical_risk_{int(datetime.now().timestamp())}",
                    title="Technical Complexity vs Experience Gap",
                    description=f"High complexity ({complexity_score}/10) with limited team experience ({team_experience}/10)",
                    category="technical",
                    probability=0.6,
                    impact=0.7,
                    risk_score=risk_score,
                    level=RiskLevel.MEDIUM if risk_score > 0.5 else RiskLevel.LOW,
                    mitigation_strategies=[
                        "Bring in technical experts or consultants",
                        "Provide additional training to team",
                        "Implement more frequent technical reviews",
                        "Create detailed technical documentation"
                    ],
                    identified_at=datetime.now()
                ))
        except Exception as e:
            logger.error(f"Error analyzing technical risks: {str(e)}")
        
        return risks
    
    async def _analyze_resource_risks(self, project_data: Dict[str, Any]) -> List[ProjectRisk]:
        """Analyze resource-related risks"""
        risks = []
        
        try:
            team_members = project_data.get("team_members", [])
            key_personnel = [m for m in team_members if m.get("is_critical", False)]
            
            for person in key_personnel:
                availability = person.get("availability_percentage", 100)
                workload = person.get("utilization_percentage", 0)
                
                if availability < 80 or workload > 90:
                    risk_score = max((100 - availability) / 100, (workload - 90) / 100)
                    
                    risks.append(ProjectRisk(
                        id=f"resource_risk_{person.get('id', 'unknown')}",
                        title=f"Key Personnel Risk: {person.get('name', 'Unknown')}",
                        description=f"Critical team member has {availability}% availability and {workload}% workload",
                        category="resource",
                        probability=0.6,
                        impact=0.8,
                        risk_score=risk_score,
                        level=RiskLevel.HIGH if risk_score > 0.7 else RiskLevel.MEDIUM,
                        mitigation_strategies=[
                            "Cross-train other team members",
                            "Document critical knowledge and processes",
                            "Identify backup resources",
                            "Adjust workload distribution"
                        ],
                        identified_at=datetime.now()
                    ))
        except Exception as e:
            logger.error(f"Error analyzing resource risks: {str(e)}")
        
        return risks
    
    async def generate_project_recommendations(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive project recommendations"""
        try:
            insights = await self.analyze_project_status(project_data)
            risks = await self.identify_project_risks(project_data)
            
            # Prioritize recommendations based on impact and urgency
            high_priority_actions = []
            medium_priority_actions = []
            low_priority_actions = []
            
            for insight in insights:
                if insight.priority == "high":
                    high_priority_actions.extend(insight.recommendations)
                elif insight.priority == "medium":
                    medium_priority_actions.extend(insight.recommendations)
                else:
                    low_priority_actions.extend(insight.recommendations)
            
            # Add risk mitigation actions
            for risk in risks:
                if risk.level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
                    high_priority_actions.extend(risk.mitigation_strategies)
                elif risk.level == RiskLevel.MEDIUM:
                    medium_priority_actions.extend(risk.mitigation_strategies)
            
            return {
                "project_id": project_data.get("id"),
                "analysis_timestamp": datetime.now().isoformat(),
                "overall_health_score": self._calculate_project_health_score(insights, risks),
                "insights_count": len(insights),
                "risks_count": len(risks),
                "recommendations": {
                    "high_priority": list(set(high_priority_actions)),
                    "medium_priority": list(set(medium_priority_actions)),
                    "low_priority": list(set(low_priority_actions))
                },
                "insights": [
                    {
                        "type": insight.type,
                        "title": insight.title,
                        "description": insight.description,
                        "priority": insight.priority,
                        "impact_score": insight.impact_score,
                        "confidence": insight.confidence
                    }
                    for insight in insights
                ],
                "risks": [
                    {
                        "id": risk.id,
                        "title": risk.title,
                        "description": risk.description,
                        "category": risk.category,
                        "level": risk.level.value,
                        "risk_score": risk.risk_score
                    }
                    for risk in risks
                ]
            }
        except Exception as e:
            logger.error(f"Error generating project recommendations: {str(e)}")
            return {"error": str(e)}
    
    def _calculate_project_health_score(self, insights: List[ProjectInsight], risks: List[ProjectRisk]) -> float:
        """Calculate overall project health score (0-100)"""
        base_score = 85.0  # Start with good baseline
        
        # Deduct points for negative insights
        for insight in insights:
            if insight.priority == "high" and "alert" in insight.type:
                base_score -= insight.impact_score * 15
            elif insight.priority == "medium" and "alert" in insight.type:
                base_score -= insight.impact_score * 8
        
        # Deduct points for risks
        for risk in risks:
            if risk.level == RiskLevel.CRITICAL:
                base_score -= risk.risk_score * 20
            elif risk.level == RiskLevel.HIGH:
                base_score -= risk.risk_score * 10
            elif risk.level == RiskLevel.MEDIUM:
                base_score -= risk.risk_score * 5
        
        # Add points for positive insights
        for insight in insights:
            if "success" in insight.type or "excellence" in insight.type:
                base_score += insight.impact_score * 5
        
        return max(0, min(100, base_score))

# Singleton instance
ai_project_manager = AIProjectManager()
