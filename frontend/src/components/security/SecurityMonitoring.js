import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchSecurityEvents } from '../../store/securitySlice';
import { Box, Typography, Grid, Paper, Button, List, ListItem, ListItemText, ListItemSecondaryAction, Chip, CircularProgress } from '@mui/material';
import { Refresh as RefreshIcon, Warning as WarningIcon, Error as ErrorIcon } from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function SecurityMonitoring() {
  const dispatch = useDispatch();
  const { securityEvents, loading, error } = useSelector((state) => state.security);
  const [timeRange, setTimeRange] = useState('24h');

  useEffect(() => {
    dispatch(fetchSecurityEvents({ timeRange }));
    const interval = setInterval(() => {
      dispatch(fetchSecurityEvents({ timeRange }));
    }, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, [dispatch, timeRange]);

  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };

  const handleRefresh = () => {
    dispatch(fetchSecurityEvents({ timeRange }));
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', padding: 2 }}><CircularProgress /></Box>;
  if (error) return <Typography color="error">Error loading security events: {error}</Typography>;

  // Calculate summary data for charts
  const summaryData = [];
  const severityCounts = { critical: 0, high: 0, medium: 0, low: 0 };
  if (securityEvents && securityEvents.length > 0) {
    const now = new Date();
    const interval = timeRange === '24h' ? 60 * 60 * 1000 : timeRange === '7d' ? 24 * 60 * 60 * 1000 : 7 * 24 * 60 * 60 * 1000;
    const startTime = timeRange === '24h' ? now - 24 * 60 * 60 * 1000 : timeRange === '7d' ? now - 7 * 24 * 60 * 60 * 1000 : now - 30 * 24 * 60 * 60 * 1000;
    let currentInterval = startTime;
    while (currentInterval < now) {
      const intervalEnd = new Date(currentInterval.getTime() + interval);
      const eventsInInterval = securityEvents.filter(event => {
        const eventTime = new Date(event.timestamp);
        return eventTime >= currentInterval && eventTime < intervalEnd;
      });
      summaryData.push({
        time: currentInterval.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        count: eventsInInterval.length
      });
      eventsInInterval.forEach(event => {
        if (event.severity === 'CRITICAL') severityCounts.critical++;
        else if (event.severity === 'HIGH') severityCounts.high++;
        else if (event.severity === 'MEDIUM') severityCounts.medium++;
        else severityCounts.low++;
      });
      currentInterval = intervalEnd;
    }
  }

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Real-Time Security Monitoring</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button 
            variant={timeRange === '24h' ? 'contained' : 'outlined'} 
            onClick={() => handleTimeRangeChange('24h')}
          >
            Last 24 Hours
          </Button>
          <Button 
            variant={timeRange === '7d' ? 'contained' : 'outlined'} 
            onClick={() => handleTimeRangeChange('7d')}
          >
            Last 7 Days
          </Button>
          <Button 
            variant={timeRange === '30d' ? 'contained' : 'outlined'} 
            onClick={() => handleTimeRangeChange('30d')}
          >
            Last 30 Days
          </Button>
        </Box>
        <Button variant="outlined" onClick={handleRefresh} startIcon={<RefreshIcon />}>Refresh Now</Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
            <Typography variant="h6">Security Event Trends</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={summaryData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#8884d8" name="Events" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
            <Typography variant="h6">Severity Distribution</Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, marginTop: 5 }}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="error">{severityCounts.critical}</Typography>
                <Typography variant="caption">Critical</Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="warning.main">{severityCounts.high}</Typography>
                <Typography variant="caption">High</Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="orange">{severityCounts.medium}</Typography>
                <Typography variant="caption">Medium</Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="textSecondary">{severityCounts.low}</Typography>
                <Typography variant="caption">Low</Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2, height: '40vh', overflow: 'auto' }}>
            <Typography variant="h6">Recent Security Events</Typography>
            {securityEvents && securityEvents.length > 0 ? (
              <List>
                {securityEvents.slice(0, 10).map((event, index) => (
                  <ListItem key={index} divider>
                    <ListItemText 
                      primary={event.eventType} 
                      secondary={`Time: ${new Date(event.timestamp).toLocaleString()} | Source: ${event.source} | ${event.description}`} 
                    />
                    <ListItemSecondaryAction>
                      <Chip 
                        label={event.severity} 
                        color={event.severity === 'CRITICAL' ? 'error' : event.severity === 'HIGH' ? 'warning' : event.severity === 'MEDIUM' ? 'default' : 'success'} 
                        size="small" 
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography>No recent security events to display.</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default SecurityMonitoring;
