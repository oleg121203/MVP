import React, { useEffect, useState } from 'react';
import { CRMClient } from '../api/crmClient';
import { CRMContact, CRMDeal, CRMTask } from '../types/crm';
import { Container, Grid, Paper, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

const CRMDashboard: React.FC = () => {
  const [contacts, setContacts] = useState<CRMContact[]>([]);
  const [deals, setDeals] = useState<CRMDeal[]>([]);
  const [tasks, setTasks] = useState<CRMTask[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const contactsData = await CRMClient.getContacts();
        const dealsData = await CRMClient.getDeals();
        const tasksData = await CRMClient.getTasks();

        setContacts(contactsData);
        setDeals(dealsData);
        setTasks(tasksData);
      } catch (error) {
        console.error('Error fetching CRM data:', error);
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
        CRM Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid component="div" sx={{ width: { xs: '100%', md: '33.33%' } }}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Contacts
            </Typography>
            <Divider />
            <List>
              {contacts.map((contact) => (
                <ListItem key={contact.id}>
                  <ListItemText primary={`${contact.firstName} ${contact.lastName}`} secondary={contact.email} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid component="div" sx={{ width: { xs: '100%', md: '33.33%' } }}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Deals
            </Typography>
            <Divider />
            <List>
              {deals.map((deal) => (
                <ListItem key={deal.id}>
                  <ListItemText primary={deal.title} secondary={`Value: $${deal.value}`} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid component="div" sx={{ width: { xs: '100%', md: '33.33%' } }}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Tasks
            </Typography>
            <Divider />
            <List>
              {tasks.map((task) => (
                <ListItem key={task.id}>
                  <ListItemText primary={task.title} secondary={`Due: ${task.dueDate}`} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default CRMDashboard;
