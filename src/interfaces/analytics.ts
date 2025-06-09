export interface ProjectAnalytics {
  id: string;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1Score: number;
  };
  timestamps: string[];
  values: number[];
}

export interface AnalyticsState {
  data: ProjectAnalytics | null;
  loading: boolean;
  error: string | null;
}
