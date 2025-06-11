#!/bin/bash

echo "🧪 VentAI Quick Test Suite"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run tests with color output
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n${YELLOW}Running: $test_name${NC}"
    echo "Command: $test_command"
    echo "----------------------------------------"
    
    if eval $test_command; then
        echo -e "${GREEN}✅ $test_name - PASSED${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name - FAILED${NC}"
        return 1
    fi
}

# Test counter
total_tests=0
passed_tests=0

# Environment check
echo "🔍 Environment Check"
echo "Python: $(python --version)"
echo "Node: $(node --version 2>/dev/null || echo 'Not installed')"
echo "Current directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"
echo ""

# Test 1: Python import tests
total_tests=$((total_tests + 1))
if run_test "Python Import Test" "python -c 'import sys; print(\"Python imports working\"); print(\"Python path:\", sys.path[:3])'"
then
    passed_tests=$((passed_tests + 1))
fi

# Test 2: Backend main module test