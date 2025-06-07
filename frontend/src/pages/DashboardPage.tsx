import React from 'react';
import { Box, Text, VStack, Heading, SimpleGrid, Flex, IconButton, Divider, Button } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { FaProjectDiagram, FaCalculator, FaRobot, FaCog } from 'react-icons/fa';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';
import ChakraIcon from '../components/common/ChakraIcon';
import ThreeScene from '../components/ThreeScene';
import AIChatInterface from '../components/AIChatInterface';

const DashboardPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <MainLayout title={t('dashboard')}>
      <Box p={{ base: 4, md: 8 }}>
        {/* Welcome Message */}
        <Heading as="h1" size="xl" mb={2}>{t('dashboard.welcome')}</Heading>
        <Text fontSize={{ base: 'md', md: 'lg' }} color="text.secondary" mb={6}>{t('dashboard.subtitle')}</Text>

        {/* Quick Stats Overview */}
        <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={4} mb={8}>
          <Card p={4} textAlign="center">
            <Heading as="h3" size="md" mb={2}>{t('dashboard.stats.projects')}</Heading>
            <Text fontSize="2xl" fontWeight="bold">3</Text>
          </Card>
          <Card p={4} textAlign="center">
            <Heading as="h3" size="md" mb={2}>{t('dashboard.stats.calculations')}</Heading>
            <Text fontSize="2xl" fontWeight="bold">12</Text>
          </Card>
          <Card p={4} textAlign="center">
            <Heading as="h3" size="md" mb={2}>{t('dashboard.stats.aiInsights')}</Heading>
            <Text fontSize="2xl" fontWeight="bold">5</Text>
          </Card>
        </SimpleGrid>

        {/* Main Content Area */}
        <Flex direction={{ base: 'column', md: 'row' }} gap={6} mb={8}>
          {/* Project Overview Sidebar */}
          <Box w={{ base: 'full', md: '250px' }} mb={{ base: 4, md: 0 }}>
            <Heading as="h2" size="md" mb={4}>{t('dashboard.projects.title')}</Heading>
            <Divider mb={4} />
            <VStack spacing={3} align="stretch">
              <Card p={3}>
                <Text fontWeight="bold">Office Ventilation</Text>
                <Text fontSize="sm" color="text.secondary">Updated: 2 days ago</Text>
              </Card>
              <Card p={3}>
                <Text fontWeight="bold">Warehouse Airflow</Text>
                <Text fontSize="sm" color="text.secondary">Updated: 1 week ago</Text>
              </Card>
              <Card p={3}>
                <Text fontWeight="bold">Residential HVAC</Text>
                <Text fontSize="sm" color="text.secondary">Updated: 3 weeks ago</Text>
              </Card>
              <Link to="/projects" style={{ textAlign: 'center' }}>
                <Text fontSize="sm" color="brand.primary">{t('dashboard.projects.viewAll')}</Text>
              </Link>
            </VStack>
          </Box>

          {/* Main Dashboard Content */}
          <Box flex={1}>
            {/* Recent Calculations */}
            <Heading as="h2" size="md" mb={4}>{t('dashboard.calculations.title')}</Heading>
            <Divider mb={4} />
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4} mb={6}>
              <Card p={4}>
                <Text fontWeight="bold">Duct Sizing - Office</Text>
                <Text fontSize="sm" color="text.secondary">Completed: 3 days ago</Text>
              </Card>
              <Card p={4}>
                <Text fontWeight="bold">Airflow Rate - Warehouse</Text>
                <Text fontSize="sm" color="text.secondary">Completed: 1 week ago</Text>
              </Card>
            </SimpleGrid>

            {/* 3D Visualization Area */}
            <Heading as="h2" size="md" mb={4}>{t('dashboard.visualization.title')}</Heading>
            <Divider mb={4} />
            <Card h={{ base: '300px', md: '400px' }} mb={6}>
              <ThreeScene />
            </Card>
          </Box>

          {/* AI Insights Sidebar */}
          <Box w={{ base: 'full', md: '300px' }}>
            <Heading as="h2" size="md" mb={4}>{t('dashboard.aiInsights.title')}</Heading>
            <Divider mb={4} />
            <Card h={{ base: '400px', md: '500px' }}>
              <AIChatInterface />
            </Card>
          </Box>
        </Flex>

        {/* Quick Access Tools */}
        <Heading as="h2" size="md" mb={4}>{t('dashboard.tools.title')}</Heading>
        <Divider mb={4} />
        <Flex wrap="wrap" gap={4} mb={8} justify={{ base: 'center', md: 'flex-start' }}>
          <Link to="/calculators">
            <Button leftIcon={<ChakraIcon icon={FaCalculator} />} variant="primary" size={{ base: 'sm', md: 'md' }}>{t('dashboard.tools.calculator')}</Button>
          </Link>
          <Button leftIcon={<ChakraIcon icon={FaProjectDiagram} />} variant="secondary" size={{ base: 'sm', md: 'md' }}>{t('dashboard.tools.newProject')}</Button>
        </Flex>

        {/* Customization Options */}
        <Flex justify="flex-end">
          <IconButton aria-label={t('dashboard.settings')} icon={<ChakraIcon icon={FaCog} />} variant="outline" size={{ base: 'sm', md: 'md' }} />
        </Flex>
      </Box>
    </MainLayout>
  );
};

export default DashboardPage;
