import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch sync configurations
export const fetchSyncConfigs = createAsyncThunk('dataSync/fetchSyncConfigs', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/sync-configs');
    if (!response.ok) {
      throw new Error('Failed to fetch sync configurations');
    }
    const data = await response.json();
    return data.configs;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new sync configuration
export const createSyncConfig = createAsyncThunk('dataSync/createSyncConfig', async (configData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/sync-configs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(configData),
    });
    if (!response.ok) {
      throw new Error('Failed to create sync configuration');
    }
    const data = await response.json();
    return data.config;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing sync configuration
export const updateSyncConfig = createAsyncThunk('dataSync/updateSyncConfig', async (configData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/sync-configs/${configData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(configData),
    });
    if (!response.ok) {
      throw new Error('Failed to update sync configuration');
    }
    const data = await response.json();
    return data.config;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete a sync configuration
export const deleteSyncConfig = createAsyncThunk('dataSync/deleteSyncConfig', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/sync-configs/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete sync configuration');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to start a sync operation
export const startSync = createAsyncThunk('dataSync/startSync', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/sync-configs/${id}/start`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to start sync operation');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const dataSyncSlice = createSlice({
  name: 'dataSync',
  initialState: {
    syncConfigs: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchSyncConfigs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSyncConfigs.fulfilled, (state, action) => {
        state.loading = false;
        state.syncConfigs = action.payload;
      })
      .addCase(fetchSyncConfigs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createSyncConfig.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createSyncConfig.fulfilled, (state, action) => {
        state.loading = false;
        state.syncConfigs.push(action.payload);
      })
      .addCase(createSyncConfig.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateSyncConfig.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateSyncConfig.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.syncConfigs.findIndex(config => config.id === action.payload.id);
        if (index !== -1) {
          state.syncConfigs[index] = action.payload;
        }
      })
      .addCase(updateSyncConfig.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteSyncConfig.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteSyncConfig.fulfilled, (state, action) => {
        state.loading = false;
        state.syncConfigs = state.syncConfigs.filter(config => config.id !== action.payload);
      })
      .addCase(deleteSyncConfig.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(startSync.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(startSync.fulfilled, (state, action) => {
        state.loading = false;
        // Optionally update the status of the sync config to indicate it's running
        const index = state.syncConfigs.findIndex(config => config.id === action.payload);
        if (index !== -1) {
          state.syncConfigs[index].status = 'running';
        }
      })
      .addCase(startSync.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default dataSyncSlice.reducer;
