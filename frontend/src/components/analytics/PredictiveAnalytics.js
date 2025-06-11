import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPredictiveData } from '../../store/reportingSlice';
import { Box, Typography, Grid, Paper, ButtonGroup, Button } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';

function PredictiveAnalytics() {
  const dispatch = useDispatch();
  const { predictiveData, loading, error } = useSelector((state) => state.reporting);
  const [timeRange, setTimeRange] = useState('quarterly');
  const [predictionType, setPredictionType] = useState('sales');

  useEffect(() => {
    dispatch(fetchPredictiveData({ timeRange, type: predictionType }));
  }, [dispatch, timeRange, predictionType]);

  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };

  const handlePredictionTypeChange = (type) => {
    setPredictionType(type);
  };

  if (loading) return <Typography>Loading predictive analytics data...</Typography>;
  if (error) return <Typography color="error">Error loading predictive analytics data: {error}</Typography>;

  const renderChart = () => {
    if (!predictiveData || predictiveData.length === 0) {
      return <Typography>No data available for the selected time range and prediction type.</Typography>;
    }

    return (
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={predictiveData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="actual" stroke="#8884d8" name="Actual" />
          <Line type="monotone" dataKey="predicted" stroke="#82ca9d" name="Predicted" strokeDasharray="5 5" />
        </LineChart>
      </ResponsiveContainer>
    );
  };

  const renderConfidenceChart = () => {
    if (!predictiveData || predictiveData.length === 0) {
      return <Typography>No confidence data available.</Typography>;
    }

    return (
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid />
          <XAxis type="number" dataKey="confidence" name="Confidence" unit="%" />
          <YAxis type="number" dataKey="value" name="Value" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter name="Predictions" data={predictiveData} fill="#8884d8" />
        </ScatterChart>
      </ResponsiveContainer>
    );
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Predictive Analytics Integration</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Prediction Controls</Typography>
            <Box sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
              <ButtonGroup variant="contained">
                <Button onClick={() => handlePredictionTypeChange('sales')} color={predictionType === 'sales' ? 'primary' : 'default'}>Sales</Button>
                <Button onClick={() => handlePredictionTypeChange('userGrowth')} color={predictionType === 'userGrowth' ? 'primary' : 'default'}>User Growth</Button>
                <Button onClick={() => handlePredictionTypeChange('churnRate')} color={predictionType === 'churnRate' ? 'primary' : 'default'}>Churn Rate</Button>
              </ButtonGroup>
              <ButtonGroup variant="contained">
                <Button onClick={() => handleTimeRangeChange('monthly')} color={timeRange === 'monthly' ? 'primary' : 'default'}>Monthly</Button>
                <Button onClick={() => handleTimeRangeChange('quarterly')} color={timeRange === 'quarterly' ? 'primary' : 'default'}>Quarterly</Button>
                <Button onClick={() => handleTimeRangeChange('yearly')} color={timeRange === 'yearly' ? 'primary' : 'default'}>Yearly</Button>
              </ButtonGroup>
            </Box>
            {renderChart()}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Confidence Levels</Typography>
            {renderConfidenceChart()}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Insights & Recommendations</Typography>
            <Box sx={{ marginTop: 2 }}>
              <Typography variant="body1"><strong>Trend Analysis:</strong> Based on the current data, the trend suggests a potential increase in {predictionType} over the next period.</Typography>
              <Typography variant="body1"><strong>Recommendation:</strong> Consider allocating additional resources to capitalize on predicted growth.</Typography>
              <Typography variant="body1"><strong>Confidence:</strong> The model shows an average confidence of 85% for this prediction.</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default PredictiveAnalytics;
