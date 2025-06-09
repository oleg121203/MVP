import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import io from 'socket.io-client';
import AIChatInterface from './AIChatInterface';
import ExportAnalytics from './ExportAnalytics';

Chart.register(...registerables);

const AnalyticsDashboard = ({ projectId }) => {
  const [metrics, setMetrics] = useState({
    completionRate: 0,
    budgetUtilization: 0,
    timeEfficiency: 0
  });
  const [insights, setInsights] = useState('');
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Completion Rate',
        data: [],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  });

  useEffect(() => {
    // Connect to WebSocket
    const socket = io('http://localhost:8000', {
      path: '/socket.io',
      transports: ['websocket']
    });

    // Subscribe to project updates
    socket.emit('subscribe', { projectId });

    // Handle real-time updates
    socket.on('analytics_update', (data) => {
      setMetrics(prev => ({
        ...prev,
        ...data.metrics
      }));
      
      if (data.insights) {
        setInsights(data.insights);
      }

      // Update chart data
      setChartData(prev => ({
        labels: [...prev.labels, new Date().toLocaleTimeString()],
        datasets: [
          {
            ...prev.datasets[0],
            data: [...prev.datasets[0].data, data.metrics.completionRate]
          }
        ]
      }));
    });

    return () => socket.disconnect();
  }, [projectId]);

  return (
    <div className="analytics-dashboard">
      <div className="dashboard-header">
        <h2>Project Analytics</h2>
        <ExportAnalytics projectId={projectId} metrics={metrics} />
      </div>
      
      <div className="dashboard-content">
        <div className="metrics-section">
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Completion Rate</h3>
              <p>{(metrics.completionRate * 100).toFixed(1)}%</p>
            </div>
            
            <div className="metric-card">
              <h3>Budget Utilization</h3>
              <p>{(metrics.budgetUtilization * 100).toFixed(1)}%</p>
            </div>
            
            <div className="metric-card">
              <h3>Time Efficiency</h3>
              <p>{metrics.timeEfficiency.toFixed(2)} tasks/day</p>
            </div>
          </div>
          <div className="chart-container">
            <Line data={chartData} />
          </div>
        </div>
        
        <div className="ai-section">
          <div className="insights-container">
            <h3>AI Insights</h3>
            <p>{insights || 'No insights yet'}</p>
          </div>
          <AIChatInterface projectId={projectId} />
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
