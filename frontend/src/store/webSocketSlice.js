import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to connect to WebSocket
export const connectWebSocket = createAsyncThunk('webSocket/connectWebSocket', async (_, { rejectWithValue, dispatch }) => {
  try {
    // In a real implementation, establish a WebSocket connection
    const ws = new WebSocket('ws://localhost:8000/ws/data-stream');
    ws.onopen = () => {
      console.log('WebSocket connected');
      // Start receiving messages
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        dispatch(updateData(data));
      };
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        dispatch(setError(error.message));
      };
      ws.onclose = () => {
        console.log('WebSocket closed');
        dispatch(disconnectWebSocket());
      };
    };
    return { status: 'connected', ws };
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to disconnect from WebSocket
export const disconnectWebSocket = createAsyncThunk('webSocket/disconnectWebSocket', async (_, { rejectWithValue, getState }) => {
  try {
    const state = getState();
    const ws = state.webSocket.ws;
    if (ws) {
      ws.close();
    }
    return { status: 'disconnected' };
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const webSocketSlice = createSlice({
  name: 'webSocket',
  initialState: {
    data: [],
    connected: false,
    error: null,
    ws: null,
  },
  reducers: {
    updateData: (state, action) => {
      state.data.push(action.payload);
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(connectWebSocket.pending, (state) => {
        state.error = null;
      })
      .addCase(connectWebSocket.fulfilled, (state, action) => {
        state.connected = true;
        state.ws = action.payload.ws;
      })
      .addCase(connectWebSocket.rejected, (state, action) => {
        state.error = action.payload;
      })
      .addCase(disconnectWebSocket.pending, (state) => {
        state.error = null;
      })
      .addCase(disconnectWebSocket.fulfilled, (state, action) => {
        state.connected = false;
        state.ws = null;
      })
      .addCase(disconnectWebSocket.rejected, (state, action) => {
        state.error = action.payload;
      });
  },
});

export const { updateData, setError } = webSocketSlice.actions;
export default webSocketSlice.reducer;
