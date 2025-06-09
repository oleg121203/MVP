import io from 'socket.io-client';
import { Server } from '../../server';
import { RedisConnectionManager } from '../../services/redis/connectionManager';
import { ProjectAnalyticsEngine } from '../../services/analytics/engine';

describe('WebSocket Integration', () => {
  let server: Server;
  let analyticsEngine: ProjectAnalyticsEngine;
  
  beforeAll(async () => {
    server = new Server();
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
