import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchWorkflows, createWorkflow, updateWorkflow, deleteWorkflow, runWorkflow } from '../../store/workflowSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon, PlayArrow as PlayArrowIcon } from '@mui/icons-material';

function WorkflowAutomation() {
  const dispatch = useDispatch();
  const { workflows, loading, error } = useSelector((state) => state.workflows);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingWorkflow, setEditingWorkflow] = useState(null);
  const [workflowName, setWorkflowName] = useState('');
  const [workflowDescription, setWorkflowDescription] = useState('');
  const [workflowSteps, setWorkflowSteps] = useState('');

  useEffect(() => {
    dispatch(fetchWorkflows());
  }, [dispatch]);

  const handleOpenDialog = (workflow = null) => {
    if (workflow) {
      setEditingWorkflow(workflow);
      setWorkflowName(workflow.name);
      setWorkflowDescription(workflow.description);
      setWorkflowSteps(workflow.steps);
    } else {
      setEditingWorkflow(null);
      setWorkflowName('');
      setWorkflowDescription('');
      setWorkflowSteps('');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveWorkflow = () => {
    if (editingWorkflow) {
      dispatch(updateWorkflow({ id: editingWorkflow.id, name: workflowName, description: workflowDescription, steps: workflowSteps }));
    } else {
      dispatch(createWorkflow({ name: workflowName, description: workflowDescription, steps: workflowSteps }));
    }
    handleCloseDialog();
  };

  const handleDeleteWorkflow = (id) => {
    dispatch(deleteWorkflow(id));
  };

  const handleRunWorkflow = (id) => {
    dispatch(runWorkflow(id));
  };

  if (loading) return <Typography>Loading workflows...</Typography>;
  if (error) return <Typography color="error">Error loading workflows: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Custom Workflow Automation</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Workflow
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Workflows List</Typography>
            {workflows.length === 0 ? (
              <Typography>No workflows available. Create a new workflow to get started.</Typography>
            ) : (
              <List>
                {workflows.map((workflow) => (
                  <ListItem key={workflow.id}>
                    <ListItemText 
                      primary={workflow.name} 
                      secondary={workflow.description} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="run" onClick={() => handleRunWorkflow(workflow.id)} size="small" sx={{ marginRight: 1 }}>
                        <PlayArrowIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(workflow)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteWorkflow(workflow.id)} size="small">
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

      {/* Dialog for Adding/Editing Workflows */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingWorkflow ? 'Edit Workflow' : 'Add New Workflow'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Workflow Name"
            fullWidth
            value={workflowName}
            onChange={(e) => setWorkflowName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={workflowDescription}
            onChange={(e) => setWorkflowDescription(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Steps (JSON format)"
            fullWidth
            multiline
            rows={5}
            value={workflowSteps}
            onChange={(e) => setWorkflowSteps(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveWorkflow} disabled={!workflowName || !workflowSteps}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default WorkflowAutomation;
