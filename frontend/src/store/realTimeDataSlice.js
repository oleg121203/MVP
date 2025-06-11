import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to start streaming data
export const startStreaming = createAsyncThunk('realTimeData/startStreaming', async (_, { rejectWithValue }) => {
  try {
    // In a real implementation, this would establish a WebSocket connection or other streaming mechanism
    // For now, simulate starting a stream
    return { status: 'streaming' };
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to stop streaming data
export const stopStreaming = createAsyncThunk('realTimeData/stopStreaming', async (_, { rejectWithValue }) => {
  try {
    // In a real implementation, this would close the WebSocket connection or streaming mechanism
    // For now, simulate stopping a stream
    return { status: 'stopped' };
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const realTimeDataSlice = createSlice({
  name: 'realTimeData',
  initialState: {
    data: [],
    streaming: false,
    error: null,
  },
  reducers: {
    // This reducer would be called by WebSocket onmessage in a real app to update data
    updateData: (state, action) => {
      state.data.push(action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(startStreaming.pending, (state) => {
        state.error = null;
      })
      .addCase(startStreaming.fulfilled, (state, action) => {
        state.streaming = true;
      })
      .addCase(startStreaming.rejected, (state, action) => {
        state.error = action.payload;
      })
      .addCase(stopStreaming.pending, (state) => {
        state.error = null;
      })
      .addCase(stopStreaming.fulfilled, (state, action) => {
        state.streaming = false;
      })
      .addCase(stopStreaming.rejected, (state, action) => {
        state.error = action.payload;
      });
  },
});

export const { updateData } = realTimeDataSlice.actions;
export default realTimeDataSlice.reducer;
