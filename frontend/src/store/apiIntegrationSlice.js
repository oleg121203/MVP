import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch API integrations
export const fetchApiIntegrations = createAsyncThunk('apiIntegrations/fetchApiIntegrations', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/integrations');
    if (!response.ok) {
      throw new Error('Failed to fetch API integrations');
    }
    const data = await response.json();
    return data.integrations;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new API integration
export const createApiIntegration = createAsyncThunk('apiIntegrations/createApiIntegration', async (integrationData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/integrations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(integrationData),
    });
    if (!response.ok) {
      throw new Error('Failed to create API integration');
    }
    const data = await response.json();
    return data.integration;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing API integration
export const updateApiIntegration = createAsyncThunk('apiIntegrations/updateApiIntegration', async (integrationData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/integrations/${integrationData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(integrationData),
    });
    if (!response.ok) {
      throw new Error('Failed to update API integration');
    }
    const data = await response.json();
    return data.integration;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete an API integration
export const deleteApiIntegration = createAsyncThunk('apiIntegrations/deleteApiIntegration', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/integrations/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete API integration');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const apiIntegrationSlice = createSlice({
  name: 'apiIntegrations',
  initialState: {
    integrations: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchApiIntegrations.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchApiIntegrations.fulfilled, (state, action) => {
        state.loading = false;
        state.integrations = action.payload;
      })
      .addCase(fetchApiIntegrations.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createApiIntegration.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createApiIntegration.fulfilled, (state, action) => {
        state.loading = false;
        state.integrations.push(action.payload);
      })
      .addCase(createApiIntegration.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateApiIntegration.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateApiIntegration.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.integrations.findIndex(integration => integration.id === action.payload.id);
        if (index !== -1) {
          state.integrations[index] = action.payload;
        }
      })
      .addCase(updateApiIntegration.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteApiIntegration.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteApiIntegration.fulfilled, (state, action) => {
        state.loading = false;
        state.integrations = state.integrations.filter(integration => integration.id !== action.payload);
      })
      .addCase(deleteApiIntegration.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default apiIntegrationSlice.reducer;
