# 🎯 **Enterprise Vector MCP Configuration для Claude Desktop**

```json
{
  "mcpServers": {
    "windsurf-enterprise-vector": {
      "command": "node",
      "args": [
        "/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/dist/enterprise-index.js",
        "/Users/olegkizyma/workspaces/MVP/ventai-app"
      ],
      "env": {
        "DATABASE_URL": "postgresql://ventai_dev:ventai_dev_password@localhost:5433/ventai_dev",
        "REDIS_URL": "redis://localhost:6380",
        "WINDSURF_ROOT": "/Users/olegkizyma/workspaces/MVP/ventai-app",
        "ENABLE_VECTOR_SEARCH": "true",
        "ENABLE_GRAPH_RELATIONS": "true",
        "NODE_ENV": "production"
      }
    }
  }
}
```

## 🔧 **Інтеграція з frontend/src/store.ts**

```typescript
// frontend/src/store.ts - Додати векторну інтеграцію

interface VectorMCPState {
  // Векторний пошук
  searchResults: VectorDocument[];
  searchQuery: string;
  isSearching: boolean;
  
  // Графові зв'язки
  graphNodes: GraphNode[];
  selectedNode: string | null;
  relationshipDepth: number;
  
  // Розумні рекомендації
  recommendations: VectorDocument[];
  contextualHelp: string[];
  
  // Синхронізація
  lastVectorSync: Date | null;
  autoSyncEnabled: boolean;
  syncStatus: 'idle' | 'syncing' | 'error';
  
  // Аналітика
  documentStats: {
    totalDocuments: number;
    vectorizedDocuments: number;
    graphRelationships: number;
  };
}

// MCP клієнт для векторних операцій
class VectorMCPClient {
  async vectorSearch(query: string, limit = 10): Promise<VectorDocument[]> {
    return await this.callMCP('vector_search_documents', { 
      query, 
      limit, 
      includeContent: true 
    });
  }
  
  async getSmartRecommendations(context: string): Promise<VectorDocument[]> {
    return await this.callMCP('smart_recommendations', { 
      context, 
      limit: 5 
    });
  }
  
  async exploreGraphRelations(nodeId: string, depth = 2): Promise<GraphNode[]> {
    return await this.callMCP('graph_relations', { 
      nodeId, 
      depth 
    });
  }
  
  async syncToVector(paths?: string[]): Promise<void> {
    await this.callMCP('sync_to_vector_store', { 
      paths, 
      forceResync: false 
    });
  }
  
  private async callMCP(tool: string, args: any): Promise<any> {
    // Інтеграція з MCP protocol через stdio або HTTP
    // Реалізація залежить від вашого MCP клієнта
  }
}

// Redux slice для векторних операцій
const vectorSlice = createSlice({
  name: 'vector',
  initialState: {
    searchResults: [],
    searchQuery: '',
    isSearching: false,
    recommendations: [],
    graphNodes: [],
    documentStats: { totalDocuments: 0, vectorizedDocuments: 0, graphRelationships: 0 }
  } as VectorMCPState,
  
  reducers: {
    setSearchQuery: (state, action) => {
      state.searchQuery = action.payload;
    },
    
    setSearchResults: (state, action) => {
      state.searchResults = action.payload;
      state.isSearching = false;
    },
    
    setRecommendations: (state, action) => {
      state.recommendations = action.payload;
    },
    
    setGraphNodes: (state, action) => {
      state.graphNodes = action.payload;
    },
    
    updateDocumentStats: (state, action) => {
      state.documentStats = action.payload;
    }
  }
});

// Async thunks для векторних операцій
export const searchDocuments = createAsyncThunk(
  'vector/searchDocuments',
  async ({ query, type }: { query: string; type?: string }) => {
    const client = new VectorMCPClient();
    return await client.vectorSearch(query, 10);
  }
);

export const getContextualRecommendations = createAsyncThunk(
  'vector/getRecommendations',
  async (context: string) => {
    const client = new VectorMCPClient();
    return await client.getSmartRecommendations(context);
  }
);
```

## 🕸️ **GraphChain інтеграція для фазових зв'язків**

```typescript
// Автоматичне створення графових зв'язків між фазами
const autoCreatePhaseRelations = async () => {
  const mcpClient = new VectorMCPClient();
  
  // Фазові залежності
  const phaseRelations = [
    { source: 'phase_1.1', target: 'phase_1.2', type: 'TRIGGERS' },
    { source: 'phase_1.2', target: 'phase_1.3', type: 'TRIGGERS' },
    { source: 'phase_2.0', target: 'phase_2.1', type: 'PART_OF' },
    { source: 'changelog_master', target: 'phase_1.1', type: 'CONTAINS' }
  ];
  
  for (const relation of phaseRelations) {
    await mcpClient.callMCP('create_graph_relation', relation);
  }
};

// Аналіз залежностей завдань
const analyzeTaskDependencies = async (currentPhase: string) => {
  const mcpClient = new VectorMCPClient();
  
  // Отримання графу для поточної фази
  const graph = await mcpClient.exploreGraphRelations(currentPhase, 3);
  
  // Аналіз блокуючих завдань
  const blockers = graph.filter(node => 
    node.relationships.some(rel => 
      rel.type === 'DEPENDS_ON' && rel.target === currentPhase
    )
  );
  
  return {
    blockers,
    dependencies: graph,
    recommendations: await mcpClient.getSmartRecommendations(
      `Complete dependencies for ${currentPhase}`
    )
  };
};
```
