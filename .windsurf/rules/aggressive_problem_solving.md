---
trigger: always_on
priority: critical
---

# 🛠️ AGGRESSIVE PROBLEM SOLVING PROTOCOL

## ⚡ NEVER STOP EXECUTION RULES
**PRIMARY DIRECTIVE: ALWAYS FIND A WAY FORWARD**
When encountering ANY blocker, immediately activate escalation ladder instead of stopping execution.

## 🚨 DOCKER DAEMON ISSUES
**AUTO-RESOLUTION SEQUENCE:**
1. **TRY STARTING DOCKER:**
   ```bash
   # For macOS
   open -a Docker
   # Wait 10 seconds, then try
   docker ps
   
   # Alternative for macOS
   brew services start docker
   
   # For Linux
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

2. **IF DOCKER STILL FAILS:**
   - Switch to local PostgreSQL installation
   - Use in-memory Redis alternative
   - Create file-based storage temporarily

## 🔧 SERVICE DEPENDENCY FAILURES
**DATABASE CONNECTION ISSUES:**
1. **PostgreSQL unreachable:**
   - Try different ports (5432, 5433, 5434)
   - Use SQLite as temporary replacement
   - Create mock database layer

2. **Redis unreachable:**
   - Try different ports (6379, 6380)
   - Use in-memory dictionary
   - Create cache stub implementation

**NETWORK SERVICE FAILURES:**
1. **External APIs down:**
   - Use cached responses
   - Create mock API responses
   - Switch to alternative endpoints

2. **Authentication services unavailable:**
   - Use development tokens
   - Create mock auth layer
   - Skip auth temporarily

## 🚀 SYSTEM DEPENDENCY ISSUES
**MISSING TOOLS:**
```bash
# Auto-install missing tools
# For macOS
brew install <tool-name>

# For Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y <tool-name>

# For Python packages
pip install <package-name>

# For Node packages
npm install -g <package-name>
```

**PERMISSION ERRORS:**
```bash
# Fix common permission issues
sudo chmod +x script.sh
sudo chown -R $USER:$USER directory/
```

**PORT CONFLICTS:**
```bash
# Find alternative ports
lsof -i :3000  # Check what's using port 3000
# Use ports 3001, 3002, 8000, 8080 as alternatives
```

## 🎯 ESCALATION DECISION TREE
```
Problem Encountered
↓
Try Direct Fix (30 seconds max)
↓
Still Failed?
↓
Try Alternative Method (60 seconds max)
↓
Still Failed?
↓
Create Workaround/Mock (2 minutes max)
↓
Still Failed?
↓
Document as Autoticket + Continue to Next Task
```

## 🚀 IMPLEMENTATION EXAMPLES

### **Docker Daemon Failed Scenario**
```bash
# 1. Try to start Docker
open -a Docker
sleep 10

# 2. If still failed, switch to local services
brew install postgresql redis
brew services start postgresql redis

# 3. Update connection strings
# DATABASE_URL=postgresql://localhost:5432/ventai
# REDIS_URL=redis://localhost:6379

# 4. Continue with development
npm run dev
```

### **External API Failed Scenario**
```typescript
// 1. Try with retry logic
const apiCall = async (retries = 3) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(API_URL);
    } catch (error) {
      if (i === retries - 1) {
        // 2. Switch to mock data
        return { data: MOCK_RESPONSE };
      }
      await sleep(1000 * (i + 1));
    }
  }
};
```

---

## ⚡ SUCCESS METRICS

### **PROBLEM RESOLUTION KPIs**
- **< 3 minutes**: Total time spent on any single blocker
- **> 95%**: Success rate in finding alternatives
- **Zero stops**: Never halt execution due to external dependencies
- **Auto-documentation**: All workarounds documented in autotickets

### **CONTINUATION PRIORITY**
1. **Feature functionality** > Perfect infrastructure
2. **Development progress** > Ideal setup
3. **Working solutions** > Elegant solutions
4. **Documentation** > Immediate fixes

---

**⚡ CORE PRINCIPLE: Every problem has multiple solutions. If approach A fails, immediately try B, C, D, etc. NEVER STOP.**
