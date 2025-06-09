import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Box, Typography, Paper, Grid, Divider } from '@mui/material';
import ChatInterface from '../chat/ChatInterface';

const AnalyticsDashboard = () => {
  const { projectId } = useParams();
  const [metrics, setMetrics] = useState({});
  const [insights, setInsights] = useState([]);
  const [trends, setTrends] = useState({ dates: [], metrics: {} });
  const [aiInsights, setAiInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const metricsRes = await axios.get(`/api/analytics/project/${projectId}/metrics`);
        setMetrics(metricsRes.data);

        const insightsRes = await axios.get(`/api/analytics/project/${projectId}/insights`);
        setInsights(insightsRes.data);

        const trendsRes = await axios.get(`/api/analytics/project/${projectId}/trends`);
        setTrends(trendsRes.data);

        const aiInsightsRes = await axios.get(`/api/analytics/project/${projectId}/ai-insights`);
        setAiInsights(aiInsightsRes.data);

        setLoading(false);
      } catch (error) {
        console.error('Error fetching analytics data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, [projectId]);

  if (loading) {
    return <Box>Loading...</Box>;
  }

  // Prepare data for chart
  const chartData = trends.dates.map((date, index) => {
    const dataPoint = { date };
    Object.keys(trends.metrics).forEach(metric => {
      dataPoint[metric] = trends.metrics[metric][index];
    });
    return dataPoint;
  });

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Project Analytics Dashboard
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }} elevation={3}>
            <Typography variant="h6">Key Metrics</Typography>
            <Divider sx={{ my: 1 }} />
            {Object.keys(metrics).length > 0 ? (
              <Box>
                {Object.entries(metrics).map(([key, value]) => (
                  <Typography key={key} variant="body1">{key}: {value}</Typography>
                ))}
              </Box>
            ) : (
              <Typography>No metrics available</Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }} elevation={3}>
            <Typography variant="h6">AI Insights</Typography>
            <Divider sx={{ my: 1 }} />
            {aiInsights.length > 0 ? (
              <Box>
                {aiInsights.map((insight, index) => (
                  <Typography key={index} variant="body1">- {insight}</Typography>
                ))}
              </Box>
            ) : (
              <Typography>No AI insights available</Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2, height: 400 }} elevation={3}>
            <Typography variant="h6">Trend Analysis</Typography>
            <Divider sx={{ my: 1 }} />
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  {Object.keys(trends.metrics).map(metric => (
                    <Line key={metric} type="monotone" dataKey={metric} stroke={`#${Math.floor(Math.random()*16777215).toString(16)}`} />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <Typography>No trend data available</Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }} elevation={3}>
            <Typography variant="h6">Real-Time Insights</Typography>
            <Divider sx={{ my: 1 }} />
            {insights.length > 0 ? (
              <Box>
                {insights.map((insight, index) => (
                  <Typography key={index} variant="body2">{JSON.stringify(insight)}</Typography>
                ))}
              </Box>
            ) : (
              <Typography>No real-time insights available</Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }} elevation={3}>
            <Typography variant="h6">AI Chat Interface</Typography>
            <Divider sx={{ my: 1 }} />
            <ChatInterface projectId={projectId} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AnalyticsDashboard;
