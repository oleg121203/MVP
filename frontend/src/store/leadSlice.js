import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch leads
export const fetchLeads = createAsyncThunk('leads/fetchLeads', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/crm/leads');
    if (!response.ok) {
      throw new Error('Failed to fetch leads');
    }
    const data = await response.json();
    return data.leads;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new lead
export const createLead = createAsyncThunk('leads/createLead', async (leadData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/crm/leads', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(leadData),
    });
    if (!response.ok) {
      throw new Error('Failed to create lead');
    }
    const data = await response.json();
    return data.lead;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing lead
export const updateLead = createAsyncThunk('leads/updateLead', async (leadData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/crm/leads/${leadData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(leadData),
    });
    if (!response.ok) {
      throw new Error('Failed to update lead');
    }
    const data = await response.json();
    return data.lead;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete a lead
export const deleteLead = createAsyncThunk('leads/deleteLead', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/crm/leads/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete lead');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const leadSlice = createSlice({
  name: 'leads',
  initialState: {
    leads: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchLeads.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLeads.fulfilled, (state, action) => {
        state.loading = false;
        state.leads = action.payload;
      })
      .addCase(fetchLeads.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createLead.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createLead.fulfilled, (state, action) => {
        state.loading = false;
        state.leads.push(action.payload);
      })
      .addCase(createLead.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateLead.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateLead.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.leads.findIndex(lead => lead.id === action.payload.id);
        if (index !== -1) {
          state.leads[index] = action.payload;
        }
      })
      .addCase(updateLead.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteLead.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteLead.fulfilled, (state, action) => {
        state.loading = false;
        state.leads = state.leads.filter(lead => lead.id !== action.payload);
      })
      .addCase(deleteLead.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default leadSlice.reducer;
