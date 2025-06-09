import { Server } from 'http';
import { Server as SocketServer, Socket } from 'socket.io';
import { ProjectAnalyticsEngine } from './analytics/engine';

type AlertItem = {
  timestamp: Date;
  message: string;
  severity: 'low' | 'medium' | 'high';
};

export class WebSocketService {
  private static instance: WebSocketService;
  private io: SocketServer;
  private analyticsEngine?: ProjectAnalyticsEngine;

  private constructor(httpServer: Server) {
    this.io = new SocketServer(httpServer, {
      cors: {
        origin: process.env.FRONTEND_URL || "http://localhost:3000",
        methods: ["GET", "POST"]
      }
    });

    this.setupConnectionHandlers();
  }

  static initialize(httpServer: Server): WebSocketService {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService(httpServer);
    }
    return WebSocketService.instance;
  }

  static getInstance(): WebSocketService {
    if (!WebSocketService.instance) {
      throw new Error('WebSocketService not initialized');
    }
    return WebSocketService.instance;
  }

  setAnalyticsEngine(engine: ProjectAnalyticsEngine): void {
    this.analyticsEngine = engine;
  }

  private setupConnectionHandlers(): void {
    this.io.on('connection', (socket: Socket) => {
      socket.on('join-project-room', (projectId: string) => {
        socket.join(`project-${projectId}`);
      });

      socket.on('disconnect', () => {
        console.log('Client disconnected');
      });
    });
  }

  broadcastAlerts(projectId: string, alerts: AlertItem[]): void {
    if (alerts.length > 0) {
      this.io.to(`project-${projectId}`).emit('alert', {
        timestamp: new Date(),
        alerts
      });
    }
  }
}
