import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ProjectAnalytics } from '../../interfaces/analytics';

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

export const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    fetchStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchSuccess: (state, action: PayloadAction<ProjectAnalytics>) => {
      state.data = action.payload;
      state.loading = false;
    },
    fetchFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    }
  }
});

export const { fetchStart, fetchSuccess, fetchFailure } = analyticsSlice.actions;
export default analyticsSlice.reducer;
