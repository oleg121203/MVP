import React, { useState, useEffect, useCallback, useMemo, memo, useRef } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import AIChat from './AIChat';
import debounce from 'lodash.debounce'; // Assume lodash is installed; add if needed

import type { RootState } from '../src/store'; // Confirmed path fix for lint error ID: aa3dd8c8-c68a-45c1-8b8b-22dc58908e37

// Memoized chart options
const chartOptions = useMemo(() => ({
  responsive: true,
  plugins: {
    legend: { position: 'top' as const },
    title: { display: true, text: 'Analytics Overview' }
  },
  scales: {
    y: { beginAtZero: true }
  }
}), []); // Empty dependency array for static memoization

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
  const fetchRef = useRef(0);

  // Debounced data fetch to avoid rapid calls
  const fetchData = useCallback(debounce(async () => {
    const fetchId = ++fetchRef.current;
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('/api/analytics');
      if (fetchId === fetchRef.current) { // Ensure only latest call updates state
        setData(response.data);
      }
    } catch (error) {
      console.error('API fetch failed, using mock data:', error);
      if (fetchId === fetchRef.current) {
        setError('API unavailable, showing mock data');
        setData({
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [{
            label: 'Project Costs (₴)',
            data: [65000, 59000, 80000, 81000, 56000, 87000],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        });
      }
    } finally {
      if (fetchId === fetchRef.current) {
        setLoading(false);
      }
    }
  }, 300), []); // 300ms debounce delay

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Memoized chart component
  const ChartComponent = useMemo(() => {
    if (!data) return null;
    return <Line data={data} options={chartOptions} />;
  }, [data]);

  const exportData = () => {
    if (data) {
      const csvContent = "data:text/csv;charset=utf-8," + 
        "Labels,Data\n" + 
        data.labels.map((label, index) => `${label},${data.datasets[0].data[index]}`).join("\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "analytics_data.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

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
      <div className="bg-white rounded-lg shadow-lg p-6 mb-4">
        {ChartComponent}
      </div>
      <AIChat />
      <button onClick={exportData} className="bg-green-500 text-white p-2 mt-4">Export Data to CSV</button>
      <div className="mt-4 text-sm text-gray-600">
        Last updated: {new Date().toLocaleString()}
      </div>
    </div>
  );
});

AnalyticsDashboard.displayName = 'AnalyticsDashboard';

export default AnalyticsDashboard;