import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import PriceDashboard from '../../src/components/PriceDashboard';
import { getPriceData } from '../../api/priceClient';
import priceReducer from '../../src/store/priceSlice';

// Mock the price client
jest.mock('../../api/priceClient', () => ({
  getPriceData: jest.fn().mockResolvedValue({
    prices: [],
    lastUpdated: new Date().toISOString()
  })
}));

const createTestStore = () => {
  return configureStore({
    reducer: {
      price: priceReducer,
    },
  });
};

const renderWithProvider = (component: React.ReactElement) => {
  const store = createTestStore();
  return render(
    <Provider store={store}>
      {component}
    </Provider>
  );
};

const mockPriceData = [
  {
    id: '1',
    name: 'Air Conditioning Unit',
    currentPrice: 1500.00,
    trend: 'up' as const,
    changePercent: 5.2,
    supplier: 'HVAC Supply Co',
    lastUpdated: '2025-06-09T15:30:00Z',
  },
  {
    id: '2',
    name: 'Ventilation Fan',
    currentPrice: 250.50,
    trend: 'down' as const,
    changePercent: -2.1,
    supplier: 'Air Tech Ltd',
    lastUpdated: '2025-06-09T15:25:00Z',
  },
];

const mockTrendData = [
  { date: '2025-06-05', price: 1450.00 },
  { date: '2025-06-06', price: 1475.00 },
  { date: '2025-06-07', price: 1480.00 },
  { date: '2025-06-08', price: 1495.00 },
  { date: '2025-06-09', price: 1500.00 },
];

describe('PriceDashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders dashboard title and description', () => {
    renderWithProvider(<PriceDashboard />);
    
    expect(screen.getByText('Price Intelligence Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Real-time market price analysis and trends')).toBeInTheDocument();
  });

  test('loads and displays price data on mount', async () => {
    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Air Conditioning Unit')).toBeInTheDocument();
      expect(screen.getByText('Ventilation Fan')).toBeInTheDocument();
      expect(screen.getByText('$1500.00')).toBeInTheDocument();
      expect(screen.getByText('$250.50')).toBeInTheDocument();
    });
  });

  test('displays loading state', async () => {
    renderWithProvider(<PriceDashboard />);

    expect(screen.getByRole('status')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
  });

  test('displays error state and retry button', async () => {
    const errorMessage = 'Failed to fetch price data';
    jest.mock('../../api/priceClient', () => ({
      getPriceData: jest.fn().mockRejectedValue(new Error(errorMessage))
    }));

    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });

    const retryButton = screen.getByText('Retry');
    expect(retryButton).toBeInTheDocument();

    // Test retry functionality
    jest.mock('../../api/priceClient', () => ({
      getPriceData: jest.fn().mockResolvedValue({
        prices: [],
        lastUpdated: new Date().toISOString()
      })
    }));
    fireEvent.click(retryButton);

    await waitFor(() => {
      expect(screen.queryByText(`Error: ${errorMessage}`)).not.toBeInTheDocument();
    });
  });

  test('displays trend indicators correctly', async () => {
    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText('📈')).toBeInTheDocument(); // Up trend
      expect(screen.getByText('📉')).toBeInTheDocument(); // Down trend
    });

    expect(screen.getByText('5.2%')).toBeInTheDocument();
    expect(screen.getByText('-2.1%')).toBeInTheDocument();
  });

  test('shows trend analysis when item is clicked', async () => {
    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Air Conditioning Unit')).toBeInTheDocument();
    });

    const firstItem = screen.getByText('Air Conditioning Unit').closest('div');
    fireEvent.click(firstItem!);

    await waitFor(() => {
      expect(screen.getByText('Price History')).toBeInTheDocument();
    });
  });

  test('refresh button reloads price data', async () => {
    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Air Conditioning Unit')).toBeInTheDocument();
    });

    const refreshButton = screen.getByText('Refresh Prices');
    fireEvent.click(refreshButton);

    await waitFor(() => {
      expect(screen.getByText('Air Conditioning Unit')).toBeInTheDocument();
    });
  });

  test('displays action buttons', async () => {
    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Refresh Prices')).toBeInTheDocument();
    });

    expect(screen.getByText('Export Report')).toBeInTheDocument();
    expect(screen.getByText('Set Alerts')).toBeInTheDocument();
  });

  test('displays supplier information', async () => {
    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Supplier: HVAC Supply Co')).toBeInTheDocument();
      expect(screen.getByText('Supplier: Air Tech Ltd')).toBeInTheDocument();
    });
  });

  test('displays last updated timestamps', async () => {
    renderWithProvider(<PriceDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Last updated/i)).toBeInTheDocument();
    }, { timeout: 10000 });
  });

  test('shows loading state initially', async () => {
    renderWithProvider(<PriceDashboard />);
    
    // Initial loading state
    expect(screen.getByRole('status')).toBeInTheDocument();
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    }, { timeout: 10000 });
  });

  test('displays last updated timestamp', async () => {
    renderWithProvider(<PriceDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/last updated/i)).toBeInTheDocument();
    }, { timeout: 10000 });
  });
});
