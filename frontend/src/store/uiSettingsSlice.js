import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to update theme settings
export const updateTheme = createAsyncThunk('uiSettings/updateTheme', async (themeData, { rejectWithValue }) => {
  try {
    // In a real implementation, this might save to a backend API or local storage
    return themeData;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update layout settings
export const updateLayout = createAsyncThunk('uiSettings/updateLayout', async (layoutType, { rejectWithValue }) => {
  try {
    // In a real implementation, this might save to a backend API or local storage
    return layoutType;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const uiSettingsSlice = createSlice({
  name: 'uiSettings',
  initialState: {
    theme: {
      primaryColor: '#1976d2',
      secondaryColor: '#dc004e',
      fontSize: 16
    },
    layout: 'default',
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(updateTheme.fulfilled, (state, action) => {
        state.theme = action.payload;
      })
      .addCase(updateTheme.rejected, (state, action) => {
        state.error = action.payload;
      })
      .addCase(updateLayout.fulfilled, (state, action) => {
        state.layout = action.payload;
      })
      .addCase(updateLayout.rejected, (state, action) => {
        state.error = action.payload;
      });
  },
});

export default uiSettingsSlice.reducer;
