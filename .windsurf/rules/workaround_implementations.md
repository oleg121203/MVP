---
trigger: always_on
priority: medium
---

# 📝 WORKAROUND IMPLEMENTATIONS

## MOCK SERVICE CREATION
When real services fail, create immediate replacements:

```typescript
// Mock database service
class MockDatabase {
  private data = new Map();
  
  async query(sql: string, params?: any[]) {
    // Return mock data based on query
    return { rows: [], rowCount: 0 };
  }
}

// Mock Redis service
class MockRedis {
  private cache = new Map();
  
  async get(key: string) {
    return this.cache.get(key);
  }
  
  async set(key: string, value: string) {
    this.cache.set(key, value);
  }
}
```

## FILE-BASED ALTERNATIVES
```typescript
// File-based storage when databases fail
import fs from 'fs/promises';

class FileStorage {
  async save(key: string, data: any) {
    await fs.writeFile(`./data/${key}.json`, JSON.stringify(data));
  }
  
  async load(key: string) {
    try {
      const data = await fs.readFile(`./data/${key}.json`, 'utf8');
      return JSON.parse(data);
    } catch {
      return null;
    }
  }
}
```

## POSTGRESQL ALTERNATIVES
```bash
# Try local PostgreSQL
brew install postgresql
brew services start postgresql

# Or use embedded SQLite
pip install sqlite3
# Update connection strings to use SQLite
```

## REDIS ALTERNATIVES
```bash
# Try local Redis
brew install redis
brew services start redis

# Or use in-memory alternative
pip install fakeredis
# Update Redis clients to use fakeredis
```

## QUICK MOCK GENERATORS
```typescript
// Quick API mock
const mockAPI = {
  get: async (url: string) => ({ data: {}, status: 200 }),
  post: async (url: string, data: any) => ({ data: { id: 1 }, status: 201 })
};

// Quick auth mock
const mockAuth = {
  login: async () => ({ token: 'dev-token', user: { id: 1 } }),
  verify: async () => true
};

// Quick cache mock
const mockCache = new Map();
```
