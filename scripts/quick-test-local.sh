#!/bin/bash

# Quick Local Testing Script for pytest-mcp-server Integration
# This script provides a fast way to test our MCP framework locally

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTEST_SERVER_PATH="../pytest-mcp-server"
TEST_TYPE="functional"
VERBOSE=false

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Quick local testing script for pytest-mcp-server integration.

OPTIONS:
    -h, --help              Show this help message
    -p, --path PATH         Path to pytest-mcp-server repository (default: ../pytest-mcp-server)
    -t, --type TYPE         Test type: functional, security, performance, issue-detection, all (default: functional)
    -v, --verbose           Enable verbose output
    -s, --setup-only        Only setup, don't run tests
    -c, --clean             Clean test data before running
    --dagger                Use Dagger for testing (requires Dagger CLI)
    --no-clone              Don't clone pytest-mcp-server if missing

EXAMPLES:
    $0                                          # Run basic functional tests
    $0 -t all                                   # Run all test types
    $0 -p ./my-pytest-server -t security       # Test specific path with security tests
    $0 --dagger -t performance                 # Use Dagger for performance tests
    $0 --setup-only                            # Just setup the environment
    $0 --clean -t all                          # Clean and run all tests

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -p|--path)
            PYTEST_SERVER_PATH="$2"
            shift 2
            ;;
        -t|--type)
            TEST_TYPE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -s|--setup-only)
            SETUP_ONLY=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        --dagger)
            USE_DAGGER=true
            shift
            ;;
        --no-clone)
            NO_CLONE=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate test type
case $TEST_TYPE in
    functional|security|performance|issue-detection|all)
        ;;
    *)
        print_error "Invalid test type: $TEST_TYPE"
        print_error "Valid types: functional, security, performance, issue-detection, all"
        exit 1
        ;;
esac

print_status "Starting MCP Framework Local Testing"
print_status "Test Type: $TEST_TYPE"
print_status "pytest-mcp-server Path: $PYTEST_SERVER_PATH"

# Clean test data if requested
if [[ "$CLEAN" == "true" ]]; then
    print_status "Cleaning test data..."
    rm -rf test-data/ test-results/
    print_success "Test data cleaned"
fi

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]] || [[ ! -d "src/mcp_client_cli" ]]; then
    print_error "Please run this script from the mcp-client-cli root directory"
    exit 1
fi

# Setup pytest-mcp-server
if [[ ! -d "$PYTEST_SERVER_PATH" ]]; then
    if [[ "$NO_CLONE" == "true" ]]; then
        print_error "pytest-mcp-server not found at $PYTEST_SERVER_PATH and --no-clone specified"
        exit 1
    fi
    
    print_status "Cloning pytest-mcp-server..."
    git clone https://github.com/tosin2013/pytest-mcp-server.git "$PYTEST_SERVER_PATH"
    print_success "Repository cloned"
else
    print_status "pytest-mcp-server found at $PYTEST_SERVER_PATH"
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed"
    print_error "Please install Node.js 18+ and try again"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [[ $NODE_VERSION -lt 18 ]]; then
    print_warning "Node.js version $NODE_VERSION detected. Version 18+ recommended."
fi

# Setup pytest-mcp-server dependencies
print_status "Setting up pytest-mcp-server dependencies..."
cd "$PYTEST_SERVER_PATH"

if [[ ! -f "package.json" ]]; then
    print_error "package.json not found in pytest-mcp-server directory"
    exit 1
fi

npm ci
if npm run build 2>/dev/null; then
    print_success "pytest-mcp-server built successfully"
else
    print_warning "Build failed, continuing with source files"
fi

cd - > /dev/null

# Check Python environment
print_status "Checking Python environment..."
if ! python -c "import sys; assert sys.version_info >= (3, 12)" 2>/dev/null; then
    print_error "Python 3.12+ is required"
    exit 1
fi

# Install dependencies
print_status "Installing MCP testing framework dependencies..."
pip install -e ".[testing]" > /dev/null 2>&1
print_success "Dependencies installed"

# Verify our testing modules
print_status "Verifying testing modules..."
if python -c "from src.mcp_client_cli.testing import MCPServerTester, MCPSecurityTester, MCPPerformanceTester; print('✓ All modules imported successfully')" 2>/dev/null; then
    print_success "Testing modules verified"
else
    print_error "Failed to import testing modules"
    exit 1
fi

# Check if configuration exists
CONFIG_FILE="examples/test-pytest-mcp-server.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    print_error "Configuration file not found: $CONFIG_FILE"
    print_error "Please ensure the configuration file exists"
    exit 1
fi

# Setup complete check
if [[ "$SETUP_ONLY" == "true" ]]; then
    print_success "Setup completed successfully!"
    print_status "You can now run tests manually:"
    print_status "  python scripts/test-pytest-mcp-server.py --server-path $PYTEST_SERVER_PATH --test-type $TEST_TYPE"
    exit 0
fi

# Run tests based on method
if [[ "$USE_DAGGER" == "true" ]]; then
    # Check Dagger CLI
    if ! command -v dagger &> /dev/null; then
        print_error "Dagger CLI is required but not installed"
        print_error "Install with: curl -L https://dl.dagger.io/dagger/install.sh | sh"
        exit 1
    fi
    
    print_status "Running tests with Dagger..."
    
    # Verify Dagger functions
    print_status "Verifying Dagger functions..."
    if dagger functions > /dev/null 2>&1; then
        print_success "Dagger functions verified"
    else
        print_error "Dagger functions verification failed"
        exit 1
    fi
    
    # Run appropriate Dagger command
    case $TEST_TYPE in
        functional)
            dagger call run-functional-tests --server-path "$PYTEST_SERVER_PATH" --config-path "$CONFIG_FILE"
            ;;
        security)
            dagger call run-security-tests --server-path "$PYTEST_SERVER_PATH" --config-path "$CONFIG_FILE"
            ;;
        performance)
            dagger call run-performance-tests --server-path "$PYTEST_SERVER_PATH" --config-path "$CONFIG_FILE"
            ;;
        all)
            dagger call run-full-test-suite --server-path "$PYTEST_SERVER_PATH" --config-path "$CONFIG_FILE" --parallel true
            ;;
        *)
            print_error "Dagger testing not implemented for type: $TEST_TYPE"
            exit 1
            ;;
    esac
else
    # Run Python tests
    print_status "Running tests with Python..."
    
    if [[ "$VERBOSE" == "true" ]]; then
        python scripts/test-pytest-mcp-server.py --server-path "$PYTEST_SERVER_PATH" --test-type "$TEST_TYPE"
    else
        python scripts/test-pytest-mcp-server.py --server-path "$PYTEST_SERVER_PATH" --test-type "$TEST_TYPE" 2>/dev/null
    fi
fi

# Check for test results
if [[ -d "test-results" ]]; then
    print_success "Tests completed! Results available in test-results/"
    
    # Show summary if available
    if [[ -f "test-results/pytest-mcp-server-report.md" ]]; then
        print_status "Test report generated: test-results/pytest-mcp-server-report.md"
        
        if [[ "$VERBOSE" == "true" ]]; then
            echo ""
            echo "=== Test Report Summary ==="
            head -20 test-results/pytest-mcp-server-report.md
            echo "..."
            echo "=== End Summary ==="
        fi
    fi
    
    # List other result files
    RESULT_FILES=$(find test-results -name "*.json" -o -name "*.html" | wc -l)
    if [[ $RESULT_FILES -gt 0 ]]; then
        print_status "Additional result files: $RESULT_FILES"
    fi
else
    print_warning "No test results directory found"
fi

print_success "Local testing completed!"

# Provide next steps
echo ""
print_status "Next steps:"
print_status "  • Review test results in test-results/"
print_status "  • Run with different test types: -t security, -t performance, -t all"
print_status "  • Try Dagger testing: --dagger"
print_status "  • Enable verbose output: -v" 