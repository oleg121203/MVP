import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchSyncConfigs, createSyncConfig, updateSyncConfig, deleteSyncConfig, startSync } from '../../store/dataSyncSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon, Sync as SyncIcon } from '@mui/icons-material';

function DataSync() {
  const dispatch = useDispatch();
  const { syncConfigs, loading, error } = useSelector((state) => state.dataSync);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingConfig, setEditingConfig] = useState(null);
  const [configName, setConfigName] = useState('');
  const [sourceType, setSourceType] = useState('api');
  const [targetType, setTargetType] = useState('database');
  const [sourceDetails, setSourceDetails] = useState('');
  const [targetDetails, setTargetDetails] = useState('');
  const [frequency, setFrequency] = useState('daily');

  useEffect(() => {
    dispatch(fetchSyncConfigs());
  }, [dispatch]);

  const handleOpenDialog = (config = null) => {
    if (config) {
      setEditingConfig(config);
      setConfigName(config.name);
      setSourceType(config.sourceType);
      setTargetType(config.targetType);
      setSourceDetails(config.sourceDetails);
      setTargetDetails(config.targetDetails);
      setFrequency(config.frequency);
    } else {
      setEditingConfig(null);
      setConfigName('');
      setSourceType('api');
      setTargetType('database');
      setSourceDetails('');
      setTargetDetails('');
      setFrequency('daily');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveConfig = () => {
    if (editingConfig) {
      dispatch(updateSyncConfig({ id: editingConfig.id, name: configName, sourceType, targetType, sourceDetails, targetDetails, frequency }));
    } else {
      dispatch(createSyncConfig({ name: configName, sourceType, targetType, sourceDetails, targetDetails, frequency }));
    }
    handleCloseDialog();
  };

  const handleDeleteConfig = (id) => {
    dispatch(deleteSyncConfig(id));
  };

  const handleStartSync = (id) => {
    dispatch(startSync(id));
  };

  const handleSourceTypeChange = (event) => {
    setSourceType(event.target.value);
  };

  const handleTargetTypeChange = (event) => {
    setTargetType(event.target.value);
  };

  const handleFrequencyChange = (event) => {
    setFrequency(event.target.value);
  };

  if (loading) return <Typography>Loading sync configurations...</Typography>;
  if (error) return <Typography color="error">Error loading sync configurations: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Enterprise Data Sync</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Sync Configuration
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Sync Configurations List</Typography>
            {syncConfigs.length === 0 ? (
              <Typography>No sync configurations available. Create a new configuration to get started.</Typography>
            ) : (
              <List>
                {syncConfigs.map((config) => (
                  <ListItem key={config.id}>
                    <ListItemText 
                      primary={config.name} 
                      secondary={`Source: ${config.sourceType} (${config.sourceDetails}), Target: ${config.targetType} (${config.targetDetails}), Frequency: ${config.frequency}`} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="sync" onClick={() => handleStartSync(config.id)} size="small" sx={{ marginRight: 1 }}>
                        <SyncIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(config)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteConfig(config.id)} size="small">
                        <DeleteIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog for Adding/Editing Sync Configurations */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingConfig ? 'Edit Sync Configuration' : 'Add New Sync Configuration'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Configuration Name"
            fullWidth
            value={configName}
            onChange={(e) => setConfigName(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="source-type-select-label">Source Type</InputLabel>
            <Select
              labelId="source-type-select-label"
              id="source-type-select"
              value={sourceType}
              label="Source Type"
              onChange={handleSourceTypeChange}
            >
              <MenuItem value="api">API</MenuItem>
              <MenuItem value="database">Database</MenuItem>
              <MenuItem value="file">File System</MenuItem>
              <MenuItem value="cloud">Cloud Storage</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label="Source Details (e.g., endpoint, connection string)"
            fullWidth
            multiline
            rows={2}
            value={sourceDetails}
            onChange={(e) => setSourceDetails(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="target-type-select-label">Target Type</InputLabel>
            <Select
              labelId="target-type-select-label"
              id="target-type-select"
              value={targetType}
              label="Target Type"
              onChange={handleTargetTypeChange}
            >
              <MenuItem value="database">Database</MenuItem>
              <MenuItem value="api">API</MenuItem>
              <MenuItem value="file">File System</MenuItem>
              <MenuItem value="cloud">Cloud Storage</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label="Target Details (e.g., connection string, endpoint)"
            fullWidth
            multiline
            rows={2}
            value={targetDetails}
            onChange={(e) => setTargetDetails(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="frequency-select-label">Sync Frequency</InputLabel>
            <Select
              labelId="frequency-select-label"
              id="frequency-select"
              value={frequency}
              label="Sync Frequency"
              onChange={handleFrequencyChange}
            >
              <MenuItem value="realtime">Real-Time</MenuItem>
              <MenuItem value="hourly">Hourly</MenuItem>
              <MenuItem value="daily">Daily</MenuItem>
              <MenuItem value="weekly">Weekly</MenuItem>
              <MenuItem value="monthly">Monthly</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveConfig} disabled={!configName || !sourceDetails || !targetDetails}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default DataSync;
