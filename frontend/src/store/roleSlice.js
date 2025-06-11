import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch roles
export const fetchRoles = createAsyncThunk('roles/fetchRoles', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/roles');
    if (!response.ok) {
      throw new Error('Failed to fetch roles');
    }
    const data = await response.json();
    return data.roles;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new role
export const createRole = createAsyncThunk('roles/createRole', async (roleData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/roles', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(roleData),
    });
    if (!response.ok) {
      throw new Error('Failed to create role');
    }
    const data = await response.json();
    return data.role;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing role
export const updateRole = createAsyncThunk('roles/updateRole', async (roleData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/roles/${roleData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(roleData),
    });
    if (!response.ok) {
      throw new Error('Failed to update role');
    }
    const data = await response.json();
    return data.role;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete a role
export const deleteRole = createAsyncThunk('roles/deleteRole', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/roles/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete role');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const roleSlice = createSlice({
  name: 'roles',
  initialState: {
    roles: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchRoles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRoles.fulfilled, (state, action) => {
        state.loading = false;
        state.roles = action.payload;
      })
      .addCase(fetchRoles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createRole.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createRole.fulfilled, (state, action) => {
        state.loading = false;
        state.roles.push(action.payload);
      })
      .addCase(createRole.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateRole.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateRole.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.roles.findIndex(role => role.id === action.payload.id);
        if (index !== -1) {
          state.roles[index] = action.payload;
        }
      })
      .addCase(updateRole.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteRole.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteRole.fulfilled, (state, action) => {
        state.loading = false;
        state.roles = state.roles.filter(role => role.id !== action.payload);
      })
      .addCase(deleteRole.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default roleSlice.reducer;
