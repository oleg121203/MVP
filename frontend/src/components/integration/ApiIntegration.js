import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchApiIntegrations, createApiIntegration, updateApiIntegration, deleteApiIntegration } from '../../store/apiIntegrationSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';

function ApiIntegration() {
  const dispatch = useDispatch();
  const { integrations, loading, error } = useSelector((state) => state.apiIntegrations);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingIntegration, setEditingIntegration] = useState(null);
  const [serviceName, setServiceName] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [apiEndpoint, setApiEndpoint] = useState('');
  const [serviceType, setServiceType] = useState('generic');

  useEffect(() => {
    dispatch(fetchApiIntegrations());
  }, [dispatch]);

  const handleOpenDialog = (integration = null) => {
    if (integration) {
      setEditingIntegration(integration);
      setServiceName(integration.name);
      setApiKey(integration.apiKey);
      setApiEndpoint(integration.endpoint);
      setServiceType(integration.type);
    } else {
      setEditingIntegration(null);
      setServiceName('');
      setApiKey('');
      setApiEndpoint('');
      setServiceType('generic');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveIntegration = () => {
    if (editingIntegration) {
      dispatch(updateApiIntegration({ id: editingIntegration.id, name: serviceName, apiKey, endpoint: apiEndpoint, type: serviceType }));
    } else {
      dispatch(createApiIntegration({ name: serviceName, apiKey, endpoint: apiEndpoint, type: serviceType }));
    }
    handleCloseDialog();
  };

  const handleDeleteIntegration = (id) => {
    dispatch(deleteApiIntegration(id));
  };

  const handleServiceTypeChange = (event) => {
    setServiceType(event.target.value);
  };

  if (loading) return <Typography>Loading API integrations...</Typography>;
  if (error) return <Typography color="error">Error loading API integrations: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>API Integration for Third-Party Services</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Integration
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Integrations List</Typography>
            {integrations.length === 0 ? (
              <Typography>No integrations available. Create a new integration to get started.</Typography>
            ) : (
              <List>
                {integrations.map((integration) => (
                  <ListItem key={integration.id}>
                    <ListItemText 
                      primary={integration.name} 
                      secondary={`Type: ${integration.type}, Endpoint: ${integration.endpoint}`} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(integration)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteIntegration(integration.id)} size="small">
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

      {/* Dialog for Adding/Editing Integrations */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingIntegration ? 'Edit Integration' : 'Add New Integration'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Service Name"
            fullWidth
            value={serviceName}
            onChange={(e) => setServiceName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="API Key"
            fullWidth
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
          <TextField
            margin="dense"
            label="API Endpoint"
            fullWidth
            value={apiEndpoint}
            onChange={(e) => setApiEndpoint(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="service-type-select-label">Service Type</InputLabel>
            <Select
              labelId="service-type-select-label"
              id="service-type-select"
              value={serviceType}
              label="Service Type"
              onChange={handleServiceTypeChange}
            >
              <MenuItem value="generic">Generic API</MenuItem>
              <MenuItem value="salesforce">Salesforce</MenuItem>
              <MenuItem value="hubspot">HubSpot</MenuItem>
              <MenuItem value="zapier">Zapier</MenuItem>
              <MenuItem value="google">Google Services</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveIntegration} disabled={!serviceName || !apiEndpoint}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ApiIntegration;
