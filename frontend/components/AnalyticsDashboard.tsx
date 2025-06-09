import React, { useState, useEffect, useCallback, useMemo, memo } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

import type { RootState } from '../store';

// Memoized chart options for performance
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' as const },
    title: { display: true, text: 'Analytics Overview' }
  },
  scales: {
    y: { beginAtZero: true }
  }
};

interface AnalyticsData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    borderColor: string;
    tension: number;
  }>;
}

const AnalyticsDashboard: React.FC = memo(() => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Memoized fetch function to prevent unnecessary re-renders
  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('/api/analytics');
      setData(response.data);
    } catch (error) {
      console.error('API fetch failed, using mock data:', error);
      setError('API unavailable, showing mock data');
      // Optimized mock data structure
      setData({
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Project Costs (₴)',
          data: [65000, 59000, 80000, 81000, 56000, 87000],
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Memoized chart component to prevent unnecessary re-renders
  const ChartComponent = useMemo(() => {
    if (!data) return null;
    return <Line data={data} options={chartOptions} />;
  }, [data]);

  if (loading) {
    return (
      <div className="p-4 animate-pulse">
        <div className="h-8 bg-gray-200 rounded mb-4 w-64"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Analytics Dashboard</h1>
      {error && (
        <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4">
          <p className="font-bold">Warning</p>
          <p>{error}</p>
        </div>
      )}
      <div className="bg-white rounded-lg shadow-lg p-6">
        {ChartComponent}
      </div>
      <div className="mt-4 text-sm text-gray-600">
        Last updated: {new Date().toLocaleString()}
      </div>
    </div>
  );
});

AnalyticsDashboard.displayName = 'AnalyticsDashboard';

export default AnalyticsDashboard;
