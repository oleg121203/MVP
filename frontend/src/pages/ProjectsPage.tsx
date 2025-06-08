import React, { useState, useEffect } from 'react';
import { Box, Heading, Button, VStack, HStack, Text, Input, Modal, ModalOverlay, ModalContent, ModalHeader, ModalFooter, ModalBody, ModalCloseButton, useDisclosure } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { apiClient } from '../api/client';

const ProjectsPage: React.FC = () => {
  const { t } = useTranslation();
  const [projects, setProjects] = useState<any[]>([]);
  const [newProjectTitle, setNewProjectTitle] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isOpen, onOpen, onClose } = useDisclosure();

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await apiClient.request<any>('/api/projects/', 'GET');
      setProjects(response.data);
      setLoading(false);
    } catch (err) {
      setError(t('projects.fetchError'));
      setLoading(false);
    }
  };

  const handleCreateProject = async () => {
    try {
      const newProject = {
        title: newProjectTitle,
        description: newProjectDescription,
      };
      await apiClient.request('/api/projects/', 'POST', newProject);
      setNewProjectTitle('');
      setNewProjectDescription('');
      onClose();
      fetchProjects();
    } catch (err) {
      setError(t('projects.createError'));
    }
  };

  if (loading) {
    return <Box>{t('projects.loading')}</Box>;
  }

  if (error) {
    return (
      <Box>
        <Text color="red.500">{error}</Text>
        <Button onClick={fetchProjects} mt={4}>{t('projects.retry')}</Button>
      </Box>
    );
  }

  return (
    <Box p={6}>
      <Heading mb={6}>{t('projects.title')}</Heading>
      <Button colorScheme="blue" onClick={onOpen} mb={4}>{t('projects.createNew')}</Button>
      
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{t('projects.newProject')}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Input
              placeholder={t('projects.titlePlaceholder')}
              value={newProjectTitle}
              onChange={(e) => setNewProjectTitle(e.target.value)}
              mb={3}
            />
            <Input
              placeholder={t('projects.descriptionPlaceholder')}
              value={newProjectDescription}
              onChange={(e) => setNewProjectDescription(e.target.value)}
            />
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={handleCreateProject}>
              {t('projects.create')}
            </Button>
            <Button variant="ghost" onClick={onClose}>{t('projects.cancel')}</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {projects.length === 0 ? (
        <Text>{t('projects.noProjects')}</Text>
      ) : (
        <VStack spacing={4} align="stretch">
          {projects.map((project) => (
            <Box key={project.id} p={4} borderWidth="1px" borderRadius="md">
              <HStack justifyContent="space-between">
                <Heading size="md">{project.title}</Heading>
                <Text fontSize="sm" color="gray.500">{new Date(project.created_at).toLocaleDateString()}</Text>
              </HStack>
              <Text mt={2}>{project.description || t('projects.noDescription')}</Text>
              <HStack mt={3} spacing={2}>
                <Button size="sm" variant="outline">{t('projects.view')}</Button>
                <Button size="sm" variant="outline">{t('projects.edit')}</Button>
                <Button size="sm" variant="outline" colorScheme="red">{t('projects.delete')}</Button>
              </HStack>
            </Box>
          ))}
        </VStack>
      )}
    </Box>
  );
};

export default ProjectsPage;
