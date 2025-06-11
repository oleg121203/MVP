import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { enableMFA, disableMFA, verifyMFACode } from '../../store/authSlice';
import { Box, Typography, Button, TextField, Dialog, DialogActions, DialogContent, DialogTitle, Alert } from '@mui/material';
import { Security as SecurityIcon } from '@mui/icons-material';

function MultiFactorAuth() {
  const dispatch = useDispatch();
  const { user, mfaEnabled, mfaError } = useSelector((state) => state.auth);
  const [openDialog, setOpenDialog] = useState(false);
  const [mfaCode, setMfaCode] = useState('');

  const handleEnableMFA = () => {
    dispatch(enableMFA());
    setOpenDialog(true);
  };

  const handleDisableMFA = () => {
    dispatch(disableMFA());
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setMfaCode('');
  };

  const handleVerifyCode = () => {
    dispatch(verifyMFACode(mfaCode));
    handleCloseDialog();
  };

  if (!user) {
    return <Typography>Please log in to manage Multi-Factor Authentication settings.</Typography>;
  }

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>
        <SecurityIcon sx={{ marginRight: 1 }} /> Multi-Factor Authentication
      </Typography>
      <Typography variant="body1" paragraph>
        Enhance your account security by enabling Multi-Factor Authentication (MFA).
      </Typography>

      {mfaEnabled ? (
        <Box>
          <Alert severity="success" sx={{ marginBottom: 2 }}>
            MFA is currently enabled for your account.
          </Alert>
          <Button variant="contained" color="secondary" onClick={handleDisableMFA}>
            Disable MFA
          </Button>
        </Box>
      ) : (
        <Box>
          <Alert severity="warning" sx={{ marginBottom: 2 }}>
            MFA is currently disabled for your account.
          </Alert>
          <Button variant="contained" color="primary" onClick={handleEnableMFA}>
            Enable MFA
          </Button>
        </Box>
      )}

      {mfaError && (
        <Alert severity="error" sx={{ marginTop: 2 }}>
          {mfaError}
        </Alert>
      )}

      {/* Dialog for MFA Code Verification */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Verify MFA Code</DialogTitle>
        <DialogContent>
          <Typography variant="body1" paragraph>
            Scan the QR code with your authenticator app and enter the code below.
          </Typography>
          {/* Placeholder for QR Code - In a real app, this would be an image or a library to generate QR codes */}
          <Box sx={{ backgroundColor: '#f0f0f0', height: 200, display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: 2 }}>
            <Typography>QR Code Placeholder</Typography>
          </Box>
          <TextField
            autoFocus
            margin="dense"
            label="MFA Code"
            fullWidth
            value={mfaCode}
            onChange={(e) => setMfaCode(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleVerifyCode} disabled={!mfaCode}>Verify</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default MultiFactorAuth;
