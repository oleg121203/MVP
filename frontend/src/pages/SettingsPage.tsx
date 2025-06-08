import React, { useState, useEffect } from 'react';
import { Box, Heading, Button, VStack, Input, Text, useToast } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { apiClient } from '../api/client';

const SettingsPage: React.FC = () => {
  const { t } = useTranslation();
  const toast = useToast();
  const [userData, setUserData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const response = await apiClient.request<any>('/api/auth/me/', 'GET');
      setUserData(response.data);
      setFirstName(response.data.first_name || '');
      setLastName(response.data.last_name || '');
      setEmail(response.data.email || '');
      setPhone(response.data.profile?.phone || '');
      setLoading(false);
    } catch (err) {
      setError(t('settings.fetchError'));
      setLoading(false);
    }
  };

  const handleSaveChanges = async () => {
    try {
      const updatedData = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        profile: {
          phone: phone,
        },
      };
      await apiClient.request('/api/auth/me/', 'PATCH', updatedData);
      toast({
        title: t('settings.updateSuccess'),
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      fetchUserData();
    } catch (err: any) {
      toast({
        title: t('settings.updateError'),
        description: err.message || t('settings.unknownError'),
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (loading) {
    return <Box>{t('settings.loading')}</Box>;
  }

  if (error) {
    return (
      <Box>
        <Text color="red.500">{error}</Text>
        <Button onClick={fetchUserData} mt={4}>{t('settings.retry')}</Button>
      </Box>
    );
  }

  return (
    <Box p={6}>
      <Heading mb={6}>{t('settings.title')}</Heading>
      <VStack spacing={4} align="stretch" maxW="500px">
        <Box>
          <Text mb={2}>{t('settings.firstName')}</Text>
          <Input
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder={t('settings.firstNamePlaceholder')}
          />
        </Box>
        <Box>
          <Text mb={2}>{t('settings.lastName')}</Text>
          <Input
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            placeholder={t('settings.lastNamePlaceholder')}
          />
        </Box>
        <Box>
          <Text mb={2}>{t('settings.email')}</Text>
          <Input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder={t('settings.emailPlaceholder')}
          />
        </Box>
        <Box>
          <Text mb={2}>{t('settings.phone')}</Text>
          <Input
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder={t('settings.phonePlaceholder')}
          />
        </Box>
        <Button
          colorScheme="blue"
          onClick={handleSaveChanges}
          mt={4}
        >
          {t('settings.saveChanges')}
        </Button>
      </VStack>
    </Box>
  );
};

export default SettingsPage;
