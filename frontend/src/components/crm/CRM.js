import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchCustomers, createCustomer, updateCustomer, deleteCustomer } from '../../store/crmSlice';
import { Grid, Paper, Typography, Box, Button, TextField, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';

function CRM() {
  const dispatch = useDispatch();
  const { customers, loading, error } = useSelector((state) => state.crm);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState(null);
  const [customerName, setCustomerName] = useState('');
  const [customerEmail, setCustomerEmail] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [customerAddress, setCustomerAddress] = useState('');

  useEffect(() => {
    dispatch(fetchCustomers());
  }, [dispatch]);

  const handleOpenDialog = (customer = null) => {
    if (customer) {
      setEditingCustomer(customer);
      setCustomerName(customer.name);
      setCustomerEmail(customer.email);
      setCustomerPhone(customer.phone);
      setCustomerAddress(customer.address);
    } else {
      setEditingCustomer(null);
      setCustomerName('');
      setCustomerEmail('');
      setCustomerPhone('');
      setCustomerAddress('');
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleSaveCustomer = () => {
    if (editingCustomer) {
      dispatch(updateCustomer({ id: editingCustomer.id, name: customerName, email: customerEmail, phone: customerPhone, address: customerAddress }));
    } else {
      dispatch(createCustomer({ name: customerName, email: customerEmail, phone: customerPhone, address: customerAddress }));
    }
    handleCloseDialog();
  };

  const handleDeleteCustomer = (id) => {
    dispatch(deleteCustomer(id));
  };

  if (loading) return <Typography>Loading customers...</Typography>;
  if (error) return <Typography color="error">Error loading customers: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Customer Relationship Management</Typography>
      <Button variant="contained" onClick={() => handleOpenDialog()} sx={{ marginBottom: 2 }}>
        Add New Customer
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Customers List</Typography>
            {customers.length === 0 ? (
              <Typography>No customers available. Create a new customer to get started.</Typography>
            ) : (
              <List>
                {customers.map((customer) => (
                  <ListItem key={customer.id}>
                    <ListItemText 
                      primary={customer.name} 
                      secondary={`Email: ${customer.email}, Phone: ${customer.phone}, Address: ${customer.address}`} 
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end" aria-label="edit" onClick={() => handleOpenDialog(customer)} size="small" sx={{ marginRight: 1 }}>
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteCustomer(customer.id)} size="small">
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

      {/* Dialog for Adding/Editing Customers */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingCustomer ? 'Edit Customer' : 'Add New Customer'}</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Name"
            fullWidth
            value={customerName}
            onChange={(e) => setCustomerName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Email"
            fullWidth
            value={customerEmail}
            onChange={(e) => setCustomerEmail(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Phone"
            fullWidth
            value={customerPhone}
            onChange={(e) => setCustomerPhone(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Address"
            fullWidth
            multiline
            rows={3}
            value={customerAddress}
            onChange={(e) => setCustomerAddress(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveCustomer} disabled={!customerName || !customerEmail}>Save</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default CRM;
