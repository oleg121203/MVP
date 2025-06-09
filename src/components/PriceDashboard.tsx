import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store';
import { setPriceData, setLoading, setError } from '../store/priceSlice';
import { priceClient } from '../api/priceClient';

interface PriceItem {
  id: string;
  name: string;
  currentPrice: number;
  trend: 'up' | 'down' | 'stable';
  changePercent: number;
  supplier: string;
  lastUpdated: string;
}

interface PriceTrend {
  date: string;
  price: number;
}

const PriceDashboard: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { data, loading, error } = useSelector((state: RootState) => state.price);
  const [selectedItem, setSelectedItem] = useState<PriceItem | null>(null);
  const [trendData, setTrendData] = useState<PriceTrend[]>([]);

  useEffect(() => {
    loadPriceData();
  }, []);

  const loadPriceData = async () => {
    try {
      dispatch(setLoading(true));
      const priceData = await priceClient.getCurrentPrices();
      dispatch(setPriceData(priceData));
    } catch (err) {
      dispatch(setError(err instanceof Error ? err.message : 'Unknown error'));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const handleItemClick = async (item: PriceItem) => {
    setSelectedItem(item);
    try {
      const trends = await priceClient.getPriceTrends(item.id);
      setTrendData(trends);
    } catch (err) {
      console.error('Failed to load price trends:', err);
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '📈';
      case 'down': return '📉';
      default: return '➡️';
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up': return 'text-red-600';
      case 'down': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
        <button 
          onClick={loadPriceData}
          className="ml-4 bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Price Intelligence Dashboard</h2>
        <p className="text-gray-600">Real-time market price analysis and trends</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Price List */}
        <div className="lg:col-span-2">
          <h3 className="text-lg font-semibold mb-4">Current Market Prices</h3>
          <div className="space-y-3">
            {data.map((item: PriceItem) => (
              <div
                key={item.id}
                onClick={() => handleItemClick(item)}
                className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
              >
                <div className="flex justify-between items-center">
                  <div>
                    <h4 className="font-medium text-gray-800">{item.name}</h4>
                    <p className="text-sm text-gray-600">Supplier: {item.supplier}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-gray-800">
                      ${item.currentPrice.toFixed(2)}
                    </div>
                    <div className={`text-sm flex items-center ${getTrendColor(item.trend)}`}>
                      {getTrendIcon(item.trend)}
                      <span className="ml-1">{item.changePercent}%</span>
                    </div>
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-500">
                  Last updated: {new Date(item.lastUpdated).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Trend Analysis */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Trend Analysis</h3>
          {selectedItem ? (
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium text-gray-800 mb-3">{selectedItem.name}</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Current Price:</span>
                  <span className="font-medium">${selectedItem.currentPrice.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Trend:</span>
                  <span className={`font-medium ${getTrendColor(selectedItem.trend)}`}>
                    {getTrendIcon(selectedItem.trend)} {selectedItem.trend}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Change:</span>
                  <span className={`font-medium ${getTrendColor(selectedItem.trend)}`}>
                    {selectedItem.changePercent}%
                  </span>
                </div>
              </div>
              
              {trendData.length > 0 && (
                <div className="mt-4">
                  <h5 className="text-sm font-medium text-gray-700 mb-2">Price History</h5>
                  <div className="space-y-1">
                    {trendData.slice(-5).map((trend, index) => (
                      <div key={index} className="flex justify-between text-sm">
                        <span className="text-gray-600">{trend.date}</span>
                        <span className="font-medium">${trend.price.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-gray-50 p-4 rounded-lg text-center text-gray-600">
              Select an item to view trend analysis
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-6 flex space-x-3">
        <button
          onClick={loadPriceData}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          Refresh Prices
        </button>
        <button
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors"
        >
          Export Report
        </button>
        <button
          className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 transition-colors"
        >
          Set Alerts
        </button>
      </div>
    </div>
  );
};

export default PriceDashboard;
