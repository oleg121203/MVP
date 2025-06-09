/**
 * Analytics module type definitions
 * @module interfaces/analytics
 * @see VENTAI_ENTERPRISE_PLAN.md [P1.2-T3]
 */

export interface ProjectMetrics {
  projectId: string;
  costAnalysis: {
    currentSpend: number;
    projectedSpend: number;
    variance: number;
    optimizationOpportunities: OptimizationOpportunity[];
  };
  timelineMetrics: {
    currentProgress: number;
    projectedCompletion: Date;
    criticalPathItems: string[];
  };
  lastUpdated: Date;
}

export interface OptimizationOpportunity {
  area: string;
  potentialSavings: number;
  confidenceScore: number;
  recommendedActions: string[];
}
