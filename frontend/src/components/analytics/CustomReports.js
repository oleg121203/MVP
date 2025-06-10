import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getCustomReports } from '../../store/customReportsSlice';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Grid, Paper, Typography, Box, Button, MenuItem, Select, FormControl, InputLabel } from '@mui/material';

function CustomReports() {
  const dispatch = useDispatch();
  const { data, loading, error } = useSelector((state) => state.customReports);
  const [chartData, setChartData] = useState([]);
  const [reportType, setReportType] = useState('cost');

  useEffect(() => {
    dispatch(getCustomReports(reportType));
  }, [dispatch, reportType]);

  useEffect(() => {
    if (data && data.length > 0) {
      // Process data for visualization
      const processedData = data.map(item => ({
        date: item.date,
        value: item[reportType]
      }));
      setChartData(processedData);
    }
  }, [data, reportType]);

  const handleReportTypeChange = (event) => {
    setReportType(event.target.value);
  };

  if (loading) return <Typography>Loading custom reports...</Typography>;
  if (error) return <Typography color="error">Error loading custom reports: {error}</Typography>;
  if (!data || data.length === 0) return <Typography>No data available for custom reports.</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Custom Analytics Reports</Typography>
      <FormControl sx={{ minWidth: 120, marginBottom: 2 }}>
        <InputLabel id="report-type-label">Report Type</InputLabel>
        <Select
          labelId="report-type-label"
          id="report-type-select"
          value={reportType}
          label="Report Type"
          onChange={handleReportTypeChange}
        >
          <MenuItem value="cost">Cost</MenuItem>
          <MenuItem value="performance">Performance</MenuItem>
          <MenuItem value="efficiency">Efficiency</MenuItem>
        </Select>
      </FormControl>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
            <Typography variant="h6">{reportType.charAt(0).toUpperCase() + reportType.slice(1)} Report</Typography>
            <ResponsiveContainer width="100%" height="80%">
              <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#82ca9d" name={reportType.charAt(0).toUpperCase() + reportType.slice(1)} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default CustomReports;
