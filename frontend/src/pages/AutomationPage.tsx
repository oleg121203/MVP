import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Box, Heading, Button, VStack, Spinner, useToast, Table, Thead, Tbody, Tr, Th, Td, Text } from '@chakra-ui/react';
import VentApiClient from '../api/VentApiClient';

interface AutomationRule {
  id: number;
  name: string;
  description: string;
  trigger_type: string;
  action_type: string;
  is_active: boolean;
  created_at: string;
}

const AutomationPage: React.FC = () => {
  const { t } = useTranslation();
  const toast = useToast();
  const [rules, setRules] = useState<AutomationRule[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRules = async () => {
      try {
        setLoading(true);
        const client = new VentApiClient();
        const response = await client.request('GET', '/api/automation/rules/');
        setRules(response.data);
      } catch (err: unknown) {
        setError(t('automation.fetchError'));
        toast({
          title: t('automation.fetchErrorTitle'),
          description: t('automation.fetchError'),
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        if (err instanceof Error) {
          console.error('Error fetching automation rules:', err.message);
        } else {
          console.error('Unexpected error fetching automation rules:', err);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchRules();
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
      <Heading as="h1" mb={6}>{t('automation.title')}</Heading>
      
      <Button colorScheme="blue" mb={6}>
        {t('automation.createNewRule')}
      </Button>
      
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>{t('automation.name')}</Th>
            <Th>{t('automation.trigger')}</Th>
            <Th>{t('automation.action')}</Th>
            <Th>{t('automation.status')}</Th>
            <Th>{t('automation.created')}</Th>
            <Th>{t('automation.actions')}</Th>
          </Tr>
        </Thead>
        <Tbody>
          {rules.length === 0 ? (
            <Tr>
              <Td colSpan={6} textAlign="center">{t('automation.noRules')}</Td>
            </Tr>
          ) : (
            rules.map((rule) => (
              <Tr key={rule.id}>
                <Td>{rule.name}</Td>
                <Td>{rule.trigger_type}</Td>
                <Td>{rule.action_type}</Td>
                <Td>{rule.is_active ? t('automation.active') : t('automation.inactive')}</Td>
                <Td>{new Date(rule.created_at).toLocaleDateString()}</Td>
                <Td>
                  <Button size="sm" mr={2}>{t('automation.edit')}</Button>
                  <Button size="sm" colorScheme="red">{t('automation.delete')}</Button>
                </Td>
              </Tr>
            ))
          )}
        </Tbody>
      </Table>
    </Box>
  );
};

export default AutomationPage;
