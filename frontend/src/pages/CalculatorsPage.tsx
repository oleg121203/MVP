import React, { useState } from 'react';
import { Box, Text, VStack, SimpleGrid, Heading, Input, Select, Flex, IconButton, Divider, Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { FaSearch, FaSave, FaQuestionCircle } from 'react-icons/fa';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import PlaceholderCalculator from '../components/calculators/PlaceholderCalculator';

const CalculatorsPage: React.FC = () => {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');

  return (
    <MainLayout title={t('calculators')}>
      <Box p={{ base: 4, md: 8 }}>
        {/* Header */}
        <Heading as="h1" size="xl" mb={6} textAlign="center">{t('calculators')}</Heading>
        <Text fontSize="md" color="text.secondary" textAlign="center" mb={8}>{t('calculators.subtitle')}</Text>

        {/* Search and Filter */}
        <Flex direction={{ base: 'column', md: 'row' }} gap={4} mb={8} align="center" maxW="container.lg" mx="auto">
          <Input 
            placeholder={t('calculators.searchPlaceholder')} 
            value={searchTerm} 
            onChange={(e) => setSearchTerm(e.target.value)} 
            leftIcon={<FaSearch />} 
            flex={1}
          />
          <Select 
            value={categoryFilter} 
            onChange={(e) => setCategoryFilter(e.target.value)}
            w={{ base: '100%', md: '200px' }}
          >
            <option value="all">{t('calculators.filters.all')}</option>
            <option value="acoustic">{t('calculators.filters.acoustic')}</option>
            <option value="airflow">{t('calculators.filters.airflow')}</option>
            <option value="energy">{t('calculators.filters.energy')}</option>
          </Select>
          <IconButton aria-label={t('calculators.help')} icon={<FaQuestionCircle />} variant="secondary" />
        </Flex>

        {/* Categories and Listings */}
        <Tabs defaultIndex={0} variant="line" mb={8} maxW="container.lg" mx="auto">
          <TabList>
            <Tab>{t('calculators.tabs.all')}</Tab>
            <Tab>{t('calculators.tabs.acoustic')}</Tab>
            <Tab>{t('calculators.tabs.airflow')}</Tab>
            <Tab>{t('calculators.tabs.energy')}</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                <Card>
                  <PlaceholderCalculator />
                  <Box mt={4} textAlign="center">
                    <Text fontWeight="bold" mb={1}>Acoustic Calculator</Text>
                    <Text fontSize="sm" color="text.secondary" mb={2}>{t('calculators.levels.basic')}</Text>
                    <Link to="/calculators/acoustic">
                      <Button size="sm">{t('calculators.use')}</Button>
                    </Link>
                  </Box>
                </Card>
                <Card>
                  <PlaceholderCalculator />
                  <Box mt={4} textAlign="center">
                    <Text fontWeight="bold" mb={1}>Air Exchange Calculator</Text>
                    <Text fontSize="sm" color="text.secondary" mb={2}>{t('calculators.levels.intermediate')}</Text>
                    <Link to="/calculators/air-exchange">
                      <Button size="sm">{t('calculators.use')}</Button>
                    </Link>
                  </Box>
                </Card>
                <Card>
                  <PlaceholderCalculator />
                  <Box mt={4} textAlign="center">
                    <Text fontWeight="bold" mb={1}>Energy Efficiency Calculator</Text>
                    <Text fontSize="sm" color="text.secondary" mb={2}>{t('calculators.levels.advanced')}</Text>
                    <Link to="/calculators/energy-efficiency">
                      <Button size="sm">{t('calculators.use')}</Button>
                    </Link>
                  </Box>
                </Card>
                {/* Add more calculator cards as needed */}
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                <Card>
                  <PlaceholderCalculator />
                  <Box mt={4} textAlign="center">
                    <Text fontWeight="bold" mb={1}>Acoustic Calculator</Text>
                    <Text fontSize="sm" color="text.secondary" mb={2}>{t('calculators.levels.basic')}</Text>
                    <Link to="/calculators/acoustic">
                      <Button size="sm">{t('calculators.use')}</Button>
                    </Link>
                  </Box>
                </Card>
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                <Card>
                  <PlaceholderCalculator />
                  <Box mt={4} textAlign="center">
                    <Text fontWeight="bold" mb={1}>Air Exchange Calculator</Text>
                    <Text fontSize="sm" color="text.secondary" mb={2}>{t('calculators.levels.intermediate')}</Text>
                    <Link to="/calculators/air-exchange">
                      <Button size="sm">{t('calculators.use')}</Button>
                    </Link>
                  </Box>
                </Card>
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                <Card>
                  <PlaceholderCalculator />
                  <Box mt={4} textAlign="center">
                    <Text fontWeight="bold" mb={1}>Energy Efficiency Calculator</Text>
                    <Text fontSize="sm" color="text.secondary" mb={2}>{t('calculators.levels.advanced')}</Text>
                    <Link to="/calculators/energy-efficiency">
                      <Button size="sm">{t('calculators.use')}</Button>
                    </Link>
                  </Box>
                </Card>
              </SimpleGrid>
            </TabPanel>
          </TabPanels>
        </Tabs>

        {/* Saved Calculations */}
        <Box maxW="container.lg" mx="auto" mb={8}>
          <Heading as="h2" size="md" mb={4}>{t('calculators.saved.title')}</Heading>
          <Divider mb={4} />
          <Card>
            <VStack spacing={3} p={4} align="stretch">
              <Flex justify="space-between" align="center">
                <Box>
                  <Text fontWeight="bold">Duct Sizing - Office Project</Text>
                  <Text fontSize="sm" color="text.secondary">Saved: 2 days ago</Text>
                </Box>
                <Button size="sm" variant="secondary">{t('calculators.saved.view')}</Button>
              </Flex>
              <Flex justify="space-between" align="center">
                <Box>
                  <Text fontWeight="bold">Airflow Rate - Warehouse</Text>
                  <Text fontSize="sm" color="text.secondary">Saved: 1 week ago</Text>
                </Box>
                <Button size="sm" variant="secondary">{t('calculators.saved.view')}</Button>
              </Flex>
            </VStack>
            <Box textAlign="center" p={2}>
              <Text fontSize="sm" color="brand.primary" cursor="pointer">{t('calculators.saved.viewAll')}</Text>
            </Box>
          </Card>
        </Box>

        {/* Help Resources */}
        <Box maxW="container.lg" mx="auto">
          <Heading as="h2" size="md" mb={4}>{t('calculators.help.title')}</Heading>
          <Divider mb={4} />
          <Flex wrap="wrap" gap={4} justify="center">
            <Button leftIcon={<FaQuestionCircle />} variant="secondary" size="sm">{t('calculators.help.guide')}</Button>
            <Button leftIcon={<FaQuestionCircle />} variant="secondary" size="sm">{t('calculators.help.tutorial')}</Button>
            <Button leftIcon={<FaQuestionCircle />} variant="secondary" size="sm">{t('calculators.help.faq')}</Button>
          </Flex>
        </Box>
      </Box>
    </MainLayout>
  );
};

export default CalculatorsPage;
