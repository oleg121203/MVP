/**
 * 🌊 Enhanced VentAI Service with Windsurf Native AI Support
 * Integration with Windsurf Enterprise MCP Server using built-in models
 */

class EnhancedVentAIService {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    this.mcpEndpoint = process.env.REACT_APP_MCP_URL || 'http://localhost:8001';
    this.cache = new Map();
    this.windsurfProviders = [];
    this.currentProvider = null;
    
    // Initialize Windsurf AI providers
    this.initializeWindsurfProviders();
  }

  /**
   * 🔧 Initialize Windsurf AI providers
   */
  async initializeWindsurfProviders() {
    try {
      const response = await this.callMCPTool('list_ai_providers');
      this.windsurfProviders = response.providers;
      
      // Пріоритет: Anthropic Claude > OpenAI > Google > xAI > DeepSeek > Windsurf
      const preferredOrder = ['anthropic', 'openai', 'google', 'xai', 'deepseek', 'windsurf'];
      
      for (const vendor of preferredOrder) {
        const provider = this.windsurfProviders.find(p => p.vendor === vendor);
        if (provider && provider.available) {
          this.currentProvider = provider;
          break;
        }
      }
      
      console.log(`🌊 Windsurf AI Providers initialized: ${this.windsurfProviders.length} providers`);
      console.log(`✅ Current provider: ${this.currentProvider?.name || 'None'}`);
    } catch (error) {
      console.error('Failed to initialize Windsurf providers:', error);
      this.windsurfProviders = [];
    }
  }

  /**
   * 📞 Call MCP tool with error handling
   */
  async callMCPTool(toolName, params = {}) {
    try {
      const response = await fetch(`${this.mcpEndpoint}/mcp/call-tool`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool: toolName, params })
      });

      if (!response.ok) {
        throw new Error(`MCP call failed: ${response.statusText}`);
      }

      const result = await response.json();
      return JSON.parse(result.content[0].text);
    } catch (error) {
      console.error(`MCP Tool Error (${toolName}):`, error);
      throw error;
    }
  }

  /**
   * 🧠 Enhanced AI Chat with Windsurf Native Models
   */
  async enhancedAIChat(message, options = {}) {
    const {
      vendor = null,
      model = null,
      includeProjectContext = true,
      analysisType = 'general',
      temperature = 0.7,
      maxTokens = 1000
    } = options;

    try {
      // Use Windsurf assistant for project-specific queries
      if (includeProjectContext && this.isProjectSpecificQuery(message)) {
        return await this.callMCPTool('ai_windsurf_assistant', {
          query: message,
          context: 'VentAI HVAC platform user interaction',
          includeProjectFiles: true
        });
      }

      // Determine best vendor for the task
      const selectedVendor = vendor || this.selectOptimalVendor(analysisType);

      // Use regular chat completion with Windsurf models
      const messages = [
        {
          role: 'system',
          content: 'You are an expert HVAC assistant for the VentAI platform. Provide accurate, helpful responses about ventilation, air conditioning, and HVAC calculations.'
        },
        { role: 'user', content: message }
      ];

      return await this.callMCPTool('ai_chat_completion', {
        messages,
        provider: selectedVendor,
        model,
        temperature,
        maxTokens,
        systemPrompt: 'Expert HVAC assistant for VentAI platform'
      });
    } catch (error) {
      console.error('Enhanced AI Chat Error:', error);
      return {
        response: 'I apologize, but I encountered an issue accessing Windsurf models. Please try again.',
        provider: 'Windsurf (Error)',
        model: 'fallback',
        vendor: 'windsurf',
        error: true
      };
    }
  }

  /**
   * 🔍 AI-Powered Code Analysis for VentAI Components
   */
  async analyzeVentAICode(filePath, analysisType = 'review') {
    try {
      return await this.callMCPTool('ai_code_analysis', {
        filePath,
        analysisType, // 'review', 'bugs', 'optimization', 'documentation', 'refactoring'
        provider: 'anthropic' // Claude is best for code analysis through Windsurf
      });
    } catch (error) {
      console.error('Code Analysis Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * 🧮 Enhanced Calculator AI with Windsurf Models
   */
  async enhancedCalculatorAssistance(calculatorType, inputData, userQuery) {
    try {
      // Create embeddings using fallback method (since Windsurf doesn't have native embeddings)
      const queryEmbedding = await this.callMCPTool('ai_create_embeddings', {
        text: `${calculatorType} calculation: ${userQuery}`,
        provider: 'windsurf-fallback'
      });

      // Search for relevant documentation and examples
      const relevantDocs = await this.callMCPTool('vector_search_documents', {
        query: `${calculatorType} ${userQuery}`,
        limit: 5,
        includeContent: true
      });

      // Get AI assistance with full context using best available Windsurf model
      const assistance = await this.callMCPTool('ai_chat_completion', {
        messages: [
          {
            role: 'system',
            content: `You are an expert HVAC calculator assistant for VentAI. Help with ${calculatorType} calculations.
            
Relevant Context:
${relevantDocs.results?.map(doc => doc.content?.substring(0, 200)).join('\n') || 'No relevant documents found'}

Current Input Data:
${JSON.stringify(inputData, null, 2)}`
          },
          { role: 'user', content: userQuery }
        ],
        provider: 'anthropic', // Claude через Windsurf для технічного аналізу
        temperature: 0.3, // Lower for technical accuracy
        maxTokens: 1500
      });

      return {
        success: true,
        response: assistance.response,
        provider: assistance.provider,
        vendor: assistance.vendor,
        relevantDocs: relevantDocs.results?.length || 0,
        embedding: queryEmbedding.embedding,
        suggestions: this.parseCalculatorSuggestions(assistance.response),
        optimizations: this.extractOptimizations(assistance.response)
      };
    } catch (error) {
      console.error('Enhanced Calculator Assistance Error:', error);
      return {
        success: false,
        error: error.message,
        fallbackResponse: 'I can help with your calculation. Please provide more details.'
      };
    }
  }

  /**
   * 🔧 Windsurf Provider Testing and Health Check
   */
  async testWindsurfProviders() {
    try {
      const testResults = await this.callMCPTool('ai_test_providers', {
        testEmbeddings: true,
        testChat: true
      });

      return {
        success: true,
        summary: testResults.summary,
        providers: testResults.providers,
        recommendations: this.generateWindsurfRecommendations(testResults)
      };
    } catch (error) {
      console.error('Windsurf Provider Testing Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * 🎯 Smart Vendor Selection for Windsurf
   */
  selectOptimalVendor(taskType) {
    const vendorPreferences = {
      code: 'anthropic',        // Claude для аналізу коду
      creative: 'xai',          // Grok для креативності  
      technical: 'openai',      // GPT для технічних завдань
      reasoning: 'openai',      // GPT-4o для складних роздумів
      hvac: 'anthropic',        // Claude для HVAC розрахунків
      general: 'anthropic'      // Claude як універсальний
    };

    const preferred = vendorPreferences[taskType] || vendorPreferences.general;
    
    // Перевіряємо, чи доступний вибраний провайдер
    const availableProvider = this.windsurfProviders.find(p => 
      p.vendor === preferred && p.available
    );
    
    if (availableProvider) {
      return preferred;
    }
    
    // Fallback до поточного провайдера
    return this.currentProvider?.vendor || 'windsurf';
  }

  /**
   * 📊 Windsurf Performance Analytics
   */
  async getWindsurfPerformanceMetrics() {
    try {
      const providers = await this.callMCPTool('list_ai_providers');
      const testResults = await this.testWindsurfProviders();
      
      const metrics = {
        totalProviders: providers.providers?.length || 0,
        availableProviders: testResults.providers?.filter(p => p.available).length || 0,
        chatCapable: testResults.summary?.chatCapable || 0,
        embeddingCapable: testResults.summary?.embeddingCapable || 0,
        performance: {
          chatAverageTime: this.calculateAverageResponseTime(testResults.providers, 'chat'),
          embeddingAverageTime: this.calculateAverageResponseTime(testResults.providers, 'embeddings')
        },
        recommendations: testResults.recommendations || []
      };
      
      return {
        success: true,
        metrics,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Performance Metrics Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * 🔍 Calculate average response time
   */
  calculateAverageResponseTime(providers, type) {
    const times = providers
      ?.filter(p => p[type]?.success && p[type].responseTime)
      .map(p => p[type].responseTime) || [];
    
    return times.length > 0 ? times.reduce((a, b) => a + b, 0) / times.length : 0;
  }

  /**
   * 💡 Generate Windsurf recommendations
   */
  generateWindsurfRecommendations(testResults) {
    const recommendations = [];
    
    if (testResults.summary?.available === 0) {
      recommendations.push({
        type: 'critical',
        message: 'No Windsurf AI providers are currently available. Check your Windsurf installation and permissions.'
      });
    }
    
    if (testResults.summary?.chatCapable < 2) {
      recommendations.push({
        type: 'warning',
        message: 'Limited chat providers available. Consider checking your Windsurf model access.'
      });
    }
    
    const fastestProvider = testResults.providers
      ?.filter(p => p.chat?.success)
      .sort((a, b) => (a.chat.responseTime || 0) - (b.chat.responseTime || 0))[0];
    
    if (fastestProvider) {
      recommendations.push({
        type: 'info',
        message: `${fastestProvider.name} is currently the fastest responding provider (${fastestProvider.chat.responseTime}ms)`
      });
    }
    
    return recommendations;
  }

      return {
        availableProviders: providers.total,
        activeProviders: testResults.summary.available,
        chatCapableProviders: testResults.summary.chatCapable,
        embeddingCapableProviders: testResults.summary.embeddingCapable,
        providerPerformance: testResults.providers.map(p => ({
          name: p.name,
          available: p.available,
          chatResponseTime: p.chat.responseTime,
          embeddingResponseTime: p.embeddings.responseTime,
          reliability: this.calculateReliability(p)
        })),
        recommendations: {
          bestForChat: this.findBestProvider(testResults.providers, 'chat'),
          bestForEmbeddings: this.findBestProvider(testResults.providers, 'embeddings'),
          mostReliable: this.findMostReliableProvider(testResults.providers)
        }
      };
    } catch (error) {
      console.error('Performance Metrics Error:', error);
      return null;
    }
  }

  // Utility methods
  isProjectSpecificQuery(message) {
    const projectKeywords = [
      'ventai', 'calculator', 'component', 'react', 'typescript', 
      'code', 'optimize', 'performance', 'bug', 'refactor'
    ];
    return projectKeywords.some(keyword => 
      message.toLowerCase().includes(keyword)
    );
  }

  parseCodeSuggestions(analysis) {
    // Parse structured suggestions from analysis text
    const suggestions = [];
    const lines = analysis.split('\n');
    
    lines.forEach(line => {
      if (line.includes('Suggestion:') || line.includes('Recommendation:')) {
        suggestions.push(line.replace(/^.*?:\s*/, '').trim());
      }
    });
    
    return suggestions;
  }

    /**
   * 🔍 Helper methods for analysis and optimization
   */
  
  isProjectSpecificQuery(message) {
    const projectKeywords = ['ventai', 'hvac', 'calculator', 'project', 'code', 'component', 'file'];
    return projectKeywords.some(keyword => 
      message.toLowerCase().includes(keyword)
    );
  }

  parseCodeSuggestions(response) {
    // Extract actionable suggestions for code improvement
    const suggestions = [];
    if (response.includes('refactor')) suggestions.push('Refactoring opportunities identified');
    if (response.includes('optimize')) suggestions.push('Performance optimization available');
    if (response.includes('security')) suggestions.push('Security improvements needed');
    if (response.includes('test')) suggestions.push('Testing improvements recommended');
    return suggestions;
  }

  parseCalculatorSuggestions(response) {
    // Extract actionable suggestions for calculator optimization
    const suggestions = [];
    if (response.includes('optimize')) suggestions.push('Performance optimization available');
    if (response.includes('validate')) suggestions.push('Input validation recommended');
    if (response.includes('accuracy')) suggestions.push('Accuracy improvements possible');
    if (response.includes('energy')) suggestions.push('Energy efficiency considerations');
    return suggestions;
  }

  extractOptimizations(response) {
    // Extract optimization recommendations
    const optimizations = {};
    if (response.includes('energy efficient')) optimizations.energy = 'Energy efficiency improvements available';
    if (response.includes('cost')) optimizations.cost = 'Cost optimization opportunities identified';
    if (response.includes('performance')) optimizations.performance = 'Performance enhancements possible';
    if (response.includes('accuracy')) optimizations.accuracy = 'Calculation accuracy improvements';
    return optimizations;
  }
}

// Export enhanced service
export default EnhancedVentAIService;

// Usage example in React component
export const useEnhancedWindsurfAI = () => {
  const [aiService] = useState(() => new EnhancedVentAIService());
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    aiService.initializeWindsurfProviders().then(() => {
      setProviders(aiService.windsurfProviders);
    });
  }, [aiService]);

  const askAI = async (message, options = {}) => {
    setLoading(true);
    try {
      const response = await aiService.enhancedAIChat(message, options);
      return response;
    } finally {
      setLoading(false);
    }
  };

  const analyzeCode = async (filePath, analysisType = 'review') => {
    setLoading(true);
    try {
      return await aiService.analyzeVentAICode(filePath, analysisType);
    } finally {
      setLoading(false);
    }
  };

  const getCalculatorHelp = async (calculatorType, inputData, query) => {
    setLoading(true);
    try {
      return await aiService.enhancedCalculatorAssistance(calculatorType, inputData, query);
    } finally {
      setLoading(false);
    }
  };

  const testProviders = async () => {
    setLoading(true);
    try {
      return await aiService.testWindsurfProviders();
    } finally {
      setLoading(false);
    }
  };

  const getMetrics = async () => {
    setLoading(true);
    try {
      return await aiService.getWindsurfPerformanceMetrics();
    } finally {
      setLoading(false);
    }
  };

  return {
    providers,
    loading,
    askAI,
    analyzeCode,
    getCalculatorHelp,
    testProviders,
    getMetrics,
    currentProvider: aiService.currentProvider
  };
};

console.log('🌊 Enhanced VentAI Service with Windsurf Native AI Support loaded!');
