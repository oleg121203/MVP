import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch workflows
export const fetchWorkflows = createAsyncThunk('workflows/fetchWorkflows', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/workflows');
    if (!response.ok) {
      throw new Error('Failed to fetch workflows');
    }
    const data = await response.json();
    return data.workflows;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new workflow
export const createWorkflow = createAsyncThunk('workflows/createWorkflow', async (workflowData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/workflows', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workflowData),
    });
    if (!response.ok) {
      throw new Error('Failed to create workflow');
    }
    const data = await response.json();
    return data.workflow;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing workflow
export const updateWorkflow = createAsyncThunk('workflows/updateWorkflow', async (workflowData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/workflows/${workflowData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workflowData),
    });
    if (!response.ok) {
      throw new Error('Failed to update workflow');
    }
    const data = await response.json();
    return data.workflow;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete a workflow
export const deleteWorkflow = createAsyncThunk('workflows/deleteWorkflow', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/workflows/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete workflow');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to run a workflow
export const runWorkflow = createAsyncThunk('workflows/runWorkflow', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/workflows/${id}/run`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to run workflow');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch workflow analysis data
export const fetchWorkflowAnalysis = createAsyncThunk('workflow/fetchWorkflowAnalysis', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/workflows/analyze');
    if (!response.ok) {
      throw new Error('Failed to fetch workflow analysis data');
    }
    const data = await response.json();
    return data.analysis;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to apply workflow optimization
export const applyOptimization = createAsyncThunk('workflow/applyOptimization', async ({ workflowId, optimizationId }, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/workflows/optimize/${workflowId}/${optimizationId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to apply optimization');
    }
    const data = await response.json();
    return data.result;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const workflowSlice = createSlice({
  name: 'workflows',
  initialState: {
    workflows: [],
    analysisData: {
      workflows: []
    },
    loading: false,
    error: null,
    optimizationStatus: 'idle',
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchWorkflows.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchWorkflows.fulfilled, (state, action) => {
        state.loading = false;
        state.workflows = action.payload;
      })
      .addCase(fetchWorkflows.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createWorkflow.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createWorkflow.fulfilled, (state, action) => {
        state.loading = false;
        state.workflows.push(action.payload);
      })
      .addCase(createWorkflow.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateWorkflow.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateWorkflow.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.workflows.findIndex(workflow => workflow.id === action.payload.id);
        if (index !== -1) {
          state.workflows[index] = action.payload;
        }
      })
      .addCase(updateWorkflow.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteWorkflow.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteWorkflow.fulfilled, (state, action) => {
        state.loading = false;
        state.workflows = state.workflows.filter(workflow => workflow.id !== action.payload);
      })
      .addCase(deleteWorkflow.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(runWorkflow.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(runWorkflow.fulfilled, (state, action) => {
        state.loading = false;
        // Optionally update the status of the workflow to indicate it's running
        const index = state.workflows.findIndex(workflow => workflow.id === action.payload);
        if (index !== -1) {
          state.workflows[index].status = 'running';
        }
      })
      .addCase(runWorkflow.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchWorkflowAnalysis.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchWorkflowAnalysis.fulfilled, (state, action) => {
        state.loading = false;
        state.analysisData = action.payload;
      })
      .addCase(fetchWorkflowAnalysis.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(applyOptimization.pending, (state) => {
        state.loading = true;
        state.optimizationStatus = 'applying';
        state.error = null;
      })
      .addCase(applyOptimization.fulfilled, (state) => {
        state.loading = false;
        state.optimizationStatus = 'success';
      })
      .addCase(applyOptimization.rejected, (state, action) => {
        state.loading = false;
        state.optimizationStatus = 'error';
        state.error = action.payload;
      });
  },
});

export default workflowSlice.reducer;
