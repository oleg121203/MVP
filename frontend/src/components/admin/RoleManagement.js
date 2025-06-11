import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchRoles, createRole, updateRole, deleteRole } from '../../store/roleSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';

function RoleManagement() {
  const dispatch = useDispatch();
  const { roles, loading, error } = useSelector((state) => state.roles);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingRole, setEditingRole] = useState(null);
  const [roleName, setRoleName] = useState('');
  const [roleDescription, setRoleDescription] = useState('');

  useEffect(() => {
    dispatch(fetchRoles());
  }, [dispatch]);

  const handleOpenDialog = (role = null) => {
    if (role) {
      setEditingRole(role);
      setRoleName(role.name);
      setRoleDescription(role.description);
    } else {
      setEditingRole(null);
      setRoleName('');
      setRoleDescription('');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveRole = () => {
    if (editingRole) {
      dispatch(updateRole({ id: editingRole.id, name: roleName, description: roleDescription }));
    } else {
      dispatch(createRole({ name: roleName, description: roleDescription }));
    }
    handleCloseDialog();
  };

  const handleDeleteRole = (id) => {
    dispatch(deleteRole(id));
  };

  if (loading) return <Typography>Loading roles...</Typography>;
  if (error) return <Typography color="error">Error loading roles: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Advanced Role Management</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Role
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Roles List</Typography>
            {roles.length === 0 ? (
              <Typography>No roles available. Create a new role to get started.</Typography>
            ) : (
              <List>
                {roles.map((role) => (
                  <ListItem key={role.id}>
                    <ListItemText primary={role.name} secondary={role.description} />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(role)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteRole(role.id)} size="small">
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

      {/* Dialog for Adding/Editing Roles */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingRole ? 'Edit Role' : 'Add New Role'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Role Name"
            fullWidth
            value={roleName}
            onChange={(e) => setRoleName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={roleDescription}
            onChange={(e) => setRoleDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveRole} disabled={!roleName}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default RoleManagement;
