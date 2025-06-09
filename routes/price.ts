import { Request, Response, Router } from 'express';
import { PriceAnalysisEngine } from '../services/price/engine';
import { RedisConnectionManager } from '../services/redis/connectionManager';

export const priceRouter = Router();
const redisManager = new RedisConnectionManager();
const priceEngine = new PriceAnalysisEngine(redisManager);

// Get pricing recommendations
priceRouter.get('/:projectId/recommendation', async (req: Request, res: Response) => {
  try {
    const marketData = await redisManager.getMarketData(req.params.projectId);
    const competitors = await priceEngine.collectMarketData();
    const recommendation = await priceEngine.generateRecommendation(
      req.params.projectId,
      marketData,
      competitors
    );
    res.json(recommendation);
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate pricing recommendation' });
  }
});

// Get price trends analysis
priceRouter.get('/:projectId/trends', async (req: Request, res: Response) => {
  try {
    const historicalData = await redisManager.getHistoricalData(req.params.projectId);
    const trends = await priceEngine.calculatePriceTrends(req.params.projectId, historicalData);
    res.json(trends);
  } catch (error) {
    res.status(500).json({ error: 'Failed to calculate price trends' });
  }
});
