import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPlatformConnections, connectPlatform, disconnectPlatform, syncPlatformData } from '../../store/integrationSlice';
import { Box, Typography, Grid, Paper, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, TextField, MenuItem, Select, FormControl, InputLabel, Alert } from '@mui/material';
import { Link as LinkIcon, Unlink as UnlinkIcon, Sync as SyncIcon, Refresh as RefreshIcon } from '@mui/icons-material';

function PlatformIntegration() {
  const dispatch = useDispatch();
  const { connections, loading, error, syncStatus } = useSelector((state) => state.integration);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState('');
  const [authToken, setAuthToken] = useState('');
  const [syncSettings, setSyncSettings] = useState({ notifications: true, dataSync: true, frequency: 'realtime' });

  useEffect(() => {
    dispatch(fetchPlatformConnections());
  }, [dispatch]);

  const handleOpenDialog = (platform = '') => {
    setSelectedPlatform(platform);
    setAuthToken('');
    setSyncSettings({ notifications: true, dataSync: true, frequency: 'realtime' });
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleConnectPlatform = () => {
    if (selectedPlatform && authToken) {
      dispatch(connectPlatform({ platform: selectedPlatform, token: authToken, settings: syncSettings }));
      handleCloseDialog();
    }
  };

  const handleDisconnectPlatform = (platformId) => {
    dispatch(disconnectPlatform(platformId));
  };

  const handleSyncPlatform = (platformId) => {
    dispatch(syncPlatformData(platformId));
  };

  const handleRefresh = () => {
    dispatch(fetchPlatformConnections());
  };

  const handleFrequencyChange = (event) => {
    setSyncSettings({ ...syncSettings, frequency: event.target.value });
  };

  if (loading) return <Typography>Loading platform connections...</Typography>;
  if (error) return <Alert severity="error">Error loading platform connections: {error}</Alert>;

  const availablePlatforms = [
    { id: 'slack', name: 'Slack', description: 'Team communication' },
    { id: 'msteams', name: 'Microsoft Teams', description: 'Unified collaboration' },
    { id: 'google', name: 'Google Workspace', description: 'Productivity tools' },
    { id: 'trello', name: 'Trello', description: 'Project management' },
    { id: 'asana', name: 'Asana', description: 'Work management' }
  ];

  const connectedPlatforms = connections || [];
  const unconnectedPlatforms = availablePlatforms.filter(p => !connectedPlatforms.some(cp => cp.platformId === p.id));

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>External Platform Integration</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 2 }}>
        <Button variant="outlined" onClick={handleRefresh} startIcon={<RefreshIcon />}>Refresh</Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
            <Typography variant="h6">Connected Platforms</Typography>
            {connectedPlatforms.length === 0 ? (
              <Typography>No platforms connected yet.</Typography>
            ) : (
              <List>
                {connectedPlatforms.map((conn) => (
                  <ListItem key={conn.platformId}>
                    <ListItemText 
                      primary={conn.platformName} 
                      secondary={`Connected on: ${new Date(conn.connectionDate).toLocaleDateString()}`} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton size="small" onClick={() => handleSyncPlatform(conn.platformId)} disabled={syncStatus === 'syncing'} sx={{ mr: 1 }}>
                        <SyncIcon />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleDisconnectPlatform(conn.platformId)} color="error">
                        <UnlinkIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
            <Typography variant="h6">Available Platforms</Typography>
            <List>
              {unconnectedPlatforms.map((platform) => (
                <ListItem key={platform.id}>
                  <ListItemText 
                    primary={platform.name} 
                    secondary={platform.description} 
                  />
                  <ListItemSecondaryAction>
                    <Button size="small" variant="contained" onClick={() => handleOpenDialog(platform.id)} startIcon={<LinkIcon />}>Connect</Button>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog for Connecting a Platform */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Connect {selectedPlatform ? availablePlatforms.find(p => p.id === selectedPlatform)?.name : 'Platform'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Authorization Token"
            fullWidth
            value={authToken}
            onChange={(e) => setAuthToken(e.target.value)}
            placeholder="Enter API token or access key"
            type="password"
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="frequency-select-label">Sync Frequency</InputLabel>
            <Select
              labelId="frequency-select-label"
              id="frequency-select"
              value={syncSettings.frequency}
              label="Sync Frequency"
              onChange={handleFrequencyChange}
            >
              <MenuItem value="realtime">Real-time</MenuItem>
              <MenuItem value="hourly">Hourly</MenuItem>
              <MenuItem value="daily">Daily</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleConnectPlatform} disabled={!authToken}>Connect</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default PlatformIntegration;
