import React, { useState } from 'react';
import { Box, Text, VStack, Heading, SimpleGrid, Flex, Button, Divider, Icon, Avatar, AvatarGroup, Input, Modal, ModalOverlay, ModalContent, ModalHeader, ModalFooter, ModalBody, ModalCloseButton, useDisclosure, Select, FormControl, FormLabel, Textarea } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { FaFolder, FaPlus, FaEdit, FaShareAlt, FaFileExport, FaComment, FaFilter } from 'react-icons/fa';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';

const ProjectManagementPage: React.FC = () => {
  const { t } = useTranslation();
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const { isOpen, onOpen, onClose } = useDisclosure();

  // Placeholder project data
  const projects = [
    { id: '1', name: 'Office Ventilation', updated: '2 days ago', status: 'In Progress' },
    { id: '2', name: 'Warehouse Airflow', updated: '1 week ago', status: 'Completed' },
    { id: '3', name: 'Residential HVAC', updated: '3 weeks ago', status: 'In Progress' },
  ];

  const filteredProjects = filterStatus === 'all' ? projects : projects.filter(p => p.status === filterStatus);

  const handleProjectSelect = (projectId: string) => {
    setSelectedProject(projectId);
  };

  return (
    <MainLayout title={t('projectManagement')}>
      <Box p={{ base: 4, md: 8 }}>
        {/* Header Section */}
        <Heading as="h1" size={{ base: 'lg', md: 'xl' }} mb={2}>{t('projectManagement.welcome')}</Heading>
        <Text fontSize={{ base: 'md', md: 'lg' }} color="text.secondary" mb={6}>{t('projectManagement.subtitle')}</Text>
        <Button leftIcon={<FaPlus />} variant="primary" mb={6} onClick={onOpen} size={{ base: 'sm', md: 'md' }}>{t('projectManagement.createNew')}</Button>

        {/* Main Content Area */}
        <Flex direction={{ base: 'column', md: 'row' }} gap={6} mb={8}>
          {/* Sidebar (Left Panel) */}
          <Box w={{ base: 'full', md: '250px' }} mb={{ base: 4, md: 0 }}>
            <Flex justify="space-between" align="center" mb={4}>
              <Heading as="h2" size="md">{t('projectManagement.projects.title')}</Heading>
              <Button leftIcon={<FaFilter />} variant="outline" size="sm" onClick={() => { /* Filter toggle logic */ }}>{t('projectManagement.projects.filter')}</Button>
            </Flex>
            <Divider mb={4} />
            <Box mb={4}>
              <Select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} size={{ base: 'sm', md: 'md' }}>
                <option value="all">{t('projectManagement.filters.all')}</option>
                <option value="In Progress">{t('projectManagement.filters.inProgress')}</option>
                <option value="Completed">{t('projectManagement.filters.completed')}</option>
              </Select>
            </Box>
            <VStack spacing={3} align="stretch" maxH={{ base: '300px', md: '500px' }} overflowY="auto">
              {filteredProjects.map(project => (
                <Card 
                  key={project.id} 
                  p={3} 
                  cursor="pointer" 
                  onClick={() => handleProjectSelect(project.id)}
                  bg={selectedProject === project.id ? 'brand.primaryLight' : 'white'}
                  borderColor={selectedProject === project.id ? 'brand.primary' : 'gray.200'}
                  borderWidth={selectedProject === project.id ? '2px' : '1px'}
                  _hover={{ boxShadow: 'md' }}
                >
                  <Text fontWeight="bold">{project.name}</Text>
                  <Text fontSize="sm" color="text.secondary">Updated: {project.updated}</Text>
                  <Text fontSize="xs" color={project.status === 'In Progress' ? 'orange.500' : 'green.500'}>{project.status}</Text>
                  <Flex justify="space-between" mt={2}>
                    <Link to={`/projects/${project.id}`}>
                      <Text fontSize="xs" color="brand.primary">{t('projectManagement.projects.viewDetails')}</Text>
                    </Link>
                    <Link to={`/projects/${project.id}/edit`}>
                      <Text fontSize="xs" color="brand.primary">{t('projectManagement.projects.edit')}</Text>
                    </Link>
                  </Flex>
                </Card>
              ))}
            </VStack>
          </Box>

          {/* Main Content Area (Right Panel) */}
          <Box flex={1}>
            {selectedProject ? (
              <>
                <Heading as="h2" size="md" mb={4}>{projects.find(p => p.id === selectedProject)?.name}</Heading>
                <Divider mb={4} />
                <Text fontSize="sm" color="text.secondary" mb={2}>Created: 1 month ago | Last Updated: {projects.find(p => p.id === selectedProject)?.updated}</Text>
                <Text fontSize="sm" color={projects.find(p => p.id === selectedProject)?.status === 'In Progress' ? 'orange.500' : 'green.500'} mb={4}>
                  Status: {projects.find(p => p.id === selectedProject)?.status}
                </Text>

                {/* Key Metrics */}
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4} mb={6}>
                  <Card p={4} textAlign="center">
                    <Heading as="h3" size="sm" mb={2}>{t('projectManagement.metrics.calculations')}</Heading>
                    <Text fontSize="xl" fontWeight="bold">5</Text>
                  </Card>
                  <Card p={4} textAlign="center">
                    <Heading as="h3" size="sm" mb={2}>{t('projectManagement.metrics.completion')}</Heading>
                    <Text fontSize="xl" fontWeight="bold">60%</Text>
                  </Card>
                  <Card p={4} textAlign="center">
                    <Heading as="h3" size="sm" mb={2}>{t('projectManagement.metrics.team')}</Heading>
                    <Text fontSize="xl" fontWeight="bold">3</Text>
                  </Card>
                </SimpleGrid>

                {/* Recent Activity */}
                <Heading as="h3" size="sm" mb={3}>{t('projectManagement.recentActivity.title')}</Heading>
                <Divider mb={3} />
                <VStack spacing={3} align="stretch" mb={6}>
                  <Card p={3}>
                    <Text fontSize="sm">Duct Calculation added by User X - 2 hours ago</Text>
                  </Card>
                  <Card p={3}>
                    <Text fontSize="sm">Project status updated to In Progress - 1 day ago</Text>
                  </Card>
                </VStack>

                {/* Quick Links */}
                <Heading as="h3" size="sm" mb={3}>{t('projectManagement.quickLinks.title')}</Heading>
                <Divider mb={3} />
                <Flex wrap="wrap" gap={3}>
                  <Link to={`/projects/${selectedProject}/calculations`}>
                    <Button variant="outline" size={{ base: 'sm', md: 'md' }}>{t('projectManagement.quickLinks.calculations')}</Button>
                  </Link>
                  <Link to={`/projects/${selectedProject}/designs`}>
                    <Button variant="outline" size={{ base: 'sm', md: 'md' }}>{t('projectManagement.quickLinks.designs')}</Button>
                  </Link>
                  <Link to={`/projects/${selectedProject}/documents`}>
                    <Button variant="outline" size={{ base: 'sm', md: 'md' }}>{t('projectManagement.quickLinks.documents')}</Button>
                  </Link>
                  <Link to={`/projects/${selectedProject}/settings`}>
                    <Button variant="outline" size={{ base: 'sm', md: 'md' }}>{t('projectManagement.quickLinks.settings')}</Button>
                  </Link>
                </Flex>
              </>
            ) : (
              <Box textAlign="center" p={{ base: 6, md: 10 }}>
                <Heading as="h2" size="md" mb={4}>{t('projectManagement.noProjectSelected.title')}</Heading>
                <Text mb={4}>{t('projectManagement.noProjectSelected.message')}</Text>
                <Button leftIcon={<FaPlus />} variant="primary" onClick={onOpen}>{t('projectManagement.createNew')}</Button>
              </Box>
            )}
          </Box>

          {/* Collaboration & Sharing Sidebar */}
          {selectedProject && (
            <Box w={{ base: 'full', md: '300px' }}>
              <Heading as="h2" size="md" mb={4}>{t('projectManagement.collaboration.title')}</Heading>
              <Divider mb={4} />
              <Card mb={6}>
                <Heading as="h3" size="sm" mb={3}>{t('projectManagement.collaboration.team')}</Heading>
                <AvatarGroup size="md" max={3} mb={3}>
                  <Avatar name="User 1" src="https://bit.ly/ryan-florence" />
                  <Avatar name="User 2" src="https://bit.ly/sage-adebayo" />
                  <Avatar name="User 3" src="https://bit.ly/kent-brockman" />
                </AvatarGroup>
                <Button variant="link" color="brand.primary" size="sm" mb={3}>{t('projectManagement.collaboration.invite')}</Button>
                <Heading as="h3" size="sm" mb={2}>{t('projectManagement.collaboration.share')}</Heading>
                <Flex wrap="wrap" gap={2} mb={3}>
                  <Button leftIcon={<FaFileExport />} variant="outline" size="sm">{t('projectManagement.collaboration.export')}</Button>
                  <Button leftIcon={<FaShareAlt />} variant="outline" size="sm">{t('projectManagement.collaboration.link')}</Button>
                </Flex>
                <Heading as="h3" size="sm" mb={2}>{t('projectManagement.collaboration.comments')}</Heading>
                <Button leftIcon={<FaComment />} variant="outline" size="sm">{t('projectManagement.collaboration.viewComments')}</Button>
              </Card>
            </Box>
          )}
        </Flex>
      </Box>

      {/* Create New Project Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size={{ base: 'full', md: 'md' }}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{t('projectManagement.createModal.title')}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <FormControl mb={4}>
              <FormLabel>{t('projectManagement.createModal.name')}</FormLabel>
              <Input placeholder={t('projectManagement.createModal.namePlaceholder')} />
            </FormControl>
            <FormControl mb={4}>
              <FormLabel>{t('projectManagement.createModal.description')}</FormLabel>
              <Textarea placeholder={t('projectManagement.createModal.descriptionPlaceholder')} />
            </FormControl>
            <FormControl mb={4}>
              <FormLabel>{t('projectManagement.createModal.category')}</FormLabel>
              <Select placeholder={t('projectManagement.createModal.categoryPlaceholder')}>
                <option value="office">{t('projectManagement.categories.office')}</option>
                <option value="warehouse">{t('projectManagement.categories.warehouse')}</option>
                <option value="residential">{t('projectManagement.categories.residential')}</option>
              </Select>
            </FormControl>
          </ModalBody>
          <ModalFooter>
            <Button variant="outline" mr={3} onClick={onClose}>{t('projectManagement.createModal.cancel')}</Button>
            <Button variant="primary">{t('projectManagement.createModal.create')}</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </MainLayout>
  );
};

export default ProjectManagementPage;
