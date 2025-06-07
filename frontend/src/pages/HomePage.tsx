import React from 'react';
import { Box, Text, VStack, Button } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';

const HomePage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <MainLayout title={t('welcome')}>
      <VStack spacing={6} align="center" mt={10}>
        <Card maxW="container.md">
          <VStack spacing={4} align="center">
            <Text fontSize="2xl" fontWeight="bold">{t('welcome')}</Text>
            <Text>Explore our ventilation solutions and AI-powered tools.</Text>
            <Box>
              <Link to="/calculators">
                <Button colorScheme="teal">{t('calculators')}</Button>
              </Link>
              <Link to="/dashboard" style={{ marginLeft: '10px' }}>
                <Button colorScheme="teal" variant="outline">{t('dashboard')}</Button>
              </Link>
            </Box>
          </VStack>
        </Card>
      </VStack>
    </MainLayout>
  );
};

export default HomePage;
