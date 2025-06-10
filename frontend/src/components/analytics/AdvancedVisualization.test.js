import React from 'react';
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import AdvancedVisualization from './AdvancedVisualization';

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
  analytics: {
    data: [
      { date: '2025-06-01', cost: 1000, performance: 80, efficiency: 75 },
      { date: '2025-06-02', cost: 1200, performance: 85, efficiency: 78 },
      { date: '2025-06-03', cost: 1100, performance: 82, efficiency: 77 },
      { date: '2025-06-04', cost: 1300, performance: 88, efficiency: 80 },
      { date: '2025-06-05', cost: 900, performance: 78, efficiency: 73 }
    ],
    loading: false,
    error: null
  }
};

const initialStateLoading = {
  analytics: {
    data: [],
    loading: true,
    error: null
  }
};

const initialStateError = {
  analytics: {
    data: [],
    loading: false,
    error: 'Failed to fetch data'
  }
};

const testStore = mockStore(initialState);
const testStoreLoading = mockStore(initialStateLoading);
const testStoreError = mockStore(initialStateError);

describe('AdvancedVisualization Component', () => {
  test('renders without crashing', () => {
    render(
      <Provider store={testStore}>
        <AdvancedVisualization />
      </Provider>
    );
    expect(screen.getByText(/Advanced Data Visualization/i)).toBeInTheDocument();
  });

  test('displays loading state', () => {
    render(
      <Provider store={testStoreLoading}>
        <AdvancedVisualization />
      </Provider>
    );
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
  });

  test('displays error state', () => {
    render(
      <Provider store={testStoreError}>
        <AdvancedVisualization />
      </Provider>
    );
    expect(screen.getByText(/Error: Failed to fetch data/i)).toBeInTheDocument();
  });

  test('displays charts when data is available', async () => {
    render(
      <Provider store={testStore}>
        <AdvancedVisualization />
      </Provider>
    );
    expect(screen.getByTestId('mock-responsive-container')).toBeInTheDocument();
  });
});
