import React, { useState, useEffect } from 'react';
import { Box, Heading, Button, VStack, HStack, Text, useToast } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { apiClient } from '../api/client';
import { useAuth } from '../context/AuthContext';

const ProjectManagementPage: React.FC = () => {
  const { t } = useTranslation();
  const toast = useToast();
  const auth = useAuth(); 
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is admin by attempting to fetch projects
    // If not admin, the backend will return an error or empty list
    fetchProjects();
  }, [t]);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await apiClient.request<any>('/api/projects/', 'GET');
      setProjects(response.data);
      setLoading(false);
    } catch (err) {
      setError(t('projectManagement.fetchError'));
      setLoading(false);
    }
  };

  const handleDeleteProject = async (projectId: string) => {
    try {
      await apiClient.request(`/api/projects/${projectId}/`, 'DELETE');
      toast({
        title: t('projectManagement.deleteSuccess'),
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      fetchProjects();
    } catch (err: any) {
      toast({
        title: t('projectManagement.deleteError'),
        description: err.message || t('projectManagement.unknownError'),
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (loading) {
    return <Box>{t('projectManagement.loading')}</Box>;
  }

  if (error) {
    return (
      <Box>
        <Text color="red.500">{error}</Text>
        {error !== t('projectManagement.accessDenied') && (
          <Button onClick={fetchProjects} mt={4}>{t('projectManagement.retry')}</Button>
        )}
      </Box>
    );
  }

  return (
    <Box p={6}>
      <Heading mb={6}>{t('projectManagement.title')}</Heading>
      {projects.length === 0 ? (
        <Text>{t('projectManagement.noProjects')}</Text>
      ) : (
        <VStack spacing={4} align="stretch">
          {projects.map((project) => (
            <Box key={project.id} p={4} borderWidth="1px" borderRadius="md">
              <HStack justifyContent="space-between">
                <Heading size="md">{project.title}</Heading>
                <Text fontSize="sm" color="gray.500">Owner: {project.owner}</Text>
              </HStack>
              <Text mt={2}>{project.description || t('projectManagement.noDescription')}</Text>
              <HStack mt={3} spacing={2}>
                <Button size="sm" variant="outline">{t('projectManagement.view')}</Button>
                <Button size="sm" variant="outline">{t('projectManagement.edit')}</Button>
                <Button 
                  size="sm" 
                  variant="outline" 
                  colorScheme="red"
                  onClick={() => handleDeleteProject(project.id)}
                >
                  {t('projectManagement.delete')}
                </Button>
              </HStack>
            </Box>
          ))}
        </VStack>
      )}
    </Box>
  );
};

export default ProjectManagementPage;
