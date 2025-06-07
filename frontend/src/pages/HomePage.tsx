import React from 'react';
import { Box, Text, VStack, Button, Heading, Image, SimpleGrid, Flex } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { FaCalculator, FaChartLine, FaLightbulb, FaRocket } from 'react-icons/fa';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';
import ChakraIcon from '../components/common/ChakraIcon';

const HomePage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <MainLayout title={t('welcome')}>
      {/* Hero Section */}
      <Box bg="background.light" pt={{ base: 12, md: 20 }} pb={{ base: 12, md: 20 }} textAlign="center" px={{ base: 4, md: 0 }}>
        <Heading as="h1" size={{ base: '2xl', md: '3xl' }} mb={4} color="brand.primary" fontWeight="extrabold">{t('ventai.hero.title')}</Heading>
        <Text fontSize={{ base: 'lg', md: 'xl' }} maxW={{ base: '90%', md: 'container.md' }} mx="auto" mb={8} color="text.secondary" lineHeight="tall">{t('ventai.hero.subtitle')}</Text>
        <Flex justify="center" gap={4} wrap="wrap" mb={6}>
          <Link to="/calculators">
            <Button variant="primary" size={{ base: 'md', md: 'lg' }} leftIcon={<ChakraIcon icon={FaCalculator} />}>{t('ventai.hero.cta')}</Button>
          </Link>
          <Link to="/projects">
            <Button variant="outline" size={{ base: 'md', md: 'lg' }} leftIcon={<ChakraIcon icon={FaRocket} />}>{t('ventai.hero.secondaryCta')}</Button>
          </Link>
        </Flex>
        <Image src="/assets/hero-ventilation.svg" alt={t('ventai.hero.imageAlt')} maxH={{ base: '300px', md: '450px' }} mt={{ base: 6, md: 10 }} mx="auto" borderRadius="lg" boxShadow="lg" />
      </Box>

      {/* Capabilities Overview */}
      <Box py={{ base: 12, md: 20 }} px={{ base: 4, md: 8 }} bg="white">
        <Heading as="h2" size={{ base: 'lg', md: 'xl' }} textAlign="center" mb={{ base: 8, md: 12 }} color="brand.dark" fontWeight="bold">{t('ventai.capabilities.title')}</Heading>
        <Text fontSize={{ base: 'md', md: 'lg' }} textAlign="center" maxW="container.md" mx="auto" mb={{ base: 8, md: 12 }} color="text.secondary">{t('ventai.capabilities.subtitle')}</Text>
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={{ base: 6, md: 8 }} maxW="container.lg" mx="auto">
          <Card p={{ base: 6, md: 8 }} textAlign="center" boxShadow="md" _hover={{ boxShadow: 'lg', transform: 'translateY(-5px)' }} transition="all 0.3s ease">
            <ChakraIcon icon={FaCalculator} boxSize={{ base: 10, md: 12 }} color="brand.primary" mb={4} />
            <Heading as="h3" size="md" mb={3} color="brand.dark">{t('ventai.capabilities.calculators.title')}</Heading>
            <Text fontSize={{ base: 'sm', md: 'md' }} color="text.secondary">{t('ventai.capabilities.calculators.description')}</Text>
          </Card>
          <Card p={{ base: 6, md: 8 }} textAlign="center" boxShadow="md" _hover={{ boxShadow: 'lg', transform: 'translateY(-5px)' }} transition="all 0.3s ease">
            <ChakraIcon icon={FaChartLine} boxSize={{ base: 10, md: 12 }} color="brand.primary" mb={4} />
            <Heading as="h3" size="md" mb={3} color="brand.dark">{t('ventai.capabilities.dashboard.title')}</Heading>
            <Text fontSize={{ base: 'sm', md: 'md' }} color="text.secondary">{t('ventai.capabilities.dashboard.description')}</Text>
          </Card>
          <Card p={{ base: 6, md: 8 }} textAlign="center" boxShadow="md" _hover={{ boxShadow: 'lg', transform: 'translateY(-5px)' }} transition="all 0.3s ease">
            <ChakraIcon icon={FaLightbulb} boxSize={{ base: 10, md: 12 }} color="brand.primary" mb={4} />
            <Heading as="h3" size="md" mb={3} color="brand.dark">{t('ventai.capabilities.aiInsights.title')}</Heading>
            <Text fontSize={{ base: 'sm', md: 'md' }} color="text.secondary">{t('ventai.capabilities.aiInsights.description')}</Text>
          </Card>
        </SimpleGrid>
        <Flex justify="center" mt={{ base: 8, md: 12 }}>
          <Link to="/capabilities">
            <Button variant="link" color="brand.primary" size={{ base: 'md', md: 'lg' }}>{t('ventai.capabilities.exploreMore')}</Button>
          </Link>
        </Flex>
      </Box>

      {/* Guided Onboarding */}
      <Box py={{ base: 12, md: 20 }} bg="brand.primaryLight" textAlign="center" px={{ base: 4, md: 0 }}>
        <Heading as="h2" size={{ base: 'lg', md: 'xl' }} mb={6} color="brand.dark" fontWeight="bold">{t('ventai.onboarding.title')}</Heading>
        <Text fontSize={{ base: 'md', md: 'lg' }} maxW={{ base: '90%', md: 'container.md' }} mx="auto" mb={8} color="text.secondary">{t('ventai.onboarding.subtitle')}</Text>
        <Link to="/onboarding">
          <Button variant="primary" size={{ base: 'md', md: 'lg' }} leftIcon={<ChakraIcon icon={FaRocket} />}>{t('ventai.onboarding.cta')}</Button>
        </Link>
      </Box>

      {/* Testimonials Section */}
      <Box py={{ base: 12, md: 20 }} bg="white" textAlign="center" px={{ base: 4, md: 8 }}>
        <Heading as="h2" size={{ base: 'lg', md: 'xl' }} mb={8} color="brand.dark" fontWeight="bold">{t('ventai.testimonials.title')}</Heading>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={{ base: 6, md: 8 }} maxW="container.lg" mx="auto">
          <Card p={{ base: 6, md: 8 }} boxShadow="md">
            <Text fontSize={{ base: 'md', md: 'lg' }} mb={4} fontStyle="italic" color="text.secondary">"{t('ventai.testimonials.quote1')}"</Text>
            <Text fontWeight="bold" color="brand.dark">- {t('ventai.testimonials.author1')}</Text>
          </Card>
          <Card p={{ base: 6, md: 8 }} boxShadow="md">
            <Text fontSize={{ base: 'md', md: 'lg' }} mb={4} fontStyle="italic" color="text.secondary">"{t('ventai.testimonials.quote2')}"</Text>
            <Text fontWeight="bold" color="brand.dark">- {t('ventai.testimonials.author2')}</Text>
          </Card>
        </SimpleGrid>
      </Box>

      {/* Call to Action Section */}
      <Box py={{ base: 12, md: 20 }} bg="background.light" textAlign="center" px={{ base: 4, md: 0 }}>
        <Heading as="h2" size={{ base: 'lg', md: 'xl' }} mb={6} color="brand.dark" fontWeight="bold">{t('ventai.cta.title')}</Heading>
        <Text fontSize={{ base: 'md', md: 'lg' }} maxW={{ base: '90%', md: 'container.md' }} mx="auto" mb={8} color="text.secondary">{t('ventai.cta.subtitle')}</Text>
        <Link to="/signup">
          <Button variant="primary" size={{ base: 'md', md: 'lg' }} leftIcon={<ChakraIcon icon={FaRocket} />}>{t('ventai.cta.button')}</Button>
        </Link>
      </Box>

      {/* Footer Section (Handled by MainLayout, but placeholder for custom content if needed) */}
      <Box py={{ base: 6, md: 10 }} textAlign="center" bg="white" borderTop="1px solid" borderColor="gray.200">
        <Text fontSize="sm" color="text.secondary">{t('ventai.footer.copyright')}</Text>
      </Box>
    </MainLayout>
  );
};

export default HomePage;
