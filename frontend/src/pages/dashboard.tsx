import React from 'react';
import { Box, Flex, Heading, Text, VStack, SimpleGrid, IconButton, Divider, Button } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { FaCog, FaCalculator, FaFolder, FaLightbulb } from 'react-icons/fa';
import Card from '../components/common/Card';
import ChakraIcon from '../components/common/ChakraIcon';
import ThreeScene from '../components/ThreeScene';
import AIChatInterface from '../components/AIChatInterface';

export default function Dashboard() {
  const { t } = useTranslation();

  return (
    <Box>
      <Box p={{ base: 4, md: 8 }}>
        {/* Welcome Message */}
        <Box mb={8}>
          <Heading as="h1" size="xl" mb={2}>{t('dashboard.welcome')}</Heading>
          <Text fontSize="md" color="text.secondary">{t('dashboard.subtitle')}</Text>
        </Box>

        {/* Quick Stats */}
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4} mb={8}>
          <Card p={4} textAlign="center">
            <Heading as="h3" size="md" mb={1}>{t('dashboard.stats.projects')}</Heading>
            <Text fontSize="2xl" fontWeight="bold">3</Text>
          </Card>
          <Card p={4} textAlign="center">
            <Heading as="h3" size="md" mb={1}>{t('dashboard.stats.calculations')}</Heading>
            <Text fontSize="2xl" fontWeight="bold">12</Text>
          </Card>
          <Card p={4} textAlign="center">
            <Heading as="h3" size="md" mb={1}>{t('dashboard.stats.aiInsights')}</Heading>
            <Text fontSize="2xl" fontWeight="bold">5</Text>
          </Card>
        </SimpleGrid>

        {/* Main Content Area */}
        <Flex direction={{ base: 'column', lg: 'row' }} gap={8} mb={8}>
          {/* Project Overview (Left Sidebar) */}
          <Box flex={{ base: 'auto', lg: 1 }} order={{ base: 2, lg: 1 }}>
            <Card p={6} mb={6}>
              <Heading as="h2" size="md" mb={4}>{t('dashboard.projects.title')}</Heading>
              <VStack spacing={3} align="stretch">
                <Box p={2} bg="background.light" borderRadius="md">
                  <Text fontWeight="bold">Project Alpha</Text>
                  <Text fontSize="sm" color="text.secondary">Updated: Today</Text>
                </Box>
                <Box p={2} bg="background.light" borderRadius="md">
                  <Text fontWeight="bold">Project Beta</Text>
                  <Text fontSize="sm" color="text.secondary">Updated: 3 days ago</Text>
                </Box>
                <Box p={2} bg="background.light" borderRadius="md">
                  <Text fontWeight="bold">Project Gamma</Text>
                  <Text fontSize="sm" color="text.secondary">Updated: 1 week ago</Text>
                </Box>
              </VStack>
              <Box mt={4} textAlign="center">
                <Text fontSize="sm" color="brand.primary" cursor="pointer">{t('dashboard.projects.viewAll')}</Text>
              </Box>
            </Card>

            {/* Recent Calculations */}
            <Card p={6}>
              <Heading as="h2" size="md" mb={4}>{t('dashboard.calculations.title')}</Heading>
              <VStack spacing={3} align="stretch">
                <Box p={2} bg="background.light" borderRadius="md">
                  <Text fontWeight="bold">Duct Sizing - Office</Text>
                  <Text fontSize="sm" color="text.secondary">Performed: Yesterday</Text>
                </Box>
                <Box p={2} bg="background.light" borderRadius="md">
                  <Text fontWeight="bold">Airflow Rate - Warehouse</Text>
                  <Text fontSize="sm" color="text.secondary">Performed: 4 days ago</Text>
                </Box>
              </VStack>
              <Box mt={4} textAlign="center">
                <Text fontSize="sm" color="brand.primary" cursor="pointer">{t('dashboard.calculations.viewAll')}</Text>
              </Box>
            </Card>
          </Box>

          {/* 3D Visualization (Main Area) */}
          <Box flex={{ base: 'auto', lg: 2 }} h={{ base: '400px', lg: '600px' }} order={{ base: 1, lg: 2 }}>
            <Card h="100%">
              <ThreeScene />
            </Card>
          </Box>

          {/* AI Insights & Chat (Right Sidebar) */}
          <Box flex={{ base: 'auto', lg: 1 }} order={{ base: 3, lg: 3 }}>
            <Card p={6} mb={6}>
              <Heading as="h2" size="md" mb={4}>{t('dashboard.aiInsights.title')}</Heading>
              <VStack spacing={3} align="stretch">
                <Box p={2} bg="background.light" borderRadius="md">
                  <Flex align="center">
                    <ChakraIcon icon={FaLightbulb} color="#008080" boxSize={4} mr={2} />
                    <Text fontWeight="bold">Energy Efficiency Tip</Text>
                  </Flex>
                  <Text fontSize="sm">Adjust duct sizes for optimal airflow and reduced energy loss.</Text>
                </Box>
                <Box p={2} bg="background.light" borderRadius="md">
                  <Flex align="center">
                    <ChakraIcon icon={FaLightbulb} color="#008080" boxSize={4} mr={2} />
                    <Text fontWeight="bold">Maintenance Alert</Text>
                  </Flex>
                  <Text fontSize="sm">Check air filters in Zone 3 - potential clog detected.</Text>
                </Box>
              </VStack>
              <Box mt={4} textAlign="center">
                <Text fontSize="sm" color="brand.primary" cursor="pointer">{t('dashboard.aiInsights.viewAll')}</Text>
              </Box>
            </Card>

            <Card p={4}>
              <AIChatInterface />
            </Card>
          </Box>
        </Flex>

        {/* Quick Access Tools */}
        <Box mb={8}>
          <Heading as="h2" size="md" mb={4}>{t('dashboard.tools.title')}</Heading>
          <Divider mb={4} />
          <Flex wrap="wrap" gap={4}>
            <Button leftIcon={<ChakraIcon icon={FaCalculator} />} variant="secondary">{t('dashboard.tools.calculator')}</Button>
            <Button leftIcon={<ChakraIcon icon={FaFolder} />} variant="secondary">{t('dashboard.tools.newProject')}</Button>
          </Flex>
        </Box>

        {/* Customization Options */}
        <Box>
          <Flex justify="space-between" align="center">
            <Box>
              <Heading as="h2" size="md">{t('dashboard.customize.title')}</Heading>
              <Text fontSize="sm" color="text.secondary">{t('dashboard.customize.subtitle')}</Text>
            </Box>
            <IconButton aria-label={t('dashboard.customize.settings')} icon={<ChakraIcon icon={FaCog} />} variant="secondary" />
          </Flex>
        </Box>
      </Box>
    </Box>
  );
}
