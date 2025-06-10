import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import CustomReports from './CustomReports';
import customReportsReducer from '../../store/customReportsSlice';

// Import jest-dom matchers
import '@testing-library/jest-dom';

// Create a test store with mock data
const testStore = configureStore({
  reducer: {
    customReports: customReportsReducer,
  },
  preloadedState: {
    customReports: {
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
    customReports: customReportsReducer,
  },
  preloadedState: {
    customReports: {
      data: [],
      loading: true,
      error: null,
    },
  },
});

const testStoreError = configureStore({
  reducer: {
    customReports: customReportsReducer,
  },
  preloadedState: {
    customReports: {
      data: [],
      loading: false,
      error: 'Failed to fetch custom reports',
    },
  },
});

describe('CustomReports Component', () => {
  test('renders without crashing', () => {
    render(
      <Provider store={testStore}>
        <CustomReports />
      </Provider>
    );
    expect(screen.getByText(/Custom Analytics Reports/i)).toBeInTheDocument();
  });

  test('displays loading state', () => {
    render(
      <Provider store={testStoreLoading}>
        <CustomReports />
      </Provider>
    );
    expect(screen.getByText(/Loading custom reports.../i)).toBeInTheDocument();
  });

  test('displays error state', () => {
    render(
      <Provider store={testStoreError}>
        <CustomReports />
      </Provider>
    );
    expect(screen.getByText(/Error loading custom reports:/i)).toBeInTheDocument();
  });

  test('displays chart when data is available', async () => {
    render(
      <Provider store={testStore}>
        <CustomReports />
      </Provider>
    );
    expect(screen.getByText(/Cost Report/i)).toBeInTheDocument();
  });
});
