jest.mock('engine.io', () => ({
  Server: jest.fn().mockImplementation(() => ({
    on: jest.fn(),
    emit: jest.fn(),
  })),
  wsEngine: jest.fn().mockImplementation(() => jest.fn()),  // Mock wsEngine as a constructor
}));

jest.mock('socket.io', () => {
  return {
    Server: jest.fn().mockImplementation(() => ({
      on: jest.fn(),
      emit: jest.fn(),
      to: jest.fn().mockReturnThis(),
      use: jest.fn().mockReturnThis()
    }))
  };
});

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

  test('should initialize successfully', () => {
    expect(webSocketService).toBeDefined();
    expect(WebSocketService.getInstance()).toBe(webSocketService);
  });

  test('should broadcast alerts', () => {
    const mockEmit = jest.fn();
    webSocketService['io'].to = jest.fn().mockReturnValue({ emit: mockEmit });
    
    const testAlerts = [{
      timestamp: new Date(),
      message: 'test alert',
      severity: 'medium' as const
    }];
    
    webSocketService.broadcastAlerts('test-project', testAlerts);
    
    expect(webSocketService['io'].to).toHaveBeenCalledWith('project-test-project');
    expect(mockEmit).toHaveBeenCalledWith('alert', {
      timestamp: expect.any(Date),
      alerts: testAlerts
    });
  });
});
