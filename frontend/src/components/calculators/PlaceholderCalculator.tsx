import React from 'react';
import { Box, Text, VStack } from '@chakra-ui/react';
import Card from '../common/Card';

const PlaceholderCalculator: React.FC = () => {
  return (
    <Card>
      <VStack spacing={4} align="start">
        <Text fontSize="xl" fontWeight="bold">Calculator Placeholder</Text>
        <Box>
          <Text>This is a placeholder for a calculator component. Replace with actual calculator logic.</Text>
        </Box>
      </VStack>
    </Card>
  );
};

export default PlaceholderCalculator;
