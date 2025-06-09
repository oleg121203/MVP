import React from 'react';
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import AnalyticsDashboard from '../AnalyticsDashboard';
import { store } from '../../app/store';

// Mock axios to avoid ES module issues
const axios = require('axios');
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: { analytics: { totalProjects: 5, completionRate: 75, onTimeDelivery: 90, budgetCompliance: 85, clientSatisfaction: 4.5 } } })),
  post: jest.fn(() => Promise.resolve({ data: { insights: ['Insight 1', 'Insight 2'] } }))
}));

jest.mock('../../redux/analyticsSlice', () => ({
  ...jest.requireActual('../../redux/analyticsSlice'),
  fetchProjectMetrics: jest.fn(() => ({ type: 'fetchProjectMetrics' })),
  fetchRealTimeInsights: jest.fn(() => ({ type: 'fetchRealTimeInsights' })),
}));

jest.mock('socket.io-client', () => {
  const mockSocket = {
    emit: jest.fn(),
    on: jest.fn(),
    off: jest.fn(),
  };
  return {
    io: () => mockSocket,
  };
});

describe('AnalyticsDashboard Component', () => {
  test('renders analytics dashboard title', () => {
    render(
      <Provider store={store}>
        <AnalyticsDashboard />
      </Provider>
    );
    expect(screen.getByText(/Analytics Dashboard/i)).toBeTruthy();
  });

  test('renders AI chat component', () => {
    render(
      <Provider store={store}>
        <AnalyticsDashboard />
      </Provider>
    );
    expect(screen.getByPlaceholderText(/Ask AI about this project.../i)).toBeTruthy();
  });
});
