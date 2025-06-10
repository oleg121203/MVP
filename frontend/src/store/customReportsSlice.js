import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch custom reports
export const getCustomReports = createAsyncThunk('customReports/getCustomReports', async (reportType, { rejectWithValue }) => {
  try {
    // Fetch from backend API
    const response = await fetch(`/api/analytics/custom-report?type=${reportType}`);
    if (!response.ok) {
      throw new Error('Failed to fetch custom reports');
    }
    const data = await response.json();
    return data.reports;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const customReportsSlice = createSlice({
  name: 'customReports',
  initialState: {
    data: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getCustomReports.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getCustomReports.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(getCustomReports.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default customReportsSlice.reducer;
