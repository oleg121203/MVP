import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchVisualizationData } from '../../store/reportingSlice';
import { Box, Typography, Grid, Paper, ButtonGroup, Button } from '@mui/material';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function DataVisualization() {
  const dispatch = useDispatch();
  const { visualizationData, loading, error } = useSelector((state) => state.reporting);
  const [chartType, setChartType] = useState('bar');
  const [timeRange, setTimeRange] = useState('monthly');

  useEffect(() => {
    dispatch(fetchVisualizationData(timeRange));
  }, [dispatch, timeRange]);

  const handleChartTypeChange = (type) => {
    setChartType(type);
  };

  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };

  if (loading) return <Typography>Loading visualization data...</Typography>;
  if (error) return <Typography color="error">Error loading visualization data: {error}</Typography>;

  const renderChart = () => {
    if (!visualizationData || visualizationData.length === 0) {
      return <Typography>No data available for the selected time range.</Typography>;
    }

    if (chartType === 'bar') {
      return (
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={visualizationData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" name="Value" />
          </BarChart>
        </ResponsiveContainer>
      );
    } else {
      return (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={visualizationData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" name="Value" />
          </LineChart>
        </ResponsiveContainer>
      );
    }
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Data Visualization Enhancements</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Visualization Controls</Typography>
            <Box sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
              <ButtonGroup variant="contained">
                <Button onClick={() => handleChartTypeChange('bar')} color={chartType === 'bar' ? 'primary' : 'default'}>Bar Chart</Button>
                <Button onClick={() => handleChartTypeChange('line')} color={chartType === 'line' ? 'primary' : 'default'}>Line Chart</Button>
              </ButtonGroup>
              <ButtonGroup variant="contained">
                <Button onClick={() => handleTimeRangeChange('daily')} color={timeRange === 'daily' ? 'primary' : 'default'}>Daily</Button>
                <Button onClick={() => handleTimeRangeChange('weekly')} color={timeRange === 'weekly' ? 'primary' : 'default'}>Weekly</Button>
                <Button onClick={() => handleTimeRangeChange('monthly')} color={timeRange === 'monthly' ? 'primary' : 'default'}>Monthly</Button>
                <Button onClick={() => handleTimeRangeChange('yearly')} color={timeRange === 'yearly' ? 'primary' : 'default'}>Yearly</Button>
              </ButtonGroup>
            </Box>
            {renderChart()}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default DataVisualization;
