import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchLeads, createLead, updateLead, deleteLead } from '../../store/leadSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';

function LeadGeneration() {
  const dispatch = useDispatch();
  const { leads, loading, error } = useSelector((state) => state.leads);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingLead, setEditingLead] = useState(null);
  const [leadName, setLeadName] = useState('');
  const [leadEmail, setLeadEmail] = useState('');
  const [leadPhone, setLeadPhone] = useState('');
  const [leadStatus, setLeadStatus] = useState('new');
  const [leadSource, setLeadSource] = useState('website');

  useEffect(() => {
    dispatch(fetchLeads());
  }, [dispatch]);

  const handleOpenDialog = (lead = null) => {
    if (lead) {
      setEditingLead(lead);
      setLeadName(lead.name);
      setLeadEmail(lead.email);
      setLeadPhone(lead.phone);
      setLeadStatus(lead.status);
      setLeadSource(lead.source);
    } else {
      setEditingLead(null);
      setLeadName('');
      setLeadEmail('');
      setLeadPhone('');
      setLeadStatus('new');
      setLeadSource('website');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveLead = () => {
    if (editingLead) {
      dispatch(updateLead({ id: editingLead.id, name: leadName, email: leadEmail, phone: leadPhone, status: leadStatus, source: leadSource }));
    } else {
      dispatch(createLead({ name: leadName, email: leadEmail, phone: leadPhone, status: leadStatus, source: leadSource }));
    }
    handleCloseDialog();
  };

  const handleDeleteLead = (id) => {
    dispatch(deleteLead(id));
  };

  const handleStatusChange = (event) => {
    setLeadStatus(event.target.value);
  };

  const handleSourceChange = (event) => {
    setLeadSource(event.target.value);
  };

  if (loading) return <Typography>Loading leads...</Typography>;
  if (error) return <Typography color="error">Error loading leads: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Lead Generation Tools</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Lead
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Leads List</Typography>
            {leads.length === 0 ? (
              <Typography>No leads available. Create a new lead to get started.</Typography>
            ) : (
              <List>
                {leads.map((lead) => (
                  <ListItem key={lead.id}>
                    <ListItemText 
                      primary={lead.name} 
                      secondary={`Email: ${lead.email}, Phone: ${lead.phone}, Status: ${lead.status}, Source: ${lead.source}`} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(lead)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteLead(lead.id)} size="small">
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

      {/* Dialog for Adding/Editing Leads */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingLead ? 'Edit Lead' : 'Add New Lead'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Name"
            fullWidth
            value={leadName}
            onChange={(e) => setLeadName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Email"
            fullWidth
            value={leadEmail}
            onChange={(e) => setLeadEmail(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Phone"
            fullWidth
            value={leadPhone}
            onChange={(e) => setLeadPhone(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="status-select-label">Status</InputLabel>
            <Select
              labelId="status-select-label"
              id="status-select"
              value={leadStatus}
              label="Status"
              onChange={handleStatusChange}
            >
              <MenuItem value="new">New</MenuItem>
              <MenuItem value="contacted">Contacted</MenuItem>
              <MenuItem value="qualified">Qualified</MenuItem>
              <MenuItem value="lost">Lost</MenuItem>
              <MenuItem value="won">Won</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel id="source-select-label">Source</InputLabel>
            <Select
              labelId="source-select-label"
              id="source-select"
              value={leadSource}
              label="Source"
              onChange={handleSourceChange}
            >
              <MenuItem value="website">Website</MenuItem>
              <MenuItem value="referral">Referral</MenuItem>
              <MenuItem value="advertisement">Advertisement</MenuItem>
              <MenuItem value="event">Event</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveLead} disabled={!leadName || !leadEmail}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default LeadGeneration;
