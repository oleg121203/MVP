import { Box, Flex, Heading } from '@chakra-ui/react';
import ThreeScene from '../components/ThreeScene';
import AIChatInterface from '../components/AIChatInterface';

export default function Dashboard() {
  return (
    <Box p={4}>
      <Flex direction="column" gap={8}>
        <Heading size="xl">HVAC AI Design Studio</Heading>
        
        <Flex gap={8}>
          <Box flex={2} h="600px">
            <ThreeScene />
          </Box>
          
          <Box flex={1}>
            <AIChatInterface />
          </Box>
        </Flex>
      </Flex>
    </Box>
  );
}
