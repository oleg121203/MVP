// Phase 1.4.3 - Optimized Redux Store Configuration
import { configureStore } from '@reduxjs/toolkit';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Analytics slice for dashboard state management
interface AnalyticsState {
  data: any | null;
  loading: boolean;
  error: string | null;
  lastUpdated: string | null;
}

const initialState: AnalyticsState = {
  data: null,
  loading: false,
  error: null,
  lastUpdated: null,
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setData: (state, action: PayloadAction<any>) => {
      state.data = action.payload;
      state.loading = false;
      state.error = null;
      state.lastUpdated = new Date().toISOString();
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

// Performance slice for monitoring
interface PerformanceState {
  loadTimes: Record<string, number>;
  memoryUsage: number;
  renderCount: number;
}

const performanceSlice = createSlice({
  name: 'performance',
  initialState: {
    loadTimes: {},
    memoryUsage: 0,
    renderCount: 0,
  } as PerformanceState,
  reducers: {
    recordLoadTime: (state, action: PayloadAction<{ component: string; time: number }>) => {
      state.loadTimes[action.payload.component] = action.payload.time;
    },
    updateMemoryUsage: (state, action: PayloadAction<number>) => {
      state.memoryUsage = action.payload;
    },
    incrementRenderCount: (state) => {
      state.renderCount += 1;
    },
  },
});

// Configure store with performance optimizations
export const store = configureStore({
  reducer: {
    analytics: analyticsSlice.reducer,
    performance: performanceSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types in serializability check
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Export actions
export const { setLoading, setData, setError, clearError } = analyticsSlice.actions;
export const { recordLoadTime, updateMemoryUsage, incrementRenderCount } = performanceSlice.actions;

export default store;
