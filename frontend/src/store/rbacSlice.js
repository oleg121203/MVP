import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch RBAC rules
export const fetchRBACRules = createAsyncThunk('rbac/fetchRBACRules', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/rbac/rules');
    if (!response.ok) {
      throw new Error('Failed to fetch RBAC rules');
    }
    const data = await response.json();
    return data.rules;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new RBAC rule
export const createRBACRule = createAsyncThunk('rbac/createRBACRule', async (ruleData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/rbac/rules', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(ruleData),
    });
    if (!response.ok) {
      throw new Error('Failed to create RBAC rule');
    }
    const data = await response.json();
    return data.rule;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing RBAC rule
export const updateRBACRule = createAsyncThunk('rbac/updateRBACRule', async (ruleData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/rbac/rules/${ruleData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(ruleData),
    });
    if (!response.ok) {
      throw new Error('Failed to update RBAC rule');
    }
    const data = await response.json();
    return data.rule;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete an RBAC rule
export const deleteRBACRule = createAsyncThunk('rbac/deleteRBACRule', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/rbac/rules/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete RBAC rule');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const rbacSlice = createSlice({
  name: 'rbac',
  initialState: {
    rbacRules: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchRBACRules.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRBACRules.fulfilled, (state, action) => {
        state.loading = false;
        state.rbacRules = action.payload;
      })
      .addCase(fetchRBACRules.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createRBACRule.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createRBACRule.fulfilled, (state, action) => {
        state.loading = false;
        state.rbacRules.push(action.payload);
      })
      .addCase(createRBACRule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateRBACRule.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateRBACRule.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.rbacRules.findIndex(rule => rule.id === action.payload.id);
        if (index !== -1) {
          state.rbacRules[index] = action.payload;
        }
      })
      .addCase(updateRBACRule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteRBACRule.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteRBACRule.fulfilled, (state, action) => {
        state.loading = false;
        state.rbacRules = state.rbacRules.filter(rule => rule.id !== action.payload);
      })
      .addCase(deleteRBACRule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default rbacSlice.reducer;
