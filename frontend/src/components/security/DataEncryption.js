import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchEncryptionSettings, updateEncryptionSettings } from '../../store/encryptionSlice';
import { Box, Typography, Button, TextField, MenuItem, Select, FormControl, InputLabel, Alert } from '@mui/material';
import { Lock as LockIcon } from '@mui/icons-material';

function DataEncryption() {
  const dispatch = useDispatch();
  const { settings, loading, error } = useSelector((state) => state.encryption);
  const [encryptionLevel, setEncryptionLevel] = useState('standard');
  const [keyRotationFrequency, setKeyRotationFrequency] = useState('monthly');
  const [customKey, setCustomKey] = useState('');

  useEffect(() => {
    dispatch(fetchEncryptionSettings());
  }, [dispatch]);

  useEffect(() => {
    if (settings) {
      setEncryptionLevel(settings.level || 'standard');
      setKeyRotationFrequency(settings.keyRotationFrequency || 'monthly');
      setCustomKey(settings.customKey || '');
    }
  }, [settings]);

  const handleEncryptionLevelChange = (event) => {
    setEncryptionLevel(event.target.value);
  };

  const handleKeyRotationFrequencyChange = (event) => {
    setKeyRotationFrequency(event.target.value);
  };

  const handleSaveSettings = () => {
    dispatch(updateEncryptionSettings({ level: encryptionLevel, keyRotationFrequency, customKey }));
  };

  if (loading) return <Typography>Loading encryption settings...</Typography>;
  if (error) return <Typography color="error">Error loading encryption settings: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>
        <LockIcon sx={{ marginRight: 1 }} /> Data Encryption Enhancements
      </Typography>
      <Typography variant="body1" paragraph>
        Configure advanced data encryption settings to protect sensitive information.
      </Typography>

      {settings ? (
        <Box>
          <Alert severity="info" sx={{ marginBottom: 2 }}>
            Current encryption settings are loaded. Update as needed.
          </Alert>
          <FormControl fullWidth margin="normal">
            <InputLabel id="encryption-level-select-label">Encryption Level</InputLabel>
            <Select
              labelId="encryption-level-select-label"
              id="encryption-level-select"
              value={encryptionLevel}
              label="Encryption Level"
              onChange={handleEncryptionLevelChange}
            >
              <MenuItem value="standard">Standard (AES-128)</MenuItem>
              <MenuItem value="enhanced">Enhanced (AES-192)</MenuItem>
              <MenuItem value="maximum">Maximum (AES-256)</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="normal">
            <InputLabel id="key-rotation-frequency-select-label">Key Rotation Frequency</InputLabel>
            <Select
              labelId="key-rotation-frequency-select-label"
              id="key-rotation-frequency-select"
              value={keyRotationFrequency}
              label="Key Rotation Frequency"
              onChange={handleKeyRotationFrequencyChange}
            >
              <MenuItem value="daily">Daily</MenuItem>
              <MenuItem value="weekly">Weekly</MenuItem>
              <MenuItem value="monthly">Monthly</MenuItem>
              <MenuItem value="quarterly">Quarterly</MenuItem>
              <MenuItem value="yearly">Yearly</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="normal"
            label="Custom Encryption Key (optional)"
            fullWidth
            multiline
            rows={3}
            value={customKey}
            onChange={(e) => setCustomKey(e.target.value)}
            placeholder="Paste your custom encryption key here, or leave blank to use system-generated keys."
          />
          <Button variant="contained" color="primary" onClick={handleSaveSettings} sx={{ marginTop: 2 }}>
            Save Settings
          </Button>
        </Box>
      ) : (
        <Alert severity="warning" sx={{ marginBottom: 2 }}>
          No encryption settings found. Default settings will be applied.
        </Alert>
      )}
    </Box>
  );
}

export default DataEncryption;
