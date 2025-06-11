import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to connect to an external data source
export const connectExternalDataSource = createAsyncThunk('externalData/connectExternalDataSource', async (connectionInfo, { rejectWithValue }) => {
  try {
    // This would be a real API call in a complete implementation
    // For now, simulate a successful connection
    return { type: connectionInfo.type, status: 'connected' };
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch data from the connected external source
export const fetchExternalData = createAsyncThunk('externalData/fetchExternalData', async (_, { rejectWithValue }) => {
  try {
    // Simulate fetching data from an external source
    // In a real implementation, this would call the actual API or database
    const mockData = [
      { id: 1, name: 'External Data 1', value: 100 },
      { id: 2, name: 'External Data 2', value: 200 },
      { id: 3, name: 'External Data 3', value: 300 },
    ];
    return mockData;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const externalDataSlice = createSlice({
  name: 'externalData',
  initialState: {
    data: [],
    loading: false,
    error: null,
    connectionStatus: 'disconnected', // disconnected, connecting, connected
    connectionType: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(connectExternalDataSource.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.connectionStatus = 'connecting';
      })
      .addCase(connectExternalDataSource.fulfilled, (state, action) => {
        state.loading = false;
        state.connectionStatus = action.payload.status;
        state.connectionType = action.payload.type;
      })
      .addCase(connectExternalDataSource.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.connectionStatus = 'disconnected';
      })
      .addCase(fetchExternalData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchExternalData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchExternalData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default externalDataSlice.reducer;
