import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch encryption settings
export const fetchEncryptionSettings = createAsyncThunk('encryption/fetchEncryptionSettings', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/encryption/settings');
    if (!response.ok) {
      throw new Error('Failed to fetch encryption settings');
    }
    const data = await response.json();
    return data.settings;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update encryption settings
export const updateEncryptionSettings = createAsyncThunk('encryption/updateEncryptionSettings', async (settingsData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/encryption/settings', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(settingsData),
    });
    if (!response.ok) {
      throw new Error('Failed to update encryption settings');
    }
    const data = await response.json();
    return data.settings;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const encryptionSlice = createSlice({
  name: 'encryption',
  initialState: {
    settings: null,
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchEncryptionSettings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchEncryptionSettings.fulfilled, (state, action) => {
        state.loading = false;
        state.settings = action.payload;
      })
      .addCase(fetchEncryptionSettings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateEncryptionSettings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateEncryptionSettings.fulfilled, (state, action) => {
        state.loading = false;
        state.settings = action.payload;
      })
      .addCase(updateEncryptionSettings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default encryptionSlice.reducer;
