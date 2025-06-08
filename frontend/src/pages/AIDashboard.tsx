import React, { useState, useEffect } from 'react';
import { Box, Flex, Heading, Text, Button, Input, VStack, Select, useToast, Spinner, UnorderedList, ListItem, Stack } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { FaComment, FaMagic, FaChartLine, FaUser, FaRobot, FaPaperPlane } from 'react-icons/fa';
import Card from '../components/common/Card';
import ChakraIcon from '../components/common/ChakraIcon';
import { AnalysisResults, ProjectInsights, ChatMessage } from '../types/api';

const AIDashboard: React.FC = () => {
  const { t } = useTranslation();
  const toast = useToast();
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [promptInput, setPromptInput] = useState('');
  const [generationResult, setGenerationResult] = useState<string | null>(null);
  const [isGenerationLoading, setIsGenerationLoading] = useState(false);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [projectInsights, setProjectInsights] = useState<ProjectInsights | null>(null);

  // Simulated project data
  const projects = [
    { id: '1', name: 'Project Alpha' },
    { id: '2', name: 'Project Beta' },
    { id: '3', name: 'Project Gamma' },
  ];

  const handleChatSend = async () => {
    if (!chatInput.trim()) return;
    const userMessage: ChatMessage = { role: 'user', content: chatInput };
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setIsChatLoading(true);

    // Simulate API call
    setTimeout(() => {
      setChatMessages(prev => [
        ...prev,
        { role: 'assistant', content: `Response to: ${userMessage.content}` },
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

  // Automated Project Analysis Section
  const ProjectAnalysis = () => {
    const [selectedProject, setSelectedProject] = useState<string | null>(null);
    const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const toast = useToast();

    const handleProjectSelect = async (projectId: string) => {
      setSelectedProject(projectId);
      setIsLoading(true);
      setError(null);

      try {
        // Fetch project data (simulated for now, replace with actual API call to get project details)
        const projectData = projects.find(p => p.id === projectId);
        if (!projectData) {
          throw new Error("Project not found");
        }

        // Call backend API for analysis
        const response = await fetch("http://localhost:8000/api/project-analysis/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            area: 1000, // Default values for demonstration
            occupancy: 50,
            climate_zone: 'Temperate',
            system_type: 'Split System',
            energy_consumption: 1200,
            ventilation_rate: 0.3,
            noise_level: 50
          }),
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        setAnalysisResults(data);
      } catch (err) {
        setError("Failed to fetch analysis results. Please try again.");
        toast({
          title: "Error",
          description: "Could not load project analysis.",
          status: "error",
          duration: 5000,
          isClosable: true,
        });
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    return (
      <Box bg="white" p={6} borderRadius="lg" shadow="md" mb={6}>
        <Heading size="md" mb={4}>Project Analysis</Heading>
        <Select 
          placeholder="Select a project for analysis" 
          onChange={(e) => handleProjectSelect(e.target.value)}
          mb={4}
        >
          {projects.map(project => (
            <option key={project.id} value={project.id}>{project.name}</option>
          ))}
        </Select>
        {isLoading && <Spinner />}
        {error && !isLoading && <Text color="red.500">{error}</Text>}
        {analysisResults && !isLoading && !error && (
          <Box>
            <Text fontWeight="bold">Compliance Status: {analysisResults.compliance_status}</Text>
            {analysisResults.compliance_issues && analysisResults.compliance_issues.length > 0 && (
              <Box mt={2}>
                <Text fontWeight="bold">Issues:</Text>
                <UnorderedList>
                  {analysisResults.compliance_issues.map((issue: string, index: number) => (
                    <ListItem key={index}>{issue}</ListItem>
                  ))}
                </UnorderedList>
              </Box>
            )}
            {analysisResults.recommendations && (
              <Box mt={4}>
                <Text fontWeight="bold">Recommendations:</Text>
                {analysisResults.recommendations.optimal_system_type && (
                  <Text>Optimal System Type: {analysisResults.recommendations.optimal_system_type}</Text>
                )}
                {analysisResults.recommendations.energy_savings_potential && (
                  <Text>Energy Savings Potential: {analysisResults.recommendations.energy_savings_potential} kWh</Text>
                )}
                {analysisResults.recommendations.priority_actions && analysisResults.recommendations.priority_actions.length > 0 && (
                  <>
                    <Text fontWeight="bold" mt={2}>Priority Actions:</Text>
                    <UnorderedList>
                      {analysisResults.recommendations.priority_actions.map((action: string, index: number) => (
                        <ListItem key={index}>{action}</ListItem>
                      ))}
                    </UnorderedList>
                  </>
                )}
              </Box>
            )}
          </Box>
        )}
      </Box>
    );
  };

  return (
    <Box>
      <Box p={{ base: 4, md: 8 }}>
        <Heading as="h1" size={{ base: 'xl', md: '2xl' }} mb={6} color="brand.primary" textAlign="center">{t('aiDashboard.title')}</Heading>
        <Text fontSize={{ base: 'md', md: 'lg' }} mb={8} textAlign="center" color="text.secondary">{t('aiDashboard.subtitle')}</Text>

        <Flex direction={{ base: 'column', md: 'row' }} gap={6}>
          {/* AI Chat Interface - Sidebar */}
          <Box flex={{ base: '1', md: '0.3' }} bg="white" p={4} borderRadius="lg" boxShadow="md" height={{ md: 'calc(100vh - 200px)' }} display="flex" flexDirection="column">
            <Flex align="center" mb={4}>
              <ChakraIcon icon={FaComment} boxSize={6} color="brand.primary" mr={2} />
              <Heading as="h2" size="md" color="brand.dark">{t('aiDashboard.chat.title')}</Heading>
            </Flex>
            <Text fontSize="sm" mb={4} color="text.secondary">{t('aiDashboard.chat.description')}</Text>
            <Box flex="1" overflowY="auto" mb={4} p={2} bg="gray.50" borderRadius="md">
              {chatMessages.map((msg, index) => (
                <Flex key={index} direction="column" mb={2} align={msg.role === 'user' ? 'flex-end' : 'flex-start'}>
                  <Flex align="center" mb={1}>
                    <ChakraIcon icon={msg.role === 'user' ? FaUser : FaRobot} boxSize={4} color={msg.role === 'user' ? 'blue.500' : 'green.500'} mr={1} />
                    <Text fontSize="xs" color="text.secondary">{msg.role === 'user' ? t('aiDashboard.chat.you') : t('aiDashboard.chat.ai')}</Text>
                  </Flex>
                  <Box bg={msg.role === 'user' ? 'blue.50' : 'green.50'} p={2} borderRadius="md" maxW="80%">
                    <Text fontSize="sm">{msg.content}</Text>
                  </Box>
                </Flex>
              ))}
              {isChatLoading && (
                <Flex align="center" mb={2}>
                  <ChakraIcon icon={FaRobot} boxSize={4} color="green.500" mr={1} />
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
                leftIcon={<ChakraIcon icon={FaPaperPlane} />}
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
                <ChakraIcon icon={FaMagic} boxSize={6} color="brand.primary" mr={2} />
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
                <ChakraIcon icon={FaChartLine} boxSize={6} color="brand.primary" mr={2} />
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

            {/* Automated Project Analysis */}
            <ProjectAnalysis />
          </VStack>
        </Flex>
      </Box>
    </Box>
  );
};

export default AIDashboard;
