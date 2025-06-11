import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch platform connections
export const fetchPlatformConnections = createAsyncThunk('integration/fetchPlatformConnections', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/integrations/external/connections');
    if (!response.ok) {
      throw new Error('Failed to fetch platform connections');
    }
    const data = await response.json();
    return data.connections;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to connect a platform
export const connectPlatform = createAsyncThunk('integration/connectPlatform', async ({ platform, token, settings }, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/integrations/external/connect/${platform}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token, settings }),
    });
    if (!response.ok) {
      throw new Error('Failed to connect platform');
    }
    const data = await response.json();
    return data.connection;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to disconnect a platform
export const disconnectPlatform = createAsyncThunk('integration/disconnectPlatform', async (platformId, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/integrations/external/disconnect/${platformId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to disconnect platform');
    }
    return platformId;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to sync platform data
export const syncPlatformData = createAsyncThunk('integration/syncPlatformData', async (platformId, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/integrations/external/sync/${platformId}`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to sync platform data');
    }
    const data = await response.json();
    return data.result;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const integrationSlice = createSlice({
  name: 'integration',
  initialState: {
    connections: [],
    loading: false,
    error: null,
    syncStatus: 'idle',
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPlatformConnections.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPlatformConnections.fulfilled, (state, action) => {
        state.loading = false;
        state.connections = action.payload;
      })
      .addCase(fetchPlatformConnections.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(connectPlatform.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(connectPlatform.fulfilled, (state, action) => {
        state.loading = false;
        state.connections.push(action.payload);
      })
      .addCase(connectPlatform.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(disconnectPlatform.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(disconnectPlatform.fulfilled, (state, action) => {
        state.loading = false;
        state.connections = state.connections.filter(conn => conn.platformId !== action.payload);
      })
      .addCase(disconnectPlatform.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(syncPlatformData.pending, (state) => {
        state.loading = true;
        state.syncStatus = 'syncing';
        state.error = null;
      })
      .addCase(syncPlatformData.fulfilled, (state) => {
        state.loading = false;
        state.syncStatus = 'success';
      })
      .addCase(syncPlatformData.rejected, (state, action) => {
        state.loading = false;
        state.syncStatus = 'error';
        state.error = action.payload;
      });
  },
});

export default integrationSlice.reducer;
