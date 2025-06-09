import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { io } from 'socket.io-client';
import { fetchProjectMetrics, fetchRealTimeInsights } from '../redux/analyticsSlice';
import Chart from 'chart.js/auto';
import AIChat from './AIChat';
import './AnalyticsDashboard.css';

const socket = io('http://localhost:8001');

const AnalyticsDashboard = ({ projectId }) => {
  const dispatch = useDispatch();
  const { metrics, insights, loading, error } = useSelector((state) => state.analytics);
  const [chartInstances, setChartInstances] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // Fetch initial data
    dispatch(fetchProjectMetrics(projectId));
    dispatch(fetchRealTimeInsights(projectId));

    // Join project room for real-time updates
    socket.emit('join', `project_${projectId}`);

    // Listen for analytics updates
    socket.on('analytics_update', (data) => {
      if (data.type === 'insights') {
        dispatch({ type: 'analytics/updateInsights', payload: data.data });
      }
    });

    // Clear all charts on unmount
    return () => {
      chartInstances.forEach(chart => chart.destroy());
      socket.emit('leave', `project_${projectId}`);
      socket.off('analytics_update');
    };
  }, [dispatch, projectId]);

  useEffect(() => {
    if (metrics) {
      // Destroy existing charts
      chartInstances.forEach(chart => chart.destroy());
      
      // Create new charts
      const newCharts = [];
      
      // Overview Chart
      const overviewCtx = document.getElementById('overviewChart').getContext('2d');
      newCharts.push(new Chart(overviewCtx, {
        type: 'bar',
        data: {
          labels: ['Completion', 'Budget', 'Timeline', 'Resources'],
          datasets: [{
            label: 'Project Metrics',
            data: [
              metrics.completion_rate,
              metrics.budget_compliance,
              metrics.timeline_adherence,
              metrics.resource_utilization
            ],
            backgroundColor: [
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 99, 132, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
              'rgba(54, 162, 235, 1)',
              'rgba(255, 99, 132, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      }));
      
      setChartInstances(newCharts);
    }
  }, [metrics]);

  if (loading) return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Loading analytics data...</p>
    </div>
  );
  
  if (error) return (
    <div className="error-container">
      <h3>Error Loading Analytics</h3>
      <p>{error}</p>
      <button onClick={() => {
        dispatch(fetchProjectMetrics(projectId));
        dispatch(fetchRealTimeInsights(projectId));
      }}>
        Retry
      </button>
    </div>
  );

  return (
    <div className="analytics-dashboard">
      <div className="dashboard-header">
        <h2>Project Analytics</h2>
        <div className="tabs">
          <button 
            className={activeTab === 'overview' ? 'active' : ''}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button 
            className={activeTab === 'insights' ? 'active' : ''}
            onClick={() => setActiveTab('insights')}
          >
            AI Insights
          </button>
        </div>
      </div>

      {activeTab === 'overview' && (
        <div className="metrics-container">
          <div className="chart-wrapper">
            <canvas id="overviewChart"></canvas>
          </div>
          
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Completion</h3>
              <div className="metric-value">
                {metrics?.completion_rate || 0}%
              </div>
            </div>
            <div className="metric-card">
              <h3>Budget</h3>
              <div className="metric-value">
                {metrics?.budget_compliance || 0}%
              </div>
            </div>
            <div className="metric-card">
              <h3>Timeline</h3>
              <div className="metric-value">
                {metrics?.timeline_adherence || 0}%
              </div>
            </div>
            <div className="metric-card">
              <h3>Resources</h3>
              <div className="metric-value">
                {metrics?.resource_utilization || 0}%
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'insights' && (
        <div className="insights-container">
          <div className="insights-list">
            {insights.length > 0 ? (
              insights.map((insight) => (
                <div key={insight.id} className="insight-card">
                  <h4>{insight.title}</h4>
                  <p>{insight.summary}</p>
                  <div className="insight-meta">
                    <span>{new Date(insight.timestamp).toLocaleString()}</span>
                    <span>{insight.confidence}% confidence</span>
                  </div>
                </div>
              ))
            ) : (
              <p>No insights available yet</p>
            )}
          </div>
          <AIChat projectId={projectId} />
        </div>
      )}
    </div>
  );
};

export default AnalyticsDashboard;
