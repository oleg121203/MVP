import React from 'react';
import { Box, Text, VStack } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import MainLayout from '../layouts/MainLayout';
import PlaceholderDashboard from '../components/dashboard/PlaceholderDashboard';

const DashboardPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <MainLayout title={t('dashboard')}>
      <VStack spacing={6} align="center" mt={6}>
        <Text fontSize="2xl" fontWeight="bold">{t('dashboard')}</Text>
        <Box maxW="container.lg" w="full">
          <PlaceholderDashboard />
        </Box>
      </VStack>
    </MainLayout>
  );
};

export default DashboardPage;
