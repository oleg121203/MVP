#!/bin/bash

# VentAI Infrastructure Quick Validation
echo "🔍 VentAI Infrastructure Quick Validation"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

CHECKS=0
PASSED=0

check_file() {
    if [[ -f "$1" ]]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 (missing: $1)"
    fi
    ((CHECKS++))
}

check_dir() {
    if [[ -d "$1" ]]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 (missing: $1)"
    fi
    ((CHECKS++))
}

echo ""
echo "🐳 Docker Infrastructure:"
check_file "frontend/Dockerfile.prod" "Frontend production Dockerfile"
check_file "backend/Dockerfile.prod" "Backend production Dockerfile"
check_file "infra/docker/docker-compose.prod.yml" "Production Docker Compose"
check_file "infra/docker/docker-compose.test.yml" "Test Docker Compose"
check_file "infra/docker/docker-compose.monitoring.yml" "Monitoring Docker Compose"

echo ""
echo "☸️ Kubernetes Infrastructure:"
check_dir "infra/k8s" "Kubernetes manifests directory"
check_file "infra/k8s/namespace.yml" "Kubernetes namespace"
check_file "infra/k8s/backend-deployment.yml" "Backend deployment"
check_file "infra/k8s/frontend-deployment.yml" "Frontend deployment"
check_file "infra/k8s/database.yml" "Database StatefulSet"
check_file "infra/k8s/ingress.yml" "Ingress configuration"

echo ""
echo "📊 Monitoring Stack:"
check_dir "infra/monitoring" "Monitoring directory"
check_file "infra/monitoring/prometheus/prometheus.yml" "Prometheus configuration"
check_file "infra/monitoring/grafana/provisioning/dashboards/dashboards.yml" "Grafana dashboards"
check_file "infra/monitoring/alertmanager/alertmanager.yml" "Alertmanager configuration"

echo ""
echo "🧪 Testing Infrastructure:"
check_dir "tests/e2e" "E2E tests directory"
check_dir "tests/performance" "Performance tests directory"
check_file "tests/e2e/Dockerfile" "E2E testing Dockerfile"
check_file "tests/performance/locustfile.py" "Load testing configuration"

echo ""
echo "🔄 CI/CD Pipelines:"
check_file ".github/workflows/ci-cd.yml" "Main CI/CD pipeline"
check_file ".github/workflows/release.yml" "Release pipeline"
check_file ".github/workflows/backup.yml" "Backup automation"
check_file ".github/workflows/dependency-updates.yml" "Dependency updates"

echo ""
echo "🔧 Automation & Scripts:"
check_dir "scripts" "Scripts directory"
check_file "scripts/validate-infrastructure.sh" "Infrastructure validation script"
check_file "package.json" "Package.json with enhanced scripts"

echo ""
echo "📋 Summary:"
echo "=========="
echo "Total checks: $CHECKS"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$((CHECKS - PASSED))${NC}"

if [[ $PASSED -eq $CHECKS ]]; then
    echo -e "${GREEN}🎉 All infrastructure validation checks passed!${NC}"
    echo -e "${GREEN}Production-ready infrastructure is complete.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some validation checks failed.${NC}"
    exit 1
fi
