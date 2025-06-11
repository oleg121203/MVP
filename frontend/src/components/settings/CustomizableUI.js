import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateTheme, updateLayout } from '../../store/uiSettingsSlice';
import { Grid, Paper, Typography, Box, Button, TextField, Slider, ColorLensIcon, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

function CustomizableUI() {
  const dispatch = useDispatch();
  const { theme, layout, error } = useSelector((state) => state.uiSettings);
  const [primaryColor, setPrimaryColor] = useState(theme.primaryColor || '#1976d2');
  const [secondaryColor, setSecondaryColor] = useState(theme.secondaryColor || '#dc004e');
  const [fontSize, setFontSize] = useState(theme.fontSize || 16);
  const [selectedLayout, setSelectedLayout] = useState(layout || 'default');

  const handleThemeUpdate = () => {
    dispatch(updateTheme({
      primaryColor,
      secondaryColor,
      fontSize
    }));
  };

  const handleLayoutUpdate = () => {
    dispatch(updateLayout(selectedLayout));
  };

  const handleFontSizeChange = (event, newValue) => {
    setFontSize(newValue);
  };

  const handleLayoutChange = (event) => {
    setSelectedLayout(event.target.value);
  };

  if (error) return <Typography color="error">Error updating UI settings: {error}</Typography>;

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h5" gutterBottom>Customizable User Interface</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Theme Settings</Typography>
            <Box sx={{ marginBottom: 2 }}>
              <TextField
                label="Primary Color"
                type="color"
                value={primaryColor}
                onChange={(e) => setPrimaryColor(e.target.value)}
                fullWidth
                sx={{ marginBottom: 1 }}
              />
              <TextField
                label="Secondary Color"
                type="color"
                value={secondaryColor}
                onChange={(e) => setSecondaryColor(e.target.value)}
                fullWidth
                sx={{ marginBottom: 1 }}
              />
              <Typography gutterBottom>Font Size ({fontSize}px)</Typography>
              <Slider
                value={fontSize}
                onChange={handleFontSizeChange}
                min={12}
                max={24}
                valueLabelDisplay="auto"
              />
            </Box>
            <Button variant="contained" onClick={handleThemeUpdate}>Update Theme</Button>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ padding: 2 }}>
            <Typography variant="h6">Layout Settings</Typography>
            <FormControl fullWidth sx={{ marginBottom: 2 }}>
              <InputLabel id="layout-select-label">Layout Type</InputLabel>
              <Select
                labelId="layout-select-label"
                id="layout-select"
                value={selectedLayout}
                label="Layout Type"
                onChange={handleLayoutChange}
              >
                <MenuItem value="default">Default</MenuItem>
                <MenuItem value="compact">Compact</MenuItem>
                <MenuItem value="wide">Wide</MenuItem>
              </Select>
            </FormControl>
            <Button variant="contained" onClick={handleLayoutUpdate}>Update Layout</Button>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default CustomizableUI;
