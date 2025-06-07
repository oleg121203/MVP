import React from 'react';
import { Box, Text, VStack } from '@chakra-ui/react';
import Card from '../common/Card';

const PlaceholderDashboard: React.FC = () => {
  return (
    <Card>
      <VStack spacing={4} align="start">
        <Text fontSize="xl" fontWeight="bold">Dashboard Placeholder</Text>
        <Box>
          <Text>This is a placeholder for a dashboard component. Replace with actual dashboard visualizations and data.</Text>
        </Box>
      </VStack>
    </Card>
  );
};

export default PlaceholderDashboard;
