import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchRBACRules, createRBACRule, updateRBACRule, deleteRBACRule } from '../../store/rbacSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';

function RoleBasedAccessControl() {
  const dispatch = useDispatch();
  const { rbacRules, loading, error } = useSelector((state) => state.rbac);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingRule, setEditingRule] = useState(null);
  const [ruleName, setRuleName] = useState('');
  const [role, setRole] = useState('user');
  const [resource, setResource] = useState('');
  const [permission, setPermission] = useState('read');

  useEffect(() => {
    dispatch(fetchRBACRules());
  }, [dispatch]);

  const handleOpenDialog = (rule = null) => {
    if (rule) {
      setEditingRule(rule);
      setRuleName(rule.name);
      setRole(rule.role);
      setResource(rule.resource);
      setPermission(rule.permission);
    } else {
      setEditingRule(null);
      setRuleName('');
      setRole('user');
      setResource('');
      setPermission('read');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveRule = () => {
    if (editingRule) {
      dispatch(updateRBACRule({ id: editingRule.id, name: ruleName, role, resource, permission }));
    } else {
      dispatch(createRBACRule({ name: ruleName, role, resource, permission }));
    }
    handleCloseDialog();
  };

  const handleDeleteRule = (id) => {
    dispatch(deleteRBACRule(id));
  };

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };

  const handlePermissionChange = (event) => {
    setPermission(event.target.value);
  };

  if (loading) return <Typography>Loading RBAC rules...</Typography>;
  if (error) return <Typography color="error">Error loading RBAC rules: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Role-Based Access Control</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Rule
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">RBAC Rules List</Typography>
            {rbacRules.length === 0 ? (
              <Typography>No RBAC rules available. Create a new rule to get started.</Typography>
            ) : (
              <List>
                {rbacRules.map((rule) => (
                  <ListItem key={rule.id}>
                    <ListItemText 
                      primary={rule.name} 
                      secondary={`Role: ${rule.role}, Resource: ${rule.resource}, Permission: ${rule.permission}`} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(rule)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteRule(rule.id)} size="small">
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

      {/* Dialog for Adding/Editing RBAC Rules */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingRule ? 'Edit RBAC Rule' : 'Add New RBAC Rule'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Rule Name"
            fullWidth
            value={ruleName}
            onChange={(e) => setRuleName(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="role-select-label">Role</InputLabel>
            <Select
              labelId="role-select-label"
              id="role-select"
              value={role}
              label="Role"
              onChange={handleRoleChange}
            >
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="manager">Manager</MenuItem>
              <MenuItem value="user">User</MenuItem>
              <MenuItem value="guest">Guest</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label="Resource"
            fullWidth
            value={resource}
            onChange={(e) => setResource(e.target.value)}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel id="permission-select-label">Permission</InputLabel>
            <Select
              labelId="permission-select-label"
              id="permission-select"
              value={permission}
              label="Permission"
              onChange={handlePermissionChange}
            >
              <MenuItem value="read">Read</MenuItem>
              <MenuItem value="write">Write</MenuItem>
              <MenuItem value="delete">Delete</MenuItem>
              <MenuItem value="full">Full Control</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveRule} disabled={!ruleName || !resource}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default RoleBasedAccessControl;
