import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8001/api/analytics';

export const fetchProjectMetrics = createAsyncThunk(
  'analytics/fetchProjectMetrics',
  async (projectId, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${API_URL}/metrics/${projectId}`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchRealTimeInsights = createAsyncThunk(
  'analytics/fetchRealTimeInsights',
  async (projectId, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${API_URL}/insights/${projectId}`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState: {
    metrics: {},
    insights: [],
    loading: false,
    error: null
  },
  reducers: {
    updateInsights: (state, action) => {
      state.insights = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProjectMetrics.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProjectMetrics.fulfilled, (state, action) => {
        state.loading = false;
        state.metrics = action.payload;
      })
      .addCase(fetchProjectMetrics.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchRealTimeInsights.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRealTimeInsights.fulfilled, (state, action) => {
        state.loading = false;
        state.insights = action.payload;
      })
      .addCase(fetchRealTimeInsights.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

export const { updateInsights } = analyticsSlice.actions;
export default analyticsSlice.reducer;
