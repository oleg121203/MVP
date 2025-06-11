import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { login, logout } from '../../store/authSlice';
import { TextField, Button, Box, Typography, Paper, Grid } from '@mui/material';

function EnterpriseAuth() {
  const dispatch = useDispatch();
  const { isAuthenticated, user, error } = useSelector((state) => state.auth);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mfaCode, setMfaCode] = useState('');

  const handleLogin = () => {
    if (username && password) {
      dispatch(login({ username, password, mfaCode }));
    } else {
      alert('Please enter username and password');
    }
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  if (isAuthenticated) {
    return (
      <Box sx={{ padding: 2 }}>
        <Typography variant="h5" gutterBottom>Enterprise Authentication</Typography>
        <Paper elevation={3} sx={{ padding: 3, maxWidth: 400, margin: 'auto' }}>
          <Typography variant="h6">Welcome, {user?.username || 'User'}!</Typography>
          <Typography>You are authenticated.</Typography>
          <Button variant="contained" color="secondary" onClick={handleLogout} sx={{ marginTop: 2 }}>
            Logout
          </Button>
        </Paper>
      </Box>
    );
  }

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Enterprise Authentication</Typography>
      {error && <Typography color="error">Error: {error}</Typography>}
      <Paper elevation={3} sx={{ padding: 3, maxWidth: 400, margin: 'auto' }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              label="Username"
              variant="outlined"
              fullWidth
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Password"
              variant="outlined"
              type="password"
              fullWidth
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="MFA Code (if applicable)"
              variant="outlined"
              fullWidth
              value={mfaCode}
              onChange={(e) => setMfaCode(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" onClick={handleLogin} fullWidth>
              Login
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}

export default EnterpriseAuth;
