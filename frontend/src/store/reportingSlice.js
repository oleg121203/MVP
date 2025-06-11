import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk to fetch report templates
export const fetchReportTemplates = createAsyncThunk('reporting/fetchReportTemplates', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/reporting/templates');
    if (!response.ok) {
      throw new Error('Failed to fetch report templates');
    }
    const data = await response.json();
    return data.templates;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new report template
export const createReportTemplate = createAsyncThunk('reporting/createReportTemplate', async (templateData, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/reporting/templates', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(templateData),
    });
    if (!response.ok) {
      throw new Error('Failed to create report template');
    }
    const data = await response.json();
    return data.template;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing report template
export const updateReportTemplate = createAsyncThunk('reporting/updateReportTemplate', async (templateData, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/reporting/templates/${templateData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(templateData),
    });
    if (!response.ok) {
      throw new Error('Failed to update report template');
    }
    const data = await response.json();
    return data.template;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete a report template
export const deleteReportTemplate = createAsyncThunk('reporting/deleteReportTemplate', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/reporting/templates/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete report template');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch report schedules
export const fetchSchedules = createAsyncThunk('reporting/fetchSchedules', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/reporting/schedules');
    if (!response.ok) {
      throw new Error('Failed to fetch report schedules');
    }
    const data = await response.json();
    return data.schedules;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to create a new report schedule
export const createSchedule = createAsyncThunk('reporting/createSchedule', async ({ scheduleData, format, destinationDetails }, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/reporting/schedules', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ scheduleData, format, destinationDetails }),
    });
    if (!response.ok) {
      throw new Error('Failed to create report schedule');
    }
    const data = await response.json();
    return data.schedule;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to update an existing report schedule
export const updateSchedule = createAsyncThunk('reporting/updateSchedule', async ({ scheduleData, format, destinationDetails }, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/reporting/schedules/${scheduleData.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ scheduleData, format, destinationDetails }),
    });
    if (!response.ok) {
      throw new Error('Failed to update report schedule');
    }
    const data = await response.json();
    return data.schedule;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to delete a report schedule
export const deleteSchedule = createAsyncThunk('reporting/deleteSchedule', async (id, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/reporting/schedules/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete report schedule');
    }
    return id;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch visualization data
export const fetchVisualizationData = createAsyncThunk('reporting/fetchVisualizationData', async (timeRange, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/reporting/visualization?range=${timeRange}`);
    if (!response.ok) {
      throw new Error('Failed to fetch visualization data');
    }
    const data = await response.json();
    return data.data;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch analytics data
export const fetchAnalyticsData = createAsyncThunk('reporting/fetchAnalyticsData', async ({ timeRange, widget }, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/analytics/data?range=${timeRange}&widget=${widget}`);
    if (!response.ok) {
      throw new Error('Failed to fetch analytics data');
    }
    const data = await response.json();
    return data.data;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

// Async thunk to fetch predictive data
export const fetchPredictiveData = createAsyncThunk('reporting/fetchPredictiveData', async ({ timeRange, type }, { rejectWithValue }) => {
  try {
    const response = await fetch(`/api/predictive/data?range=${timeRange}&type=${type}`);
    if (!response.ok) {
      throw new Error('Failed to fetch predictive data');
    }
    const data = await response.json();
    return data.data;
  } catch (error) {
    return rejectWithValue(error.message);
  }
});

const reportingSlice = createSlice({
  name: 'reporting',
  initialState: {
    templates: [],
    schedules: [],
    visualizationData: [],
    analyticsData: [],
    predictiveData: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchReportTemplates.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchReportTemplates.fulfilled, (state, action) => {
        state.loading = false;
        state.templates = action.payload;
      })
      .addCase(fetchReportTemplates.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createReportTemplate.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createReportTemplate.fulfilled, (state, action) => {
        state.loading = false;
        state.templates.push(action.payload);
      })
      .addCase(createReportTemplate.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateReportTemplate.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateReportTemplate.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.templates.findIndex(template => template.id === action.payload.id);
        if (index !== -1) {
          state.templates[index] = action.payload;
        }
      })
      .addCase(updateReportTemplate.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteReportTemplate.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteReportTemplate.fulfilled, (state, action) => {
        state.loading = false;
        state.templates = state.templates.filter(template => template.id !== action.payload);
      })
      .addCase(deleteReportTemplate.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchSchedules.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSchedules.fulfilled, (state, action) => {
        state.loading = false;
        state.schedules = action.payload;
      })
      .addCase(fetchSchedules.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(createSchedule.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createSchedule.fulfilled, (state, action) => {
        state.loading = false;
        state.schedules.push(action.payload);
      })
      .addCase(createSchedule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateSchedule.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateSchedule.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.schedules.findIndex(schedule => schedule.id === action.payload.id);
        if (index !== -1) {
          state.schedules[index] = action.payload;
        }
      })
      .addCase(updateSchedule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteSchedule.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteSchedule.fulfilled, (state, action) => {
        state.loading = false;
        state.schedules = state.schedules.filter(schedule => schedule.id !== action.payload);
      })
      .addCase(deleteSchedule.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchVisualizationData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVisualizationData.fulfilled, (state, action) => {
        state.loading = false;
        state.visualizationData = action.payload;
      })
      .addCase(fetchVisualizationData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchAnalyticsData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAnalyticsData.fulfilled, (state, action) => {
        state.loading = false;
        state.analyticsData = action.payload;
      })
      .addCase(fetchAnalyticsData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchPredictiveData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPredictiveData.fulfilled, (state, action) => {
        state.loading = false;
        state.predictiveData = action.payload;
      })
      .addCase(fetchPredictiveData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default reportingSlice.reducer;
