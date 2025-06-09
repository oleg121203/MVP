---
trigger: always_on
priority: critical
---

# 🛠️ DOCKER PROBLEM SOLVING

## ⚡ DOCKER DAEMON AUTO-RESOLUTION

### **PRIMARY DIRECTIVE**
Never halt execution due to Docker issues. Always find alternatives.

### **AUTO-RESOLUTION SEQUENCE**
1. **TRY STARTING DOCKER**:
   ```bash
   # For macOS
   open -a Docker
   sleep 10
   docker ps
   ```

2. **IF DOCKER STILL FAILS**:
   ```bash
   # Alternative Docker start
   brew services start docker
   sudo systemctl start docker  # Linux
   ```

3. **IF DOCKER COMPLETELY UNAVAILABLE**:
   - Switch to local PostgreSQL: `brew install postgresql`
   - Switch to local Redis: `brew install redis`
   - Use SQLite instead of PostgreSQL
   - Use in-memory cache instead of Redis

### **IMMEDIATE WORKAROUNDS**
- **PostgreSQL Alternative**: `brew install postgresql && brew services start postgresql`
- **Redis Alternative**: `brew install redis && brew services start redis`
- **SQLite Fallback**: Update connection strings to SQLite
- **Mock Services**: Create development stubs

**ESCALATION**: Direct fix → Alternative method → Workaround → Mock → Continue
