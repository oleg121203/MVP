/**
 * 🌊 Windsurf Exact Models Integration Service
 * Direct integration with Windsurf MCP Server - Exact Model Mapping
 * Generated from actual Windsurf MCP server response on 2024-12-28
 */

export class WindsurfExactModelsService {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    this.mcpEndpoint = process.env.REACT_APP_MCP_URL || 'http://localhost:8001';
    this.cache = new Map();
    this.providers = null;
    this.models = null;
    
    // Initialize with exact Windsurf data
    this.initializeExactModels();
  }

  /**
   * 🎯 Exact Windsurf Models from MCP Server Response (ОНОВЛЕНО 2025-06-11)
   * This matches EXACTLY what Windsurf returns
   */
  initializeExactModels() {
    // Точні дані з реального Windsurf API (11 червня 2025)
    this.providers = [
      {
        "vendor": "windsurf",
        "name": "Windsurf Built-in",
        "available": true,
        "models": [
          {
            "id": "windsurf-swe-1",
            "name": "SWE-1 (free limited time)",
            "vendor": "windsurf",
            "family": "swe",
            "type": "chat",
            "available": true,
            "credits": "free",
            "features": ["code-generation", "debugging", "refactoring"]
          },
          {
            "id": "windsurf-swe-1-lite",
            "name": "SWE-1-lite",
            "vendor": "windsurf",
            "family": "swe",
            "type": "chat",
            "available": true,
            "credits": "free",
            "features": ["quick-assistance", "code-completion"]
          }
        ]
      },
      {
        "vendor": "openai",
        "name": "OpenAI (via Windsurf)",
        "available": true,
        "totalCredits": "1x credit",
        "models": [
          {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "vendor": "openai",
            "family": "gpt-4",
            "type": "chat",
            "available": true,
            "credits": "1x credit"
          },
          {
            "id": "gpt-4o-mini",
            "name": "GPT-4o mini",
            "vendor": "openai",
            "family": "gpt-4",
            "type": "chat",
            "available": true,
            "credits": "0.1x credit"
          },
          {
            "id": "o3-mini-reasoning",
            "name": "o3-mini (medium reasoning)",
            "vendor": "openai",
            "family": "o3",
            "type": "reasoning",
            "available": true,
            "credits": "1x credit"
          }
        ]
      },
      {
        "vendor": "anthropic",
        "name": "Anthropic (via Windsurf)",
        "available": true,
        "models": [
          {
            "id": "claude-3.5-sonnet",
            "name": "Claude 3.5 Sonnet",
            "vendor": "anthropic",
            "family": "claude",
            "type": "chat",
            "available": true,
            "credits": "1x credit"
          },
          {
            "id": "claude-3.7-sonnet-thinking",
            "name": "Claude 3.7 Sonnet (Thinking)",
            "vendor": "anthropic",
            "family": "claude",
            "type": "reasoning",
            "available": true,
            "credits": "1.25x credit"
          }
        ]
      },
      {
        "vendor": "google",
        "name": "Google (via Windsurf)",
        "available": true,
        "models": [
          {
            "id": "gemini-2.5-pro",
            "name": "Gemini 2.5 Pro (promo)",
            "vendor": "google",
            "family": "gemini",
            "type": "chat",
            "available": true,
            "credits": "0.75x credit"
          },
          {
            "id": "gemini-2.5-flash",
            "name": "Gemini 2.5 Flash",
            "vendor": "google",
            "family": "gemini",
            "type": "chat",
            "available": true,
            "credits": "0.1x credit"
          }
        ]
      },
      {
        "vendor": "xai",
        "name": "xAI (via Windsurf)",
        "available": true,
        "models": [
          {
            "id": "grok-3",
            "name": "xAI Grok-3",
            "vendor": "xai",
            "family": "grok",
            "type": "chat",
            "available": true,
            "credits": "1x credit"
          }
        ]
      },
      {
        "vendor": "deepseek",
        "name": "DeepSeek (via Windsurf)",
        "available": true,
        "models": [
          {
            "id": "deepseek-v3",
            "name": "DeepSeek V3 (0324)",
            "vendor": "deepseek",
            "family": "deepseek",
            "type": "chat",
            "available": true,
            "credits": "free"
          }
        ]
      }
    ];

    // Точні capabilities як у Windsurf
    this.capabilities = {
      chat: [
        "windsurf:SWE-1 (free limited time)",
        "windsurf:SWE-1-lite",
        "openai:GPT-4o",
        "openai:GPT-4o mini",
        "anthropic:Claude 3.5 Sonnet",
        "google:Gemini 2.5 Pro (promo)",
        "google:Gemini 2.5 Flash",
        "xai:xAI Grok-3",
        "deepseek:DeepSeek V3 (0324)"
      ],
      reasoning: [
        "openai:o3-mini (medium reasoning)",
        "anthropic:Claude 3.7 Sonnet (Thinking)"
      ]
    };

    // Flatten all models for easy access
    this.models = this.providers.flatMap(provider => 
      provider.models.map(model => ({
        ...model,
        providerName: provider.name,
        providerAvailable: provider.available
      }))
    );

    console.log('🌊 Windsurf Exact Models initialized:', {
      providers: this.providers.length,
      models: this.models.length,
      freeModels: this.getFreeModels().length,
      reasoningModels: this.getReasoningModels().length
    });
  }

  /**
   * 📞 Call MCP tool with exact parameters
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
      // Fallback to local data if MCP call fails
      if (toolName === 'list_ai_providers') {
        return { providers: this.providers };
      }
      throw error;
    }
  }

  /**
   * 🔍 Get all available providers
   */
  getProviders() {
    return this.providers;
  }

  /**
   * 🤖 Get all available models
   */
  getModels() {
    return this.models;
  }

  /**
   * 💰 Get free models only
   */
  getFreeModels() {
    return this.models.filter(model => model.credits === 'free');
  }

  /**
   * 🧠 Get reasoning models only
   */
  getReasoningModels() {
    return this.models.filter(model => model.type === 'reasoning');
  }

  /**
   * 🎯 Get models by vendor
   */
  getModelsByVendor(vendor) {
    return this.models.filter(model => model.vendor === vendor);
  }

  /**
   * 🔧 Get model by ID
   */
  getModelById(modelId) {
    return this.models.find(model => model.id === modelId);
  }

  /**
   * ⚡ Select best model for task type
   */
  selectBestModel(taskType = 'general', preferFree = false) {
    // Define vendor preferences by task type
    const vendorPreferences = {
      'general': ['anthropic', 'openai', 'google', 'xai', 'deepseek', 'windsurf'],
      'reasoning': ['anthropic', 'openai', 'google', 'xai', 'deepseek', 'windsurf'],
      'coding': ['windsurf', 'anthropic', 'openai', 'google', 'xai', 'deepseek'],
      'analysis': ['anthropic', 'openai', 'google', 'xai', 'deepseek', 'windsurf'],
      'creative': ['openai', 'anthropic', 'google', 'xai', 'deepseek', 'windsurf'],
      'fast': ['openai', 'google', 'deepseek', 'windsurf', 'anthropic', 'xai']
    };

    const preferences = vendorPreferences[taskType] || vendorPreferences['general'];
    
    // If preferFree, try free models first
    if (preferFree) {
      const freeModels = this.getFreeModels();
      for (const vendor of preferences) {
        const model = freeModels.find(m => m.vendor === vendor);
        if (model) return model;
      }
    }

    // For reasoning tasks, prefer reasoning models
    if (taskType === 'reasoning') {
      const reasoningModels = this.getReasoningModels();
      for (const vendor of preferences) {
        const model = reasoningModels.find(m => m.vendor === vendor);
        if (model) return model;
      }
    }

    // Select best available model by vendor preference
    for (const vendor of preferences) {
      const providerModels = this.getModelsByVendor(vendor);
      if (providerModels.length > 0) {
        // Return the first model (usually the best one) from this vendor
        return providerModels[0];
      }
    }

    // Fallback to first available model
    return this.models[0] || null;
  }

  /**
   * 🧠 Enhanced AI Chat with exact Windsurf model selection
   */
  async enhancedAIChat(message, options = {}) {
    const {
      vendor = null,
      modelId = null,
      taskType = 'general',
      includeProjectContext = true,
      temperature = 0.7,
      maxTokens = 1000,
      preferFree = false
    } = options;

    try {
      // Determine the best model to use
      let selectedModel;
      
      if (modelId) {
        selectedModel = this.getModelById(modelId);
      } else if (vendor) {
        const vendorModels = this.getModelsByVendor(vendor);
        selectedModel = vendorModels[0] || null;
      } else {
        selectedModel = this.selectBestModel(taskType, preferFree);
      }

      if (!selectedModel) {
        throw new Error('No suitable model found');
      }

      // For Windsurf models with project context
      if (selectedModel.vendor === 'windsurf' && includeProjectContext) {
        return await this.callMCPTool('ai_windsurf_assistant', {
          query: message,
          context: 'VentAI HVAC platform user interaction',
          includeProjectFiles: true
        });
      }

      // For all other models, use chat completion
      const messages = [
        {
          role: 'system',
          content: 'You are an expert HVAC assistant for the VentAI platform. Provide accurate, helpful responses about ventilation, air conditioning, and HVAC calculations.'
        },
        { role: 'user', content: message }
      ];

      return await this.callMCPTool('ai_chat_completion', {
        vendor: selectedModel.vendor,
        model: selectedModel.id,
        messages,
        temperature,
        max_tokens: maxTokens
      });

    } catch (error) {
      console.error('Enhanced AI Chat Error:', error);
      
      // Fallback to simple response
      return {
        content: [{
          text: `I apologize, but I'm experiencing technical difficulties. However, I can help you with HVAC questions. You asked: "${message}". For immediate assistance, please try again or contact support.`
        }]
      };
    }
  }

  /**
   * 📊 Get provider statistics
   */
  getProviderStats() {
    return this.providers.map(provider => ({
      vendor: provider.vendor,
      name: provider.name,
      available: provider.available,
      modelCount: provider.models.length,
      freeModels: provider.models.filter(m => m.credits === 'free').length,
      reasoningModels: provider.models.filter(m => m.type === 'reasoning').length,
      chatModels: provider.models.filter(m => m.type === 'chat').length
    }));
  }

  /**
   * 🔄 Refresh providers from MCP server
   */
  async refreshProviders() {
    try {
      const response = await this.callMCPTool('list_ai_providers');
      this.providers = response.providers;
      this.models = this.providers.flatMap(provider => 
        provider.models.map(model => ({
          ...model,
          providerName: provider.name,
          providerAvailable: provider.available
        }))
      );
      
      console.log('🔄 Providers refreshed from MCP server');
      return this.providers;
    } catch (error) {
      console.error('Failed to refresh providers:', error);
      return this.providers; // Return cached data
    }
  }

  /**
   * 🎯 Get model recommendations for specific tasks
   */
  getModelRecommendations(taskType = 'general') {
    const recommendations = {
      'hvac_calculations': {
        primary: this.selectBestModel('analysis'),
        alternatives: [
          this.getModelById('claude-3-5-sonnet-20241022'),
          this.getModelById('gpt-4o'),
          this.getModelById('gemini-2.5-pro')
        ].filter(Boolean),
        reason: 'Best for technical calculations and analysis'
      },
      'customer_support': {
        primary: this.selectBestModel('general'),
        alternatives: [
          this.getModelById('gpt-4o-mini'),
          this.getModelById('gemini-2.5-flash'),
          this.getModelById('deepseek-v3')
        ].filter(Boolean),
        reason: 'Optimized for customer interactions'
      },
      'code_review': {
        primary: this.getModelById('windsurf-swe-1'),
        alternatives: [
          this.getModelById('claude-3-5-sonnet-20241022'),
          this.getModelById('gpt-4o'),
          this.getModelById('windsurf-swe-1-lite')
        ].filter(Boolean),
        reason: 'Specialized for software engineering tasks'
      },
      'complex_reasoning': {
        primary: this.selectBestModel('reasoning'),
        alternatives: [
          this.getModelById('claude-3-7-sonnet-thinking'),
          this.getModelById('o3-mini-reasoning')
        ].filter(Boolean),
        reason: 'Advanced reasoning capabilities'
      },
      'budget_friendly': {
        primary: this.selectBestModel('general', true),
        alternatives: this.getFreeModels(),
        reason: 'Free models for cost-conscious usage'
      }
    };

    return recommendations[taskType] || recommendations['general'];
  }

  /**
   * 🎪 Demo all models (for testing)
   */
  async demoAllModels(testMessage = "Hello! Can you briefly introduce yourself?") {
    const results = [];
    
    for (const model of this.models) {
      try {
        console.log(`🧪 Testing ${model.name} (${model.vendor})...`);
        
        const result = await this.enhancedAIChat(testMessage, {
          modelId: model.id,
          maxTokens: 100
        });
        
        results.push({
          model: model.name,
          vendor: model.vendor,
          credits: model.credits,
          type: model.type,
          success: true,
          response: result.content?.[0]?.text || 'No response',
          contextWindow: model.context_window
        });
        
        // Brief delay between requests
        await new Promise(resolve => setTimeout(resolve, 1000));
        
      } catch (error) {
        results.push({
          model: model.name,
          vendor: model.vendor,
          credits: model.credits,
          type: model.type,
          success: false,
          error: error.message,
          contextWindow: model.context_window
        });
      }
    }
    
    return results;
  }
}

/**
 * 🎣 React Hook for Windsurf Models
 */
export function useEnhancedWindsurfAI() {
  const [service] = React.useState(() => new WindsurfExactModelsService());
  const [providers, setProviders] = React.useState(service.getProviders());
  const [models, setModels] = React.useState(service.getModels());
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  const refreshProviders = async () => {
    setLoading(true);
    setError(null);
    try {
      const newProviders = await service.refreshProviders();
      setProviders(newProviders);
      setModels(service.getModels());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const chatWithAI = async (message, options = {}) => {
    setLoading(true);
    setError(null);
    try {
      return await service.enhancedAIChat(message, options);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const selectBestModel = (taskType, preferFree = false) => {
    return service.selectBestModel(taskType, preferFree);
  };

  const getFreeModels = () => {
    return service.getFreeModels();
  };

  const getReasoningModels = () => {
    return service.getReasoningModels();
  };

  const getModelsByVendor = (vendor) => {
    return service.getModelsByVendor(vendor);
  };

  const getModelRecommendations = (taskType) => {
    return service.getModelRecommendations(taskType);
  };

  const demoAllModels = async (testMessage) => {
    setLoading(true);
    setError(null);
    try {
      return await service.demoAllModels(testMessage);
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    // Data
    providers,
    models,
    loading,
    error,
    
    // Methods
    refreshProviders,
    chatWithAI,
    selectBestModel,
    getFreeModels,
    getReasoningModels,
    getModelsByVendor,
    getModelRecommendations,
    demoAllModels,
    
    // Service instance for advanced usage
    service
  };
}

// Default export
export default WindsurfExactModelsService;
