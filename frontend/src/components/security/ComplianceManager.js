import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchComplianceStatus, generateComplianceReport } from '../../store/securitySlice';
import { Box, Typography, Grid, Paper, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, TextField, MenuItem, Select, FormControl, InputLabel, Alert } from '@mui/material';
import { Assessment as AssessmentIcon, Description as DescriptionIcon, Refresh as RefreshIcon } from '@mui/icons-material';

function ComplianceManager() {
  const dispatch = useDispatch();
  const { complianceStatus, loading, error } = useSelector((state) => state.security);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedStandard, setSelectedStandard] = useState('gdpr');
  const [reportFormat, setReportFormat] = useState('pdf');

  useEffect(() => {
    dispatch(fetchComplianceStatus());
  }, [dispatch]);

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleStandardChange = (event) => {
    setSelectedStandard(event.target.value);
  };

  const handleFormatChange = (event) => {
    setReportFormat(event.target.value);
  };

  const handleGenerateReport = () => {
    dispatch(generateComplianceReport({ standard: selectedStandard, format: reportFormat }));
    handleCloseDialog();
  };

  const handleRefresh = () => {
    dispatch(fetchComplianceStatus());
  };

  if (loading) return <Typography>Loading compliance status...</Typography>;
  if (error) return <Alert severity="error">Error loading compliance status: {error}</Alert>;

  const complianceStandards = [
    { id: 'gdpr', name: 'GDPR', description: 'General Data Protection Regulation (EU)' },
    { id: 'hipaa', name: 'HIPAA', description: 'Health Insurance Portability and Accountability Act (US)' },
    { id: 'ccpa', name: 'CCPA', description: 'California Consumer Privacy Act (US)' },
    { id: 'iso27001', name: 'ISO 27001', description: 'Information Security Management System' },
    { id: 'soc2', name: 'SOC 2', description: 'Service Organization Control 2' }
  ];

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Compliance Manager</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
        <Button variant="contained" onClick={handleOpenDialog} startIcon={<DescriptionIcon />}>Generate Report</Button>
        <Button variant="outlined" onClick={handleRefresh} startIcon={<RefreshIcon />}>Refresh</Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Compliance Status Overview</Typography>
            <List>
              {complianceStandards.map((standard) => {
                const status = complianceStatus.find(s => s.standard === standard.id) || { complianceLevel: 0, lastAudit: 'Never', issues: [] };
                return (
                  <ListItem key={standard.id} divider>
                    <ListItemText 
                      primary={`${standard.name} - ${standard.description}`} 
                      secondary={`Compliance Level: ${status.complianceLevel}% | Last Audit: ${status.lastAudit} | Issues: ${status.issues.length}`} 
                    />
                    <ListItemSecondaryAction>
                      <Button size="small" variant="outlined" startIcon={<AssessmentIcon />}>View Details</Button>
                    </ListItemSecondaryAction>
                  </ListItem>
                );
              })}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog for Generating Compliance Report */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Generate Compliance Report</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="dense">
            <InputLabel id="standard-select-label">Compliance Standard</InputLabel>
            <Select
              labelId="standard-select-label"
              id="standard-select"
              value={selectedStandard}
              label="Compliance Standard"
              onChange={handleStandardChange}
            >
              {complianceStandards.map(standard => (
                <MenuItem key={standard.id} value={standard.id}>{standard.name}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel id="format-select-label">Report Format</InputLabel>
            <Select
              labelId="format-select-label"
              id="format-select"
              value={reportFormat}
              label="Report Format"
              onChange={handleFormatChange}
            >
              <MenuItem value="pdf">PDF</MenuItem>
              <MenuItem value="docx">DOCX</MenuItem>
              <MenuItem value="csv">CSV</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleGenerateReport}>Generate</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ComplianceManager;
