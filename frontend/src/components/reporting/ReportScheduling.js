import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchSchedules, createSchedule, updateSchedule, deleteSchedule } from '../../store/reportingSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';

function ReportScheduling() {
  const dispatch = useDispatch();
  const { schedules, loading, error } = useSelector((state) => state.reporting);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingSchedule, setEditingSchedule] = useState(null);
  const [scheduleName, setScheduleName] = useState('');
  const [reportTemplate, setReportTemplate] = useState('');
  const [frequency, setFrequency] = useState('daily');
  const [time, setTime] = useState('09:00');
  const [destination, setDestination] = useState('email');
  const [format, setFormat] = useState('pdf');
  const [destinationDetails, setDestinationDetails] = useState('');

  useEffect(() => {
    dispatch(fetchSchedules());
  }, [dispatch]);

  const handleOpenDialog = (schedule = null) => {
    if (schedule) {
      setEditingSchedule(schedule);
      setScheduleName(schedule.name);
      setReportTemplate(schedule.template);
      setFrequency(schedule.frequency);
      setTime(schedule.time);
      setDestination(schedule.destination);
      setFormat(schedule.format || 'pdf');
      setDestinationDetails(schedule.destinationDetails || '');
    } else {
      setEditingSchedule(null);
      setScheduleName('');
      setReportTemplate('');
      setFrequency('daily');
      setTime('09:00');
      setDestination('email');
      setFormat('pdf');
      setDestinationDetails('');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveSchedule = () => {
    if (editingSchedule) {
      dispatch(updateSchedule({ id: editingSchedule.id, name: scheduleName, template: reportTemplate, frequency, time, destination, format, destinationDetails }));
    } else {
      dispatch(createSchedule({ name: scheduleName, template: reportTemplate, frequency, time, destination, format, destinationDetails }));
    }
    handleCloseDialog();
  };

  const handleDeleteSchedule = (id) => {
    dispatch(deleteSchedule(id));
  };

  const handleFrequencyChange = (event) => {
    setFrequency(event.target.value);
  };

  const handleDestinationChange = (event) => {
    setDestination(event.target.value);
    setDestinationDetails('');
  };

  const handleFormatChange = (event) => {
    setFormat(event.target.value);
  };

  if (loading) return <Typography>Loading report schedules...</Typography>;
  if (error) return <Typography color="error">Error loading report schedules: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Automated Report Scheduling</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Schedule
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Report Schedules List</Typography>
            {schedules.length === 0 ? (
              <Typography>No report schedules available. Create a new schedule to get started.</Typography>
            ) : (
              <List>
                {schedules.map((schedule) => (
                  <ListItem key={schedule.id}>
                    <ListItemText 
                      primary={schedule.name} 
                      secondary={`Template: ${schedule.template}, Frequency: ${schedule.frequency}, Time: ${schedule.time}, Destination: ${schedule.destination}, Format: ${schedule.format || 'PDF'}`} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(schedule)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteSchedule(schedule.id)} size="small">
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

      {/* Dialog for Adding/Editing Report Schedules */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingSchedule ? 'Edit Report Schedule' : 'Add New Report Schedule'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Schedule Name"
            fullWidth
            value={scheduleName}
            onChange={(e) => setScheduleName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Report Template"
            fullWidth
            value={reportTemplate}
            onChange={(e) => setReportTemplate(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="frequency-select-label">Frequency</InputLabel>
            <Select
              labelId="frequency-select-label"
              id="frequency-select"
              value={frequency}
              label="Frequency"
              onChange={handleFrequencyChange}
            >
              <MenuItem value="daily">Daily</MenuItem>
              <MenuItem value="weekly">Weekly</MenuItem>
              <MenuItem value="monthly">Monthly</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label="Time"
            type="time"
            fullWidth
            value={time}
            onChange={(e) => setTime(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="destination-select-label">Destination</InputLabel>
            <Select
              labelId="destination-select-label"
              id="destination-select"
              value={destination}
              label="Destination"
              onChange={handleDestinationChange}
            >
              <MenuItem value="email">Email</MenuItem>
              <MenuItem value="ftp">FTP</MenuItem>
              <MenuItem value="cloud">Cloud Storage</MenuItem>
              <MenuItem value="api">API Endpoint</MenuItem>
              <MenuItem value="sftp">SFTP</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel id="format-select-label">Report Format</InputLabel>
            <Select
              labelId="format-select-label"
              id="format-select"
              value={format}
              label="Report Format"
              onChange={handleFormatChange}
            >
              <MenuItem value="pdf">PDF</MenuItem>
              <MenuItem value="csv">CSV</MenuItem>
              <MenuItem value="excel">Excel</MenuItem>
            </Select>
          </FormControl>
          {destination === 'email' && (
            <TextField
              margin="dense"
              label="Email Addresses (comma separated)"
              fullWidth
              value={destinationDetails}
              onChange={(e) => setDestinationDetails(e.target.value)}
            />
          )}
          {destination === 'ftp' && (
            <TextField
              margin="dense"
              label="FTP Path (e.g., ftp://server.com/path)"
              fullWidth
              value={destinationDetails}
              onChange={(e) => setDestinationDetails(e.target.value)}
            />
          )}
          {destination === 'cloud' && (
            <TextField
              margin="dense"
              label="Cloud Storage Path"
              fullWidth
              value={destinationDetails}
              onChange={(e) => setDestinationDetails(e.target.value)}
            />
          )}
          {destination === 'api' && (
            <TextField
              margin="dense"
              label="API Endpoint URL"
              fullWidth
              value={destinationDetails}
              onChange={(e) => setDestinationDetails(e.target.value)}
            />
          )}
          {destination === 'sftp' && (
            <TextField
              margin="dense"
              label="SFTP Path (e.g., sftp://server.com/path)"
              fullWidth
              value={destinationDetails}
              onChange={(e) => setDestinationDetails(e.target.value)}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveSchedule} disabled={!scheduleName || !reportTemplate}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ReportScheduling;
