import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch security settings
export const fetchSecuritySettings = createAsyncThunk('security/fetchSecuritySettings', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/security/settings');
    if (!response.ok) {
      throw new Error('Failed to fetch security settings');
    }
    const data = await response.json();
    return data.settings;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update MFA setting
export const updateMFASetting = createAsyncThunk('security/updateMFASetting', async (enabled, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/security/mfa', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ enabled }),
    });
    if (!response.ok) {
      throw new Error('Failed to update MFA setting');
    }
    return enabled;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update RBAC policy
export const updateRBACPolicy = createAsyncThunk('security/updateRBACPolicy', async (policy, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/security/rbac', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ policy }),
    });
    if (!response.ok) {
      throw new Error('Failed to update RBAC policy');
    }
    return policy;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to manage encryption key
export const manageEncryptionKey = createAsyncThunk('security/manageEncryptionKey', async ({ action, key }, { rejectWithValue }) => {
  try {
    const body = action === 'import' ? { action, key } : { action };
    const response = await fetch('/api/security/encryption-key', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      throw new Error(`Failed to ${action} encryption key`);
    }
    const data = await response.json();
    return data.status;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch audit logs
export const fetchAuditLogs = createAsyncThunk('security/fetchAuditLogs', async ({ type, date }, { rejectWithValue }) => {
  try {
    let url = '/api/audit/logs';
    const params = new URLSearchParams();
    if (type && type !== 'all') params.append('type', type);
    if (date) params.append('date', date);
    if (params.toString()) url += `?${params.toString()}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Failed to fetch audit logs');
    }
    const data = await response.json();
    return data.logs;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch security events
export const fetchSecurityEvents = createAsyncThunk('security/fetchSecurityEvents', async ({ timeRange }, { rejectWithValue }) => {
  try {
    const url = `/api/security/events?range=${timeRange}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Failed to fetch security events');
    }
    const data = await response.json();
    return data.events;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch compliance status
export const fetchComplianceStatus = createAsyncThunk('security/fetchComplianceStatus', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/compliance/status');
    if (!response.ok) {
      throw new Error('Failed to fetch compliance status');
    }
    const data = await response.json();
    return data.status;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to generate compliance report
export const generateComplianceReport = createAsyncThunk('security/generateComplianceReport', async ({ standard, format }, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/compliance/report/${standard}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ format }),
    });
    if (!response.ok) {
      throw new Error('Failed to generate compliance report');
    }
    const data = await response.json();
    return data.reportUrl;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const securitySlice = createSlice({
  name: 'security',
  initialState: {
    settings: {
      mfaEnabled: false,
      rbacPolicy: '',
      encryptionKeyStatus: 'Unknown',
      lastKeyRotation: 'Never'
    },
    auditLogs: [],
    securityEvents: [],
    complianceStatus: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchSecuritySettings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSecuritySettings.fulfilled, (state, action) => {
        state.loading = false;
        state.settings = action.payload;
      })
      .addCase(fetchSecuritySettings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateMFASetting.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateMFASetting.fulfilled, (state, action) => {
        state.loading = false;
        state.settings.mfaEnabled = action.payload;
      })
      .addCase(updateMFASetting.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateRBACPolicy.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateRBACPolicy.fulfilled, (state, action) => {
        state.loading = false;
        state.settings.rbacPolicy = action.payload;
      })
      .addCase(updateRBACPolicy.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(manageEncryptionKey.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(manageEncryptionKey.fulfilled, (state, action) => {
        state.loading = false;
        state.settings.encryptionKeyStatus = action.payload.status || 'Updated';
        if (action.meta.arg.action !== 'import') {
          state.settings.lastKeyRotation = new Date().toISOString();
        }
      })
      .addCase(manageEncryptionKey.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchAuditLogs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAuditLogs.fulfilled, (state, action) => {
        state.loading = false;
        state.auditLogs = action.payload;
      })
      .addCase(fetchAuditLogs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchSecurityEvents.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSecurityEvents.fulfilled, (state, action) => {
        state.loading = false;
        state.securityEvents = action.payload;
      })
      .addCase(fetchSecurityEvents.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchComplianceStatus.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchComplianceStatus.fulfilled, (state, action) => {
        state.loading = false;
        state.complianceStatus = action.payload;
      })
      .addCase(fetchComplianceStatus.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(generateComplianceReport.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(generateComplianceReport.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(generateComplianceReport.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default securitySlice.reducer;
