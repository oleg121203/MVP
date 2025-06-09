/**
 * ProjectAnalyticsEngine tests
 * @module tests/analytics
 * @see VENTAI_ENTERPRISE_PLAN.md [P1.2-T3]
 */

import { ProjectAnalyticsEngine } from '../services/analytics/engine';
import { RedisConnectionManager } from '../services/redis/connectionManager';
import type { RedisClientType } from 'redis';
import { createClient } from 'redis';
import { ProjectMetrics } from '../interfaces/analytics';
import { webSocketService } from '../services/websocket';

// Mock msgpack directly in test file
jest.mock('msgpack-lite', () => ({
  encode: (data: unknown) => Buffer.from(JSON.stringify(data)),
  decode: (buf: Buffer) => JSON.parse(buf.toString())
}));

describe('ProjectAnalyticsEngine', () => {
  let analyticsEngine: ProjectAnalyticsEngine;
  let redisManager: jest.Mocked<RedisConnectionManager>;
  let redisClient: jest.Mocked<RedisClientType>;

  beforeAll(async () => {
    redisClient = {
      connect: jest.fn(),
      get: jest.fn(),
      setEx: jest.fn(),
      quit: jest.fn(),
      on: jest.fn()
    } as unknown as jest.Mocked<RedisClientType>;

    redisManager = {
      getConnection: jest.fn().mockResolvedValue(redisClient),
      releaseConnection: jest.fn()
    } as unknown as jest.Mocked<RedisConnectionManager>;

    analyticsEngine = new ProjectAnalyticsEngine(redisManager);
  });

  afterAll(async () => {
    await redisClient.quit();
  });

  describe('getRealTimeInsights', () => {
    beforeEach(() => {
      jest.spyOn(console, 'error').mockImplementation(() => {});
    });

    afterEach(() => {
      (console.error as jest.Mock).mockRestore();
    });

    it('should return project metrics for valid project ID', async () => {
      const testProjectId = '123e4567-e89b-12d3-a456-426614174000';
      const metrics = await analyticsEngine.getRealTimeInsights(testProjectId);
      
      expect(metrics).toHaveProperty('projectId');
      expect(metrics).toHaveProperty('costAnalysis');
      expect(metrics).toHaveProperty('timelineMetrics');
    });

    it('should handle Redis errors gracefully', async () => {
      redisClient.get.mockRejectedValueOnce(new Error('Redis error'));
      const testProjectId = '123e4567-e89b-12d3-a456-426614174000';
      
      await expect(analyticsEngine.getRealTimeInsights(testProjectId))
        .resolves.toHaveProperty('projectId');
      
      expect(console.error).toHaveBeenCalledWith(
        'Redis cache error:', 
        expect.any(Error)
      );
    });
  });

  describe('calculateAndCacheMetrics', () => {
    it('should successfully cache project metrics', async () => {
      const testProjectId = '123e4567-e89b-12d3-a456-426614174000';
      await expect(analyticsEngine.calculateAndCacheMetrics(testProjectId))
        .resolves.not.toThrow();
    });
  });

  describe('batchCalculateMetrics', () => {
    it('should process batch of project IDs', async () => {
      const projectIds = [
        '123e4567-e89b-12d3-a456-426614174000',
        '223e4567-e89b-12d3-a456-426614174001'
      ];
      
      const results = await analyticsEngine.batchCalculateMetrics(projectIds);
      
      expect(results).toHaveLength(2);
      expect(results[0]).toHaveProperty('projectId');
      expect(results[1]).toHaveProperty('projectId');
    });

    it('should handle empty batch', async () => {
      const projectIds: string[] = [];
      
      const results = await analyticsEngine.batchCalculateMetrics(projectIds);
      
      expect(results).toHaveLength(0);
    });

    it('should handle batch with invalid project IDs', async () => {
      const projectIds = [
        '123e4567-e89b-12d3-a456-426614174000',
        'invalid-project-id'
      ];
      
      const results = await analyticsEngine.batchCalculateMetrics(projectIds);
      
      expect(results).toHaveLength(1);
      expect(results[0]).toHaveProperty('projectId');
    });
  });

  describe('generateMetrics', () => {
    it('should include optimization opportunities', () => {
      const testProjectId = '123e4567-e89b-12d3-a456-426614174000';
      const metrics = analyticsEngine['generateMetrics'](testProjectId);
      
      expect(metrics.costAnalysis.optimizationOpportunities.length).toBeGreaterThan(0);
      expect(metrics.timelineMetrics).toHaveProperty('riskAssessment');
      expect(metrics).toHaveProperty('qualityMetrics');
    });

    it('should include cost analysis', () => {
      const testProjectId = '123e4567-e89b-12d3-a456-426614174000';
      const metrics = analyticsEngine['generateMetrics'](testProjectId);
      
      expect(metrics.costAnalysis).toHaveProperty('totalCost');
      expect(metrics.costAnalysis).toHaveProperty('costBreakdown');
    });

    it('should include timeline metrics', () => {
      const testProjectId = '123e4567-e89b-12d3-a456-426614174000';
      const metrics = analyticsEngine['generateMetrics'](testProjectId);
      
      expect(metrics.timelineMetrics).toHaveProperty('deploymentTimeline');
      expect(metrics.timelineMetrics).toHaveProperty('riskAssessment');
    });
  });

  describe('Alert Broadcasting', () => {
    test('should broadcast alerts via WebSocket', async () => {
      const mockBroadcast = jest.spyOn(webSocketService, 'broadcastAlerts');
      
      await analyticsEngine.getRealTimeInsights('test-project');
      
      expect(mockBroadcast).toHaveBeenCalled();
    });
  });
});
