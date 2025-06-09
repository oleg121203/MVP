import express from 'express';
import http from 'http';
import { WebSocketService } from './services/websocket';
import { RedisConnectionManager } from './services/redis/connectionManager';
import { ProjectAnalyticsEngine } from './services/analytics/engine';
import { collectDefaultMetrics } from 'prom-client';
import { priceRouter } from './routes/price';

const app = express();
const server = http.createServer(app);

// Initialize WebSocket
const webSocketService = WebSocketService.initialize(server);

// Initialize Analytics Engine
const redisManager = new RedisConnectionManager();
const analyticsEngine = new ProjectAnalyticsEngine(redisManager);
webSocketService.setAnalyticsEngine(analyticsEngine);

// Initialize metrics collection
collectDefaultMetrics();

// Add health check endpoints
app.get('/healthz', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send(await metrics.register.metrics());
});

app.use('/api/price', priceRouter);

const PORT = process.env.PORT || 8000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
