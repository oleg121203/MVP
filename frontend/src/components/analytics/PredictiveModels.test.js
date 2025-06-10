import React from 'react';
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import PredictiveModels from './PredictiveModels';

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
  predictiveModels: {
    data: {
      costTrend: [
        { date: '2025-06-06', predicted_cost: 1100 },
        { date: '2025-06-07', predicted_cost: 1150 },
        { date: '2025-06-08', predicted_cost: 1200 }
      ],
      patternAnalysis: {
        anomalies: [
          { date: '2025-06-05', value: 900, reason: 'Significant drop in cost' }
        ]
      }
    },
    loading: false,
    error: null
  }
};

const initialStateLoading = {
  predictiveModels: {
    data: { costTrend: [], patternAnalysis: { anomalies: [] } },
    loading: true,
    error: null
  }
};

const initialStateError = {
  predictiveModels: {
    data: { costTrend: [], patternAnalysis: { anomalies: [] } },
    loading: false,
    error: 'Failed to fetch predictive data'
  }
};

const testStore = mockStore(initialState);
const testStoreLoading = mockStore(initialStateLoading);
const testStoreError = mockStore(initialStateError);

describe('PredictiveModels Component', () => {
  test('renders without crashing', () => {
    render(
      <Provider store={testStore}>
        <PredictiveModels />
      </Provider>
    );
    expect(screen.getByText(/Predictive Analytics Models/i)).toBeInTheDocument();
  });

  test('displays loading state', () => {
    render(
      <Provider store={testStoreLoading}>
        <PredictiveModels />
      </Provider>
    );
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
  });

  test('displays error state', () => {
    render(
      <Provider store={testStoreError}>
        <PredictiveModels />
      </Provider>
    );
    expect(screen.getByText(/Error: Failed to fetch predictive data/i)).toBeInTheDocument();
  });

  test('displays chart when data is available', async () => {
    render(
      <Provider store={testStore}>
        <PredictiveModels />
      </Provider>
    );
    expect(screen.getByTestId('mock-responsive-container')).toBeInTheDocument();
  });
});
