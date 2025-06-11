import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk for login
export const login = createAsyncThunk('auth/login', async (credentials, { rejectWithValue }) => {
  try {
    // In a real implementation, this would call an API endpoint for authentication
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    if (!response.ok) {
      throw new Error('Authentication failed');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk for logout
export const logout = createAsyncThunk('auth/logout', async (_, { rejectWithValue }) => {
  try {
    // In a real implementation, this would call an API endpoint to invalidate the session
    const response = await fetch('/api/auth/logout', {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Logout failed');
    }
    return;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk for enabling MFA
export const enableMFA = createAsyncThunk('auth/enableMFA', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/auth/mfa/enable', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to enable MFA');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk for disabling MFA
export const disableMFA = createAsyncThunk('auth/disableMFA', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/auth/mfa/disable', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to disable MFA');
    }
    return true;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk for verifying MFA code
export const verifyMFACode = createAsyncThunk('auth/verifyMFACode', async (code, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/auth/mfa/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });
    if (!response.ok) {
      throw new Error('Failed to verify MFA code');
    }
    return true;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    isAuthenticated: false,
    user: null,
    token: null,
    loading: false,
    error: null,
    mfaEnabled: false,
    mfaError: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(logout.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(logout.fulfilled, (state) => {
        state.loading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      })
      .addCase(logout.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(enableMFA.pending, (state) => {
        state.loading = true;
        state.mfaError = null;
      })
      .addCase(enableMFA.fulfilled, (state) => {
        state.loading = false;
        state.mfaEnabled = true;
      })
      .addCase(enableMFA.rejected, (state, action) => {
        state.loading = false;
        state.mfaError = action.payload;
      })
      .addCase(disableMFA.pending, (state) => {
        state.loading = true;
        state.mfaError = null;
      })
      .addCase(disableMFA.fulfilled, (state) => {
        state.loading = false;
        state.mfaEnabled = false;
      })
      .addCase(disableMFA.rejected, (state, action) => {
        state.loading = false;
        state.mfaError = action.payload;
      })
      .addCase(verifyMFACode.pending, (state) => {
        state.loading = true;
        state.mfaError = null;
      })
      .addCase(verifyMFACode.fulfilled, (state) => {
        state.loading = false;
        state.mfaEnabled = true;
      })
      .addCase(verifyMFACode.rejected, (state, action) => {
        state.loading = false;
        state.mfaError = action.payload;
      });
  },
});

export default authSlice.reducer;
