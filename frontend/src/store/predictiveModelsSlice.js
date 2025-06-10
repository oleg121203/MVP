import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch predictive data
export const getPredictiveData = createAsyncThunk('predictiveModels/getPredictiveData', async (_, { rejectWithValue }) => {
  try {
    // Fetch from backend API
    const response = await fetch('/api/predictive/cost-trend?future_days=7');
    if (!response.ok) {
      throw new Error('Failed to fetch predictive data');
    }
    const data = await response.json();
    return data.predictions;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const predictiveModelsSlice = createSlice({
  name: 'predictiveModels',
  initialState: {
    data: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getPredictiveData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getPredictiveData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(getPredictiveData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default predictiveModelsSlice.reducer;
