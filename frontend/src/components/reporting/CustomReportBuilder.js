import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchReportTemplates, createReportTemplate, updateReportTemplate, deleteReportTemplate } from '../../store/reportingSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';

function CustomReportBuilder() {
  const dispatch = useDispatch();
  const { templates, loading, error } = useSelector((state) => state.reporting);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState(null);
  const [templateName, setTemplateName] = useState('');
  const [templateDescription, setTemplateDescription] = useState('');
  const [templateConfig, setTemplateConfig] = useState('');

  useEffect(() => {
    dispatch(fetchReportTemplates());
  }, [dispatch]);

  const handleOpenDialog = (template = null) => {
    if (template) {
      setEditingTemplate(template);
      setTemplateName(template.name);
      setTemplateDescription(template.description);
      setTemplateConfig(template.config);
    } else {
      setEditingTemplate(null);
      setTemplateName('');
      setTemplateDescription('');
      setTemplateConfig('');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveTemplate = () => {
    if (editingTemplate) {
      dispatch(updateReportTemplate({ id: editingTemplate.id, name: templateName, description: templateDescription, config: templateConfig }));
    } else {
      dispatch(createReportTemplate({ name: templateName, description: templateDescription, config: templateConfig }));
    }
    handleCloseDialog();
  };

  const handleDeleteTemplate = (id) => {
    dispatch(deleteReportTemplate(id));
  };

  if (loading) return <Typography>Loading report templates...</Typography>;
  if (error) return <Typography color="error">Error loading report templates: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Custom Report Builder</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Template
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Report Templates List</Typography>
            {templates.length === 0 ? (
              <Typography>No report templates available. Create a new template to get started.</Typography>
            ) : (
              <List>
                {templates.map((template) => (
                  <ListItem key={template.id}>
                    <ListItemText 
                      primary={template.name} 
                      secondary={template.description} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(template)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteTemplate(template.id)} size="small">
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

      {/* Dialog for Adding/Editing Report Templates */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingTemplate ? 'Edit Report Template' : 'Add New Report Template'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Template Name"
            fullWidth
            value={templateName}
            onChange={(e) => setTemplateName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={templateDescription}
            onChange={(e) => setTemplateDescription(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Configuration (JSON format)"
            fullWidth
            multiline
            rows={5}
            value={templateConfig}
            onChange={(e) => setTemplateConfig(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveTemplate} disabled={!templateName || !templateConfig}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default CustomReportBuilder;
