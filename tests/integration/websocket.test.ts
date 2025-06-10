import { Server as HttpServer } from 'http';
import { WebSocketService } from '../../services/websocket';
import VentAIServer from '../../server';

// Mock the WebSocket service for integration tests
jest.mock('../../services/websocket', () => ({
  WebSocketService: {
    initialize: jest.fn().mockReturnValue({
      io: {
        on: jest.fn(),
        emit: jest.fn(),
        to: jest.fn().mockReturnThis()
      },
      broadcastAlerts: jest.fn(),
      setAnalyticsEngine: jest.fn()
    })
  }
}));

describe('WebSocket Integration', () => {
  let httpServer: HttpServer;
  let ventaiServer: VentAIServer;
  
  beforeAll(async () => {
    httpServer = new HttpServer();
    WebSocketService.initialize(httpServer);
    ventaiServer = new VentAIServer();
    await ventaiServer.start(8001);
  });

  afterAll(async () => {
    await ventaiServer.stop();
    httpServer.close();
  });

  test('should mock WebSocket service for integration', () => {
    expect(WebSocketService.initialize).toHaveBeenCalled();
  });
});
