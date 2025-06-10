import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import AdvancedVisualization from './AdvancedVisualization';
import analyticsReducer from '../../store/analyticsSlice';

// Import jest-dom matchers
import '@testing-library/jest-dom';

// Create a theme
const theme = createTheme();

// Create a test store with mock data
const testStore = configureStore({
  reducer: {
    analytics: analyticsReducer,
  },
  preloadedState: {
    analytics: {
      data: [
        { date: '2025-06-01', cost: 1000, performance: 80, efficiency: 75 },
        { date: '2025-06-02', cost: 1200, performance: 85, efficiency: 78 },
        { date: '2025-06-03', cost: 1100, performance: 82, efficiency: 77 },
      ],
      loading: false,
      error: null,
    },
  },
});

const testStoreLoading = configureStore({
  reducer: {
    analytics: analyticsReducer,
  },
  preloadedState: {
    analytics: {
      data: [],
      loading: true,
      error: null,
    },
  },
});

const testStoreError = configureStore({
  reducer: {
    analytics: analyticsReducer,
  },
  preloadedState: {
    analytics: {
      data: [],
      loading: false,
      error: 'Failed to fetch data',
    },
  },
});

describe('AdvancedVisualization Component', () => {
  test('renders without crashing', () => {
    render(
      <Provider store={testStore}>
        <ThemeProvider theme={theme}>
          <AdvancedVisualization />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Advanced Data Visualization/i)).toBeInTheDocument();
  });

  test('displays loading state', () => {
    render(
      <Provider store={testStoreLoading}>
        <ThemeProvider theme={theme}>
          <AdvancedVisualization />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Loading data.../i)).toBeInTheDocument();
  });

  test('displays error state', () => {
    render(
      <Provider store={testStoreError}>
        <ThemeProvider theme={theme}>
          <AdvancedVisualization />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Error loading data:/i)).toBeInTheDocument();
  });

  test('displays charts when data is available', async () => {
    render(
      <Provider store={testStore}>
        <ThemeProvider theme={theme}>
          <AdvancedVisualization />
        </ThemeProvider>
      </Provider>
    );
    expect(screen.getByText(/Cost Analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/Performance Trends/i)).toBeInTheDocument();
  });
});
