import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import PredictiveModels from './PredictiveModels';
import predictiveModelsReducer from '../../store/predictiveModelsSlice';

// Import jest-dom matchers
import '@testing-library/jest-dom';

// Create a theme
const theme = createTheme();

// Create a test store with mock data
const testStore = configureStore({
  reducer: {
    predictiveModels: predictiveModelsReducer,
  },
  preloadedState: {
    predictiveModels: {
      data: [
        { date: '2025-06-06', predicted_cost: 950 },
        { date: '2025-06-07', predicted_cost: 1050 },
        { date: '2025-06-08', predicted_cost: 1100 },
      ],
      loading: false,
      error: null,
    },
  },
});

const testStoreLoading = configureStore({
  reducer: {
    predictiveModels: predictiveModelsReducer,
  },
  preloadedState: {
    predictiveModels: {
      data: [],
      loading: true,
      error: null,
    },
  },
});

const testStoreError = configureStore({
  reducer: {
    predictiveModels: predictiveModelsReducer,
  },
  preloadedState: {
    predictiveModels: {
      data: [],
      loading: false,
      error: 'Failed to fetch predictive data',
    },
  },
});

describe('PredictiveModels Component', () => {
  test('renders without crashing', () => {
    render(
      <Provider store={testStore}>
        <ThemeProvider theme={theme}>
          <PredictiveModels />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Predictive Analytics/i)).toBeInTheDocument();
  });

  test('displays loading state', () => {
    render(
      <Provider store={testStoreLoading}>
        <ThemeProvider theme={theme}>
          <PredictiveModels />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Loading predictive data.../i)).toBeInTheDocument();
  });

  test('displays error state', () => {
    render(
      <Provider store={testStoreError}>
        <ThemeProvider theme={theme}>
          <PredictiveModels />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Error loading predictive data:/i)).toBeInTheDocument();
  });

  test('displays chart when data is available', async () => {
    render(
      <Provider store={testStore}>
        <ThemeProvider theme={theme}>
          <PredictiveModels />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Cost Prediction/i)).toBeInTheDocument();
  });
});
