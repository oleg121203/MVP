import io from 'socket.io-client';

console.log('NODE_PATH:', process.env.NODE_PATH);

try {
  console.log('Express resolved from:', require.resolve('express'));
} catch (e) {
  console.error('Could not resolve express:', (e as Error).message);
}
import Server from '../../server';
import { RedisConnectionManager } from '../../services/redis/connectionManager';
import { ProjectAnalyticsEngine } from '../../services/analytics/engine';

describe('WebSocket Integration', () => {
  let server: any;
  let analyticsEngine: ProjectAnalyticsEngine;
  
  beforeAll(async () => {
    const PORT = 8001; // Use a different port for integration tests
    server = new Server();
    await server.start(PORT);
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
