import { Server } from 'http';
import { WebSocketService } from '../services/websocket';
import io from 'socket.io-client';

describe('WebSocketService', () => {
  let httpServer: Server;
  let webSocketService: WebSocketService;
  
  beforeAll(() => {
    httpServer = new Server();
    webSocketService = WebSocketService.initialize(httpServer);
  });

  afterAll(() => {
    httpServer.close();
  });

  test('should broadcast alerts to project room', (done) => {
    const client = io('http://localhost:8000');
    
    client.on('connect', () => {
      client.emit('join-project-room', 'test-project');
      
      client.on('alert', (data) => {
        expect(data.alerts).toHaveLength(1);
        expect(data.alerts[0].message).toContain('test alert');
        client.disconnect();
        done();
      });
      
      webSocketService.broadcastAlerts('test-project', [{
        timestamp: new Date(),
        message: 'test alert',
        severity: 'medium'
      }]);
    });
  });
});
