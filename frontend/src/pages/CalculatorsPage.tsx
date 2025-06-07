import React, { useState } from 'react';
import { Box, Text, VStack, Heading, SimpleGrid, Flex, Input, Button, Divider, InputGroup, InputLeftElement, Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { FaCalculator, FaSearch, FaLifeRing } from 'react-icons/fa';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';
import ChakraIcon from '../components/common/ChakraIcon';

const CalculatorsPage: React.FC = () => {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');

  return (
    <MainLayout title={t('calculators')}>
      <Box p={{ base: 4, md: 8 }}>
        {/* Search and Filter */}
        <Flex direction={{ base: 'column', md: 'row' }} gap={4} mb={8} align="center" maxW="container.lg" mx="auto">
          <InputGroup flex={1}>
            <InputLeftElement pointerEvents="none">
              <ChakraIcon icon={FaSearch} color="gray.300" />
            </InputLeftElement>
            <Input 
              placeholder={t('calculators.searchPlaceholder')} 
              value={searchTerm} 
              onChange={(e) => setSearchTerm(e.target.value)}
              borderRadius="full"
              px={4}
            />
          </InputGroup>
          <Button 
            variant="outline" 
            leftIcon={<ChakraIcon icon={FaLifeRing} />} 
            borderRadius="full"
            size={{ base: 'sm', md: 'md' }}
          >
            {t('calculators.help')}
          </Button>
        </Flex>

        {/* Categorized Listings via Tabs */}
        <Box maxW="container.lg" mx="auto" mb={10}>
          <Tabs variant="soft-rounded" colorScheme="teal" size={{ base: 'sm', md: 'md' }}>
            <TabList mb={4} flexWrap={{ base: 'wrap', md: 'nowrap' }} justifyContent={{ base: 'center', md: 'flex-start' }}>
              <Tab onClick={() => setCategoryFilter('all')} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.categories.all')}</Tab>
              <Tab onClick={() => setCategoryFilter('airflow')} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.categories.airflow')}</Tab>
              <Tab onClick={() => setCategoryFilter('duct')} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.categories.duct')}</Tab>
              <Tab onClick={() => setCategoryFilter('energy')} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.categories.energy')}</Tab>
            </TabList>
            <TabPanels>
              <TabPanel p={0}>
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={{ base: 4, md: 6 }}>
                  {/* Airflow Calculators */}
                  {categoryFilter === 'all' || categoryFilter === 'airflow' ? (
                    <>
                      <Card p={{ base: 4, md: 6 }} _hover={{ boxShadow: 'md' }} transition="box-shadow 0.2s">
                        <Flex align="center" mb={3}>
                          <ChakraIcon icon={FaCalculator} color="brand.primary" mr={2} boxSize={{ base: 5, md: 6 }} />
                          <Heading as="h3" size="md">{t('calculators.items.airVelocity')}</Heading>
                        </Flex>
                        <Text mb={4} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.descriptions.airVelocity')}</Text>
                        <Link to="/calculators/air-velocity">
                          <Button variant="link" color="brand.primary" size={{ base: 'sm', md: 'md' }}>{t('calculators.use')}</Button>
                        </Link>
                      </Card>
                      <Card p={{ base: 4, md: 6 }} _hover={{ boxShadow: 'md' }} transition="box-shadow 0.2s">
                        <Flex align="center" mb={3}>
                          <ChakraIcon icon={FaCalculator} color="brand.primary" mr={2} boxSize={{ base: 5, md: 6 }} />
                          <Heading as="h3" size="md">{t('calculators.items.airflowRate')}</Heading>
                        </Flex>
                        <Text mb={4} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.descriptions.airflowRate')}</Text>
                        <Link to="/calculators/airflow-rate">
                          <Button variant="link" color="brand.primary" size={{ base: 'sm', md: 'md' }}>{t('calculators.use')}</Button>
                        </Link>
                      </Card>
                    </>
                  ) : null}

                  {/* Duct Sizing Calculators */}
                  {categoryFilter === 'all' || categoryFilter === 'duct' ? (
                    <>
                      <Card p={{ base: 4, md: 6 }} _hover={{ boxShadow: 'md' }} transition="box-shadow 0.2s">
                        <Flex align="center" mb={3}>
                          <ChakraIcon icon={FaCalculator} color="brand.primary" mr={2} boxSize={{ base: 5, md: 6 }} />
                          <Heading as="h3" size="md">{t('calculators.items.ductSize')}</Heading>
                        </Flex>
                        <Text mb={4} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.descriptions.ductSize')}</Text>
                        <Link to="/calculators/duct-size">
                          <Button variant="link" color="brand.primary" size={{ base: 'sm', md: 'md' }}>{t('calculators.use')}</Button>
                        </Link>
                      </Card>
                      <Card p={{ base: 4, md: 6 }} _hover={{ boxShadow: 'md' }} transition="box-shadow 0.2s">
                        <Flex align="center" mb={3}>
                          <ChakraIcon icon={FaCalculator} color="brand.primary" mr={2} boxSize={{ base: 5, md: 6 }} />
                          <Heading as="h3" size="md">{t('calculators.items.pressureLoss')}</Heading>
                        </Flex>
                        <Text mb={4} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.descriptions.pressureLoss')}</Text>
                        <Link to="/calculators/pressure-loss">
                          <Button variant="link" color="brand.primary" size={{ base: 'sm', md: 'md' }}>{t('calculators.use')}</Button>
                        </Link>
                      </Card>
                    </>
                  ) : null}

                  {/* Energy Efficiency Calculators */}
                  {categoryFilter === 'all' || categoryFilter === 'energy' ? (
                    <>
                      <Card p={{ base: 4, md: 6 }} _hover={{ boxShadow: 'md' }} transition="box-shadow 0.2s">
                        <Flex align="center" mb={3}>
                          <ChakraIcon icon={FaCalculator} color="brand.primary" mr={2} boxSize={{ base: 5, md: 6 }} />
                          <Heading as="h3" size="md">{t('calculators.items.energyConsumption')}</Heading>
                        </Flex>
                        <Text mb={4} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.descriptions.energyConsumption')}</Text>
                        <Link to="/calculators/energy-consumption">
                          <Button variant="link" color="brand.primary" size={{ base: 'sm', md: 'md' }}>{t('calculators.use')}</Button>
                        </Link>
                      </Card>
                      <Card p={{ base: 4, md: 6 }} _hover={{ boxShadow: 'md' }} transition="box-shadow 0.2s">
                        <Flex align="center" mb={3}>
                          <ChakraIcon icon={FaCalculator} color="brand.primary" mr={2} boxSize={{ base: 5, md: 6 }} />
                          <Heading as="h3" size="md">{t('calculators.items.heatLoad')}</Heading>
                        </Flex>
                        <Text mb={4} fontSize={{ base: 'sm', md: 'md' }}>{t('calculators.descriptions.heatLoad')}</Text>
                        <Link to="/calculators/heat-load">
                          <Button variant="link" color="brand.primary" size={{ base: 'sm', md: 'md' }}>{t('calculators.use')}</Button>
                        </Link>
                      </Card>
                    </>
                  ) : null}
                </SimpleGrid>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Box>

        {/* Saved Calculations Section */}
        <Box maxW="container.lg" mx="auto" mb={10}>
          <Heading as="h2" size="md" mb={4}>{t('calculators.saved.title')}</Heading>
          <Divider mb={4} />
          <VStack spacing={3} align="stretch">
            <Card p={{ base: 3, md: 4 }}>
              <Text fontWeight="bold">Duct Sizing - Office Project</Text>
              <Text fontSize="sm" color="text.secondary">Saved: 1 day ago</Text>
            </Card>
            <Card p={{ base: 3, md: 4 }}>
              <Text fontWeight="bold">Airflow Rate - Warehouse</Text>
              <Text fontSize="sm" color="text.secondary">Saved: 5 days ago</Text>
            </Card>
            <Card p={{ base: 3, md: 4 }}>
              <Text fontWeight="bold">Energy Efficiency - Residential</Text>
              <Text fontSize="sm" color="text.secondary">Saved: 2 weeks ago</Text>
            </Card>
            <Link to="/saved-calculations" style={{ textAlign: 'center' }}>
              <Text fontSize="sm" color="brand.primary">{t('calculators.saved.viewAll')}</Text>
            </Link>
          </VStack>
        </Box>

        {/* Help Resources */}
        <Box maxW="container.lg" mx="auto">
          <Heading as="h2" size="md" mb={4}>{t('calculators.resources.title')}</Heading>
          <Divider mb={4} />
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={{ base: 4, md: 6 }}>
            <Card p={{ base: 3, md: 4 }}>
              <Heading as="h3" size="sm" mb={2}>{t('calculators.resources.guides')}</Heading>
              <Link to="/guides">
                <Text fontSize="sm" color="brand.primary">{t('calculators.resources.viewGuides')}</Text>
              </Link>
            </Card>
            <Card p={{ base: 3, md: 4 }}>
              <Heading as="h3" size="sm" mb={2}>{t('calculators.resources.faq')}</Heading>
              <Link to="/faq">
                <Text fontSize="sm" color="brand.primary">{t('calculators.resources.viewFaq')}</Text>
              </Link>
            </Card>
          </SimpleGrid>
        </Box>
      </Box>
    </MainLayout>
  );
};

export default CalculatorsPage;
