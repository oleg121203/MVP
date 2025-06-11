import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAuditLogs } from '../../store/securitySlice';
import { Box, Typography, Paper, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Grid, MenuItem, Select, FormControl, InputLabel, Chip } from '@mui/material';
import { Search as SearchIcon, FilterList as FilterListIcon, Refresh as RefreshIcon } from '@mui/icons-material';

function AuditLogViewer() {
  const dispatch = useDispatch();
  const { auditLogs, loading, error } = useSelector((state) => state.security);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterDate, setFilterDate] = useState('');

  useEffect(() => {
    dispatch(fetchAuditLogs({ type: filterType, date: filterDate }));
  }, [dispatch, filterType, filterDate]);

  const handleSearch = () => {
    // Simple client-side search for now
    // In a real app, this would be a server-side filter
    if (!searchTerm.trim()) {
      return auditLogs;
    }
    return auditLogs.filter(log => 
      log.action.toLowerCase().includes(searchTerm.toLowerCase()) || 
      log.user.toLowerCase().includes(searchTerm.toLowerCase()) || 
      log.details.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const handleTypeFilterChange = (event) => {
    setFilterType(event.target.value);
  };

  const handleDateFilterChange = (event) => {
    setFilterDate(event.target.value);
  };

  const handleRefresh = () => {
    dispatch(fetchAuditLogs({ type: filterType, date: filterDate }));
  };

  if (loading) return <Typography>Loading audit logs...</Typography>;
  if (error) return <Typography color="error">Error loading audit logs: {error}</Typography>;

  const filteredLogs = handleSearch();

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Audit Log Viewer</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField 
            value={searchTerm} 
            onChange={(e) => setSearchTerm(e.target.value)} 
            placeholder="Search logs..." 
            variant="outlined" 
            size="small"
            sx={{ width: 200 }}
            InputProps={{
              startAdornment: <SearchIcon />
            }}
          />
          <FormControl sx={{ minWidth: 120 }} size="small">
            <InputLabel id="type-filter-label">Type</InputLabel>
            <Select
              labelId="type-filter-label"
              id="type-filter"
              value={filterType}
              label="Type"
              onChange={handleTypeFilterChange}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="login">Login</MenuItem>
              <MenuItem value="logout">Logout</MenuItem>
              <MenuItem value="data_access">Data Access</MenuItem>
              <MenuItem value="config_change">Config Change</MenuItem>
              <MenuItem value="security">Security</MenuItem>
            </Select>
          </FormControl>
          <TextField 
            type="date"
            value={filterDate}
            onChange={handleDateFilterChange}
            variant="outlined"
            size="small"
            sx={{ width: 140 }}
          />
        </Box>
        <Button variant="outlined" onClick={handleRefresh} startIcon={<RefreshIcon />}>Refresh</Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2, height: '60vh', overflow: 'auto' }}>
            <Typography variant="h6">Audit Logs</Typography>
            {filteredLogs.length === 0 ? (
              <Typography>No audit logs found matching the search criteria.</Typography>
            ) : (
              <List>
                {filteredLogs.map((log, index) => (
                  <ListItem key={index} divider>
                    <ListItemText 
                      primary={`${log.action} by ${log.user}`} 
                      secondary={`Time: ${new Date(log.timestamp).toLocaleString()} | ${log.details}`} 
                    />
                    <ListItemSecondaryAction>
                      <Chip 
                        label={log.severity} 
                        color={log.severity === 'INFO' ? 'default' : log.severity === 'WARNING' ? 'warning' : 'error'} 
                        size="small" 
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default AuditLogViewer;
