import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import CustomReports from './CustomReports';
import customReportsReducer from '../../store/customReportsSlice';

// Import jest-dom matchers
import '@testing-library/jest-dom';

// Mock Recharts components
jest.mock('recharts', () => ({
  LineChart: () => <div data-testid="mock-line-chart" />,
  BarChart: () => <div data-testid="mock-bar-chart" />,
  Line: () => null,
  Bar: () => null,
  XAxis: () => null,
  YAxis: () => null,
  CartesianGrid: () => null,
  Tooltip: () => null,
  Legend: () => null,
  ResponsiveContainer: ({ children }) => <div data-testid="mock-responsive-container">{children}</div>
}));

// Mock Redux store
const middlewares = [thunk];
const mockStore = configureStore(middlewares);

const initialState = {
  customReports: {
    data: [
      { id: 1, title: 'Custom Report 1', date: '2025-06-01', insights: 'Insight 1', dataPoints: [{ date: '2025-06-01', value: 100 }] },
      { id: 2, title: 'Custom Report 2', date: '2025-06-02', insights: 'Insight 2', dataPoints: [{ date: '2025-06-02', value: 200 }] }
    ],
    loading: false,
    error: null
  }
};

const initialStateLoading = {
  customReports: {
    data: [],
    loading: true,
    error: null
  }
};

const initialStateError = {
  customReports: {
    data: [],
    loading: false,
    error: 'Failed to fetch custom reports'
  }
};

const testStore = mockStore(initialState);
const testStoreLoading = mockStore(initialStateLoading);
const testStoreError = mockStore(initialStateError);

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
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
  });

  test('displays error state', () => {
    render(
      <Provider store={testStoreError}>
        <CustomReports />
      </Provider>
    );
    expect(screen.getByText(/Error: Failed to fetch custom reports/i)).toBeInTheDocument();
  });

  test('displays chart when data is available', async () => {
    render(
      <Provider store={testStore}>
        <CustomReports />
      </Provider>
    );
    expect(screen.getByTestId('mock-responsive-container')).toBeInTheDocument();
  });
});
