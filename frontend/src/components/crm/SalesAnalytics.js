import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchSalesData } from '../../store/salesAnalyticsSlice';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Grid, Paper, Typography, Box, ButtonGroup, Button } from '@mui/material';

function SalesAnalytics() {
  const dispatch = useDispatch();
  const { data, loading, error } = useSelector((state) => state.salesAnalytics);
  const [chartData, setChartData] = useState([]);
  const [viewMode, setViewMode] = useState('monthly');

  useEffect(() => {
    dispatch(fetchSalesData(viewMode));
  }, [dispatch, viewMode]);

  useEffect(() => {
    if (data && data.length > 0) {
      // Process data for visualization
      const processedData = data.map(item => ({
        date: item.date,
        sales: item.sales,
        leads: item.leads,
        conversionRate: item.conversionRate
      }));
      setChartData(processedData);
    }
  }, [data]);

  const handleViewModeChange = (mode) => {
    setViewMode(mode);
  };

  if (loading) return <Typography>Loading sales data...</Typography>;
  if (error) return <Typography color="error">Error loading sales data: {error}</Typography>;
  if (!data || data.length === 0) return <Typography>No sales data available for visualization.</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Sales Analytics Dashboard</Typography>
      <ButtonGroup sx={{ marginBottom: 2 }}>
        <Button 
          variant={viewMode === 'weekly' ? 'contained' : 'outlined'} 
          onClick={() => handleViewModeChange('weekly')}
        >
          Weekly
        </Button>
        <Button 
          variant={viewMode === 'monthly' ? 'contained' : 'outlined'} 
          onClick={() => handleViewModeChange('monthly')}
        >
          Monthly
        </Button>
        <Button 
          variant={viewMode === 'quarterly' ? 'contained' : 'outlined'} 
          onClick={() => handleViewModeChange('quarterly')}
        >
          Quarterly
        </Button>
        <Button 
          variant={viewMode === 'yearly' ? 'contained' : 'outlined'} 
          onClick={() => handleViewModeChange('yearly')}
        >
          Yearly
        </Button>
      </ButtonGroup>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">Sales Performance ({viewMode.charAt(0).toUpperCase() + viewMode.slice(1)})</Typography>
            <ResponsiveContainer width="100%" height="80%">
              <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="sales" fill="#8884d8" name="Sales ($)" />
                <Bar dataKey="leads" fill="#82ca9d" name="Leads" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">Conversion Rate ({viewMode.charAt(0).toUpperCase() + viewMode.slice(1)})</Typography>
            <ResponsiveContainer width="100%" height="80%">
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="conversionRate" stroke="#ffc658" name="Conversion Rate (%)" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default SalesAnalytics;
