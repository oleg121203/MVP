import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { mockAnalyticsData } from '../components/analytics/mockData';

// Async thunk to fetch analytics data
export const getAnalyticsData = createAsyncThunk(
  'analytics/getAnalyticsData',
  async (_, { rejectWithValue }) => {
    try {
      // For testing purposes, return mock data
      // const response = await axios.get('/api/analytics/data');
      // return response.data;
      return mockAnalyticsData;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Initial state
const initialState = {
  data: [],
  loading: false,
  error: null,
};

// Analytics slice
const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getAnalyticsData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getAnalyticsData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(getAnalyticsData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default analyticsSlice.reducer;
