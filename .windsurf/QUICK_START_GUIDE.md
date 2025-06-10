# 🚀 Windsurf AI Integration - Quick Start Guide

## ⚡ **IMMEDIATE USAGE** (Production Ready)

### **1. Start the HTTP MCP Server**
```bash
cd /Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server
npm run start:http
```
Server will be available at: `http://localhost:8001`

### **2. Frontend Integration**
```javascript
// Import the enhanced service
import { WindsurfExactModelsService } from './src/services/windsurfExactModels.js';

// Initialize
const windsurfAI = new WindsurfExactModelsService();

// Get all providers and models
const providers = await windsurfAI.listProviders();
console.log(`Available: ${providers.length} providers with ${windsurfAI.getTotalModels()} models`);

// Chat with AI
const response = await windsurfAI.chatWithAI(
    "Hello! Please explain HVAC optimization.", 
    "claude-3-5-sonnet-20241022"
);
```

### **3. React Component Usage**
```jsx
import { WindsurfModelsShowcase } from './src/components/WindsurfModelsShowcase.jsx';

function App() {
  return (
    <div>
      <h1>VentAI with Windsurf AI</h1>
      <WindsurfModelsShowcase />
    </div>
  );
}
```

### **4. Direct API Calls**
```javascript
// List all AI providers
const response = await fetch('http://localhost:8001/mcp/call-tool', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    tool: 'list_ai_providers', 
    params: {} 
  })
});

// Chat with specific model
const chatResponse = await fetch('http://localhost:8001/mcp/call-tool', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    tool: 'ai_chat_completion', 
    params: {
      message: "Your question here",
      model_id: "windsurf-swe-1",
      vendor: "windsurf"
    }
  })
});
```

## 💎 **FREE MODELS** (Cost Optimization)

### **Available Free Models**
```javascript
const freeModels = [
  { id: 'windsurf-swe-1', name: 'SWE-1', vendor: 'windsurf' },
  { id: 'windsurf-swe-1-lite', name: 'SWE-1-lite', vendor: 'windsurf' },
  { id: 'deepseek-v3', name: 'DeepSeek V3', vendor: 'deepseek' }
];
```

### **Low-Cost Models**
```javascript
const lowCostModels = [
  { id: 'gpt-4o-mini', name: 'GPT-4o mini', vendor: 'openai', credits: '0.1x' },
  { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', vendor: 'google', credits: '0.1x' }
];
```

## 🎪 **DEMO & TESTING**

### **Run Complete Demo**
```bash
cd /Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server
node demo-simple.js
```

### **Run Integration Test**
```bash
node final-integration-test.js
```

### **Health Check**
```bash
curl http://localhost:8001/health
```

## 🔧 **AVAILABLE TOOLS** (21 Total)

### **AI-Specific Tools**
- `list_ai_providers` - Get all providers and models
- `ai_chat_completion` - Chat with any AI model
- `ai_windsurf_assistant` - Windsurf-context assistant
- `ai_code_analysis` - AI-powered code analysis
- `ai_create_embeddings` - Create text embeddings
- `ai_test_providers` - Test provider availability

### **File & Vector Operations**
- `read_file` - Read with vector indexing
- `write_file` - Write with vector indexing  
- `vector_search_documents` - Semantic search
- `smart_recommendations` - AI recommendations
- `graph_relations` - Document relationships

## 📊 **MODEL SELECTION STRATEGY**

### **By Task Type**
```javascript
// Code tasks -> Use Windsurf SWE models
const codeModel = 'windsurf-swe-1';

// Complex reasoning -> Use Claude or o3-mini
const reasoningModel = 'claude-3-7-sonnet-thinking';

// Quick queries -> Use mini models
const quickModel = 'gpt-4o-mini';

// Cost optimization -> Use free models
const freeModel = 'deepseek-v3';
```

### **Smart Selection Logic**
```javascript
const service = new WindsurfExactModelsService();

// Get best model for task
const bestModel = service.selectBestModel('code_analysis');

// Get free models only
const freeModels = service.getFreeModels();

// Get reasoning models
const reasoningModels = service.getReasoningModels();
```

## 🔥 **PRODUCTION CHECKLIST**

### **✅ Ready for Immediate Use**
- [x] HTTP MCP Server operational
- [x] All 11 models accessible
- [x] Frontend service created
- [x] React components ready
- [x] Demo scripts validated
- [x] Documentation complete

### **🚀 Deployment Commands**
```bash
# 1. Start MCP server
npm run start:http

# 2. Verify health
curl http://localhost:8001/health

# 3. Test integration
node demo-simple.js

# 4. Ready for frontend integration!
```

---

**🎯 Status**: ✅ **PRODUCTION READY**  
**🌊 Integration**: **100% COMPLETE**  
**🚀 Next Action**: **Deploy to production** or **integrate with existing frontend**
