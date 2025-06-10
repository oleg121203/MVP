import React, { useState } from 'react';
import { Container, Paper, Typography, Button, CircularProgress, Box } from '@mui/material';
import { integrationService } from '../services/integrationService';

const IntegrationPanel: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [syncStatus, setSyncStatus] = useState<string>('');

  const handleSyncLeads = async () => {
    setLoading(true);
    setSyncStatus('');
    try {
      await integrationService.syncLeadsToCRM();
      setSyncStatus('Leads successfully synced to CRM.');
    } catch (error) {
      setSyncStatus('Failed to sync leads to CRM. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const handleSyncSourcesAndCampaigns = async () => {
    setLoading(true);
    setSyncStatus('');
    try {
      await integrationService.syncLeadSourcesAndCampaigns();
      setSyncStatus('Lead sources and campaigns successfully synced.');
    } catch (error) {
      setSyncStatus('Failed to sync lead sources and campaigns. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const handleSyncCRMToVentAI = async () => {
    setLoading(true);
    setSyncStatus('');
    try {
      await integrationService.syncCRMToVentAI();
      setSyncStatus('CRM data successfully synced to VentAI systems.');
    } catch (error) {
      setSyncStatus('Failed to sync CRM data to VentAI systems. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Integration Panel
      </Typography>
      <Paper sx={{ p: 3, height: '100%' }}>
        <Typography variant="h6" gutterBottom>
          Data Synchronization Controls
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              onClick={handleSyncLeads}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={24} /> : null}
            >
              Sync Leads to CRM
            </Button>
            <Button
              variant="contained"
              onClick={handleSyncSourcesAndCampaigns}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={24} /> : null}
            >
              Sync Sources & Campaigns
            </Button>
            <Button
              variant="contained"
              onClick={handleSyncCRMToVentAI}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={24} /> : null}
            >
              Sync CRM to VentAI
            </Button>
          </Box>
          {syncStatus && (
            <Typography variant="body1" color={syncStatus.includes('successfully') ? 'success.main' : 'error.main'}>
              {syncStatus}
            </Typography>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default IntegrationPanel;
