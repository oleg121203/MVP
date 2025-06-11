import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch customers
export const fetchCustomers = createAsyncThunk('crm/fetchCustomers', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/crm/customers');
    if (!response.ok) {
      throw new Error('Failed to fetch customers');
    }
    const data = await response.json();
    return data.customers;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new customer
export const createCustomer = createAsyncThunk('crm/createCustomer', async (customerData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/crm/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customerData),
    });
    if (!response.ok) {
      throw new Error('Failed to create customer');
    }
    const data = await response.json();
    return data.customer;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing customer
export const updateCustomer = createAsyncThunk('crm/updateCustomer', async (customerData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/crm/customers/${customerData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customerData),
    });
    if (!response.ok) {
      throw new Error('Failed to update customer');
    }
    const data = await response.json();
    return data.customer;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete a customer
export const deleteCustomer = createAsyncThunk('crm/deleteCustomer', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/crm/customers/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete customer');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const crmSlice = createSlice({
  name: 'crm',
  initialState: {
    customers: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchCustomers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCustomers.fulfilled, (state, action) => {
        state.loading = false;
        state.customers = action.payload;
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createCustomer.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createCustomer.fulfilled, (state, action) => {
        state.loading = false;
        state.customers.push(action.payload);
      })
      .addCase(createCustomer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateCustomer.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateCustomer.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.customers.findIndex(customer => customer.id === action.payload.id);
        if (index !== -1) {
          state.customers[index] = action.payload;
        }
      })
      .addCase(updateCustomer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteCustomer.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteCustomer.fulfilled, (state, action) => {
        state.loading = false;
        state.customers = state.customers.filter(customer => customer.id !== action.payload);
      })
      .addCase(deleteCustomer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default crmSlice.reducer;
