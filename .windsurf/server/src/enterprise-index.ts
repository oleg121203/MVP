#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
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

/**
 * 🚀 Windsurf Enterprise MCP Server з векторним зберіганням
 * Інтеграція PostgreSQL + Redis + Vector Search + Graph Relations
 */
class WindsurfEnterpriseMCPServer {
  private server: Server;
  private allowedDirs: string[] = [];
  private windsurfRoot: string;
  private vectorStore: WindsurfVectorStore;

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
              args.path as string,
              args.pattern as string,
              args.excludePatterns as string[]
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
   * 🔍 Векторний пошук документів
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
   * 🧠 Розумні рекомендації
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
   * 🕸️ Графові зв'язки
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
   * 🔄 Синхронізація з векторним сховищем
   */
  private async syncToVectorStore(paths?: string[], forceResync: boolean = false) {
    try {
      if (paths && paths.length > 0) {
        // Синхронізація конкретних шляхів
        for (const filePath of paths) {
          if (this.isPathAllowed(filePath) && await fs.pathExists(filePath)) {
            const content = await fsPromises.readFile(filePath, 'utf-8');
            const docId = `file_${path.basename(filePath, '.md')}_${Date.now()}`;
            
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
        // Повна синхронізація
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
   * 🔗 Створення графового зв'язку
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
   * 📖 Читання файлу з векторною індексацією
   */
  private async readFile(filePath: string, addToVector: boolean = false) {
    if (!this.isPathAllowed(filePath)) {
      throw new Error(`Access denied: ${filePath}`);
    }

    const content = await fsPromises.readFile(filePath, 'utf-8');
    
    // Додавання до векторного сховища якщо потрібно
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
   * ✍️ Запис файлу з векторною індексацією
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

    // Додавання до векторного сховища якщо потрібно
    if (addToVector) {
      const docId = `${docType}_${path.basename(filePath, path.extname(filePath))}_${Date.now()}`;
      await this.vectorStore.addDocument({
        id: docId,
        type: docType as any,
        content,
        metadata: {
          path: filePath,
          timestamp: new Date().toISOString(),
          tags: [docType, 'write_operation']
        }
      });
    }

    await this.logOperation('write_file', { 
      path: filePath, 
      size: content.length, 
      addedToVector: addToVector,
      docType 
    });

    return {
      content: [
        {
          type: 'text',
          text: `Successfully wrote ${content.length} characters to ${filePath}${addToVector ? ' (added to vector store)' : ''}`,
        },
      ],
    };
  }

  /**
   * ✏️ Редагування файлу з оновленням векторного сховища
   */
  private async editFile(
    filePath: string,
    edits: Array<{oldText: string, newText: string}>,
    dryRun = false,
    updateVector = false
  ) {
    if (!this.isPathAllowed(filePath)) {
      throw new Error(`Access denied: ${filePath}`);
    }

    const originalContent = await fsPromises.readFile(filePath, 'utf-8');
    let modifiedContent = originalContent;

    const appliedEdits: Array<{oldText: string, newText: string, found: boolean}> = [];

    for (const edit of edits) {
      const found = modifiedContent.includes(edit.oldText);
      if (found) {
        modifiedContent = modifiedContent.replace(edit.oldText, edit.newText);
      }
      appliedEdits.push({ ...edit, found });
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
      
      // Оновлення векторного сховища
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

  // Імплементація інших стандартних методів (аналогічно попередній версії)
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

  private async listDirectory(dirPath: string) {
    if (!this.isPathAllowed(dirPath)) {
      throw new Error(`Access denied: ${dirPath}`);
    }

    const items = await fs.readdir(dirPath);
    const itemsWithTypes = await Promise.all(
      items.map(async (item) => {
        const itemPath = path.join(dirPath, item);
        const stats = await fs.stat(itemPath);
        return `${stats.isDirectory() ? '[DIR]' : '[FILE]'} ${item}`;
      })
    );

    await this.logOperation('list_directory', { path: dirPath, itemCount: items.length });

    return {
      content: [
        {
          type: 'text',
          text: itemsWithTypes.join('\n'),
        },
      ],
    };
  }

  private async moveFile(source: string, destination: string) {
    if (!this.isPathAllowed(source) || !this.isPathAllowed(destination)) {
      throw new Error(`Access denied`);
    }

    if (await fs.pathExists(destination)) {
      throw new Error(`Destination already exists: ${destination}`);
    }

    await fs.move(source, destination);
    await this.logOperation('move_file', { source, destination });

    return {
      content: [
        {
          type: 'text',
          text: `Moved ${source} to ${destination}`,
        },
      ],
    };
  }

  private async searchFiles(searchPath: string, pattern: string, excludePatterns: string[] = []) {
    if (!this.isPathAllowed(searchPath)) {
      throw new Error(`Access denied: ${searchPath}`);
    }

    const globPattern = path.join(searchPath, '**', pattern);
    const matches = await glob(globPattern, { 
      nocase: true,
      ignore: excludePatterns 
    });

    const filteredMatches = matches.filter(match => this.isPathAllowed(match));

    await this.logOperation('search_files', { 
      searchPath, 
      pattern, 
      excludePatterns, 
      matchCount: filteredMatches.length 
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
   * 🚀 Запуск сервера
   */
  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('🚀 Windsurf Enterprise MCP Server (Vector-Enabled) running on stdio');
  }

  /**
   * 🔒 Graceful shutdown
   */
  async shutdown(): Promise<void> {
    await this.vectorStore.close();
    console.error('👋 Windsurf Enterprise MCP Server shutdown complete');
  }
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
