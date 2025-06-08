#!/bin/bash

# VentAI Performance Testing Script
# Tests application performance under load

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
DURATION="${DURATION:-60s}"
USERS="${USERS:-10}"
RESULTS_DIR="tests/performance/results"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v curl &> /dev/null; then
        log_error "curl is required but not installed"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        log_error "python3 is required but not installed"
        exit 1
    fi
    
    if ! python3 -c "import locust" &> /dev/null; then
        log_warning "locust not installed, installing..."
        pip3 install locust
    fi
    
    log_success "All dependencies available"
}

# Test application availability
test_availability() {
    log_info "Testing application availability..."
    
    # Test frontend
    if curl -f "$FRONTEND_URL" &> /dev/null; then
        log_success "Frontend is available at $FRONTEND_URL"
    else
        log_error "Frontend is not available at $FRONTEND_URL"
        exit 1
    fi
    
    # Test backend
    if curl -f "$BACKEND_URL/docs" &> /dev/null; then
        log_success "Backend is available at $BACKEND_URL"
    else
        log_error "Backend is not available at $BACKEND_URL"
        exit 1
    fi
}

# Run Lighthouse performance audit
run_lighthouse() {
    log_info "Running Lighthouse performance audit..."
    
    if command -v lighthouse &> /dev/null; then
        mkdir -p "$RESULTS_DIR/lighthouse"
        
        lighthouse "$FRONTEND_URL" \
            --output html \
            --output json \
            --output-path "$RESULTS_DIR/lighthouse/report" \
            --chrome-flags="--headless --no-sandbox" \
            --quiet
        
        log_success "Lighthouse audit completed"
    else
        log_warning "Lighthouse not installed, skipping audit"
    fi
}

# Run load testing with locust
run_load_test() {
    log_info "Running load test with Locust..."
    
    mkdir -p "$RESULTS_DIR/locust"
    
    # Create locust file if it doesn't exist
    if [[ ! -f "tests/performance/locustfile.py" ]]; then
        log_info "Creating basic locust configuration..."
        cat > tests/performance/locustfile.py << 'EOF'
from locust import HttpUser, task, between

class VentAIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts"""
        pass
    
    @task(3)
    def view_homepage(self):
        """Load the homepage"""
        self.client.get("/")
    
    @task(1)
    def api_health_check(self):
        """Check API health"""
        self.client.get("/docs", name="/api/docs")
EOF
    fi
    
    # Run locust test
    locust -f tests/performance/locustfile.py \
        --host="$FRONTEND_URL" \
        --users="$USERS" \
        --spawn-rate=2 \
        --run-time="$DURATION" \
        --html="$RESULTS_DIR/locust/report.html" \
        --csv="$RESULTS_DIR/locust/results" \
        --headless
    
    log_success "Load test completed"
}

# Run basic performance metrics
run_basic_metrics() {
    log_info "Collecting basic performance metrics..."
    
    mkdir -p "$RESULTS_DIR/metrics"
    
    # Measure response times
    echo "Testing response times..." > "$RESULTS_DIR/metrics/response_times.txt"
    
    for i in {1..10}; do
        frontend_time=$(curl -o /dev/null -s -w "%{time_total}" "$FRONTEND_URL")
        backend_time=$(curl -o /dev/null -s -w "%{time_total}" "$BACKEND_URL/docs")
        
        echo "Test $i: Frontend=${frontend_time}s, Backend=${backend_time}s" >> "$RESULTS_DIR/metrics/response_times.txt"
    done
    
    log_success "Basic metrics collected"
}

# Generate performance report
generate_report() {
    log_info "Generating performance report..."
    
    cat > "$RESULTS_DIR/performance_report.md" << EOF
# VentAI Performance Test Report

Generated: $(date)

## Test Configuration
- Frontend URL: $FRONTEND_URL
- Backend URL: $BACKEND_URL
- Test Duration: $DURATION
- Concurrent Users: $USERS

## Results

### Response Time Analysis
$(cat "$RESULTS_DIR/metrics/response_times.txt" 2>/dev/null || echo "No response time data available")

### Load Test Results
- Locust report: [View HTML Report](locust/report.html)
- Raw data: locust/results.csv

### Lighthouse Audit
- Lighthouse report: [View HTML Report](lighthouse/report.html)

## Recommendations

1. Monitor response times during peak usage
2. Consider implementing caching strategies
3. Optimize database queries if backend response times are high
4. Implement CDN for static assets
5. Consider horizontal scaling for high load scenarios

EOF
    
    log_success "Performance report generated at $RESULTS_DIR/performance_report.md"
}

# Main execution
main() {
    echo "🚀 VentAI Performance Testing Suite"
    echo "==================================="
    
    check_dependencies
    test_availability
    
    # Create results directory
    mkdir -p "$RESULTS_DIR"
    
    # Run tests
    run_basic_metrics
    run_load_test
    run_lighthouse
    
    # Generate report
    generate_report
    
    echo ""
    log_success "Performance testing completed!"
    echo "📊 Results available in: $RESULTS_DIR"
    echo "📋 View the report: $RESULTS_DIR/performance_report.md"
}

# Execute main function
main "$@"
