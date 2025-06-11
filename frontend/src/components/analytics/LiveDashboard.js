import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { connectWebSocket, disconnectWebSocket } from '../../store/webSocketSlice';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Grid, Paper, Typography, Box, Button } from '@mui/material';

function LiveDashboard() {
  const dispatch = useDispatch();
  const { data, connected, error } = useSelector((state) => state.webSocket);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (connected) {
      // WebSocket connection is managed by the slice
      // Data updates are handled by the slice as well
    }
  }, [connected]);

  useEffect(() => {
    if (data && data.length > 0) {
      // Process data for visualization (keep last 30 data points for performance)
      const processedData = data.slice(-30).map(item => ({
        time: new Date(item.timestamp).toLocaleTimeString(),
        value: item.value
      }));
      setChartData(processedData);
    }
  }, [data]);

  const handleConnect = () => {
    dispatch(connectWebSocket());
  };

  const handleDisconnect = () => {
    dispatch(disconnectWebSocket());
  };

  if (error) return <Typography color="error">Error in WebSocket connection: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Live Dashboard Updates</Typography>
      <Box sx={{ marginBottom: 2 }}>
        <Button 
          variant="contained" 
          onClick={handleConnect} 
          disabled={connected}
          sx={{ marginRight: 1 }}
        >
          Connect WebSocket
        </Button>
        <Button 
          variant="contained" 
          color="secondary" 
          onClick={handleDisconnect} 
          disabled={!connected}
        >
          Disconnect WebSocket
        </Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">Live Data Stream</Typography>
            {connected ? (
              <Typography>WebSocket: Connected</Typography>
            ) : (
              <Typography>WebSocket: Disconnected</Typography>
            )}
            <ResponsiveContainer width="100%" height="80%">
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#8884d8" name="Live Data Value" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default LiveDashboard;
