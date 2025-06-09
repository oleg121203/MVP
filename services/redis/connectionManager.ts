import { createClient } from 'redis';
import type { RedisClientType } from 'redis';

// Use mock in test environment, real package otherwise
const msgpack = process.env.NODE_ENV === 'test'
  ? require('msgpack-lite')
  : require('msgpack-lite');

const DEFAULT_POOL_SIZE = 5;

export class RedisConnectionManager {
  private pool: RedisClientType[] = [];
  private available: RedisClientType[] = [];

  constructor(poolSize: number = DEFAULT_POOL_SIZE) {
    for (let i = 0; i < poolSize; i++) {
      const client = createClient({
        url: process.env.REDIS_URL || 'redis://localhost:6379'
      }) as RedisClientType;
      this.pool.push(client);
      this.available.push(client);
    }
  }

  async getConnection(): Promise<RedisClientType> {
    while (this.available.length === 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return this.available.pop()!;
  }

  releaseConnection(client: RedisClientType): void {
    this.available.push(client);
  }

  async closeAll(): Promise<void> {
    await Promise.all(this.pool.map(client => client.quit()));
  }

  // Optimized serialization
  static serialize(data: any): string {
    return msgpack.encode(data).toString('base64');
  }

  static deserialize(data: string): any {
    return msgpack.decode(Buffer.from(data, 'base64'));
  }

  async getMarketData(projectId: string): Promise<any> {
    // Implementation to retrieve market data from Redis
  }

  async getHistoricalData(projectId: string): Promise<any[]> {
    // Implementation to retrieve historical data from Redis
  }
}
