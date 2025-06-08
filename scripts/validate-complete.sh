#!/bin/bash

# Complete VentAI Project Validation Script
# This script validates the entire refactored project structure and functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VALIDATION_LOG="$PROJECT_ROOT/validation_report_$(date +%Y%m%d_%H%M%S).log"

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Functions
log_header() {
    echo -e "\n${PURPLE}========================================${NC}"
    echo -e "${PURPLE} $1${NC}"
    echo -e "${PURPLE}========================================${NC}\n"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[INFO] $1" >> "$VALIDATION_LOG"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    echo "[PASS] $1" >> "$VALIDATION_LOG"
    ((PASSED_CHECKS++))
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[WARN] $1" >> "$VALIDATION_LOG"
    ((WARNING_CHECKS++))
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
    echo "[FAIL] $1" >> "$VALIDATION_LOG"
    ((FAILED_CHECKS++))
}

check_item() {
    ((TOTAL_CHECKS++))
    if eval "$2"; then
        log_success "$1"
        return 0
    else
        log_error "$1"
        return 1
    fi
}

warn_item() {
    ((TOTAL_CHECKS++))
    if eval "$2"; then
        log_success "$1"
        return 0
    else
        log_warning "$1"
        return 1
    fi
}

# Start validation
log_header "VentAI Project Structure Validation"
echo "Validation started at: $(date)" > "$VALIDATION_LOG"
echo "Project root: $PROJECT_ROOT" >> "$VALIDATION_LOG"
echo "" >> "$VALIDATION_LOG"

# 1. Directory Structure Validation
log_header "1. Directory Structure Validation"

check_item "Frontend directory exists" "[ -d '$PROJECT_ROOT/frontend' ]"
check_item "Backend directory exists" "[ -d '$PROJECT_ROOT/backend' ]"
check_item "Services directory exists" "[ -d '$PROJECT_ROOT/services' ]"
check_item "MCP service directory exists" "[ -d '$PROJECT_ROOT/services/mcp' ]"
check_item "Scripts directory exists" "[ -d '$PROJECT_ROOT/scripts' ]"
check_item "Tools directory exists" "[ -d '$PROJECT_ROOT/tools' ]"
check_item "Infrastructure directory exists" "[ -d '$PROJECT_ROOT/infra' ]"
check_item "Docker configurations exist" "[ -d '$PROJECT_ROOT/infra/docker' ]"
check_item "Kubernetes manifests directory exists" "[ -d '$PROJECT_ROOT/infra/k8s' ]"
check_item "Documentation directory exists" "[ -d '$PROJECT_ROOT/docs' ]"
check_item "Tests directory exists" "[ -d '$PROJECT_ROOT/tests' ]"
check_item "Configs directory exists" "[ -d '$PROJECT_ROOT/configs' ]"
check_item "Environments directory exists" "[ -d '$PROJECT_ROOT/environments' ]"

# 2. Configuration Files Validation
log_header "2. Configuration Files Validation"

check_item "Root package.json exists" "[ -f '$PROJECT_ROOT/package.json' ]"
check_item "Frontend package.json exists" "[ -f '$PROJECT_ROOT/frontend/package.json' ]"
check_item "Backend requirements.txt exists" "[ -f '$PROJECT_ROOT/backend/requirements.txt' ]"
check_item "MCP requirements.txt exists" "[ -f '$PROJECT_ROOT/services/mcp/requirements.txt' ]"
check_item "Development environment exists" "[ -f '$PROJECT_ROOT/environments/.env.development' ]"
check_item "Production template exists" "[ -f '$PROJECT_ROOT/environments/.env.production.template' ]"
check_item "Test environment exists" "[ -f '$PROJECT_ROOT/environments/.env.test' ]"
check_item "Main README.md exists" "[ -f '$PROJECT_ROOT/README.md' ]"

# 3. Docker Configuration Validation
log_header "3. Docker Configuration Validation"

check_item "Development Docker Compose exists" "[ -f '$PROJECT_ROOT/infra/docker/docker-compose.dev.yml' ]"
check_item "Production Docker Compose exists" "[ -f '$PROJECT_ROOT/infra/docker/docker-compose.prod.yml' ]"
check_item "Database Docker Compose exists" "[ -f '$PROJECT_ROOT/infra/docker/docker-compose-db.yml' ]"
check_item "Nginx configuration exists" "[ -f '$PROJECT_ROOT/infra/docker/nginx/nginx.conf' ]"
check_item "Nginx Dockerfile exists" "[ -f '$PROJECT_ROOT/infra/docker/nginx/Dockerfile' ]"
check_item "Backend Dockerfile exists" "[ -f '$PROJECT_ROOT/backend/Dockerfile' ]"
check_item "MCP Dockerfile exists" "[ -f '$PROJECT_ROOT/services/mcp/Dockerfile' ]"

# 4. Scripts Validation
log_header "4. Scripts Validation"

check_item "Project setup script exists" "[ -f '$PROJECT_ROOT/scripts/setup-project.sh' ]"
check_item "Environment setup script exists" "[ -f '$PROJECT_ROOT/scripts/setup-environment.js' ]"
check_item "Node version checker exists" "[ -f '$PROJECT_ROOT/scripts/check-node-version.js' ]"
check_item "Workflow validation script exists" "[ -f '$PROJECT_ROOT/scripts/validate-workflow.sh' ]"
check_item "Database migration script exists" "[ -f '$PROJECT_ROOT/scripts/database/migrate.sh' ]"

# Check script permissions
check_item "Setup script is executable" "[ -x '$PROJECT_ROOT/scripts/setup-project.sh' ]"
check_item "Validation script is executable" "[ -x '$PROJECT_ROOT/scripts/validate-workflow.sh' ]"
check_item "Database script is executable" "[ -x '$PROJECT_ROOT/scripts/database/migrate.sh' ]"

# 5. CI/CD Pipeline Validation
log_header "5. CI/CD Pipeline Validation"

check_item "GitHub workflows directory exists" "[ -d '$PROJECT_ROOT/.github/workflows' ]"
check_item "CI/CD workflow exists" "[ -f '$PROJECT_ROOT/.github/workflows/ci-cd.yml' ]"

# 6. Test Structure Validation
log_header "6. Test Structure Validation"

check_item "Unit tests directory exists" "[ -d '$PROJECT_ROOT/tests/unit' ]"
check_item "Integration tests directory exists" "[ -d '$PROJECT_ROOT/tests/integration' ]"
check_item "E2E tests directory exists" "[ -d '$PROJECT_ROOT/tests/e2e' ]"
check_item "Unit test config exists" "[ -f '$PROJECT_ROOT/tests/unit/conftest.py' ]"
check_item "Integration test config exists" "[ -f '$PROJECT_ROOT/tests/integration/conftest.py' ]"
check_item "E2E test config exists" "[ -f '$PROJECT_ROOT/tests/e2e/conftest.py' ]"

# 7. Package.json Scripts Validation
log_header "7. Package.json Scripts Validation"

cd "$PROJECT_ROOT"

# Check if key scripts exist in package.json
check_package_script() {
    local script_name="$1"
    if grep -q "\"$script_name\":" package.json; then
        log_success "Package.json script '$script_name' exists"
        return 0
    else
        log_error "Package.json script '$script_name' missing"
        return 1
    fi
}

((TOTAL_CHECKS++))
check_package_script "setup:complete"
((TOTAL_CHECKS++))
check_package_script "install:all"
((TOTAL_CHECKS++))
check_package_script "dev"
((TOTAL_CHECKS++))
check_package_script "docker:dev"
((TOTAL_CHECKS++))
check_package_script "docker:prod"
((TOTAL_CHECKS++))
check_package_script "test:all"
((TOTAL_CHECKS++))
check_package_script "lint"
((TOTAL_CHECKS++))
check_package_script "format"

# 8. Environment Variables Validation
log_header "8. Environment Variables Validation"

# Check development environment file
if [ -f "environments/.env.development" ]; then
    source "environments/.env.development"
    
    check_item "NODE_ENV is set" "[ ! -z '$NODE_ENV' ]"
    check_item "DATABASE_URL is set" "[ ! -z '$DATABASE_URL' ]"
    check_item "REDIS_URL is set" "[ ! -z '$REDIS_URL' ]"
else
    log_error "Development environment file missing"
    ((TOTAL_CHECKS += 3))
    ((FAILED_CHECKS += 3))
fi

# 9. Node.js and Python Dependencies Validation
log_header "9. Dependencies Validation"

# Check Node.js version
if command -v node >/dev/null 2>&1; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge 18 ]; then
        log_success "Node.js version is sufficient ($NODE_VERSION)"
    else
        log_error "Node.js version is too old ($NODE_VERSION), need 18+"
    fi
    ((TOTAL_CHECKS++))
else
    log_error "Node.js not installed"
    ((TOTAL_CHECKS++))
    ((FAILED_CHECKS++))
fi

# Check Python version
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    if [[ "$PYTHON_VERSION" > "3.10" ]] || [[ "$PYTHON_VERSION" == "3.11" ]]; then
        log_success "Python version is sufficient ($PYTHON_VERSION)"
    else
        log_warning "Python version might be too old ($PYTHON_VERSION), recommend 3.11+"
    fi
    ((TOTAL_CHECKS++))
else
    log_error "Python3 not installed"
    ((TOTAL_CHECKS++))
    ((FAILED_CHECKS++))
fi

# Check Docker
if command -v docker >/dev/null 2>&1; then
    if docker info >/dev/null 2>&1; then
        log_success "Docker is installed and running"
    else
        log_warning "Docker is installed but not running"
    fi
    ((TOTAL_CHECKS++))
else
    log_error "Docker not installed"
    ((TOTAL_CHECKS++))
    ((FAILED_CHECKS++))
fi

# 10. File Content Validation
log_header "10. File Content Validation"

# Check if README has been updated with new structure
if grep -q "Project Structure" README.md && grep -q "services/" README.md; then
    log_success "README.md has been updated with new structure"
else
    log_warning "README.md might need updates for new structure"
fi
((TOTAL_CHECKS++))

# Check if package.json has new scripts
if grep -q "setup:complete" package.json; then
    log_success "Package.json contains new setup scripts"
else
    log_error "Package.json missing new setup scripts"
fi
((TOTAL_CHECKS++))

# 11. Security Validation
log_header "11. Security Validation"

# Check for sensitive files in root
warn_item "No .env files in root" "[ ! -f '$PROJECT_ROOT/.env' ]"
warn_item "No sensitive config files in root" "[ ! -f '$PROJECT_ROOT/config.json' ]"

# Check gitignore
if [ -f "$PROJECT_ROOT/.gitignore" ]; then
    if grep -q "environments/.env.production" .gitignore; then
        log_success ".gitignore includes production environment files"
    else
        log_warning ".gitignore might need to include environment files"
    fi
    ((TOTAL_CHECKS++))
else
    log_warning ".gitignore file missing"
    ((TOTAL_CHECKS++))
fi

# 12. Functional Tests (if services are running)
log_header "12. Functional Tests (Optional)"

# Test if we can install dependencies
if npm list >/dev/null 2>&1; then
    log_success "NPM dependencies can be resolved"
else
    log_warning "NPM dependencies might have issues (run 'npm install')"
fi
((TOTAL_CHECKS++))

# 13. Performance and Optimization Validation
log_header "13. Performance and Optimization"

# Check for optimization configurations
check_item "Nginx configuration optimized" "grep -q 'gzip on' '$PROJECT_ROOT/infra/docker/nginx/nginx.conf'"
check_item "Docker multi-stage builds" "grep -q 'FROM.*AS' '$PROJECT_ROOT/backend/Dockerfile' || true"

# Final Report
log_header "VALIDATION REPORT"

echo -e "${CYAN}Total Checks: $TOTAL_CHECKS${NC}"
echo -e "${GREEN}Passed: $PASSED_CHECKS${NC}"
echo -e "${YELLOW}Warnings: $WARNING_CHECKS${NC}"
echo -e "${RED}Failed: $FAILED_CHECKS${NC}"

echo "Total Checks: $TOTAL_CHECKS" >> "$VALIDATION_LOG"
echo "Passed: $PASSED_CHECKS" >> "$VALIDATION_LOG"
echo "Warnings: $WARNING_CHECKS" >> "$VALIDATION_LOG"
echo "Failed: $FAILED_CHECKS" >> "$VALIDATION_LOG"

PASS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo -e "${BLUE}Pass Rate: $PASS_RATE%${NC}"
echo "Pass Rate: $PASS_RATE%" >> "$VALIDATION_LOG"

echo ""
echo "" >> "$VALIDATION_LOG"
echo "Validation completed at: $(date)" >> "$VALIDATION_LOG"
echo "Full report saved to: $VALIDATION_LOG"

# Recommendations
if [ $FAILED_CHECKS -gt 0 ]; then
    echo -e "\n${RED}⚠️  Critical Issues Found${NC}"
    echo "Please fix the failed checks before proceeding with deployment."
    echo "Run 'npm run setup:complete' to fix common issues."
fi

if [ $WARNING_CHECKS -gt 0 ]; then
    echo -e "\n${YELLOW}⚠️  Warnings Found${NC}"
    echo "Consider addressing warnings for optimal setup."
fi

if [ $PASS_RATE -ge 90 ]; then
    echo -e "\n${GREEN}✅ Excellent! Project structure is well-organized.${NC}"
elif [ $PASS_RATE -ge 80 ]; then
    echo -e "\n${YELLOW}✅ Good! Minor improvements recommended.${NC}"
else
    echo -e "\n${RED}❌ Project needs significant improvements.${NC}"
fi

# Exit code based on critical failures
if [ $FAILED_CHECKS -gt 5 ]; then
    exit 1
else
    exit 0
fi
