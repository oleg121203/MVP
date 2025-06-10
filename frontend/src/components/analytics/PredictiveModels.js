import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getPredictiveData } from '../../store/predictiveModelsSlice';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Grid, Paper, Typography, Box } from '@mui/material';

function PredictiveModels() {
  const dispatch = useDispatch();
  const { data, loading, error } = useSelector((state) => state.predictiveModels);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    dispatch(getPredictiveData());
  }, [dispatch]);

  useEffect(() => {
    if (data && data.length > 0) {
      // Process data for visualization
      const processedData = data.map(item => ({
        date: item.date,
        predicted_cost: item.predicted_cost
      }));
      setChartData(processedData);
    }
  }, [data]);

  if (loading) return <Typography>Loading predictive data...</Typography>;
  if (error) return <Typography color="error">Error loading predictive data: {error}</Typography>;
  if (!data || data.length === 0) return <Typography>No predictive data available for visualization.</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Predictive Analytics</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">Cost Prediction</Typography>
            <ResponsiveContainer width="100%" height="80%">
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="predicted_cost" stroke="#ff7300" name="Predicted Cost" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default PredictiveModels;
