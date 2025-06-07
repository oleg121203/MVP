import React, { useState, useEffect } from 'react';
import { Box, Flex, Heading, Text, Button, Input, VStack, Icon, Select, useToast } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { FaComment, FaMagic, FaChartLine, FaUser, FaRobot, FaPaperPlane } from 'react-icons/fa';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/common/Card';

const AIDashboard: React.FC = () => {
  const { t } = useTranslation();
  const toast = useToast();
  const [chatMessages, setChatMessages] = useState<Array<{ role: string, content: string }>>([]);
  const [chatInput, setChatInput] = useState('');
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [promptInput, setPromptInput] = useState('');
  const [generationResult, setGenerationResult] = useState<string | null>(null);
  const [isGenerationLoading, setIsGenerationLoading] = useState(false);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [projectInsights, setProjectInsights] = useState<any>(null);

  // Simulated project data
  const projects = [
    { id: '1', name: 'Project Alpha' },
    { id: '2', name: 'Project Beta' },
    { id: '3', name: 'Project Gamma' },
  ];

  const handleChatSend = async () => {
    if (!chatInput.trim()) return;
    const userMessage = { role: 'user', content: chatInput };
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setIsChatLoading(true);

    // Simulate API call
    setTimeout(() => {
      setChatMessages(prev => [
        ...prev,
        { role: 'ai', content: `Response to: ${userMessage.content}` },
      ]);
      setIsChatLoading(false);
    }, 1000);
  };

  const handleGenerate = async () => {
    if (!promptInput.trim()) return;
    setIsGenerationLoading(true);

    // Simulate API call
    setTimeout(() => {
      setGenerationResult(`Generated content based on: ${promptInput}`);
      setIsGenerationLoading(false);
    }, 2000);
  };

  useEffect(() => {
    if (selectedProject) {
      // Simulate fetching project insights
      setTimeout(() => {
        setProjectInsights({
          analysis: 'All parameters within norms.',
          optimization: 'Consider alternative materials for cost reduction.',
          compliance: 'Compliant with all regulations.',
        });
      }, 1000);
    } else {
      setProjectInsights(null);
    }
  }, [selectedProject]);

  return (
    <MainLayout title={t('aiDashboard.title')}>
      <Box p={{ base: 4, md: 8 }}>
        <Heading as="h1" size={{ base: 'xl', md: '2xl' }} mb={6} color="brand.primary" textAlign="center">{t('aiDashboard.title')}</Heading>
        <Text fontSize={{ base: 'md', md: 'lg' }} mb={8} textAlign="center" color="text.secondary">{t('aiDashboard.subtitle')}</Text>

        <Flex direction={{ base: 'column', md: 'row' }} gap={6}>
          {/* AI Chat Interface - Sidebar */}
          <Box flex={{ base: '1', md: '0.3' }} bg="white" p={4} borderRadius="lg" boxShadow="md" height={{ md: 'calc(100vh - 200px)' }} display="flex" flexDirection="column">
            <Flex align="center" mb={4}>
              <Icon as={FaComment} boxSize={6} color="brand.primary" mr={2} />
              <Heading as="h2" size="md" color="brand.dark">{t('aiDashboard.chat.title')}</Heading>
            </Flex>
            <Text fontSize="sm" mb={4} color="text.secondary">{t('aiDashboard.chat.description')}</Text>
            <Box flex="1" overflowY="auto" mb={4} p={2} bg="gray.50" borderRadius="md">
              {chatMessages.map((msg, index) => (
                <Flex key={index} direction="column" mb={2} align={msg.role === 'user' ? 'flex-end' : 'flex-start'}>
                  <Flex align="center" mb={1}>
                    <Icon as={msg.role === 'user' ? FaUser : FaRobot} boxSize={4} color={msg.role === 'user' ? 'blue.500' : 'green.500'} mr={1} />
                    <Text fontSize="xs" color="text.secondary">{msg.role === 'user' ? t('aiDashboard.chat.you') : t('aiDashboard.chat.ai')}</Text>
                  </Flex>
                  <Box bg={msg.role === 'user' ? 'blue.50' : 'green.50'} p={2} borderRadius="md" maxW="80%">
                    <Text fontSize="sm">{msg.content}</Text>
                  </Box>
                </Flex>
              ))}
              {isChatLoading && (
                <Flex align="center" mb={2}>
                  <Icon as={FaRobot} boxSize={4} color="green.500" mr={1} />
                  <Text fontSize="xs" color="text.secondary">{t('aiDashboard.chat.ai')}</Text>
                  <Text fontSize="sm" ml={2} color="text.secondary">{t('aiDashboard.chat.typing')}</Text>
                </Flex>
              )}
            </Box>
            <Flex gap={2}>
              <Input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder={t('aiDashboard.chat.placeholder')}
                onKeyPress={(e) => e.key === 'Enter' && handleChatSend()}
                flex="1"
              />
              <Button
                onClick={handleChatSend}
                isLoading={isChatLoading}
                loadingText={t('aiDashboard.chat.sending')}
                leftIcon={<FaPaperPlane />}
                variant="primary"
              >
                {t('aiDashboard.chat.send')}
              </Button>
            </Flex>
          </Box>

          {/* Main Content Area */}
          <VStack flex={{ base: '1', md: '0.7' }} spacing={6} align="stretch">
            {/* AI Generation Tool */}
            <Card p={{ base: 4, md: 6 }} boxShadow="md">
              <Flex align="center" mb={4}>
                <Icon as={FaMagic} boxSize={6} color="brand.primary" mr={2} />
                <Heading as="h2" size="md" color="brand.dark">{t('aiDashboard.generation.title')}</Heading>
              </Flex>
              <Text fontSize="sm" mb={4} color="text.secondary">{t('aiDashboard.generation.description')}</Text>
              <Input
                value={promptInput}
                onChange={(e) => setPromptInput(e.target.value)}
                placeholder={t('aiDashboard.generation.placeholder')}
                mb={4}
                size="lg"
              />
              <Button
                onClick={handleGenerate}
                isLoading={isGenerationLoading}
                loadingText={t('aiDashboard.generation.generating')}
                variant="primary"
                mb={4}
              >
                {t('aiDashboard.generation.generate')}
              </Button>
              {generationResult && (
                <Box mt={4} p={4} bg="gray.50" borderRadius="md">
                  <Heading as="h3" size="sm" mb={2} color="brand.dark">{t('aiDashboard.generation.result')}</Heading>
                  <Text fontSize="sm" whiteSpace="pre-wrap">{generationResult}</Text>
                </Box>
              )}
            </Card>

            {/* Project-Specific AI Insights */}
            <Card p={{ base: 4, md: 6 }} boxShadow="md">
              <Flex align="center" mb={4}>
                <Icon as={FaChartLine} boxSize={6} color="brand.primary" mr={2} />
                <Heading as="h2" size="md" color="brand.dark">{t('aiDashboard.insights.title')}</Heading>
              </Flex>
              <Text fontSize="sm" mb={4} color="text.secondary">{t('aiDashboard.insights.description')}</Text>
              <Select
                placeholder={t('aiDashboard.insights.selectProject')}
                value={selectedProject || ''}
                onChange={(e) => setSelectedProject(e.target.value)}
                mb={4}
              >
                {projects.map(project => (
                  <option key={project.id} value={project.id}>{project.name}</option>
                ))}
              </Select>
              {selectedProject && projectInsights ? (
                <Box mt={4} p={4} bg="gray.50" borderRadius="md">
                  <Heading as="h3" size="sm" mb={2} color="brand.dark">{t('aiDashboard.insights.results')}</Heading>
                  <Text fontSize="sm" mb={2}><strong>{t('aiDashboard.insights.analysis')}:</strong> {projectInsights.analysis}</Text>
                  <Text fontSize="sm" mb={2}><strong>{t('aiDashboard.insights.optimization')}:</strong> {projectInsights.optimization}</Text>
                  <Text fontSize="sm"><strong>{t('aiDashboard.insights.compliance')}:</strong> {projectInsights.compliance}</Text>
                </Box>
              ) : selectedProject ? (
                <Text fontSize="sm" color="text.secondary">{t('aiDashboard.insights.loading')}</Text>
              ) : (
                <Text fontSize="sm" color="text.secondary">{t('aiDashboard.insights.noProjectSelected')}</Text>
              )}
            </Card>
          </VStack>
        </Flex>
      </Box>
    </MainLayout>
  );
};

export default AIDashboard;
