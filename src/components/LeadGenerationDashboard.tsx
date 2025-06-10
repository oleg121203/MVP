import React, { useEffect, useState } from 'react';
import { LeadGenerationClient } from '../api/leadGenerationClient';
import { Lead, LeadSource, LeadCampaign } from '../types/leadGeneration';
import { Container, Grid, Paper, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

const LeadGenerationDashboard: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [sources, setSources] = useState<LeadSource[]>([]);
  const [campaigns, setCampaigns] = useState<LeadCampaign[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const leadsData = await LeadGenerationClient.getLeads();
        const sourcesData = await LeadGenerationClient.getLeadSources();
        const campaignsData = await LeadGenerationClient.getLeadCampaigns();

        setLeads(leadsData);
        setSources(sourcesData);
        setCampaigns(campaignsData);
      } catch (error) {
        console.error('Error fetching lead generation data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Lead Generation Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid component="div" sx={{ width: { xs: '100%', md: '33.33%' } }}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Leads
            </Typography>
            <Divider />
            <List>
              {leads.map((lead) => (
                <ListItem key={lead.id}>
                  <ListItemText primary={`${lead.firstName} ${lead.lastName}`} secondary={lead.email} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid component="div" sx={{ width: { xs: '100%', md: '33.33%' } }}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Lead Sources
            </Typography>
            <Divider />
            <List>
              {sources.map((source) => (
                <ListItem key={source.id}>
                  <ListItemText primary={source.name} secondary={source.description} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid component="div" sx={{ width: { xs: '100%', md: '33.33%' } }}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Lead Campaigns
            </Typography>
            <Divider />
            <List>
              {campaigns.map((campaign) => (
                <ListItem key={campaign.id}>
                  <ListItemText primary={campaign.name} secondary={`Status: ${campaign.status}`} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LeadGenerationDashboard;
