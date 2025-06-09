export interface OptimizationOpportunity {
  category: string;
  item: string;
  currentCost: number;
  recommendedAlternative: string;
  potentialSavings: number;
  impact: string;
}

export interface CostAnalysis {
  currentSpend: number;
  projectedSpend: number;
  variance: number;
  optimizationOpportunities: OptimizationOpportunity[];
}

export interface RiskAssessment {
  highRiskItems: number;
  mediumRiskItems: number;
  lowRiskItems: number;
}

export interface TimelineMetrics {
  currentProgress: number;
  projectedCompletion: Date;
  criticalPathItems: string[];
  riskAssessment: RiskAssessment;
}

export interface QualityMetrics {
  complianceScore: number;
  outstandingIssues: number;
  lastInspectionDate: Date;
}

export interface SustainabilityMetrics {
  carbonFootprint: number;
  energyEfficiency: number;
  waterUsage: number;
  wasteReduction: number;
}

export interface ProjectMetrics {
  projectId: string;
  costAnalysis: CostAnalysis;
  timelineMetrics: TimelineMetrics;
  qualityMetrics: QualityMetrics;
  sustainabilityMetrics?: SustainabilityMetrics;
  lastUpdated: Date;
}
