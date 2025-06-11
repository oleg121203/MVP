import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAnalyticsData } from '../../store/reportingSlice';
import { Box, Typography, Grid, Paper, ButtonGroup, Button, Card, CardContent, CardHeader } from '@mui/material';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

function AnalyticsDashboard() {
  const dispatch = useDispatch();
  const { analyticsData, loading, error } = useSelector((state) => state.reporting);
  const [chartType, setChartType] = useState('bar');
  const [timeRange, setTimeRange] = useState('monthly');
  const [selectedWidget, setSelectedWidget] = useState('overview');

  useEffect(() => {
    dispatch(fetchAnalyticsData({ timeRange, widget: selectedWidget }));
  }, [dispatch, timeRange, selectedWidget]);

  const handleChartTypeChange = (type) => {
    setChartType(type);
  };

  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };

  const handleWidgetChange = (widget) => {
    setSelectedWidget(widget);
  };

  if (loading) return <Typography>Loading analytics data...</Typography>;
  if (error) return <Typography color="error">Error loading analytics data: {error}</Typography>;

  const renderChart = () => {
    if (!analyticsData || analyticsData.length === 0) {
      return <Typography>No data available for the selected time range and widget.</Typography>;
    }

    if (chartType === 'bar') {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={analyticsData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" name="Value" />
          </BarChart>
        </ResponsiveContainer>
      );
    } else if (chartType === 'line') {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={analyticsData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" name="Value" />
          </LineChart>
        </ResponsiveContainer>
      );
    } else {
      const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];
      return (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={analyticsData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {analyticsData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      );
    }
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Advanced Analytics Dashboard</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
            <Typography variant="h6">Dashboard Widgets</Typography>
            <ButtonGroup orientation="vertical" variant="contained" fullWidth sx={{ marginTop: 2 }}>
              <Button onClick={() => handleWidgetChange('overview')} color={selectedWidget === 'overview' ? 'primary' : 'default'}>Overview</Button>
              <Button onClick={() => handleWidgetChange('sales')} color={selectedWidget === 'sales' ? 'primary' : 'default'}>Sales</Button>
              <Button onClick={() => handleWidgetChange('userActivity')} color={selectedWidget === 'userActivity' ? 'primary' : 'default'}>User Activity</Button>
              <Button onClick={() => handleWidgetChange('performance')} color={selectedWidget === 'performance' ? 'primary' : 'default'}>Performance</Button>
            </ButtonGroup>
          </Paper>
        </Grid>
        <Grid item xs={12} md={9}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Visualization Controls</Typography>
            <Box sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
              <ButtonGroup variant="contained">
                <Button onClick={() => handleChartTypeChange('bar')} color={chartType === 'bar' ? 'primary' : 'default'}>Bar Chart</Button>
                <Button onClick={() => handleChartTypeChange('line')} color={chartType === 'line' ? 'primary' : 'default'}>Line Chart</Button>
                <Button onClick={() => handleChartTypeChange('pie')} color={chartType === 'pie' ? 'primary' : 'default'}>Pie Chart</Button>
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
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader title="Quick Stats" />
            <CardContent>
              <Typography variant="h6">Total Sales</Typography>
              <Typography variant="body2">$125,000</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader title="Quick Stats" />
            <CardContent>
              <Typography variant="h6">Active Users</Typography>
              <Typography variant="body2">1,250</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader title="Quick Stats" />
            <CardContent>
              <Typography variant="h6">Conversion Rate</Typography>
              <Typography variant="body2">12.5%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader title="Quick Stats" />
            <CardContent>
              <Typography variant="h6">Performance Index</Typography>
              <Typography variant="body2">85/100</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default AnalyticsDashboard;
