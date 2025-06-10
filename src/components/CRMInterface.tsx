import React, { useState, useEffect } from 'react';
import { Container, Paper, Typography, Tab, Tabs, Box, List, ListItem, ListItemText, Divider } from '@mui/material';
import { CRMClient } from '../api/crmClient';
import { CRMContact, CRMDeal, CRMTask } from '../types/crm';

function TabPanel({ children, value, index, ...other }: { children: React.ReactNode; value: number; index: number }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`crm-tabpanel-${index}`}
      aria-labelledby={`crm-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `crm-tab-${index}`,
    'aria-controls': `crm-tabpanel-${index}`,
  };
}

const CRMInterface: React.FC = () => {
  const [value, setValue] = useState(0);
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

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        CRM Interface
      </Typography>
      <Paper sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={value} onChange={handleChange} aria-label="CRM entity tabs">
            <Tab label="Contacts" {...a11yProps(0)} />
            <Tab label="Deals" {...a11yProps(1)} />
            <Tab label="Tasks" {...a11yProps(2)} />
          </Tabs>
        </Box>
        <TabPanel value={value} index={0}>
          <List>
            {contacts.map((contact) => (
              <React.Fragment key={contact.id}>
                <ListItem>
                  <ListItemText
                    primary={`${contact.firstName} ${contact.lastName}`}
                    secondary={`Email: ${contact.email}, Phone: ${contact.phone}`}
                  />
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </TabPanel>
        <TabPanel value={value} index={1}>
          <List>
            {deals.map((deal) => (
              <React.Fragment key={deal.id}>
                <ListItem>
                  <ListItemText
                    primary={deal.title}
                    secondary={`Stage: ${deal.stage}, Value: $${deal.value}, Status: ${deal.status}`}
                  />
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </TabPanel>
        <TabPanel value={value} index={2}>
          <List>
            {tasks.map((task) => (
              <React.Fragment key={task.id}>
                <ListItem>
                  <ListItemText
                    primary={task.description || 'Task'}
                    secondary={`Due Date: ${task.dueDate}, Status: ${task.status}, Contact: ${task.contactId}`}
                  />
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </TabPanel>
      </Paper>
    </Container>
  );
};

export default CRMInterface;
