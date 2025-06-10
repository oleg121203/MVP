#!/usr/bin/env node

import { config } from 'dotenv';
import { OpenAI } from 'openai';
import { Anthropic } from '@anthropic-ai/sdk';

// Завантажуємо змінні середовища
config({ path: './.env' });

/**
 * 🤖 Multi-AI Provider для Windsurf Enterprise MCP Server
 * Підтримка OpenAI, Anthropic Claude, Google Gemini, Mistral, Grok та локальних моделей
 */

interface AIProvider {
  name: string;
  type: 'openai' | 'anthropic' | 'google' | 'mistral' | 'grok' | 'local' | 'windsurf';
  available: boolean;
  models: string[];
  supportsEmbeddings: boolean;
  supportsChat: boolean;
}

interface EmbeddingResult {
  embedding: number[];
  provider: string;
  model: string;
  tokens?: number;
}

interface ChatResponse {
  content: string;
  provider: string;
  model: string;
  tokens?: {
    input: number;
    output: number;
  };
}

export class MultiAIProvider {
  private providers: Map<string, any> = new Map();
  private availableProviders: AIProvider[] = [];

  constructor() {
    this.initializeProviders();
  }

  /**
   * 🔧 Ініціалізація всіх доступних AI провайдерів
   */
  private initializeProviders(): void {
    // OpenAI
    if (process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== 'test-openai-key-12345') {
      const openai = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY
      });
      this.providers.set('openai', openai);
      this.availableProviders.push({
        name: 'OpenAI',
        type: 'openai',
        available: true,
        models: ['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large', 'gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        supportsEmbeddings: true,
        supportsChat: true
      });
    }

    // Anthropic Claude
    if (process.env.ANTHROPIC_API_KEY && process.env.ANTHROPIC_API_KEY !== 'test-anthropic-key-12345') {
      const anthropic = new Anthropic({
        apiKey: process.env.ANTHROPIC_API_KEY
      });
      this.providers.set('anthropic', anthropic);
      this.availableProviders.push({
        name: 'Anthropic Claude',
        type: 'anthropic',
        available: true,
        models: ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', 'claude-3-haiku-20240307'],
        supportsEmbeddings: false,
        supportsChat: true
      });
    }

    // Google Gemini
    if (process.env.GEMINI_API_KEY && process.env.GEMINI_API_KEY !== 'test-gemini-key-12345') {
      // Gemini через REST API
      this.availableProviders.push({
        name: 'Google Gemini',
        type: 'google',
        available: true,
        models: ['gemini-1.5-flash', 'gemini-1.5-pro', 'text-embedding-004'],
        supportsEmbeddings: true,
        supportsChat: true
      });
    }

    // Mistral
    if (process.env.MISTRAL_API_KEY) {
      this.availableProviders.push({
        name: 'Mistral AI',
        type: 'mistral',
        available: true,
        models: ['mistral-embed', 'mistral-large-latest', 'mistral-medium', 'mistral-small'],
        supportsEmbeddings: true,
        supportsChat: true
      });
    }

    // Grok (через X.AI API)
    if (process.env.GROK_API_KEY) {
      this.availableProviders.push({
        name: 'Grok (X.AI)',
        type: 'grok',
        available: true,
        models: ['grok-beta', 'grok-vision-beta'],
        supportsEmbeddings: false,
        supportsChat: true
      });
    }

    // Локальні моделі (Ollama)
    if (process.env.OLLAMA_BASE_URL) {
      this.availableProviders.push({
        name: 'Ollama (Local)',
        type: 'local',
        available: true,
        models: ['llama2', 'codellama', 'mistral', 'llama3', 'deepseek-coder', 'nomic-embed-text'],
        supportsEmbeddings: true,
        supportsChat: true
      });
    }

    // Windsurf встроєні моделі (симуляція)
    this.availableProviders.push({
      name: 'Windsurf Built-in',
      type: 'windsurf',
      available: true,
      models: ['windsurf-claude-3.5-sonnet', 'windsurf-gpt-4o', 'windsurf-gemini-1.5-pro'],
      supportsEmbeddings: false,
      supportsChat: true
    });

    console.log(`🤖 Initialized ${this.availableProviders.length} AI providers`);
    this.availableProviders.forEach(provider => {
      console.log(`   ✅ ${provider.name}: ${provider.models.length} models`);
    });
  }

  /**
   * 📋 Отримати список доступних провайдерів
   */
  getAvailableProviders(): AIProvider[] {
    return this.availableProviders;
  }

  /**
   * 🎯 Створення embeddings з автоматичним вибором найкращого провайдера
   */
  async createEmbeddings(
    text: string, 
    preferredProvider?: string,
    preferredModel?: string
  ): Promise<EmbeddingResult> {
    const embeddingProviders = this.availableProviders.filter(p => p.supportsEmbeddings);
    
    if (embeddingProviders.length === 0) {
      throw new Error('No embedding providers available');
    }

    // Пріоритет провайдерів для embeddings
    const providerPriority = [
      'openai',      // Найкраща якість
      'google',      // Хороша якість, безкоштовні ліміти
      'mistral',     // Швидкий і дешевий
      'local'        // Локальний fallback
    ];

    let selectedProvider = embeddingProviders[0];
    
    if (preferredProvider) {
      const preferred = embeddingProviders.find(p => p.type === preferredProvider);
      if (preferred) selectedProvider = preferred;
    } else {
      // Автоматичний вибір за пріоритетом
      for (const providerType of providerPriority) {
        const provider = embeddingProviders.find(p => p.type === providerType);
        if (provider) {
          selectedProvider = provider;
          break;
        }
      }
    }

    const model = preferredModel || selectedProvider.models.find(m => m.includes('embed')) || selectedProvider.models[0];

    try {
      switch (selectedProvider.type) {
        case 'openai':
          return await this.createOpenAIEmbedding(text, model);
        
        case 'google':
          return await this.createGeminiEmbedding(text, model);
        
        case 'mistral':
          return await this.createMistralEmbedding(text, model);
        
        case 'local':
          return await this.createOllamaEmbedding(text, model);
        
        default:
          throw new Error(`Embedding not supported for provider: ${selectedProvider.type}`);
      }
    } catch (error) {
      console.error(`❌ Embedding failed with ${selectedProvider.name}:`, error);
      
      // Fallback до наступного провайдера
      const nextProvider = embeddingProviders.find(p => p.type !== selectedProvider.type);
      if (nextProvider) {
        console.log(`🔄 Trying fallback provider: ${nextProvider.name}`);
        return await this.createEmbeddings(text, nextProvider.type);
      }
      
      throw error;
    }
  }

  /**
   * 💬 Генерація чат відповіді з вибором провайдера
   */
  async generateChatResponse(
    messages: Array<{role: string, content: string}>,
    preferredProvider?: string,
    preferredModel?: string,
    options?: {
      temperature?: number;
      maxTokens?: number;
      systemPrompt?: string;
    }
  ): Promise<ChatResponse> {
    const chatProviders = this.availableProviders.filter(p => p.supportsChat);
    
    if (chatProviders.length === 0) {
      throw new Error('No chat providers available');
    }

    // Пріоритет провайдерів для чату
    const providerPriority = [
      'anthropic',   // Найкращий для аналізу коду
      'openai',      // Універсальний
      'google',      // Безкоштовні ліміти
      'windsurf',    // Контекст Windsurf
      'local',       // Локальний
      'mistral',     // Швидкий
      'grok'         // Креативний
    ];

    let selectedProvider = chatProviders[0];
    
    if (preferredProvider) {
      const preferred = chatProviders.find(p => p.type === preferredProvider);
      if (preferred) selectedProvider = preferred;
    } else {
      for (const providerType of providerPriority) {
        const provider = chatProviders.find(p => p.type === providerType);
        if (provider) {
          selectedProvider = provider;
          break;
        }
      }
    }

    const model = preferredModel || selectedProvider.models.find(m => !m.includes('embed')) || selectedProvider.models[0];

    try {
      switch (selectedProvider.type) {
        case 'openai':
          return await this.generateOpenAIResponse(messages, model, options);
        
        case 'anthropic':
          return await this.generateAnthropicResponse(messages, model, options);
        
        case 'google':
          return await this.generateGeminiResponse(messages, model, options);
        
        case 'windsurf':
          return await this.generateWindsurfResponse(messages, model, options);
        
        case 'local':
          return await this.generateOllamaResponse(messages, model, options);
        
        default:
          throw new Error(`Chat not supported for provider: ${selectedProvider.type}`);
      }
    } catch (error) {
      console.error(`❌ Chat failed with ${selectedProvider.name}:`, error);
      
      // Fallback до наступного провайдера
      const nextProvider = chatProviders.find(p => p.type !== selectedProvider.type);
      if (nextProvider) {
        console.log(`🔄 Trying fallback provider: ${nextProvider.name}`);
        return await this.generateChatResponse(messages, nextProvider.type, undefined, options);
      }
      
      throw error;
    }
  }

  // ==================== PROVIDER IMPLEMENTATIONS ====================

  private async createOpenAIEmbedding(text: string, model: string): Promise<EmbeddingResult> {
    const openai = this.providers.get('openai');
    const response = await openai.embeddings.create({
      model: model,
      input: text,
      encoding_format: 'float'
    });

    return {
      embedding: response.data[0].embedding,
      provider: 'OpenAI',
      model: model,
      tokens: response.usage?.total_tokens
    };
  }

  private async createGeminiEmbedding(text: string, model: string): Promise<EmbeddingResult> {
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:embedContent?key=${process.env.GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: {
          parts: [{ text: text }]
        }
      })
    });

    const data = await response.json();
    return {
      embedding: data.embedding.values,
      provider: 'Google Gemini',
      model: model
    };
  }

  private async createMistralEmbedding(text: string, model: string): Promise<EmbeddingResult> {
    const response = await fetch('https://api.mistral.ai/v1/embeddings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.MISTRAL_API_KEY}`
      },
      body: JSON.stringify({
        model: model,
        input: [text]
      })
    });

    const data = await response.json();
    return {
      embedding: data.data[0].embedding,
      provider: 'Mistral AI',
      model: model,
      tokens: data.usage?.total_tokens
    };
  }

  private async createOllamaEmbedding(text: string, model: string): Promise<EmbeddingResult> {
    const response = await fetch(`${process.env.OLLAMA_BASE_URL}/api/embeddings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: model,
        prompt: text
      })
    });

    const data = await response.json();
    return {
      embedding: data.embedding,
      provider: 'Ollama (Local)',
      model: model
    };
  }

  private async generateOpenAIResponse(
    messages: Array<{role: string, content: string}>,
    model: string,
    options?: any
  ): Promise<ChatResponse> {
    const openai = this.providers.get('openai');
    const response = await openai.chat.completions.create({
      model: model,
      messages: messages,
      temperature: options?.temperature || 0.7,
      max_tokens: options?.maxTokens || 1000
    });

    return {
      content: response.choices[0].message.content || '',
      provider: 'OpenAI',
      model: model,
      tokens: {
        input: response.usage?.prompt_tokens || 0,
        output: response.usage?.completion_tokens || 0
      }
    };
  }

  private async generateAnthropicResponse(
    messages: Array<{role: string, content: string}>,
    model: string,
    options?: any
  ): Promise<ChatResponse> {
    const anthropic = this.providers.get('anthropic');
    
    // Конвертуємо формат повідомлень для Claude
    const systemMessage = messages.find(m => m.role === 'system');
    const userMessages = messages.filter(m => m.role !== 'system');

    const response = await anthropic.messages.create({
      model: model,
      max_tokens: options?.maxTokens || 1000,
      temperature: options?.temperature || 0.7,
      system: systemMessage?.content || options?.systemPrompt,
      messages: userMessages
    });

    return {
      content: response.content[0].text,
      provider: 'Anthropic Claude',
      model: model,
      tokens: {
        input: response.usage.input_tokens,
        output: response.usage.output_tokens
      }
    };
  }

  private async generateGeminiResponse(
    messages: Array<{role: string, content: string}>,
    model: string,
    options?: any
  ): Promise<ChatResponse> {
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${process.env.GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: messages.map(m => ({
          role: m.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: m.content }]
        })),
        generationConfig: {
          temperature: options?.temperature || 0.7,
          maxOutputTokens: options?.maxTokens || 1000
        }
      })
    });

    const data = await response.json();
    return {
      content: data.candidates[0].content.parts[0].text,
      provider: 'Google Gemini',
      model: model
    };
  }

  private async generateWindsurfResponse(
    messages: Array<{role: string, content: string}>,
    model: string,
    options?: any
  ): Promise<ChatResponse> {
    // Симуляція Windsurf API - тут може бути інтеграція з внутрішніми моделями Windsurf
    const contextualPrompt = `
    You are a Windsurf AI assistant with deep knowledge of:
    - TypeScript/JavaScript development
    - React/Vue/Angular frameworks  
    - Node.js backend development
    - Database design and optimization
    - DevOps and deployment strategies
    
    Context: Working in VentAI project with MCP server integration.
    
    User query: ${messages[messages.length - 1].content}
    `;

    // Fallback до OpenAI з Windsurf контекстом
    if (this.providers.has('openai')) {
      return await this.generateOpenAIResponse([
        { role: 'system', content: contextualPrompt },
        ...messages.slice(-3) // Останні 3 повідомлення для контексту
      ], 'gpt-4o', options);
    }

    return {
      content: `Windsurf Assistant: ${messages[messages.length - 1].content}\n\n[Simulated response - integrate with actual Windsurf API]`,
      provider: 'Windsurf Built-in',
      model: model
    };
  }

  private async generateOllamaResponse(
    messages: Array<{role: string, content: string}>,
    model: string,
    options?: any
  ): Promise<ChatResponse> {
    const response = await fetch(`${process.env.OLLAMA_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: model,
        messages: messages,
        stream: false,
        options: {
          temperature: options?.temperature || 0.7,
          num_predict: options?.maxTokens || 1000
        }
      })
    });

    const data = await response.json();
    return {
      content: data.message.content,
      provider: 'Ollama (Local)',
      model: model
    };
  }

  /**
   * 🔄 Тестування всіх провайдерів
   */
  async testAllProviders(): Promise<{
    embeddings: Array<{provider: string, success: boolean, error?: string}>;
    chat: Array<{provider: string, success: boolean, error?: string}>;
  }> {
    const embeddingResults = [];
    const chatResults = [];

    // Тестування embeddings
    for (const provider of this.availableProviders.filter(p => p.supportsEmbeddings)) {
      try {
        await this.createEmbeddings('test', provider.type);
        embeddingResults.push({ provider: provider.name, success: true });
      } catch (error) {
        embeddingResults.push({ 
          provider: provider.name, 
          success: false, 
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }

    // Тестування чату
    for (const provider of this.availableProviders.filter(p => p.supportsChat)) {
      try {
        await this.generateChatResponse([{role: 'user', content: 'Hello'}], provider.type);
        chatResults.push({ provider: provider.name, success: true });
      } catch (error) {
        chatResults.push({ 
          provider: provider.name, 
          success: false, 
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }

    return { embeddings: embeddingResults, chat: chatResults };
  }
}
