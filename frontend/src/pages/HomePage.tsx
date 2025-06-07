import React from 'react';
import { Box, Text, VStack, Button, Heading, Image, SimpleGrid, Icon } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { FaCalculator, FaChartLine, FaLightbulb } from 'react-icons/fa';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';

const HomePage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <MainLayout title={t('welcome')}>
      {/* Hero Section */}
      <Box bg="background.light" pt={16} pb={20} textAlign="center">
        <Heading as="h1" size="2xl" mb={4} color="brand.primary">{t('ventai.hero.title')}</Heading>
        <Text fontSize="xl" maxW="container.md" mx="auto" mb={8}>{t('ventai.hero.subtitle')}</Text>
        <Link to="/calculators">
          <Button variant="primary" size="lg">{t('ventai.hero.cta')}</Button>
        </Link>
        <Image src="/path/to/hero-image.svg" alt={t('ventai.hero.imageAlt')} maxH="400px" mt={10} mx="auto" />
      </Box>

      {/* Capabilities Overview */}
      <Box py={16} px={{ base: 4, md: 8 }} bg="white">
        <Heading as="h2" size="xl" textAlign="center" mb={12}>{t('ventai.capabilities.title')}</Heading>
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} maxW="container.lg" mx="auto">
          <Card p={6} textAlign="center">
            <Icon as={FaCalculator} boxSize={10} color="brand.primary" mb={4} />
            <Heading as="h3" size="md" mb={2}>{t('ventai.capabilities.calculators.title')}</Heading>
            <Text>{t('ventai.capabilities.calculators.description')}</Text>
          </Card>
          <Card p={6} textAlign="center">
            <Icon as={FaChartLine} boxSize={10} color="brand.primary" mb={4} />
            <Heading as="h3" size="md" mb={2}>{t('ventai.capabilities.dashboard.title')}</Heading>
            <Text>{t('ventai.capabilities.dashboard.description')}</Text>
          </Card>
          <Card p={6} textAlign="center">
            <Icon as={FaLightbulb} boxSize={10} color="brand.primary" mb={4} />
            <Heading as="h3" size="md" mb={2}>{t('ventai.capabilities.aiInsights.title')}</Heading>
            <Text>{t('ventai.capabilities.aiInsights.description')}</Text>
          </Card>
        </SimpleGrid>
      </Box>

      {/* Guided Onboarding */}
      <Box py={16} bg="background.light" textAlign="center">
        <Heading as="h2" size="xl" mb={6}>{t('ventai.onboarding.title')}</Heading>
        <Text fontSize="lg" maxW="container.md" mx="auto" mb={8}>{t('ventai.onboarding.subtitle')}</Text>
        <Link to="/onboarding">
          <Button variant="primary" size="md">{t('ventai.onboarding.cta')}</Button>
        </Link>
      </Box>

      {/* Footer Section (Handled by MainLayout, but placeholder for custom content if needed) */}
      <Box py={10} textAlign="center" bg="white" borderTop="1px solid" borderColor="gray.200">
        <Text fontSize="sm" color="text.secondary">{t('ventai.footer.copyright')}</Text>
      </Box>
    </MainLayout>
  );
};

export default HomePage;
