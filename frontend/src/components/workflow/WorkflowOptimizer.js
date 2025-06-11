import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchWorkflowAnalysis, applyOptimization } from '../../store/workflowSlice';
import { Box, Typography, Grid, Paper, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, CircularProgress, Alert } from '@mui/material';
import { Refresh as RefreshIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function WorkflowOptimizer() {
  const dispatch = useDispatch();
  const { analysisData, optimizationStatus, loading, error } = useSelector((state) => state.workflow);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);

  useEffect(() => {
    dispatch(fetchWorkflowAnalysis());
  }, [dispatch]);

  const handleRefresh = () => {
    dispatch(fetchWorkflowAnalysis());
  };

  const handleSelectWorkflow = (workflow) => {
    setSelectedWorkflow(workflow);
  };

  const handleApplyOptimization = (optimizationId) => {
    if (selectedWorkflow) {
      dispatch(applyOptimization({ workflowId: selectedWorkflow.id, optimizationId }));
    }
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', padding: 2 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">Error loading workflow analysis: {error}</Alert>;

  const renderWorkflowList = () => {
    return (
      <Box>
        <Typography variant="h6">Workflows</Typography>
        <Paper elevation={1} sx={{ height: 400, overflow: 'auto', padding: 2, marginBottom: 2 }}>
          <List>
            {analysisData.workflows && analysisData.workflows.map((workflow) => (
              <ListItem 
                key={workflow.id} 
                onClick={() => handleSelectWorkflow(workflow)} 
                selected={selectedWorkflow && selectedWorkflow.id === workflow.id}
                sx={{ cursor: 'pointer' }}
              >
                <ListItemText 
                  primary={workflow.name} 
                  secondary={`Efficiency: ${workflow.efficiencyScore}% | Bottlenecks: ${workflow.bottlenecks.length}`} 
                />
                <ListItemSecondaryAction>
                  <Chip label={`${workflow.efficiencyScore}%`} color={workflow.efficiencyScore > 80 ? 'success' : workflow.efficiencyScore > 50 ? 'warning' : 'error'} size="small" />
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
      </Box>
    );
  };

  const renderAnalysisDetails = () => {
    if (!selectedWorkflow) {
      return <Typography>Select a workflow to view detailed analysis and optimization suggestions.</Typography>;
    }

    const chartData = selectedWorkflow.steps.map(step => ({
      name: step.name,
      duration: step.averageDuration,
      bottleneck: step.isBottleneck ? step.averageDuration : 0
    }));

    return (
      <Box>
        <Typography variant="h6">Analysis for {selectedWorkflow.name}</Typography>
        <Box sx={{ marginBottom: 2 }}>
          <Typography variant="body1"><strong>Efficiency Score:</strong> {selectedWorkflow.efficiencyScore}%</Typography>
          <Typography variant="body1"><strong>Total Steps:</strong> {selectedWorkflow.steps.length}</Typography>
          <Typography variant="body1"><strong>Bottlenecks Detected:</strong> {selectedWorkflow.bottlenecks.length}</Typography>
        </Box>
        <Typography variant="subtitle1">Workflow Duration Breakdown</Typography>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="duration" fill="#8884d8" name="Duration (min)" />
            <Bar dataKey="bottleneck" fill="#ff7300" name="Bottleneck (min)" />
          </BarChart>
        </ResponsiveContainer>
        <Typography variant="h6" sx={{ marginTop: 2 }}>Optimization Suggestions</Typography>
        {selectedWorkflow.suggestions.length === 0 ? (
          <Typography>No optimization suggestions available for this workflow.</Typography>
        ) : (
          <List>
            {selectedWorkflow.suggestions.map((suggestion) => (
              <ListItem key={suggestion.id}>
                <ListItemText 
                  primary={suggestion.title} 
                  secondary={`Impact: ${suggestion.impact} | Effort: ${suggestion.effort} | ${suggestion.description}`} 
                />
                <ListItemSecondaryAction>
                  <Button 
                    size="small" 
                    variant="contained" 
                    onClick={() => handleApplyOptimization(suggestion.id)}
                    disabled={optimizationStatus === 'applying'}
                    startIcon={<CheckCircleIcon />}
                  >
                    Apply
                  </Button>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}
        {optimizationStatus === 'success' && <Alert severity="success" sx={{ marginTop: 2 }}>Optimization applied successfully!</Alert>}
        {optimizationStatus === 'error' && <Alert severity="error" sx={{ marginTop: 2 }}>Failed to apply optimization.</Alert>}
      </Box>
    );
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Workflow Optimization Tools</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 2 }}>
        <Button variant="outlined" onClick={handleRefresh} startIcon={<RefreshIcon />}>Refresh Analysis</Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
            {renderWorkflowList()}
          </Paper>
        </Grid>
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ padding: 2, height: '100%' }}>
            {renderAnalysisDetails()}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default WorkflowOptimizer;
