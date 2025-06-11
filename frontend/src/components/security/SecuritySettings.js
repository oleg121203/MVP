import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchSecuritySettings, updateMFASetting, updateRBACPolicy, manageEncryptionKey } from '../../store/securitySlice';
import { Box, Typography, Grid, Paper, Button, TextField, Switch, FormControlLabel, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, Alert } from '@mui/material';
import { Security as SecurityIcon, VpnKey as VpnKeyIcon, Refresh as RefreshIcon } from '@mui/icons-material';

function SecuritySettings() {
  const dispatch = useDispatch();
  const { settings, loading, error } = useSelector((state) => state.security);
  const [mfaEnabled, setMfaEnabled] = useState(false);
  const [rbacPolicy, setRbacPolicy] = useState('');
  const [openKeyDialog, setOpenKeyDialog] = useState(false);
  const [encryptionKey, setEncryptionKey] = useState('');
  const [keyAction, setKeyAction] = useState('generate');

  useEffect(() => {
    dispatch(fetchSecuritySettings());
  }, [dispatch]);

  useEffect(() => {
    if (settings) {
      setMfaEnabled(settings.mfaEnabled || false);
      setRbacPolicy(settings.rbacPolicy || '');
    }
  }, [settings]);

  const handleMfaToggle = () => {
    const newMfaState = !mfaEnabled;
    setMfaEnabled(newMfaState);
    dispatch(updateMFASetting(newMfaState));
  };

  const handleRbacPolicyChange = (event) => {
    setRbacPolicy(event.target.value);
  };

  const handleUpdateRbacPolicy = () => {
    if (rbacPolicy.trim()) {
      dispatch(updateRBACPolicy(rbacPolicy));
    }
  };

  const handleOpenKeyDialog = (action = 'generate') => {
    setKeyAction(action);
    setEncryptionKey('');
    setOpenKeyDialog(true);
  };

  const handleCloseKeyDialog = () => {
    setOpenKeyDialog(false);
  };

  const handleManageKey = () => {
    if (keyAction === 'generate') {
      dispatch(manageEncryptionKey({ action: 'generate' }));
    } else if (keyAction === 'rotate') {
      dispatch(manageEncryptionKey({ action: 'rotate' }));
    } else if (keyAction === 'import' && encryptionKey.trim()) {
      dispatch(manageEncryptionKey({ action: 'import', key: encryptionKey }));
    }
    handleCloseKeyDialog();
  };

  const handleRefresh = () => {
    dispatch(fetchSecuritySettings());
  };

  if (loading) return <Typography>Loading security settings...</Typography>;
  if (error) return <Alert severity="error">Error loading security settings: {error}</Alert>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Security Settings</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 2 }}>
        <Button variant="outlined" onClick={handleRefresh} startIcon={<RefreshIcon />}>Refresh</Button>
      </Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Authentication Settings</Typography>
            <Box sx={{ marginBottom: 2 }}>
              <FormControlLabel
                control={<Switch checked={mfaEnabled} onChange={handleMfaToggle} />}
                label="Enable Multi-Factor Authentication (MFA)"
              />
              <Typography variant="body2" color="textSecondary">
                {mfaEnabled ? 'MFA is enabled for all users.' : 'MFA is disabled. Enable for enhanced security.'}
              </Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Role-Based Access Control (RBAC)</Typography>
            <TextField
              fullWidth
              multiline
              rows={4}
              value={rbacPolicy}
              onChange={handleRbacPolicyChange}
              label="RBAC Policy (JSON)"
              variant="outlined"
              placeholder="Enter RBAC policy in JSON format"
              sx={{ marginBottom: 2 }}
            />
            <Button variant="contained" onClick={handleUpdateRbacPolicy} disabled={!rbacPolicy.trim()} startIcon={<SecurityIcon />}>
              Update Policy
            </Button>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Encryption Key Management</Typography>
            <Box sx={{ display: 'flex', gap: 1, marginTop: 2 }}>
              <Button variant="contained" onClick={() => handleOpenKeyDialog('generate')} startIcon={<VpnKeyIcon />}>
                Generate New Key
              </Button>
              <Button variant="contained" onClick={() => handleOpenKeyDialog('rotate')} startIcon={<VpnKeyIcon />}>
                Rotate Key
              </Button>
              <Button variant="contained" onClick={() => handleOpenKeyDialog('import')} startIcon={<VpnKeyIcon />}>
                Import Key
              </Button>
            </Box>
            <Typography variant="body2" color="textSecondary" sx={{ marginTop: 1 }}>
              Current key status: {settings.encryptionKeyStatus || 'Unknown'} | Last rotated: {settings.lastKeyRotation || 'Never'}
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog for Encryption Key Management */}
      <Dialog open={openKeyDialog} onClose={handleCloseKeyDialog}>
        <DialogTitle>{keyAction.charAt(0).toUpperCase() + keyAction.slice(1)} Encryption Key</DialogTitle>
        <DialogContent>
          {keyAction === 'import' && (
            <TextField
              autoFocus
              margin="dense"
              label="Encryption Key"
              fullWidth
              value={encryptionKey}
              onChange={(e) => setEncryptionKey(e.target.value)}
              placeholder="Enter or paste encryption key"
              type="password"
            />
          )}
          {keyAction === 'generate' && (
            <Typography>Are you sure you want to generate a new encryption key? This will replace the current key.</Typography>
          )}
          {keyAction === 'rotate' && (
            <Typography>Are you sure you want to rotate the encryption key? This will create a new key based on the current one.</Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseKeyDialog}>Cancel</Button>
          <Button onClick={handleManageKey} disabled={keyAction === 'import' && !encryptionKey.trim()}>Confirm</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default SecuritySettings;
