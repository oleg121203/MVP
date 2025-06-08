#!/bin/bash

# Simplified VentAI Project Validation
echo "=========================================="
echo " VentAI Project Structure Validation"
echo "=========================================="

# Basic directory checks
echo "Checking directory structure..."

PASSED=0
FAILED=0
TOTAL=0

check_dir() {
    ((TOTAL++))
    if [ -d "$1" ]; then
        echo "✅ $2"
        ((PASSED++))
    else
        echo "❌ $2"
        ((FAILED++))
    fi
}

check_file() {
    ((TOTAL++))
    if [ -f "$1" ]; then
        echo "✅ $2"
        ((PASSED++))
    else
        echo "❌ $2"
        ((FAILED++))
    fi
}

# Directory structure checks
check_dir "frontend" "Frontend directory exists"
check_dir "backend" "Backend directory exists"
check_dir "services" "Services directory exists"
check_dir "services/mcp" "MCP service directory exists"
check_dir "scripts" "Scripts directory exists"
check_dir "tools" "Tools directory exists"
check_dir "infra" "Infrastructure directory exists"
check_dir "infra/docker" "Docker configurations exist"
check_dir "infra/k8s" "Kubernetes manifests directory exists"
check_dir "docs" "Documentation directory exists"
check_dir "tests" "Tests directory exists"
check_dir "configs" "Configs directory exists"
check_dir "environments" "Environments directory exists"

echo ""
echo "Checking configuration files..."

# Configuration files
check_file "package.json" "Root package.json exists"
check_file "frontend/package.json" "Frontend package.json exists"
check_file "backend/requirements.txt" "Backend requirements.txt exists"
check_file "services/mcp/requirements.txt" "MCP requirements.txt exists"
check_file "environments/.env.development" "Development environment exists"
check_file "environments/.env.production.template" "Production template exists"
check_file "environments/.env.test" "Test environment exists"
check_file "README.md" "Main README.md exists"

echo ""
echo "Checking Docker configuration..."

# Docker configuration
check_file "infra/docker/docker-compose.dev.yml" "Development Docker Compose exists"
check_file "infra/docker/docker-compose.prod.yml" "Production Docker Compose exists"
check_file "infra/docker/docker-compose-db.yml" "Database Docker Compose exists"
check_file "infra/docker/nginx/nginx.conf" "Nginx configuration exists"
check_file "infra/docker/nginx/Dockerfile" "Nginx Dockerfile exists"
check_file "backend/Dockerfile" "Backend Dockerfile exists"
check_file "services/mcp/Dockerfile" "MCP Dockerfile exists"

echo ""
echo "Checking scripts..."

# Scripts
check_file "scripts/setup-project.sh" "Project setup script exists"
check_file "scripts/setup-environment.js" "Environment setup script exists"
check_file "scripts/check-node-version.js" "Node version checker exists"
check_file "scripts/validate-workflow.sh" "Workflow validation script exists"
check_file "scripts/database/migrate.sh" "Database migration script exists"

echo ""
echo "Checking CI/CD..."

# CI/CD
check_dir ".github/workflows" "GitHub workflows directory exists"
check_file ".github/workflows/ci-cd.yml" "CI/CD workflow exists"

echo ""
echo "=========================================="
echo " VALIDATION SUMMARY"
echo "=========================================="
echo "Total checks: $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"

PASS_RATE=$((PASSED * 100 / TOTAL))
echo "Pass rate: $PASS_RATE%"

if [ $PASS_RATE -ge 90 ]; then
    echo "🎉 Excellent! Project structure is well-organized."
elif [ $PASS_RATE -ge 80 ]; then
    echo "👍 Good! Minor improvements recommended."
else
    echo "⚠️  Project needs improvements."
fi

# Check key package.json scripts
echo ""
echo "Checking package.json scripts..."
if grep -q "setup:complete" package.json; then
    echo "✅ Setup scripts configured"
else
    echo "❌ Setup scripts missing"
    ((FAILED++))
fi

if grep -q "docker:dev" package.json; then
    echo "✅ Docker scripts configured"
else
    echo "❌ Docker scripts missing"
    ((FAILED++))
fi

if grep -q "test:all" package.json; then
    echo "✅ Test scripts configured"
else
    echo "❌ Test scripts missing"
    ((FAILED++))
fi

echo ""
echo "🏁 Validation completed!"

if [ $FAILED -eq 0 ]; then
    echo "🎯 All checks passed! Ready for development."
    exit 0
else
    echo "🔧 $FAILED issues found. Please review and fix."
    exit 1
fi
