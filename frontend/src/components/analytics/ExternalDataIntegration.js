import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { connectExternalDataSource, fetchExternalData } from '../../store/externalDataSlice';
import { Grid, Paper, Typography, Box, Button, TextField, MenuItem, Select, FormControl, InputLabel } from '@mui/material';

function ExternalDataIntegration() {
  const dispatch = useDispatch();
  const { data, loading, error, connectionStatus } = useSelector((state) => state.externalData);
  const [sourceType, setSourceType] = useState('api');
  const [apiUrl, setApiUrl] = useState('');
  const [apiKey, setApiKey] = useState('');

  useEffect(() => {
    // Fetch data if a connection is established
    if (connectionStatus === 'connected') {
      dispatch(fetchExternalData());
    }
  }, [dispatch, connectionStatus]);

  const handleSourceTypeChange = (event) => {
    setSourceType(event.target.value);
  };

  const handleConnect = () => {
    if (sourceType === 'api' && apiUrl && apiKey) {
      dispatch(connectExternalDataSource({ type: sourceType, url: apiUrl, key: apiKey }));
    } else {
      alert('Please provide API URL and Key');
    }
  };

  if (loading) return <Typography>Loading external data...</Typography>;
  if (error) return <Typography color="error">Error: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>External Data Integration</Typography>
      <FormControl sx={{ minWidth: 120, marginBottom: 2 }}>
        <InputLabel id="source-type-label">Source Type</InputLabel>
        <Select
          labelId="source-type-label"
          id="source-type-select"
          value={sourceType}
          label="Source Type"
          onChange={handleSourceTypeChange}
        >
          <MenuItem value="api">API</MenuItem>
          <MenuItem value="database">Database</MenuItem>
          <MenuItem value="csv">CSV File</MenuItem>
        </Select>
      </FormControl>
      {sourceType === 'api' && (
        <Box sx={{ marginBottom: 2 }}>
          <TextField 
            label="API URL" 
            variant="outlined" 
            fullWidth 
            value={apiUrl} 
            onChange={(e) => setApiUrl(e.target.value)} 
            sx={{ marginBottom: 1 }}
          />
          <TextField 
            label="API Key" 
            variant="outlined" 
            fullWidth 
            type="password"
            value={apiKey} 
            onChange={(e) => setApiKey(e.target.value)} 
          />
        </Box>
      )}
      <Button variant="contained" onClick={handleConnect} disabled={connectionStatus === 'connected'}>
        {connectionStatus === 'connected' ? 'Connected' : 'Connect to Source'}
      </Button>
      {connectionStatus === 'connected' && (
        <Grid container spacing={3} sx={{ marginTop: 2 }}>
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ padding: 2, height: 300 }}>
              <Typography variant="h6">External Data Overview</Typography>
              {data && data.length > 0 ? (
                <Typography>Data loaded: {data.length} records</Typography>
              ) : (
                <Typography>No data available from external source.</Typography>
              )}
            </Paper>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}

export default ExternalDataIntegration;
