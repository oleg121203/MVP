import io from 'socket.io-client';
import { createServer } from '../../server';
import { RedisConnectionManager } from '../../services/redis/connectionManager';
import { ProjectAnalyticsEngine } from '../../services/analytics/engine';

describe('WebSocket Integration', () => {
  let server: any;
  let analyticsEngine: ProjectAnalyticsEngine;
  
  beforeAll(async () => {
    server = createServer();
    await server.start();
    const redisManager = new RedisConnectionManager();
    analyticsEngine = new ProjectAnalyticsEngine(redisManager);
  });

  afterAll(async () => {
    await server.stop();
  });

  test('should broadcast alerts from engine to client', (done) => {
    const client = io('http://localhost:8000');
    
    client.on('connect', () => {
      client.emit('join-project-room', 'test-project');
      
      client.on('alert', (data: { alerts: Array<{message: string}> }) => {
        expect(data.alerts).toBeDefined();
        expect(data.alerts.length).toBeGreaterThan(0);
        client.disconnect();
        done();
      });
      
      analyticsEngine.getRealTimeInsights('test-project');
    });
  });
});
