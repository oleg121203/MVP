import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { ProjectAnalytics } from '../interfaces/analytics';

interface AnalyticsState {
  data: ProjectAnalytics | null;
  loading: boolean;
  error: string | null;
}

const initialState: AnalyticsState = {
  data: null,
  loading: false,
  error: null
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    setAnalyticsData(state, action: PayloadAction<ProjectAnalytics>) {
      state.data = action.payload;
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setError(state, action: PayloadAction<string>) {
      state.error = action.payload;
    }
  }
});

export const { setAnalyticsData, setLoading, setError } = analyticsSlice.actions;
export default analyticsSlice.reducer;// src/frontend/interfaces/analytics.d.ts
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