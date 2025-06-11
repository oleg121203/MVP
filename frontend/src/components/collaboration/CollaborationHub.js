import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchCollaborationData, sendMessage, uploadDocument, assignTask } from '../../store/collaborationSlice';
import { Box, Typography, Grid, Paper, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, Divider, Chip } from '@mui/material';
import { Send as SendIcon, Upload as UploadIcon, Assignment as AssignmentIcon, Refresh as RefreshIcon } from '@mui/icons-material';

function CollaborationHub() {
  const dispatch = useDispatch();
  const { collaborationData, loading, error } = useSelector((state) => state.collaboration);
  const [activeTab, setActiveTab] = useState('chat');
  const [messageText, setMessageText] = useState('');
  const [documentFile, setDocumentFile] = useState(null);
  const [taskDescription, setTaskDescription] = useState('');
  const [taskAssignee, setTaskAssignee] = useState('');
  const [openTaskDialog, setOpenTaskDialog] = useState(false);

  useEffect(() => {
    dispatch(fetchCollaborationData());
  }, [dispatch]);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  const handleSendMessage = () => {
    if (messageText.trim()) {
      dispatch(sendMessage({ content: messageText, timestamp: new Date().toISOString(), user: 'Current User' }));
      setMessageText('');
    }
  };

  const handleUploadDocument = () => {
    if (documentFile) {
      dispatch(uploadDocument({ file: documentFile, name: documentFile.name, timestamp: new Date().toISOString(), user: 'Current User' }));
      setDocumentFile(null);
    }
  };

  const handleOpenTaskDialog = () => {
    setOpenTaskDialog(true);
  };

  const handleCloseTaskDialog = () => {
    setOpenTaskDialog(false);
    setTaskDescription('');
    setTaskAssignee('');
  };

  const handleAssignTask = () => {
    if (taskDescription.trim() && taskAssignee.trim()) {
      dispatch(assignTask({ description: taskDescription, assignee: taskAssignee, status: 'Open', timestamp: new Date().toISOString() }));
      handleCloseTaskDialog();
    }
  };

  const handleRefresh = () => {
    dispatch(fetchCollaborationData());
  };

  if (loading) return <Typography>Loading collaboration data...</Typography>;
  if (error) return <Typography color="error">Error loading collaboration data: {error}</Typography>;

  const renderChatContent = () => {
    return (
      <Box>
        <Typography variant="h6">Team Chat</Typography>
        <Paper elevation={1} sx={{ height: 300, overflow: 'auto', padding: 2, marginBottom: 2 }}>
          <List>
            {collaborationData.chatMessages && collaborationData.chatMessages.map((msg, index) => (
              <ListItem key={index} alignItems="flex-start">
                <ListItemText 
                  primary={msg.content} 
                  secondary={`${msg.user} - ${new Date(msg.timestamp).toLocaleTimeString()}`} 
                />
              </ListItem>
            ))}
          </List>
        </Paper>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField 
            fullWidth 
            value={messageText} 
            onChange={(e) => setMessageText(e.target.value)} 
            placeholder="Type a message..." 
            variant="outlined" 
            size="small"
          />
          <Button variant="contained" onClick={handleSendMessage} disabled={!messageText.trim()} endIcon={<SendIcon />}>
            Send
          </Button>
        </Box>
      </Box>
    );
  };

  const renderDocumentsContent = () => {
    return (
      <Box>
        <Typography variant="h6">Shared Documents</Typography>
        <Paper elevation={1} sx={{ height: 300, overflow: 'auto', padding: 2, marginBottom: 2 }}>
          <List>
            {collaborationData.documents && collaborationData.documents.map((doc, index) => (
              <ListItem key={index}>
                <ListItemText 
                  primary={doc.name} 
                  secondary={`${doc.user} - ${new Date(doc.timestamp).toLocaleDateString()}`} 
                />
                <ListItemSecondaryAction>
                  <IconButton size="small" onClick={() => alert(`Downloading ${doc.name}`)}>
                    <UploadIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <input
            type="file"
            accept=".pdf,.docx,.xlsx"
            onChange={(e) => setDocumentFile(e.target.files[0])}
            style={{ display: 'none' }}
            id="upload-document"
          />
          <label htmlFor="upload-document">
            <Button variant="contained" component="span" startIcon={<UploadIcon />}>
              Choose File
            </Button>
          </label>
          <Button variant="contained" onClick={handleUploadDocument} disabled={!documentFile} endIcon={<UploadIcon />}>
            Upload
          </Button>
          {documentFile && <Typography variant="body2">Selected: {documentFile.name}</Typography>}
        </Box>
      </Box>
    );
  };

  const renderTasksContent = () => {
    return (
      <Box>
        <Typography variant="h6">Task Management</Typography>
        <Paper elevation={1} sx={{ height: 300, overflow: 'auto', padding: 2, marginBottom: 2 }}>
          <List>
            {collaborationData.tasks && collaborationData.tasks.map((task, index) => (
              <ListItem key={index}>
                <ListItemText 
                  primary={task.description} 
                  secondary={`Assigned to: ${task.assignee} | Status: ${task.status} | Created: ${new Date(task.timestamp).toLocaleDateString()}`} 
                />
                <ListItemSecondaryAction>
                  <Chip label={task.status} color={task.status === 'Open' ? 'default' : task.status === 'In Progress' ? 'primary' : 'secondary'} size="small" />
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
        <Button variant="contained" onClick={handleOpenTaskDialog} startIcon={<AssignmentIcon />}>
          Assign New Task
        </Button>
      </Box>
    );
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Team Collaboration Hub</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 2 }}>
        <Box>
          <Button variant="contained" onClick={() => handleTabChange('chat')} color={activeTab === 'chat' ? 'primary' : 'default'} sx={{ marginRight: 1 }}>Chat</Button>
          <Button variant="contained" onClick={() => handleTabChange('documents')} color={activeTab === 'documents' ? 'primary' : 'default'} sx={{ marginRight: 1 }}>Documents</Button>
          <Button variant="contained" onClick={() => handleTabChange('tasks')} color={activeTab === 'tasks' ? 'primary' : 'default'}>Tasks</Button>
        </Box>
        <Button variant="outlined" onClick={handleRefresh} startIcon={<RefreshIcon />}>Refresh</Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            {activeTab === 'chat' && renderChatContent()}
            {activeTab === 'documents' && renderDocumentsContent()}
            {activeTab === 'tasks' && renderTasksContent()}
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog for Assigning New Tasks */}
      <Dialog open={openTaskDialog} onClose={handleCloseTaskDialog}>
        <DialogTitle>Assign New Task</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Task Description"
            fullWidth
            value={taskDescription}
            onChange={(e) => setTaskDescription(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Assignee"
            fullWidth
            value={taskAssignee}
            onChange={(e) => setTaskAssignee(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseTaskDialog}>Cancel</Button>
          <Button onClick={handleAssignTask} disabled={!taskDescription || !taskAssignee}>Assign</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default CollaborationHub;
