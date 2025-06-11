import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch sales data
export const fetchSalesData = createAsyncThunk('salesAnalytics/fetchSalesData', async (viewMode, { rejectWithValue }) => {
  try {
    // In a real implementation, this would fetch from an API endpoint
    // For now, return mock data based on the view mode
    let data = [];
    switch (viewMode) {
      case 'weekly':
        data = [
          { date: 'Week 1', sales: 5000, leads: 200, conversionRate: 2.5 },
          { date: 'Week 2', sales: 7000, leads: 250, conversionRate: 2.8 },
          { date: 'Week 3', sales: 6000, leads: 220, conversionRate: 2.7 },
          { date: 'Week 4', sales: 8000, leads: 280, conversionRate: 2.9 },
        ];
        break;
      case 'monthly':
        data = [
          { date: 'Jan', sales: 20000, leads: 800, conversionRate: 2.5 },
          { date: 'Feb', sales: 25000, leads: 900, conversionRate: 2.8 },
          { date: 'Mar', sales: 22000, leads: 850, conversionRate: 2.6 },
          { date: 'Apr', sales: 28000, leads: 950, conversionRate: 2.9 },
          { date: 'May', sales: 30000, leads: 1000, conversionRate: 3.0 },
          { date: 'Jun', sales: 27000, leads: 920, conversionRate: 2.9 },
        ];
        break;
      case 'quarterly':
        data = [
          { date: 'Q1', sales: 65000, leads: 2500, conversionRate: 2.6 },
          { date: 'Q2', sales: 80000, leads: 3000, conversionRate: 2.7 },
          { date: 'Q3', sales: 75000, leads: 2800, conversionRate: 2.7 },
          { date: 'Q4', sales: 85000, leads: 3200, conversionRate: 2.7 },
        ];
        break;
      case 'yearly':
        data = [
          { date: '2021', sales: 250000, leads: 10000, conversionRate: 2.5 },
          { date: '2022', sales: 300000, leads: 12000, conversionRate: 2.5 },
          { date: '2023', sales: 280000, leads: 11000, conversionRate: 2.5 },
          { date: '2024', sales: 320000, leads: 13000, conversionRate: 2.5 },
          { date: '2025', sales: 350000, leads: 14000, conversionRate: 2.5 },
        ];
        break;
      default:
        data = [];
    }
    return data;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const salesAnalyticsSlice = createSlice({
  name: 'salesAnalytics',
  initialState: {
    data: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchSalesData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSalesData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchSalesData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default salesAnalyticsSlice.reducer;
