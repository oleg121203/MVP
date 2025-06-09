import { RedisConnectionManager } from '../../services/redis/connectionManager';
import type { RedisClientType } from 'redis';

describe('RedisConnectionManager', () => {
  let manager: RedisConnectionManager;
  
  beforeEach(() => {
    manager = new RedisConnectionManager(1);
  });
  
  it('should create with specified pool size', () => {
    expect(manager).toBeInstanceOf(RedisConnectionManager);
  });
  
  it('should get and release connections', async () => {
    const client = await manager.getConnection();
    expect(client).toBeDefined();
    manager.releaseConnection(client);
  });

  it('should serialize and deserialize data', () => {
    const testData = { key: 'value' };
    const serialized = RedisConnectionManager.serialize(testData);
    const deserialized = RedisConnectionManager.deserialize(serialized);
    expect(deserialized).toEqual(testData);
  });

  it('should handle pool exhaustion', async () => {
    // Single connection pool
    const singlePoolManager = new RedisConnectionManager(1); 
    const client1 = await singlePoolManager.getConnection();
    
    // Should wait when pool is exhausted
    await expect(
      Promise.race([
        singlePoolManager.getConnection(),
        new Promise(resolve => setTimeout(() => resolve('timeout'), 50))
      ])
    ).resolves.toBe('timeout');
    
    singlePoolManager.releaseConnection(client1);
  });

  it('should handle serialization errors', () => {
    const circularObj: any = { self: null };
    circularObj.self = circularObj;
    
    expect(() => RedisConnectionManager.serialize(circularObj))
      .toThrow();
  });

  it('should handle deserialization errors', () => {
    expect(() => RedisConnectionManager.deserialize('invalid-data'))
      .toThrow();
  });
});
