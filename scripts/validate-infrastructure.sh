#!/bin/bash

# VentAI Infrastructure Validation Script
# Validates all production-ready infrastructure components

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Validation counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

# File validation function
check_file() {
    local file_path="$1"
    local description="$2"
    
    if [[ -f "$file_path" ]]; then
        log_success "$description exists: $file_path"
        return 0
    else
        log_error "$description missing: $file_path"
        return 1
    fi
}

# Directory validation function
check_directory() {
    local dir_path="$1"
    local description="$2"
    
    if [[ -d "$dir_path" ]]; then
        log_success "$description exists: $dir_path"
        return 0
    else
        log_error "$description missing: $dir_path"
        return 1
    fi
}

# Docker configuration validation
validate_docker_configs() {
    log_info "Validating Docker configurations..."
    
    # Production Dockerfiles
    check_file "$PROJECT_ROOT/frontend/Dockerfile.prod" "Frontend production Dockerfile"
    check_file "$PROJECT_ROOT/backend/Dockerfile.prod" "Backend production Dockerfile"
    check_file "$PROJECT_ROOT/infra/docker/nginx/Dockerfile" "Nginx Dockerfile"
    
    # Docker Compose files
    check_file "$PROJECT_ROOT/infra/docker/docker-compose.prod.yml" "Production Docker Compose"
    check_file "$PROJECT_ROOT/infra/docker/docker-compose.test.yml" "Test Docker Compose"
    check_file "$PROJECT_ROOT/infra/docker/docker-compose.monitoring.yml" "Monitoring Docker Compose"
    
    # Nginx configurations
    check_file "$PROJECT_ROOT/infra/docker/nginx/nginx.conf" "Main Nginx configuration"
    check_file "$PROJECT_ROOT/infra/docker/nginx/frontend.conf" "Frontend Nginx configuration"
    
    # Validate Docker Compose syntax
    log_info "Validating Docker Compose syntax..."
    
    if docker-compose -f "$PROJECT_ROOT/infra/docker/docker-compose.prod.yml" config >/dev/null 2>&1; then
        log_success "Production Docker Compose syntax is valid"
    else
        log_error "Production Docker Compose syntax is invalid"
    fi
    
    if docker-compose -f "$PROJECT_ROOT/infra/docker/docker-compose.test.yml" config >/dev/null 2>&1; then
        log_success "Test Docker Compose syntax is valid"
    else
        log_error "Test Docker Compose syntax is invalid"
    fi
    
    if docker-compose -f "$PROJECT_ROOT/infra/docker/docker-compose.monitoring.yml" config >/dev/null 2>&1; then
        log_success "Monitoring Docker Compose syntax is valid"
    else
        log_error "Monitoring Docker Compose syntax is invalid"
    fi
}

# Test infrastructure validation
validate_test_infrastructure() {
    log_info "Validating test infrastructure..."
    
    # E2E tests
    check_directory "$PROJECT_ROOT/tests/e2e" "E2E tests directory"
    check_file "$PROJECT_ROOT/tests/e2e/Dockerfile" "E2E tests Dockerfile"
    check_file "$PROJECT_ROOT/tests/e2e/package.json" "E2E tests package.json"
    check_file "$PROJECT_ROOT/tests/e2e/playwright.config.ts" "Playwright configuration"
    check_file "$PROJECT_ROOT/tests/e2e/tests/app.spec.ts" "E2E test specification"
    
    # Performance tests
    check_directory "$PROJECT_ROOT/tests/performance" "Performance tests directory"
    check_file "$PROJECT_ROOT/tests/performance/run-performance-tests.sh" "Performance test script"
    check_file "$PROJECT_ROOT/tests/performance/locustfile.py" "Locust configuration"
    
    # Check if performance test script is executable
    if [[ -x "$PROJECT_ROOT/tests/performance/run-performance-tests.sh" ]]; then
        log_success "Performance test script is executable"
    else
        log_error "Performance test script is not executable"
    fi
    
    # Unit and integration test configurations
    check_file "$PROJECT_ROOT/tests/unit/conftest.py" "Unit test configuration"
    check_file "$PROJECT_ROOT/tests/integration/conftest.py" "Integration test configuration"
    check_file "$PROJECT_ROOT/tests/e2e/conftest.py" "E2E test configuration"
}

# Monitoring infrastructure validation
validate_monitoring_infrastructure() {
    log_info "Validating monitoring infrastructure..."
    
    # Prometheus configuration
    check_directory "$PROJECT_ROOT/infra/monitoring/prometheus" "Prometheus configuration directory"
    check_file "$PROJECT_ROOT/infra/monitoring/prometheus/prometheus.yml" "Prometheus configuration"
    check_file "$PROJECT_ROOT/infra/monitoring/prometheus/rules/alerts.yml" "Prometheus alert rules"
    
    # Grafana configuration
    check_directory "$PROJECT_ROOT/infra/monitoring/grafana" "Grafana configuration directory"
    check_file "$PROJECT_ROOT/infra/monitoring/grafana/provisioning/datasources/prometheus.yml" "Grafana datasource configuration"
    check_file "$PROJECT_ROOT/infra/monitoring/grafana/provisioning/dashboards/dashboards.yml" "Grafana dashboard configuration"
    
    # Alertmanager configuration
    check_file "$PROJECT_ROOT/infra/monitoring/alertmanager/alertmanager.yml" "Alertmanager configuration"
}

# Kubernetes infrastructure validation
validate_kubernetes_infrastructure() {
    log_info "Validating Kubernetes infrastructure..."
    
    # Check K8s directory structure
    check_directory "$PROJECT_ROOT/infra/k8s" "Kubernetes manifests directory"
    check_file "$PROJECT_ROOT/infra/k8s/namespace.yml" "Kubernetes namespace"
    check_file "$PROJECT_ROOT/infra/k8s/configmap.yml" "Kubernetes configmap"
    check_file "$PROJECT_ROOT/infra/k8s/backend-deployment.yml" "Backend deployment"
    check_file "$PROJECT_ROOT/infra/k8s/frontend-deployment.yml" "Frontend deployment"
    check_file "$PROJECT_ROOT/infra/k8s/database.yml" "Database deployment"
    check_file "$PROJECT_ROOT/infra/k8s/ingress.yml" "Ingress configuration"
    
    # Validate YAML syntax if kubectl is available
    if command -v kubectl >/dev/null 2>&1; then
        log_info "Validating Kubernetes YAML syntax..."
        
        if kubectl apply --dry-run=client -f "$PROJECT_ROOT/infra/k8s/" >/dev/null 2>&1; then
            log_success "Kubernetes manifests syntax is valid"
        else
            log_error "Kubernetes manifests have syntax errors"
        fi
    else
        log_warning "kubectl not available, skipping K8s syntax validation"
    fi
}

# Package.json validation
validate_package_json() {
    log_info "Validating package.json scripts..."
    
    # Check if new scripts exist
    if npm run 2>/dev/null | grep -q "test:performance"; then
        log_success "Performance test script exists"
    else
        log_error "Performance test script missing"
    fi
    
    if npm run 2>/dev/null | grep -q "docker:test"; then
        log_success "Docker test script exists"
    else
        log_error "Docker test script missing"
    fi
    
    if npm run 2>/dev/null | grep -q "k8s:deploy"; then
        log_success "Kubernetes deployment script exists"
    else
        log_error "Kubernetes deployment script missing"
    fi
    
    if npm run 2>/dev/null | grep -q "monitoring:up"; then
        log_success "Monitoring startup script exists"
    else
        log_error "Monitoring startup script missing"
    fi
}

# Automation scripts validation
validate_automation_scripts() {
    log_info "Validating automation scripts..."
    
    # Check existing scripts from previous refactoring
    check_file "$PROJECT_ROOT/scripts/setup-project.sh" "Project setup script"
    check_file "$PROJECT_ROOT/scripts/validate-complete.sh" "Complete validation script"
    check_file "$PROJECT_ROOT/scripts/database/migrate.sh" "Database migration script"
    
    # Check if scripts are executable
    local scripts=(
        "$PROJECT_ROOT/scripts/setup-project.sh"
        "$PROJECT_ROOT/scripts/validate-complete.sh"
        "$PROJECT_ROOT/scripts/database/migrate.sh"
        "$PROJECT_ROOT/tests/performance/run-performance-tests.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -x "$script" ]]; then
            log_success "$(basename "$script") is executable"
        else
            log_error "$(basename "$script") is not executable"
        fi
    done
}

# Environment configuration validation
validate_environment_config() {
    log_info "Validating environment configurations..."
    
    check_directory "$PROJECT_ROOT/environments" "Environment configurations directory"
    check_file "$PROJECT_ROOT/environments/.env.development" "Development environment"
    check_file "$PROJECT_ROOT/environments/.env.production.template" "Production environment template"
    check_file "$PROJECT_ROOT/environments/.env.test" "Test environment"
}

# Services validation
validate_services_config() {
    log_info "Validating services configuration..."
    
    check_directory "$PROJECT_ROOT/services/mcp" "MCP service directory"
    check_file "$PROJECT_ROOT/services/mcp/requirements.txt" "MCP service requirements"
    check_file "$PROJECT_ROOT/services/mcp/Dockerfile" "MCP service Dockerfile"
}

# Backend dependencies validation
validate_backend_dependencies() {
    log_info "Validating backend dependencies..."
    
    # Check if Gunicorn is in requirements.txt
    if grep -q "gunicorn" "$PROJECT_ROOT/backend/requirements.txt" 2>/dev/null; then
        log_success "Gunicorn is included in backend requirements"
    else
        log_error "Gunicorn is missing from backend requirements"
    fi
    
    # Check if health endpoint exists in main.py
    if grep -q "/health" "$PROJECT_ROOT/backend/src/fastapi_app/main.py" 2>/dev/null; then
        log_success "Health endpoint exists in FastAPI main.py"
    else
        log_error "Health endpoint missing from FastAPI main.py"
    fi
}

# Overall project structure validation
validate_project_structure() {
    log_info "Validating overall project structure..."
    
    # Key directories
    local key_dirs=(
        "scripts"
        "tools"
        "infra/docker"
        "infra/k8s"
        "infra/monitoring"
        "docs"
        "tests/integration"
        "tests/unit"
        "tests/e2e"
        "tests/performance"
        "services/mcp"
        "configs"
        "environments"
    )
    
    for dir in "${key_dirs[@]}"; do
        check_directory "$PROJECT_ROOT/$dir" "$(basename "$dir") directory"
    done
}

# Main validation function
main() {
    echo "🔍 VentAI Infrastructure Validation Suite"
    echo "=========================================="
    echo "Validating production-ready infrastructure components..."
    echo ""
    
    cd "$PROJECT_ROOT"
    
    # Run all validations
    validate_project_structure
    echo ""
    
    validate_docker_configs
    echo ""
    
    validate_test_infrastructure
    echo ""
    
    validate_monitoring_infrastructure
    echo ""
    
    validate_kubernetes_infrastructure
    echo ""
    
    validate_package_json
    echo ""
    
    validate_automation_scripts
    echo ""
    
    validate_environment_config
    echo ""
    
    validate_services_config
    echo ""
    
    validate_backend_dependencies
    echo ""
    
    # Final summary
    echo "Validation Summary"
    echo "=================="
    echo -e "Total checks: ${BLUE}$TOTAL_CHECKS${NC}"
    echo -e "Passed: ${GREEN}$PASSED_CHECKS${NC}"
    echo -e "Failed: ${RED}$FAILED_CHECKS${NC}"
    echo ""
    
    if [[ $FAILED_CHECKS -eq 0 ]]; then
        echo -e "${GREEN}🎉 All infrastructure validation checks passed!${NC}"
        echo -e "${GREEN}Production-ready infrastructure is complete.${NC}"
        exit 0
    else
        echo -e "${RED}❌ $FAILED_CHECKS validation checks failed.${NC}"
        echo -e "${YELLOW}Please review and fix the failing components.${NC}"
        exit 1
    fi
}

# Execute main function
main "$@"
