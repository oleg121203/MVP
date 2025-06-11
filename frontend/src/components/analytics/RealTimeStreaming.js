import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { startStreaming, stopStreaming } from '../../store/realTimeDataSlice';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Grid, Paper, Typography, Box, Button } from '@mui/material';

function RealTimeStreaming() {
  const dispatch = useDispatch();
  const { data, streaming, error } = useSelector((state) => state.realTimeData);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (streaming) {
      // Simulate real-time data updates (in a real app, this would be from a WebSocket or stream)
      const interval = setInterval(() => {
        // This would be updated by actual streaming data
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [streaming]);

  useEffect(() => {
    if (data && data.length > 0) {
      // Process data for visualization (keep last 20 data points for performance)
      const processedData = data.slice(-20).map(item => ({
        time: new Date(item.timestamp).toLocaleTimeString(),
        value: item.value
      }));
      setChartData(processedData);
    }
  }, [data]);

  const handleStartStreaming = () => {
    dispatch(startStreaming());
  };

  const handleStopStreaming = () => {
    dispatch(stopStreaming());
  };

  if (error) return <Typography color="error">Error in streaming: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Real-time Data Streaming</Typography>
      <Box sx={{ marginBottom: 2 }}>
        <Button 
          variant="contained" 
          onClick={handleStartStreaming} 
          disabled={streaming}
          sx={{ marginRight: 1 }}
        >
          Start Streaming
        </Button>
        <Button 
          variant="contained" 
          color="secondary" 
          onClick={handleStopStreaming} 
          disabled={!streaming}
        >
          Stop Streaming
        </Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">Real-time Data</Typography>
            {streaming ? (
              <Typography>Streaming: Active</Typography>
            ) : (
              <Typography>Streaming: Inactive</Typography>
            )}
            <ResponsiveContainer width="100%" height="80%">
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#8884d8" name="Data Value" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default RealTimeStreaming;
