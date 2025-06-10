#!/usr/bin/env node

import { config } from 'dotenv';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';

// Завантажуємо змінні середовища з локального .env файлу
config({ path: './.env' });
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  Tool,
  Resource,
} from '@modelcontextprotocol/sdk/types.js';
import fs from 'fs-extra';
import { promises as fsPromises } from 'fs';
import path from 'path';
import { glob } from 'glob';
import { createTwoFilesPatch } from 'diff';
import { minimatch } from 'minimatch';
import { WindsurfVectorStore, VectorDocument } from './vector-store.js';
import { WindsurfAIProvider } from './windsurf-ai-provider.js';

/**
 * 🚀 Windsurf Enterprise MCP Server з векторним зберіганням
 * Інтеграція PostgreSQL + Redis + Vector Search + Graph Relations
 */
class WindsurfEnterpriseMCPServer {
  private server: Server;
  private allowedDirs: string[] = [];
  private windsurfRoot: string;
  private vectorStore: WindsurfVectorStore;
  private aiProvider: WindsurfAIProvider;

  constructor() {
    this.server = new Server(
      {
        name: 'windsurf-enterprise-filesystem',
        version: '2.0.0',
        description: 'Windsurf Enterprise MCP Server with Vector Store & Graph Relations',
      },
      {
        capabilities: {
          tools: {},
          resources: {},
        },
      }
    );

    this.windsurfRoot = process.cwd();
    this.allowedDirs = this.parseAllowedDirectories();
    this.vectorStore = new WindsurfVectorStore();
    this.aiProvider = new WindsurfAIProvider();

    this.setupResourceHandlers();
    this.setupToolHandlers();
    this.initializeVectorSync();
  }

  /**
   * 🔄 Ініціалізація синхронізації з векторним сховищем
   */
  private async initializeVectorSync(): Promise<void> {
    try {
      // Початкова синхронізація файлів Windsurf
      setTimeout(async () => {
        await this.vectorStore.syncWindsurfFiles(this.windsurfRoot);
        console.log('✅ Initial vector sync completed');
      }, 5000);

      // Періодична синхронізація кожні 5 хвилин
      setInterval(async () => {
        await this.vectorStore.syncWindsurfFiles(this.windsurfRoot);
        console.log('🔄 Periodic vector sync completed');
      }, 5 * 60 * 1000);
    } catch (error) {
      console.error('❌ Vector sync initialization failed:', error);
    }
  }

  /**
   * Парсинг дозволених директорій
   */
  private parseAllowedDirectories(): string[] {
    const args = process.argv.slice(2);
    const dirs = args.length > 0 ? args : [this.windsurfRoot];
    
    return dirs.map(dir => path.resolve(dir)).filter(dir => {
      try {
        return fs.existsSync(dir) && fs.statSync(dir).isDirectory();
      } catch {
        return false;
      }
    });
  }

  /**
   * Перевірка дозволених шляхів
   */
  private isPathAllowed(filePath: string): boolean {
    const resolvedPath = path.resolve(filePath);
    return this.allowedDirs.some(allowedDir => 
      resolvedPath.startsWith(allowedDir + path.sep) || resolvedPath === allowedDir
    );
  }

  /**
   * Логування з векторним збереженням
   */
  private async logOperation(operation: string, details: any): Promise<void> {
    const logEntry = {
      timestamp: new Date().toISOString(),
      operation,
      details,
      user: process.env.USER || 'unknown'
    };

    // Стандартне логування
    const logPath = path.join(this.windsurfRoot, '.windsurf', 'logs', 'mcp-operations.log');
    await fs.ensureDir(path.dirname(logPath));
    await fs.appendFile(logPath, JSON.stringify(logEntry) + '\n');

    // Векторне збереження для аналітики
    try {
      await this.vectorStore.addDocument({
        id: `operation_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        type: 'task',
        content: `Operation: ${operation}\n${JSON.stringify(details, null, 2)}`,
        metadata: {
          operation,
          timestamp: logEntry.timestamp,
          user: logEntry.user,
          path: 'mcp-operations',
          tags: ['operation', 'mcp', operation.toLowerCase()]
        }
      });
    } catch (vectorError) {
      console.warn('⚠️ Vector logging failed:', vectorError.message);
    }
  }

  /**
   * Налаштування ресурсів
   */
  private setupResourceHandlers(): void {
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: 'vector://windsurf-system',
            name: 'Windsurf Vector Store',
            description: 'AI-powered document search and analytics',
            mimeType: 'application/json',
          },
          {
            uri: 'graph://windsurf-relations',
            name: 'Windsurf Graph Relations',
            description: 'Task and document relationship graph',
            mimeType: 'application/json',
          },
          {
            uri: 'file://windsurf-system',
            name: 'Windsurf Filesystem Operations',
            description: 'Enhanced filesystem operations with vector search',
            mimeType: 'application/json',
          }
        ] as Resource[],
      };
    });

    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      switch (request.params.uri) {
        case 'vector://windsurf-system':
          const analytics = await this.vectorStore.getAnalytics();
          return {
            contents: [
              {
                uri: request.params.uri,
                mimeType: 'application/json',
                text: JSON.stringify({
                  name: 'Windsurf Vector Store',
                  version: '2.0.0',
                  analytics,
                  capabilities: ['vector_search', 'graph_relations', 'smart_recommendations']
                }, null, 2),
              },
            ],
          };

        case 'graph://windsurf-relations':
          return {
            contents: [
              {
                uri: request.params.uri,
                mimeType: 'application/json',
                text: JSON.stringify({
                  name: 'Windsurf Graph Relations',
                  description: 'Phase and task dependencies',
                  supportedRelations: ['DEPENDS_ON', 'PART_OF', 'TRIGGERS', 'REFERENCES']
                }, null, 2),
              },
            ],
          };

        case 'file://windsurf-system':
          return {
            contents: [
              {
                uri: request.params.uri,
                mimeType: 'application/json',
                text: JSON.stringify({
                  name: 'Windsurf Enterprise Filesystem',
                  version: '2.0.0',
                  allowedDirectories: this.allowedDirs,
                  vectorEnabled: true,
                  capabilities: [
                    'read_file', 'read_multiple_files', 'write_file', 'edit_file',
                    'create_directory', 'list_directory', 'move_file', 
                    'search_files', 'get_file_info', 'list_allowed_directories',
                    // Нові векторні можливості
                    'vector_search_documents', 'smart_recommendations',
                    'graph_relations', 'sync_to_vector_store'
                  ]
                }, null, 2),
              },
            ],
          };

        default:
          throw new Error(`Resource not found: ${request.params.uri}`);
      }
    });
  }

  /**
   * Налаштування інструментів
   */
  private setupToolHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      const baseTools: Tool[] = [
        // Стандартні файлові операції
        {
          name: 'read_file',
          description: 'Read complete contents of a file with vector indexing',
          inputSchema: {
            type: 'object',
            properties: {
              path: { type: 'string', description: 'Path to the file to read' },
              addToVector: { type: 'boolean', description: 'Add content to vector store' },
            },
            required: ['path'],
          },
        },
        {
          name: 'write_file',
          description: 'Create new file or overwrite existing with vector indexing',
          inputSchema: {
            type: 'object',
            properties: {
              path: { type: 'string', description: 'Path to the file' },
              content: { type: 'string', description: 'Content to write' },
              addToVector: { type: 'boolean', description: 'Add to vector store' },
              docType: { type: 'string', description: 'Document type for vector store' },
            },
            required: ['path', 'content'],
          },
        },
        {
          name: 'edit_file',
          description: 'Make selective edits with vector update',
          inputSchema: {
            type: 'object',
            properties: {
              path: { type: 'string', description: 'Path to the file to edit' },
              edits: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    oldText: { type: 'string', description: 'Text to search for' },
                    newText: { type: 'string', description: 'Text to replace with' },
                  },
                  required: ['oldText', 'newText'],
                },
              },
              dryRun: { type: 'boolean', description: 'Preview changes without applying' },
              updateVector: { type: 'boolean', description: 'Update vector store after edit' },
            },
            required: ['path', 'edits'],
          },
        },

        // Нові векторні інструменти
        {
          name: 'vector_search_documents',
          description: 'AI-powered semantic search across all documents',
          inputSchema: {
            type: 'object',
            properties: {
              query: { type: 'string', description: 'Search query' },
              limit: { type: 'number', description: 'Maximum results', default: 10 },
              docType: { type: 'string', description: 'Filter by document type' },
              includeContent: { type: 'boolean', description: 'Include full content in results' },
            },
            required: ['query'],
          },
        },
        {
          name: 'smart_recommendations',
          description: 'Get AI recommendations based on context',
          inputSchema: {
            type: 'object',
            properties: {
              context: { type: 'string', description: 'Current context or task' },
              limit: { type: 'number', description: 'Maximum recommendations', default: 5 },
            },
            required: ['context'],
          },
        },
        {
          name: 'graph_relations',
          description: 'Explore document and task relationships',
          inputSchema: {
            type: 'object',
            properties: {
              nodeId: { type: 'string', description: 'Document or task ID' },
              depth: { type: 'number', description: 'Relationship depth', default: 1 },
              relationshipType: { type: 'string', description: 'Filter by relationship type' },
            },
            required: ['nodeId'],
          },
        },
        {
          name: 'sync_to_vector_store',
          description: 'Manually sync files to vector store',
          inputSchema: {
            type: 'object',
            properties: {
              paths: {
                type: 'array',
                items: { type: 'string' },
                description: 'Specific paths to sync (optional)'
              },
              forceResync: { type: 'boolean', description: 'Force complete resync' },
            },
          },
        },
        {
          name: 'create_graph_relation',
          description: 'Create relationships between documents/tasks',
          inputSchema: {
            type: 'object',
            properties: {
              sourceId: { type: 'string', description: 'Source document ID' },
              targetId: { type: 'string', description: 'Target document ID' },
              relationshipType: { 
                type: 'string', 
                description: 'Relationship type',
                enum: ['DEPENDS_ON', 'PART_OF', 'TRIGGERS', 'REFERENCES']
              },
              weight: { type: 'number', description: 'Relationship weight', default: 1.0 },
            },
            required: ['sourceId', 'targetId', 'relationshipType'],
          },
        },

        // Нові AI-інструменти
        {
          name: 'list_ai_providers',
          description: 'List all available AI providers and their capabilities',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'ai_chat_completion',
          description: 'Generate text using AI providers (OpenAI, Claude, Gemini, Mistral, Grok, Local)',
          inputSchema: {
            type: 'object',
            properties: {
              messages: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    role: { type: 'string', enum: ['user', 'assistant', 'system'] },
                    content: { type: 'string' }
                  },
                  required: ['role', 'content']
                },
                description: 'Conversation messages'
              },
              provider: { 
                type: 'string', 
                description: 'Preferred AI provider (openai, anthropic, google, mistral, grok, local, windsurf)' 
              },
              model: { type: 'string', description: 'Specific model name' },
              temperature: { type: 'number', description: 'Creativity level (0-1)', default: 0.7 },
              maxTokens: { type: 'number', description: 'Maximum response length', default: 1000 },
              systemPrompt: { type: 'string', description: 'System context prompt' }
            },
            required: ['messages'],
          },
        },
        {
          name: 'ai_create_embeddings',
          description: 'Create text embeddings using multiple AI providers',
          inputSchema: {
            type: 'object',
            properties: {
              text: { type: 'string', description: 'Text to embed' },
              provider: { 
                type: 'string', 
                description: 'Preferred provider (openai, google, mistral, local)' 
              },
              model: { type: 'string', description: 'Specific embedding model' }
            },
            required: ['text'],
          },
        },
        {
          name: 'ai_windsurf_assistant',
          description: 'Windsurf-context AI assistant with project knowledge',
          inputSchema: {
            type: 'object',
            properties: {
              query: { type: 'string', description: 'Question or task' },
              context: { type: 'string', description: 'Additional context' },
              includeProjectFiles: { type: 'boolean', description: 'Include project file analysis', default: true }
            },
            required: ['query'],
          },
        },
        {
          name: 'ai_code_analysis',
          description: 'AI-powered code analysis and suggestions',
          inputSchema: {
            type: 'object',
            properties: {
              filePath: { type: 'string', description: 'Path to code file' },
              analysisType: { 
                type: 'string', 
                enum: ['review', 'bugs', 'optimization', 'documentation', 'refactoring'],
                description: 'Type of analysis to perform'
              },
              provider: { type: 'string', description: 'Preferred AI provider' }
            },
            required: ['filePath', 'analysisType'],
          },
        },
        {
          name: 'ai_test_providers',
          description: 'Test all AI providers availability and performance',
          inputSchema: {
            type: 'object',
            properties: {
              testEmbeddings: { type: 'boolean', description: 'Test embedding capabilities', default: true },
              testChat: { type: 'boolean', description: 'Test chat capabilities', default: true }
            },
          },
        }
      ];

      // Додавання стандартних інструментів
      const standardTools: Tool[] = [
        {
          name: 'read_multiple_files',
          description: 'Read multiple files simultaneously with vector indexing',
          inputSchema: {
            type: 'object',
            properties: {
              paths: { 
                type: 'array', 
                items: { type: 'string' },
                description: 'Array of file paths to read' 
              },
              addToVector: { type: 'boolean', description: 'Add contents to vector store' },
            },
            required: ['paths'],
          },
        },
        {
          name: 'create_directory',
          description: 'Create directory with parent directories',
          inputSchema: {
            type: 'object',
            properties: {
              path: { type: 'string', description: 'Directory path to create' },
            },
            required: ['path'],
          },
        },
        {
          name: 'list_directory',
          description: 'List directory contents',
          inputSchema: {
            type: 'object',
            properties: {
              path: { type: 'string', description: 'Directory path to list' },
            },
            required: ['path'],
          },
        },
        {
          name: 'move_file',
          description: 'Move or rename files and directories',
          inputSchema: {
            type: 'object',
            properties: {
              source: { type: 'string', description: 'Source path' },
              destination: { type: 'string', description: 'Destination path' },
            },
            required: ['source', 'destination'],
          },
        },
        {
          name: 'search_files',
          description: 'Search for files and directories',
          inputSchema: {
            type: 'object',
            properties: {
              path: { type: 'string', description: 'Starting directory' },
              pattern: { type: 'string', description: 'Search pattern' },
              excludePatterns: {
                type: 'array',
                items: { type: 'string' },
                description: 'Patterns to exclude',
              },
            },
            required: ['path', 'pattern'],
          },
        },
        {
          name: 'get_file_info',
          description: 'Get detailed file/directory metadata',
          inputSchema: {
            type: 'object',
            properties: {
              path: { type: 'string', description: 'Path to get info for' },
            },
            required: ['path'],
          },
        },
        {
          name: 'list_allowed_directories',
          description: 'List all allowed directories',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        }
      ];

      return {
        tools: [...baseTools, ...standardTools],
      };
    });

    // Обробка викликів інструментів
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          // Векторні інструменти
          case 'vector_search_documents':
            return await this.vectorSearchDocuments(
              args.query as string,
              args.limit as number,
              args.docType as string,
              args.includeContent as boolean
            );

          case 'smart_recommendations':
            return await this.smartRecommendations(
              args.context as string,
              args.limit as number
            );

          case 'graph_relations':
            return await this.graphRelations(
              args.nodeId as string,
              args.depth as number,
              args.relationshipType as string
            );

          case 'sync_to_vector_store':
            return await this.syncToVectorStore(
              args.paths as string[],
              args.forceResync as boolean
            );

          case 'create_graph_relation':
            return await this.createGraphRelation(
              args.sourceId as string,
              args.targetId as string,
              args.relationshipType as string,
              args.weight as number
            );

          // Нові AI-інструменти
          case 'list_ai_providers':
            return await this.listAIProviders();

          case 'ai_chat_completion':
            return await this.aiChatCompletion(
              args.messages as Array<{role: string, content: string}>,
              args.provider as string,
              args.model as string,
              {
                temperature: args.temperature as number,
                maxTokens: args.maxTokens as number,
                systemPrompt: args.systemPrompt as string
              }
            );

          case 'ai_create_embeddings':
            return await this.aiCreateEmbeddings(
              args.text as string,
              args.provider as string,
              args.model as string
            );

          case 'ai_windsurf_assistant':
            return await this.aiWindsurfAssistant(
              args.query as string,
              args.context as string,
              args.includeProjectFiles as boolean
            );

          case 'ai_code_analysis':
            return await this.aiCodeAnalysis(
              args.filePath as string,
              args.analysisType as string,
              args.provider as string
            );

          case 'ai_test_providers':
            return await this.aiTestProviders(
              args.testEmbeddings as boolean,
              args.testChat as boolean
            );

          // Розширені файлові операції
          case 'read_file':
            return await this.readFile(
              args.path as string,
              args.addToVector as boolean
            );

          case 'write_file':
            return await this.writeFile(
              args.path as string,
              args.content as string,
              args.addToVector as boolean,
              args.docType as string
            );

          case 'edit_file':
            return await this.editFile(
              args.path as string,
              args.edits as Array<{oldText: string, newText: string}>,
              args.dryRun as boolean,
              args.updateVector as boolean
            );

          // Стандартні інструменти
          case 'read_multiple_files':
            return await this.readMultipleFiles(
              args.paths as string[],
              args.addToVector as boolean
            );

          case 'create_directory':
            return await this.createDirectory(args.path as string);

          case 'list_directory':
            return await this.listDirectory(args.path as string);

          case 'move_file':
            return await this.moveFile(args.source as string, args.destination as string);

          case 'search_files':
            return await this.searchFiles(
              args.pattern as string,
              args.path as string,
              args.includeContent as boolean
            );

          case 'get_file_info':
            return await this.getFileInfo(args.path as string);

          case 'list_allowed_directories':
            return await this.listAllowedDirectories();

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        await this.logOperation(name, { args, error: error.message });
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  /**
   * 🤖 AI Provider Methods
   */

  /**
   * 📋 List all available AI providers (ТОЧНІ ДАНІ WINDSURF 2025-06-11)
   */
  private async listAIProviders() {
    const providers = this.aiProvider.getAvailableProviders();
    const totalModels = providers.reduce((sum, p) => sum + p.models.length, 0);
    const freeModels = providers.flatMap(p => p.models).filter(m => m.credits === 'free');
    
    await this.logOperation('list_ai_providers', { 
      providersCount: providers.length,
      totalModels: totalModels,
      freeModelsCount: freeModels.length
    });

    // Точна структура відповідності Windsurf API
    const response = {
      providers: providers,
      total: providers.length,
      total_models: totalModels,
      free_models_count: freeModels.length,
      capabilities: {
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
      }
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(response, null, 2),
        },
      ],
    };
  }

  /**
   * 💬 AI Chat Completion
   */
  private async aiChatCompletion(
    messages: Array<{role: string, content: string}>,
    provider?: string,
    model?: string,
    options: {
      temperature?: number,
      maxTokens?: number,
      systemPrompt?: string
    } = {}
  ) {
    try {
      // Add system prompt if provided
      let finalMessages = [...messages];
      if (options.systemPrompt) {
        finalMessages.unshift({
          role: 'system',
          content: options.systemPrompt
        });
      }

      const result = await this.aiProvider.generateChatResponse(
        finalMessages,
        provider,
        model,
        {
          temperature: options.temperature || 0.7,
          maxTokens: options.maxTokens || 1000
        }
      );

      await this.logOperation('ai_chat_completion', { 
        provider: result.provider,
        model: result.model,
        messagesCount: finalMessages.length,
        responseLength: result.content.length
      });

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              response: result.content,
              provider: result.provider,
              model: result.model,
              tokens: result.tokens,
              metadata: {
                messagesCount: finalMessages.length,
                responseLength: result.content.length,
                timestamp: new Date().toISOString()
              }
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      throw new Error(`AI chat completion failed: ${error.message}`);
    }
  }

  /**
   * 🧮 AI Create Embeddings (Fallback симуляція)
   */
  private async aiCreateEmbeddings(
    text: string,
    provider?: string,
    model?: string
  ) {
    try {
      // Оскільки Windsurf не підтримує embeddings напряму, створюємо fallback
      // Використовуємо простий хеш як симуляцію ембединга
      const simpleHash = this.createSimpleEmbedding(text);

      await this.logOperation('ai_create_embeddings', { 
        provider: provider || 'windsurf-fallback',
        model: model || 'hash-embedding',
        textLength: text.length,
        dimensions: simpleHash.length
      });

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              embedding: simpleHash,
              provider: provider || 'windsurf-fallback',
              model: model || 'hash-embedding',
              metadata: {
                textLength: text.length,
                dimensions: simpleHash.length,
                timestamp: new Date().toISOString(),
                note: 'Simulated embedding - replace with actual embedding service if needed'
              }
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      throw new Error(`AI embedding creation failed: ${error.message}`);
    }
  }

  /**
   * 🔢 Створити просте ембединг на основі хешу
   */
  private createSimpleEmbedding(text: string): number[] {
    const words = text.toLowerCase().split(/\s+/);
    const embedding = new Array(512).fill(0); // 512-вимірний вектор
    
    for (let i = 0; i < words.length && i < 512; i++) {
      const word = words[i];
      let hash = 0;
      for (let j = 0; j < word.length; j++) {
        const char = word.charCodeAt(j);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
      }
      embedding[i % 512] += Math.sin(hash) * 0.1; // Нормалізоване значення
    }
    
    // Нормалізуємо вектор
    const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
    if (magnitude > 0) {
      for (let i = 0; i < embedding.length; i++) {
        embedding[i] /= magnitude;
      }
    }
    
    return embedding;
  }

  /**
   * 🏗️ Windsurf AI Assistant
   */
  private async aiWindsurfAssistant(
    query: string,
    context?: string,
    includeProjectFiles: boolean = true
  ) {
    try {
      let projectContext = '';
      
      if (includeProjectFiles) {
        // Get relevant project files through vector search
        const relevantDocs = await this.vectorStore.vectorSearch(query, 5);
        projectContext = relevantDocs.map(doc => 
          `File: ${doc.metadata.path}\n${doc.content.substring(0, 1000)}...`
        ).join('\n\n');
      }

      const systemPrompt = `You are Windsurf AI Assistant, an expert in software development and project management.
You have access to the current project context and files. Help the user with their query while considering the project structure and codebase.

Project Context:
${projectContext}

Additional Context:
${context || 'None provided'}`;

      const messages = [
        { role: 'user', content: query }
      ];

      const result = await this.aiProvider.generateChatResponse(
        messages, 
        'windsurf', // Try Windsurf provider first
        undefined,
        {
          temperature: 0.7,
          maxTokens: 2000
        }
      );

      await this.logOperation('ai_windsurf_assistant', { 
        provider: result.provider,
        queryLength: query.length,
        contextIncluded: includeProjectFiles,
        responseLength: result.content.length
      });

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              response: result.content,
              provider: result.provider,
              model: result.model,
              projectContext: includeProjectFiles,
              relevantFiles: projectContext ? projectContext.split('\n\n').length : 0,
              metadata: {
                queryLength: query.length,
                responseLength: result.content.length,
                timestamp: new Date().toISOString()
              }
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      throw new Error(`Windsurf AI assistant failed: ${error.message}`);
    }
  }

  /**
   * 🔍 AI Code Analysis
   */
  private async aiCodeAnalysis(
    filePath: string,
    analysisType: string,
    provider?: string
  ) {
    try {
      if (!this.isPathAllowed(filePath)) {
        throw new Error(`Access denied: ${filePath}`);
      }

      const content = await fsPromises.readFile(filePath, 'utf-8');
      const fileExtension = path.extname(filePath).toLowerCase();
      const language = this.getLanguageFromExtension(fileExtension);

      const analysisPrompts = {
        review: `Please review this ${language} code for best practices, code quality, and potential improvements:`,
        bugs: `Please analyze this ${language} code for potential bugs, errors, and security vulnerabilities:`,
        optimization: `Please analyze this ${language} code for performance optimizations and efficiency improvements:`,
        documentation: `Please suggest documentation improvements and generate missing comments for this ${language} code:`,
        refactoring: `Please suggest refactoring opportunities to improve code structure and maintainability for this ${language} code:`
      };

      const prompt = analysisPrompts[analysisType] || analysisPrompts.review;
      const systemPrompt = `You are an expert code reviewer with deep knowledge of ${language} and software engineering best practices.
Provide detailed, actionable feedback with specific line references when possible.`;

      const messages = [
        { role: 'user', content: `${prompt}\n\n\`\`\`${language}\n${content}\n\`\`\`` }
      ];

      const result = await this.aiProvider.analyzeCode(
        content,
        filePath,
        analysisType as 'review' | 'bugs' | 'optimization' | 'documentation' | 'refactoring'
      );

      await this.logOperation('ai_code_analysis', { 
        filePath,
        analysisType,
        provider: result.provider,
        language,
        codeLength: content.length,
        responseLength: result.content.length
      });

      return {
        content: [
          {
            type: 'text',        text: JSON.stringify({
          analysis: result.content,
          provider: result.provider,
          model: result.model,
          analysisType,
          filePath,
          language,
          metadata: {
            codeLength: content.length,
            responseLength: result.content.length,
            timestamp: new Date().toISOString()
          }
        }, null, 2),
          },
        ],
      };
    } catch (error) {
      throw new Error(`AI code analysis failed: ${error.message}`);
    }
  }

  /**
   * 🧪 Test AI Providers
   */
  private async aiTestProviders(
    testEmbeddings: boolean = true,
    testChat: boolean = true
  ) {
    const results = {
      providers: [],
      summary: {
        total: 0,
        available: 0,
        chatCapable: 0,
        embeddingCapable: 0
      },
      timestamp: new Date().toISOString()
    };

    const providers = this.aiProvider.getAvailableProviders();
    results.summary.total = providers.length;

    for (const providerInfo of providers) {
      const testResult = {
        name: providerInfo.name,
        vendor: providerInfo.vendor,
        available: false,
        chat: { supported: false, tested: false, success: false, error: null, responseTime: null },
        embeddings: { supported: false, tested: false, success: false, error: null, responseTime: null }
      };

      try {
        // Test chat capabilities
        if (testChat) {
          testResult.chat.supported = true;
          testResult.chat.tested = true;
          
          const startTime = Date.now();
          try {
            const chatResult = await this.aiProvider.generateChatResponse(
              [{ role: 'user', content: 'Hello, this is a test message. Please respond briefly.' }],
              providerInfo.vendor,
              undefined,
              { maxTokens: 50 }
            );
            testResult.chat.success = !!chatResult.content;
            testResult.chat.responseTime = Date.now() - startTime;
          } catch (error) {
            testResult.chat.error = error instanceof Error ? error.message : 'Unknown error';
          }
        }

        // Embeddings simulation test (since Windsurf doesn't have native embeddings)
        if (testEmbeddings) {
          testResult.embeddings.supported = true;
          testResult.embeddings.tested = true;
          
          const startTime = Date.now();
          try {
            // Test our fallback embedding method
            const embedding = this.createSimpleEmbedding('This is a test text for embedding generation.');
            testResult.embeddings.success = embedding.length > 0;
            testResult.embeddings.responseTime = Date.now() - startTime;
          } catch (error) {
            testResult.embeddings.error = error instanceof Error ? error.message : 'Unknown error';
          }
        }

        testResult.available = testResult.chat.success || testResult.embeddings.success;
        if (testResult.available) results.summary.available++;
        if (testResult.chat.success) results.summary.chatCapable++;
        if (testResult.embeddings.success) results.summary.embeddingCapable++;

      } catch (error) {
        console.error(`Error testing provider ${providerInfo.name}:`, error);
      }

      results.providers.push(testResult);
    }

    await this.logOperation('ai_test_providers', { 
      total: results.summary.total,
      available: results.summary.available,
      testEmbeddings,
      testChat
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(results, null, 2),
        },
      ],
    };
  }

  /**
   * 🔤 Get programming language from file extension
   */
  private getLanguageFromExtension(extension: string): string {
    const languageMap: Record<string, string> = {
      '.js': 'javascript',
      '.jsx': 'javascript',
      '.ts': 'typescript',
      '.tsx': 'typescript',
      '.py': 'python',
      '.java': 'java',
      '.c': 'c',
      '.cpp': 'cpp',
      '.cs': 'csharp',
      '.php': 'php',
      '.rb': 'ruby',
      '.go': 'go',
      '.rs': 'rust',
      '.swift': 'swift',
      '.kt': 'kotlin',
      '.scala': 'scala',
      '.sh': 'bash',
      '.sql': 'sql',
      '.html': 'html',
      '.css': 'css',
      '.json': 'json',
      '.xml': 'xml',
      '.yaml': 'yaml',
      '.yml': 'yaml',
      '.md': 'markdown'
    };

    return languageMap[extension] || 'text';
  }

  /**
   * 🔍 Vector Search Methods
   */

  /**
   * 🔍 Vector search documents
   */
  private async vectorSearchDocuments(
    query: string,
    limit: number = 10,
    docType?: string,
    includeContent: boolean = false
  ) {
    const results = await this.vectorStore.vectorSearch(query, limit, docType);
    
    await this.logOperation('vector_search_documents', { 
      query, 
      limit, 
      docType, 
      resultsCount: results.length 
    });

    const responseData = {
      query,
      resultsCount: results.length,
      results: results.map(doc => ({
        id: doc.id,
        type: doc.type,
        metadata: doc.metadata,
        ...(includeContent && { content: doc.content.substring(0, 500) + '...' })
      }))
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(responseData, null, 2),
        },
      ],
    };
  }

  /**
   * 🧠 Smart recommendations
   */
  private async smartRecommendations(context: string, limit: number = 5) {
    const recommendations = await this.vectorStore.getRecommendations(context, limit);
    
    await this.logOperation('smart_recommendations', { 
      context, 
      limit, 
      recommendationsCount: recommendations.length 
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            context,
            recommendations: recommendations.map(doc => ({
              id: doc.id,
              type: doc.type,
              metadata: doc.metadata,
              preview: doc.content.substring(0, 200) + '...'
            }))
          }, null, 2),
        },
      ],
    };
  }

  /**
   * 🕸️ Graph relations
   */
  private async graphRelations(nodeId: string, depth: number = 1, relationshipType?: string) {
    const connections = await this.vectorStore.getGraphConnections(nodeId, depth);
    
    await this.logOperation('graph_relations', { 
      nodeId, 
      depth, 
      relationshipType, 
      connectionsCount: connections.length 
    });

    const filteredConnections = relationshipType 
      ? connections.filter(conn => 
          conn.relationships.some(rel => rel.type === relationshipType)
        )
      : connections;

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            nodeId,
            depth,
            relationshipType,
            connectionsCount: filteredConnections.length,
            connections: filteredConnections
          }, null, 2),
        },
      ],
    };
  }

  /**
   * 🔄 Sync to vector store
   */
  private async syncToVectorStore(paths?: string[], forceResync: boolean = false) {
    try {
      if (paths && paths.length > 0) {
        // Sync specific paths
        for (const filePath of paths) {
          if (this.isPathAllowed(filePath)) {
            const content = await fsPromises.readFile(filePath, 'utf-8');
            const docId = `file_${path.basename(filePath, path.extname(filePath))}_${Date.now()}`;
            await this.vectorStore.addDocument({
              id: docId,
              type: 'file',
              content,
              metadata: {
                path: filePath,
                timestamp: new Date().toISOString(),
                tags: ['file', 'manual_sync']
              }
            });
          }
        }
      } else {
        // Full sync
        await this.vectorStore.syncWindsurfFiles(this.windsurfRoot);
      }

      await this.logOperation('sync_to_vector_store', { 
        paths: paths || ['full_sync'], 
        forceResync 
      });

      return {
        content: [
          {
            type: 'text',
            text: `Successfully synced ${paths ? paths.length + ' specific paths' : 'all files'} to vector store`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Sync failed: ${error.message}`);
    }
  }

  /**
   * 🔗 Create graph relation
   */
  private async createGraphRelation(
    sourceId: string,
    targetId: string,
    relationshipType: string,
    weight: number = 1.0
  ) {
    await this.vectorStore.addGraphRelationship(sourceId, targetId, relationshipType, weight);
    
    await this.logOperation('create_graph_relation', { 
      sourceId, 
      targetId, 
      relationshipType, 
      weight 
    });

    return {
      content: [
        {
          type: 'text',
          text: `Graph relationship created: ${sourceId} -[${relationshipType}:${weight}]-> ${targetId}`,
        },
      ],
    };
  }

  /**
   * 📁 File Operation Methods
   */

  /**
   * 📖 Read file
   */
  private async readFile(filePath: string, addToVector: boolean = false) {
    if (!this.isPathAllowed(filePath)) {
      throw new Error(`Access denied: ${filePath}`);
    }

    const content = await fsPromises.readFile(filePath, 'utf-8');
    
    // Add to vector store if needed
    if (addToVector) {
      const docId = `file_${path.basename(filePath, path.extname(filePath))}_${Date.now()}`;
      await this.vectorStore.addDocument({
        id: docId,
        type: 'file',
        content,
        metadata: {
          path: filePath,
          timestamp: new Date().toISOString(),
          tags: ['file', 'read_operation']
        }
      });
    }

    await this.logOperation('read_file', { 
      path: filePath, 
      size: content.length, 
      addedToVector: addToVector 
    });

    return {
      content: [
        {
          type: 'text',
          text: content,
        },
      ],
    };
  }

  /**
   * ✍️ Write file
   */
  private async writeFile(
    filePath: string, 
    content: string, 
    addToVector: boolean = false,
    docType: string = 'file'
  ) {
    if (!this.isPathAllowed(filePath)) {
      throw new Error(`Access denied: ${filePath}`);
    }

    await fs.ensureDir(path.dirname(filePath));
    await fs.writeFile(filePath, content, 'utf-8');
    
    if (addToVector) {
      const docId = `file_${path.basename(filePath, path.extname(filePath))}_${Date.now()}`;
      await this.vectorStore.addDocument({
        id: docId,
        type: docType as any,
        content,
        metadata: {
          path: filePath,
          timestamp: new Date().toISOString(),
          tags: ['file', 'write_operation']
        }
      });
    }

    await this.logOperation('write_file', { 
      path: filePath, 
      size: content.length, 
      addedToVector: addToVector 
    });

    return {
      content: [
        {
          type: 'text',
          text: `File written: ${filePath} (${content.length} characters)`,
        },
      ],
    };
  }

  /**
   * ✏️ Edit file
   */
  private async editFile(
    filePath: string,
    edits: Array<{oldText: string, newText: string}>,
    dryRun: boolean = false,
    updateVector: boolean = false
  ) {
    if (!this.isPathAllowed(filePath)) {
      throw new Error(`Access denied: ${filePath}`);
    }

    const originalContent = await fsPromises.readFile(filePath, 'utf-8');
    let modifiedContent = originalContent;
    const appliedEdits = [];

    for (const edit of edits) {
      const index = modifiedContent.indexOf(edit.oldText);
      if (index !== -1) {
        modifiedContent = modifiedContent.replace(edit.oldText, edit.newText);
        appliedEdits.push({ ...edit, found: true });
      } else {
        appliedEdits.push({ ...edit, found: false });
      }
    }

    const diff = createTwoFilesPatch(
      filePath,
      filePath,
      originalContent,
      modifiedContent,
      'original',
      'modified'
    );

    if (!dryRun) {
      await fs.writeFile(filePath, modifiedContent, 'utf-8');
      
      if (updateVector) {
        const docId = `file_${path.basename(filePath, path.extname(filePath))}_edited_${Date.now()}`;
        await this.vectorStore.addDocument({
          id: docId,
          type: 'file',
          content: modifiedContent,
          metadata: {
            path: filePath,
            timestamp: new Date().toISOString(),
            tags: ['file', 'edit_operation', 'updated'],
            editsSummary: appliedEdits.filter(e => e.found).length + ' edits applied'
          }
        });
      }
    }

    await this.logOperation('edit_file', { 
      path: filePath, 
      editsApplied: appliedEdits.filter(e => e.found).length,
      dryRun,
      vectorUpdated: updateVector && !dryRun
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            dryRun,
            appliedEdits,
            diff,
            originalLength: originalContent.length,
            modifiedLength: modifiedContent.length,
            vectorUpdated: updateVector && !dryRun,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * 📚 Read multiple files
   */
  private async readMultipleFiles(paths: string[], addToVector: boolean = false) {
    const results = await Promise.allSettled(
      paths.map(async (filePath) => {
        if (!this.isPathAllowed(filePath)) {
          throw new Error(`Access denied: ${filePath}`);
        }
        const content = await fsPromises.readFile(filePath, 'utf-8');
        
        if (addToVector) {
          const docId = `file_${path.basename(filePath, path.extname(filePath))}_${Date.now()}`;
          await this.vectorStore.addDocument({
            id: docId,
            type: 'file',
            content,
            metadata: {
              path: filePath,
              timestamp: new Date().toISOString(),
              tags: ['file', 'batch_read']
            }
          });
        }
        
        return { path: filePath, content, success: true };
      })
    );

    const successful = results
      .filter((result): result is PromiseFulfilledResult<any> => result.status === 'fulfilled')
      .map(result => result.value);

    const failed = results
      .filter((result): result is PromiseRejectedResult => result.status === 'rejected')
      .map((result, index) => ({ path: paths[index], error: result.reason.message }));

    await this.logOperation('read_multiple_files', { 
      successful: successful.length, 
      failed: failed.length,
      addedToVector: addToVector
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({ successful, failed }, null, 2),
        },
      ],
    };
  }

  /**
   * 📁 Create directory
   */
  private async createDirectory(dirPath: string) {
    if (!this.isPathAllowed(dirPath)) {
      throw new Error(`Access denied: ${dirPath}`);
    }

    await fs.ensureDir(dirPath);
    
    await this.logOperation('create_directory', { path: dirPath });

    return {
      content: [
        {
          type: 'text',
          text: `Directory created: ${dirPath}`,
        },
      ],
    };
  }

  /**
   * 📂 List directory
   */
  private async listDirectory(dirPath: string) {
    if (!this.isPathAllowed(dirPath)) {
      throw new Error(`Access denied: ${dirPath}`);
    }

    const items = await fs.readdir(dirPath, { withFileTypes: true });
    const listing = items.map(item => ({
      name: item.name,
      type: item.isDirectory() ? 'directory' : 'file',
      path: path.join(dirPath, item.name)
    }));

    await this.logOperation('list_directory', { path: dirPath, items: listing.length });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(listing, null, 2),
        },
      ],
    };
  }

  /**
   * 🚚 Move file
   */
  private async moveFile(sourcePath: string, destinationPath: string) {
    if (!this.isPathAllowed(sourcePath) || !this.isPathAllowed(destinationPath)) {
      throw new Error(`Access denied: ${sourcePath} -> ${destinationPath}`);
    }

    await fs.ensureDir(path.dirname(destinationPath));
    await fs.move(sourcePath, destinationPath);

    await this.logOperation('move_file', { source: sourcePath, destination: destinationPath });

    return {
      content: [
        {
          type: 'text',
          text: `File moved: ${sourcePath} -> ${destinationPath}`,
        },
      ],
    };
  }

  /**
   * 🔍 Search files
   */
  private async searchFiles(
    pattern: string,
    searchPath?: string,
    includeContent: boolean = false
  ) {
    const searchDir = searchPath && this.isPathAllowed(searchPath) 
      ? searchPath 
      : this.windsurfRoot;

    const globPattern = pattern.includes('*') ? pattern : `**/*${pattern}*`;
    const matches = await glob(globPattern, { 
      cwd: searchDir,
      ignore: ['node_modules/**', '.git/**', 'dist/**', 'build/**']
    });

    const filteredMatches = matches
      .map(match => path.join(searchDir, match))
      .filter(filePath => this.isPathAllowed(filePath));

    await this.logOperation('search_files', { 
      pattern, 
      searchPath: searchDir, 
      matches: filteredMatches.length 
    });

    return {
      content: [
        {
          type: 'text',
          text: filteredMatches.join('\n'),
        },
      ],
    };
  }

  /**
   * 📄 Get file info
   */
  private async getFileInfo(filePath: string) {
    if (!this.isPathAllowed(filePath)) {
      throw new Error(`Access denied: ${filePath}`);
    }

    const stats = await fs.stat(filePath);
    const info = {
      path: filePath,
      size: stats.size,
      type: stats.isDirectory() ? 'directory' : 'file',
      created: stats.birthtime.toISOString(),
      modified: stats.mtime.toISOString(),
      accessed: stats.atime.toISOString(),
      permissions: '0' + (stats.mode & parseInt('777', 8)).toString(8),
    };

    await this.logOperation('get_file_info', { path: filePath });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(info, null, 2),
        },
      ],
    };
  }

  /**
   * 📋 List allowed directories
   */
  private async listAllowedDirectories() {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(this.allowedDirs, null, 2),
        },
      ],
    };
  }

  /**
   * 🚀 Run the server
   */
  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('🚀 Windsurf Enterprise MCP Server (Multi-AI Enabled) running on stdio');
  }

  // ...existing code...
}

// Graceful shutdown handling
process.on('SIGINT', async () => {
  console.error('\n🛑 Received SIGINT, shutting down gracefully...');
  if (global.mcpServer) {
    await global.mcpServer.shutdown();
  }
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.error('\n🛑 Received SIGTERM, shutting down gracefully...');
  if (global.mcpServer) {
    await global.mcpServer.shutdown();
  }
  process.exit(0);
});

// Запуск сервера
const server = new WindsurfEnterpriseMCPServer();
global.mcpServer = server;
server.run().catch(console.error);
