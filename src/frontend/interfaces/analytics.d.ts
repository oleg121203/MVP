interface AnalyticsMetric {
    value: number;
    trend: 'up' | 'down' | 'stable';
    lastUpdated: string;
  }
  
  interface ProjectAnalytics {
    completionRate: AnalyticsMetric;
    budgetUtilization: AnalyticsMetric; 
    timeEfficiency: AnalyticsMetric;
    insights: string[];
  }
  
  export type { ProjectAnalytics, AnalyticsMetric };