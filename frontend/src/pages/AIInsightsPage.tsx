import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Box, Heading, Text, VStack, Spinner, useToast } from '@chakra-ui/react';
import VentApiClient from '../api/VentApiClient';

interface AIInsight {
  id: number;
  title: string;
  description: string;
  event_type: string;
  created_at: string;
  data: Record<string, any>;
}

const AIInsightsPage: React.FC = () => {
  const { t } = useTranslation();
  const toast = useToast();
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        setLoading(true);
        const client = new VentApiClient();
        const response = await client.request('GET', '/api/ai/insights/');
        setInsights(response.data);
      } catch (err: unknown) {
        setError(t('aiInsights.fetchError'));
        toast({
          title: t('aiInsights.fetchErrorTitle'),
          description: t('aiInsights.fetchError'),
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        if (err instanceof Error) {
          console.error('Error fetching AI insights:', err.message);
        } else {
          console.error('Unexpected error fetching AI insights:', err);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, [t, toast]);

  if (loading) {
    return (
      <Box p={6} maxW="container.xl" mx="auto">
        <Spinner size="xl" />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={6} maxW="container.xl" mx="auto">
        <Text color="red.500">{error}</Text>
      </Box>
    );
  }

  return (
    <Box p={6} maxW="container.xl" mx="auto">
      <Heading as="h1" mb={6}>{t('aiInsights.title')}</Heading>
      <VStack spacing={4} align="stretch">
        {insights.length === 0 ? (
          <Text>{t('aiInsights.noInsights')}</Text>
        ) : (
          insights.map((insight) => (
            <Box key={insight.id} p={4} borderWidth={1} borderRadius={8} boxShadow="sm">
              <Heading as="h3" size="md">{insight.title}</Heading>
              <Text mt={2}>{insight.description}</Text>
              <Text mt={2} fontSize="sm" color="gray.500">
                {t('aiInsights.eventType')}: {insight.event_type}
              </Text>
              <Text fontSize="sm" color="gray.500">
                {t('aiInsights.createdAt')}: {new Date(insight.created_at).toLocaleString()}
              </Text>
            </Box>
          ))
        )}
      </VStack>
    </Box>
  );
};

export default AIInsightsPage;
