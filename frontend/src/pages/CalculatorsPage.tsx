import React from 'react';
import { Box, Text, VStack, SimpleGrid } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import PlaceholderCalculator from '../components/calculators/PlaceholderCalculator';

const CalculatorsPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <MainLayout title={t('calculators')}>
      <VStack spacing={6} align="center" mt={6}>
        <Text fontSize="2xl" fontWeight="bold">{t('calculators')}</Text>
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} maxW="container.lg">
          <Card>
            <PlaceholderCalculator />
            <Box mt={4} textAlign="center">
              <Link to="/calculators/acoustic">
                <Button size="sm">Acoustic Calculator</Button>
              </Link>
            </Box>
          </Card>
          <Card>
            <PlaceholderCalculator />
            <Box mt={4} textAlign="center">
              <Link to="/calculators/air-exchange">
                <Button size="sm">Air Exchange Calculator</Button>
              </Link>
            </Box>
          </Card>
          {/* Add more calculator cards as needed */}
        </SimpleGrid>
      </VStack>
    </MainLayout>
  );
};

export default CalculatorsPage;
