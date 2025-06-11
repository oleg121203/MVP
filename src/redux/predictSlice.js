import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Mock prediction API
const runPredictionAPI = async (inputData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        prediction: Math.random() * 100,
        confidence: Math.random(),
        inputData
      });
    }, 1500);
  });
};

export const runPrediction = createAsyncThunk(
  'predict/run',
  async (inputData) => {
    const response = await runPredictionAPI(inputData);
    return response;
  }
);

const predictSlice = createSlice({
  name: 'predict',
  initialState: {
    result: null,
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(runPrediction.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(runPrediction.fulfilled, (state, action) => {
        state.loading = false;
        state.result = action.payload;
      })
      .addCase(runPrediction.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export default predictSlice.reducer;
