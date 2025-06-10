import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getAnalyticsData } from '../../store/analyticsSlice';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Grid, Paper, Typography, Box } from '@mui/material';

function AdvancedVisualization() {
  const dispatch = useDispatch();
  const { data, loading, error } = useSelector((state) => state.analytics);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    dispatch(getAnalyticsData());
  }, [dispatch]);

  useEffect(() => {
    if (data && data.length > 0) {
      // Process data for visualization
      const processedData = data.map(item => ({
        date: item.date,
        cost: item.cost,
        performance: item.performance,
        efficiency: item.efficiency
      }));
      setChartData(processedData);
    }
  }, [data]);

  if (loading) return <Typography>Loading data...</Typography>;
  if (error) return <Typography color="error">Error loading data: {error}</Typography>;
  if (!data || data.length === 0) return <Typography>No data available for visualization.</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Advanced Data Visualization</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">Cost Analysis</Typography>
            <ResponsiveContainer width="100%" height="80%">
              <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="cost" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">Performance Trends</Typography>
            <ResponsiveContainer width="100%" height="80%">
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="performance" stroke="#8884d8" />
                <Line type="monotone" dataKey="efficiency" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default AdvancedVisualization;
