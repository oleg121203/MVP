import React from 'react';
import { Provider } from 'react-redux';
import { store } from '../store';
import PriceDashboard from '../components/PriceDashboard';

const PriceAnalytics: React.FC = () => {
  return (
    <Provider store={store}>
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              Price Intelligence Analytics
            </h1>
            <p className="mt-2 text-gray-600">
              Monitor market prices, analyze trends, and optimize costs with AI-powered insights
            </p>
          </div>
          
          <PriceDashboard />
        </div>
      </div>
    </Provider>
  );
};

export default PriceAnalytics;
