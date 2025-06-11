import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch collaboration data
export const fetchCollaborationData = createAsyncThunk('collaboration/fetchCollaborationData', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/collaboration/data');
    if (!response.ok) {
      throw new Error('Failed to fetch collaboration data');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to send a message
export const sendMessage = createAsyncThunk('collaboration/sendMessage', async (messageData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/collaboration/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(messageData),
    });
    if (!response.ok) {
      throw new Error('Failed to send message');
    }
    const data = await response.json();
    return data.message;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to upload a document
export const uploadDocument = createAsyncThunk('collaboration/uploadDocument', async (documentData, { rejectWithValue }) => {
  try {
    const formData = new FormData();
    formData.append('file', documentData.file);
    formData.append('metadata', JSON.stringify({
      name: documentData.name,
      timestamp: documentData.timestamp,
      user: documentData.user
    }));

    const response = await fetch('/api/collaboration/documents', {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error('Failed to upload document');
    }
    const data = await response.json();
    return data.document;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to assign a task
export const assignTask = createAsyncThunk('collaboration/assignTask', async (taskData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/collaboration/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });
    if (!response.ok) {
      throw new Error('Failed to assign task');
    }
    const data = await response.json();
    return data.task;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const collaborationSlice = createSlice({
  name: 'collaboration',
  initialState: {
    collaborationData: {
      chatMessages: [],
      documents: [],
      tasks: []
    },
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchCollaborationData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCollaborationData.fulfilled, (state, action) => {
        state.loading = false;
        state.collaborationData = action.payload;
      })
      .addCase(fetchCollaborationData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(sendMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.collaborationData.chatMessages.push(action.payload);
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(uploadDocument.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(uploadDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.collaborationData.documents.push(action.payload);
      })
      .addCase(uploadDocument.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(assignTask.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(assignTask.fulfilled, (state, action) => {
        state.loading = false;
        state.collaborationData.tasks.push(action.payload);
      })
      .addCase(assignTask.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default collaborationSlice.reducer;
