import express, { Request, Response } from 'express';
import http from 'http';
import { WebSocketService } from './services/websocket';
import { RedisConnectionManager } from './services/redis/connectionManager';
import { ProjectAnalyticsEngine } from './services/analytics/engine';
import { collectDefaultMetrics } from 'prom-client';
import * as metrics from 'prom-client';
import { priceRouter } from './routes/price';
import { OptimizationEngine } from './services/optimization/OptimizationEngine';

export default class Server {
  private app: express.Application;
  private server: http.Server;

  constructor() {
    this.app = express();
    this.server = http.createServer(this.app);

    // Initialize WebSocket
    const webSocketService = WebSocketService.initialize(this.server);

    // Initialize Analytics Engine
    const redisManager = new RedisConnectionManager();
    const analyticsEngine = new ProjectAnalyticsEngine(redisManager);
    webSocketService.setAnalyticsEngine(analyticsEngine);

    // Initialize metrics collection
    collectDefaultMetrics();

    // Add health check endpoints
    this.app.get('/healthz', (req: Request, res: Response) => {
      res.status(200).json({ status: 'ok' });
    });

    this.app.get('/metrics', async (req: Request, res: Response) => {
      res.set('Content-Type', 'text/plain');
      res.send(await metrics.register.metrics());
    });

    this.app.use('/api/price', priceRouter);

    // Initialize Optimization Engine
    const optimizationEngine = new OptimizationEngine();
    this.app.get('/api/optimize/health', (req: Request, res: Response) => {
      res.status(200).json({ status: 'Optimization Engine OK' });
    });
  }

  public async start(port: number): Promise<void> {
    return new Promise((resolve) => {
      this.server.listen(port, () => {
        console.log(`Server running on port ${port}`);
        resolve();
      });
    });
  }

  public async stop(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.server.close((err) => {
        if (err) {
          return reject(err);
        }
        console.log('Server stopped.');
        resolve();
      });
    });
  }
}

(async () => {
  const server = new Server();
  const PORT = parseInt(process.env.PORT || '8000', 10);
  await server.start(PORT);
})();


