#!/usr/bin/env node

import { config } from 'dotenv';
import { createClient } from 'redis';

// Завантажуємо змінні середовища
config({ path: './.env' });
import { Pool } from 'pg';
import fs from 'fs-extra';
import { promises as fsPromises } from 'fs';
import { createTwoFilesPatch } from 'diff';
import { minimatch } from 'minimatch';
import { MultiAIProvider } from './multi-ai-provider.js';

/**
 * 🎯 Enterprise Vector Store для Windsurf MCP System
 * Інтеграція PostgreSQL + Redis + Vector DB для документів/завдань
 */

interface VectorDocument {
  id: string;
  type: 'changelog' | 'phase' | 'task' | 'file' | 'rule' | 'activation';
  content: string;
  metadata: {
    phase?: string;
    timestamp: string;
    path: string;
    status?: string;
    priority?: number;
    tags?: string[];
    operation?: string;
    editsSummary?: string;
    [key: string]: any;
  };
  embedding?: number[];
  graph_connections?: string[];
}

interface GraphNode {
  id: string;
  type: string;
  properties: Record<string, any>;
  relationships: Array<{
    target: string;
    type: 'DEPENDS_ON' | 'PART_OF' | 'TRIGGERS' | 'REFERENCES';
    weight?: number;
  }>;
}

export class WindsurfVectorStore {
  private redis: any;
  private postgres: Pool;
  private aiProvider: MultiAIProvider;
  private vectorDimension = 1536; // OpenAI ada-002 dimensions

  constructor() {
    // Redis connection для кешування та швидкого доступу
    this.redis = createClient({
      url: process.env.REDIS_URL || 'redis://localhost:6380'
    });

    // PostgreSQL з pgvector для векторних операцій
    this.postgres = new Pool({
      connectionString: process.env.DATABASE_URL || 'postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev',
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    // Multi-AI Provider для роботи з різними AI моделями
    this.aiProvider = new MultiAIProvider();

    this.initializeDatabase();
  }

  /**
   * 🔧 Ініціалізація векторної бази даних
   */
  private async initializeDatabase(): Promise<void> {
    try {
      await this.redis.connect();
      console.log('✅ Redis connected for Windsurf Vector Store');

      // Створення таблиць для векторного збереження
      await this.postgres.query(`
        CREATE EXTENSION IF NOT EXISTS vector;
        
        -- Таблиця для векторних документів
        CREATE TABLE IF NOT EXISTS windsurf_documents (
          id VARCHAR(255) PRIMARY KEY,
          type VARCHAR(50) NOT NULL,
          content TEXT NOT NULL,
          metadata JSONB DEFAULT '{}',
          embedding vector(${this.vectorDimension}),
          created_at TIMESTAMP DEFAULT NOW(),
          updated_at TIMESTAMP DEFAULT NOW(),
          search_vector tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
        );

        -- Таблиця для графових зв'язків
        CREATE TABLE IF NOT EXISTS windsurf_graph (
          id VARCHAR(255) PRIMARY KEY,
          source_id VARCHAR(255) REFERENCES windsurf_documents(id),
          target_id VARCHAR(255) REFERENCES windsurf_documents(id),
          relationship_type VARCHAR(50) NOT NULL,
          weight FLOAT DEFAULT 1.0,
          metadata JSONB DEFAULT '{}',
          created_at TIMESTAMP DEFAULT NOW()
        );

        -- Індекси для оптимізації
        CREATE INDEX IF NOT EXISTS idx_windsurf_docs_type ON windsurf_documents(type);
        CREATE INDEX IF NOT EXISTS idx_windsurf_docs_metadata ON windsurf_documents USING GIN(metadata);
        CREATE INDEX IF NOT EXISTS idx_windsurf_docs_search ON windsurf_documents USING GIN(search_vector);
        CREATE INDEX IF NOT EXISTS idx_windsurf_docs_embedding ON windsurf_documents USING ivfflat (embedding vector_cosine_ops);
        CREATE INDEX IF NOT EXISTS idx_windsurf_graph_source ON windsurf_graph(source_id);
        CREATE INDEX IF NOT EXISTS idx_windsurf_graph_target ON windsurf_graph(target_id);
        CREATE INDEX IF NOT EXISTS idx_windsurf_graph_type ON windsurf_graph(relationship_type);
      `);

      console.log('✅ PostgreSQL Vector Store initialized');
    } catch (error) {
      console.error('❌ Vector Store initialization failed:', error);
    }
  }

  /**
   * 📄 Додавання документу до векторної бази з підтримкою великих файлів
   */
  async addDocument(doc: VectorDocument): Promise<void> {
    try {
      // Перевірка розміру контенту (PostgreSQL tsvector ліміт: 1MB)
      const contentSize = Buffer.byteLength(doc.content, 'utf8');
      
      if (contentSize > 800000) { // 800KB safety margin
        console.log(`📄 Large document detected (${Math.round(contentSize/1024)}KB), splitting...`);
        
        // Розбиваємо великий документ на частини
        const chunks = this.splitLargeDocument(doc.content);
        
        for (let i = 0; i < chunks.length; i++) {
          const chunkDoc: VectorDocument = {
            ...doc,
            id: `${doc.id}_chunk_${i + 1}`,
            content: chunks[i],
            metadata: {
              ...doc.metadata,
              isChunk: true,
              chunkNumber: i + 1,
              totalChunks: chunks.length,
              originalDocId: doc.id
            }
          };
          
          await this.addSingleDocument(chunkDoc);
        }
        
        console.log(`✅ Split large document into ${chunks.length} chunks`);
        return;
      }
      
      // Звичайна обробка для невеликих документів
      await this.addSingleDocument(doc);
      
    } catch (error) {
      console.error(`❌ Failed to add document ${doc.id}:`, error);
      throw error;
    }
  }

  /**
   * 📝 Додавання одного документу (внутрішня функція)
   */
  private async addSingleDocument(doc: VectorDocument): Promise<void> {
    try {
      // Генерація embedding з Multi-AI Provider
      let embedding: number[] | null = null;
      if (doc.content.length > 10) {
        try {
          const embeddingResult = await this.aiProvider.createEmbeddings(
            doc.content.substring(0, 8000) // Ліміт для більшості провайдерів
          );
          embedding = embeddingResult.embedding;
          console.log(`✅ Embedding created using ${embeddingResult.provider} (${embeddingResult.model})`);
        } catch (embeddingError) {
          console.warn('⚠️ Embedding generation failed, storing without vector');
        }
      }

      // Збереження в PostgreSQL
      await this.postgres.query(`
        INSERT INTO windsurf_documents (id, type, content, metadata, embedding)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (id) DO UPDATE SET
          content = EXCLUDED.content,
          metadata = EXCLUDED.metadata,
          embedding = EXCLUDED.embedding,
          updated_at = NOW()
      `, [doc.id, doc.type, doc.content, JSON.stringify(doc.metadata), embedding]);

      // Кешування в Redis для швидкого доступу
      await this.redis.setEx(
        `windsurf:doc:${doc.id}`,
        3600, // 1 година
        JSON.stringify(doc)
      );

      // Індексація для пошуку
      await this.redis.sAdd(`windsurf:type:${doc.type}`, doc.id);

      // Додавання тегів до індексу
      if (doc.metadata.tags) {
        for (const tag of doc.metadata.tags) {
          await this.redis.sAdd(`windsurf:tag:${tag}`, doc.id);
        }
      }

      console.log(`✅ Document added to vector store: ${doc.id}`);
    } catch (error) {
      console.error(`❌ Failed to add document ${doc.id}:`, error);
      throw error;
    }
  }

  /**
   * 🔍 Векторний пошук документів
   */
  async vectorSearch(query: string, limit: number = 10, type?: string): Promise<VectorDocument[]> {
    try {
      // Спробуємо генерувати embedding для пошуку
      let queryEmbedding: number[];
      try {
        const embeddingResult = await this.aiProvider.createEmbeddings(query);
        queryEmbedding = embeddingResult.embedding;
        console.log(`🔍 Search embedding created using ${embeddingResult.provider}`);
      } catch (error) {
        console.log('🔄 Embedding unavailable, using text search fallback');
        return this.textSearch(query, limit, type);
      }

      // Векторний пошук в PostgreSQL
      let sql = `
        SELECT id, type, content, metadata, embedding <=> $1 AS distance
        FROM windsurf_documents
        WHERE embedding IS NOT NULL
      `;
      const params: any[] = [JSON.stringify(queryEmbedding)];

      if (type) {
        sql += ` AND type = $2`;
        params.push(type);
      }

      sql += ` ORDER BY distance LIMIT $${params.length + 1}`;
      params.push(limit);

      const result = await this.postgres.query(sql, params);

      return result.rows.map(row => ({
        id: row.id,
        type: row.type,
        content: row.content,
        metadata: row.metadata,
        embedding: row.embedding
      }));
    } catch (error) {
      console.error('❌ Vector search failed:', error);
      return this.textSearch(query, limit, type);
    }
  }

  /**
   * 📝 Текстовий пошук (fallback)
   */
  async textSearch(query: string, limit: number = 10, type?: string): Promise<VectorDocument[]> {
    try {
      let sql = `
        SELECT id, type, content, metadata,
               ts_rank(search_vector, plainto_tsquery($1)) AS rank
        FROM windsurf_documents
        WHERE search_vector @@ plainto_tsquery($1)
      `;
      const params: any[] = [query];

      if (type) {
        sql += ` AND type = $2`;
        params.push(type);
      }

      sql += ` ORDER BY rank DESC LIMIT $${params.length + 1}`;
      params.push(limit);

      const result = await this.postgres.query(sql, params);

      return result.rows.map(row => ({
        id: row.id,
        type: row.type,
        content: row.content,
        metadata: row.metadata
      }));
    } catch (error) {
      console.error('❌ Text search failed:', error);
      return [];
    }
  }

  /**
   * 🕸️ Додавання графового зв'язку
   */
  async addGraphRelationship(
    sourceId: string,
    targetId: string,
    relationshipType: string,
    weight: number = 1.0,
    metadata: Record<string, any> = {}
  ): Promise<void> {
    try {
      const relationshipId = `${sourceId}_${relationshipType}_${targetId}`;
      
      await this.postgres.query(`
        INSERT INTO windsurf_graph (id, source_id, target_id, relationship_type, weight, metadata)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (id) DO UPDATE SET
          weight = EXCLUDED.weight,
          metadata = EXCLUDED.metadata
      `, [relationshipId, sourceId, targetId, relationshipType, weight, JSON.stringify(metadata)]);

      // Кешування графу в Redis
      await this.redis.sAdd(`windsurf:graph:${sourceId}`, `${relationshipType}:${targetId}:${weight}`);

      console.log(`✅ Graph relationship added: ${sourceId} -[${relationshipType}]-> ${targetId}`);
    } catch (error) {
      console.error('❌ Failed to add graph relationship:', error);
      throw error;
    }
  }

  /**
   * 🌐 Отримання графових зв'язків
   */
  async getGraphConnections(nodeId: string, depth: number = 1): Promise<GraphNode[]> {
    try {
      const visited = new Set<string>();
      const nodes: GraphNode[] = [];
      const queue = [{ id: nodeId, currentDepth: 0 }];

      while (queue.length > 0) {
        const { id, currentDepth } = queue.shift()!;
        
        if (visited.has(id) || currentDepth > depth) continue;
        visited.add(id);

        // Отримання документу
        const doc = await this.getDocument(id);
        if (!doc) continue;

        // Отримання зв'язків
        const relationships: any[] = [];
        const graphQuery = await this.postgres.query(`
          SELECT target_id, relationship_type, weight, metadata
          FROM windsurf_graph
          WHERE source_id = $1
        `, [id]);

        for (const rel of graphQuery.rows) {
          relationships.push({
            target: rel.target_id,
            type: rel.relationship_type,
            weight: rel.weight
          });

          if (currentDepth < depth) {
            queue.push({ id: rel.target_id, currentDepth: currentDepth + 1 });
          }
        }

        nodes.push({
          id,
          type: doc.type,
          properties: doc.metadata,
          relationships
        });
      }

      return nodes;
    } catch (error) {
      console.error('❌ Failed to get graph connections:', error);
      return [];
    }
  }

  /**
   * 📖 Отримання документу за ID
   */
  async getDocument(id: string): Promise<VectorDocument | null> {
    try {
      // Спочатку з кешу Redis
      const cached = await this.redis.get(`windsurf:doc:${id}`);
      if (cached) {
        return JSON.parse(cached);
      }

      // Потім з PostgreSQL
      const result = await this.postgres.query(
        'SELECT * FROM windsurf_documents WHERE id = $1',
        [id]
      );

      if (result.rows.length === 0) return null;

      const doc = {
        id: result.rows[0].id,
        type: result.rows[0].type,
        content: result.rows[0].content,
        metadata: result.rows[0].metadata,
        embedding: result.rows[0].embedding
      };

      // Кешування в Redis
      await this.redis.setEx(`windsurf:doc:${id}`, 3600, JSON.stringify(doc));

      return doc;
    } catch (error) {
      console.error(`❌ Failed to get document ${id}:`, error);
      return null;
    }
  }

  /**
   * 📊 Аналітика по документах
   */
  async getAnalytics(): Promise<any> {
    try {
      const stats = await this.postgres.query(`
        SELECT 
          type,
          COUNT(*) as count,
          AVG(CASE WHEN embedding IS NOT NULL THEN 1 ELSE 0 END) as embedding_coverage
        FROM windsurf_documents
        GROUP BY type
      `);

      const graphStats = await this.postgres.query(`
        SELECT 
          relationship_type,
          COUNT(*) as count,
          AVG(weight) as avg_weight
        FROM windsurf_graph
        GROUP BY relationship_type
      `);

      return {
        documents: stats.rows,
        relationships: graphStats.rows,
        totalDocuments: stats.rows.reduce((sum, row) => sum + parseInt(row.count), 0),
        totalRelationships: graphStats.rows.reduce((sum, row) => sum + parseInt(row.count), 0)
      };
    } catch (error) {
      console.error('❌ Failed to get analytics:', error);
      return { documents: [], relationships: [], totalDocuments: 0, totalRelationships: 0 };
    }
  }

  /**
   * 🔄 Синхронізація з файловою системою Windsurf
   */
  async syncWindsurfFiles(windsurfPath: string): Promise<void> {
    try {
      console.log('🔄 Syncing Windsurf files to vector store...');

      // Синхронізація CHANGELOG.md
      const changelogPath = `${windsurfPath}/CHANGELOG.md`;
      if (await fs.pathExists(changelogPath)) {
        const content = await fsPromises.readFile(changelogPath, 'utf-8');
        await this.addDocument({
          id: 'changelog_master',
          type: 'changelog',
          content,
          metadata: {
            path: changelogPath,
            timestamp: new Date().toISOString(),
            tags: ['changelog', 'master', 'progress']
          }
        });
      }

      // Синхронізація docs/changelog/
      const changelogDir = `${windsurfPath}/docs/changelog`;
      if (await fs.pathExists(changelogDir)) {
        const files = await fs.readdir(changelogDir);
        for (const file of files) {
          if (file.endsWith('.md')) {
            const filePath = `${changelogDir}/${file}`;
            const content = await fsPromises.readFile(filePath, 'utf-8');
            const phaseMatch = file.match(/phase(\d+(?:\.\d+)?)/);
            
            await this.addDocument({
              id: `phase_${file.replace('.md', '')}`,
              type: 'phase',
              content,
              metadata: {
                path: filePath,
                phase: phaseMatch ? phaseMatch[1] : 'unknown',
                timestamp: new Date().toISOString(),
                tags: ['phase', 'changelog', phaseMatch ? `phase-${phaseMatch[1]}` : 'misc']
              }
            });

            // Додавання зв'язку з головним changelog
            await this.addGraphRelationship(
              'changelog_master',
              `phase_${file.replace('.md', '')}`,
              'CONTAINS',
              1.0
            );
          }
        }
      }

      // Синхронізація .windsurf/ директорії
      const windsurfConfigDir = `${windsurfPath}/.windsurf`;
      await this.syncDirectory(windsurfConfigDir, 'rule');

      console.log('✅ Windsurf files synchronized to vector store');
    } catch (error) {
      console.error('❌ Windsurf sync failed:', error);
    }
  }

  /**
   * 📁 Синхронізація директорії
   */
  private async syncDirectory(dirPath: string, type: string): Promise<void> {
    if (!await fs.pathExists(dirPath)) return;

    const items = await fs.readdir(dirPath, { withFileTypes: true });
    
    for (const item of items) {
      const itemPath = `${dirPath}/${item.name}`;
      
      if (item.isFile() && item.name.endsWith('.md')) {
        const content = await fsPromises.readFile(itemPath, 'utf-8');
        const docId = `${type}_${item.name.replace('.md', '')}`;
        
        await this.addDocument({
          id: docId,
          type: type as any,
          content,
          metadata: {
            path: itemPath,
            timestamp: new Date().toISOString(),
            tags: [type, item.name.replace('.md', '')]
          }
        });
      } else if (item.isDirectory()) {
        await this.syncDirectory(itemPath, `${type}_${item.name}`);
      }
    }
  }

  /**
   * 🧠 Інтелектуальні рекомендації
   */
  async getRecommendations(context: string, limit: number = 5): Promise<VectorDocument[]> {
    try {
      // Пошук схожих документів
      const similar = await this.vectorSearch(context, limit * 2);
      
      // Аналіз графових зв'язків
      const recommendations: VectorDocument[] = [];
      const seen = new Set<string>();

      for (const doc of similar) {
        if (recommendations.length >= limit) break;
        
        if (!seen.has(doc.id)) {
          recommendations.push(doc);
          seen.add(doc.id);
        }

        // Додавання пов'язаних документів
        const connections = await this.getGraphConnections(doc.id, 1);
        for (const conn of connections) {
          if (recommendations.length >= limit) break;
          
          for (const rel of conn.relationships) {
            if (!seen.has(rel.target)) {
              const relatedDoc = await this.getDocument(rel.target);
              if (relatedDoc) {
                recommendations.push(relatedDoc);
                seen.add(rel.target);
              }
            }
          }
        }
      }

      return recommendations.slice(0, limit);
    } catch (error) {
      console.error('❌ Failed to get recommendations:', error);
      return [];
    }
  }

  /**
   * 🔒 Закриття з'єднань
   */
  async close(): Promise<void> {
    try {
      await this.redis.quit();
      await this.postgres.end();
      console.log('✅ Vector Store connections closed');
    } catch (error) {
      console.error('❌ Failed to close connections:', error);
    }
  }

  /**
   * 📄 Розбиття великих документів на частини для уникнення tsvector ліміту
   */
  private splitLargeDocument(content: string, maxChunkSize: number = 800000): string[] {
    const chunks: string[] = [];
    const lines = content.split('\n');
    let currentChunk = '';
    
    for (const line of lines) {
      // Якщо додання лінії перевищить ліміт, зберігаємо поточний chunk
      if (currentChunk.length + line.length + 1 > maxChunkSize) {
        if (currentChunk.trim()) {
          chunks.push(currentChunk.trim());
        }
        currentChunk = line;
      } else {
        currentChunk += (currentChunk ? '\n' : '') + line;
      }
    }
    
    // Додаємо останній chunk
    if (currentChunk.trim()) {
      chunks.push(currentChunk.trim());
    }
    
    return chunks;
  }
}

// Експорт для використання в MCP сервері
export { VectorDocument, GraphNode };
