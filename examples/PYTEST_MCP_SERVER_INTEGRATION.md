# Testing Against pytest-mcp-server Integration Guide

This guide demonstrates how to use our comprehensive MCP testing framework to validate the [pytest-mcp-server](https://github.com/tosin2013/pytest-mcp-server) implementation.

## Overview

The pytest-mcp-server is a Model Context Protocol (MCP) server that provides pytest testing capabilities. Our testing framework can comprehensively validate this server's functionality, security, performance, and reliability.

## Quick Start

### 1. Local Testing (Recommended for Development)

```bash
# Basic functional tests
./scripts/quick-test-local.sh

# All test types
./scripts/quick-test-local.sh -t all

# Security-focused testing
./scripts/quick-test-local.sh -t security

# Performance benchmarking
./scripts/quick-test-local.sh -t performance

# Use Dagger for containerized testing
./scripts/quick-test-local.sh --dagger -t all
```

### 2. Manual Python Testing

```bash
# Install dependencies
pip install -e ".[testing]"

# Clone pytest-mcp-server
git clone https://github.com/tosin2013/pytest-mcp-server.git ../pytest-mcp-server

# Run comprehensive tests
python scripts/test-pytest-mcp-server.py \
  --server-path ../pytest-mcp-server \
  --test-type all
```

### 3. Dagger Pipeline Testing

```bash
# Install Dagger CLI
curl -L https://dl.dagger.io/dagger/install.sh | sh

# Run functional tests
dagger call run-functional-tests \
  --server-path ../pytest-mcp-server \
  --config-path examples/test-pytest-mcp-server.json

# Run full test suite
dagger call run-full-test-suite \
  --server-path ../pytest-mcp-server \
  --config-path examples/test-pytest-mcp-server.json \
  --parallel true
```

## Testing Scenarios

### Functional Testing

Tests core MCP protocol compliance and pytest-specific functionality:

- **Protocol Compliance**: Validates MCP handshake, capabilities exchange, and message format
- **Tool Execution**: Tests pytest tool invocation and result handling
- **Resource Access**: Validates test file and result resource access
- **Error Handling**: Tests error scenarios and recovery mechanisms

```bash
# Functional testing only
./scripts/quick-test-local.sh -t functional
```

### Security Testing

Comprehensive security validation following OWASP guidelines:

- **Authentication Testing**: No credentials, invalid credentials, expired tokens
- **Authorization Testing**: Privilege escalation, unauthorized access attempts
- **Input Validation**: Malicious payload injection, XSS, SQL injection
- **Data Sanitization**: Path traversal, command injection prevention

```bash
# Security testing
./scripts/quick-test-local.sh -t security
```

### Performance Testing

Benchmarks server performance under various load conditions:

- **Response Time Analysis**: Cold start, warm sequential, burst scenarios
- **Concurrent Connection Testing**: Scalability under load
- **Resource Usage Monitoring**: Memory, CPU, file descriptor usage
- **Memory Leak Detection**: Long-running stability testing

```bash
# Performance benchmarking
./scripts/quick-test-local.sh -t performance
```

### Issue Detection and Remediation

Automated issue detection with remediation suggestions:

- **Pattern Recognition**: Common failure patterns and root causes
- **Health Monitoring**: Server health metrics and trends
- **Automated Remediation**: Configuration fixes, dependency resolution
- **Failure Analysis**: Systematic failure categorization

```bash
# Issue detection testing
./scripts/quick-test-local.sh -t issue-detection
```

## Configuration

### Basic Configuration (`examples/test-pytest-mcp-server.json`)

```json
{
  "systemPrompt": "Testing pytest-mcp-server integration",
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0.1
  },
  "mcpServers": {
    "pytest-mcp-server": {
      "command": "node",
      "args": ["../pytest-mcp-server/src/index.ts"],
      "env": {
        "NODE_ENV": "test",
        "DATA_DIR": "./test-data"
      },
      "enabled": true
    }
  },
  "testingConfig": {
    "timeout": 30,
    "retries": 3,
    "parallel": true,
    "confidenceThreshold": 0.85
  }
}
```

### Advanced Configuration Options

```json
{
  "testingConfig": {
    "securityTesting": {
      "enabled": true,
      "authenticationTests": true,
      "inputValidationTests": true,
      "maliciousPayloads": ["<script>", "'; DROP TABLE", "../../../etc/passwd"]
    },
    "performanceTesting": {
      "enabled": true,
      "concurrentConnections": [1, 5, 10, 20],
      "testDuration": 60,
      "memoryLeakDetection": true
    },
    "issueDetection": {
      "enabled": true,
      "healthMonitoring": true,
      "patternRecognition": true,
      "autoRemediation": false
    }
  }
}
```

## GitHub Actions Integration

### Automated Testing Workflow

The repository includes a comprehensive GitHub Actions workflow (`.github/workflows/test-pytest-mcp-server.yml`) that:

1. **Multi-Environment Testing**: Tests across Python 3.12 and Node.js 18/20
2. **Cross-Platform Validation**: Ubuntu, macOS, and Windows
3. **Comprehensive Test Matrix**: All test types with parallel execution
4. **Automated Reporting**: Consolidated test reports and artifact collection
5. **Performance Benchmarking**: Daily performance regression testing

### Triggering Tests

```bash
# Manual workflow dispatch
gh workflow run test-pytest-mcp-server.yml \
  -f test_type=all \
  -f server_branch=main

# Specific test types
gh workflow run test-pytest-mcp-server.yml \
  -f test_type=security

# Different server branch
gh workflow run test-pytest-mcp-server.yml \
  -f test_type=all \
  -f server_branch=develop
```

### Required Secrets

Configure these secrets in your GitHub repository:

- `OPENAI_API_KEY`: For LLM-based testing (optional)
- `ANTHROPIC_API_KEY`: Alternative LLM provider (optional)

## Test Results and Reporting

### Result Structure

```
test-results/
├── pytest-mcp-server-report.md          # Comprehensive test report
├── functional-tests.json                # Functional test results
├── security-tests.json                  # Security test results
├── performance-tests.json               # Performance benchmarks
├── issue-detection.json                 # Detected issues and remediation
├── test-summary.html                    # HTML report
└── raw-logs/                            # Detailed logs
    ├── server-logs.txt
    ├── client-logs.txt
    └── dagger-logs.txt
```

### Confidence Scoring

All test results include confidence scores based on methodological pragmatism:

- **95-100%**: High confidence, systematic verification completed
- **85-94%**: Good confidence, minor uncertainties identified
- **70-84%**: Moderate confidence, some assumptions made
- **Below 70%**: Low confidence, requires manual review

### Report Analysis

```bash
# View test summary
cat test-results/pytest-mcp-server-report.md

# Check specific test results
jq '.tests[] | select(.status == "FAILED")' test-results/functional-tests.json

# Performance metrics
jq '.metrics' test-results/performance-tests.json
```

## Troubleshooting

### Common Issues

1. **Node.js Version Compatibility**
   ```bash
   # Check Node.js version
   node --version
   
   # Install Node.js 18+ if needed
   nvm install 18
   nvm use 18
   ```

2. **Python Dependencies**
   ```bash
   # Reinstall dependencies
   pip install -e ".[testing]" --force-reinstall
   ```

3. **Dagger Issues**
   ```bash
   # Verify Dagger installation
   dagger version
   
   # Check Dagger functions
   dagger functions
   ```

4. **pytest-mcp-server Build Issues**
   ```bash
   # Manual build
   cd ../pytest-mcp-server
   npm ci
   npm run build
   ```

### Debug Mode

```bash
# Enable verbose output
./scripts/quick-test-local.sh -v -t functional

# Clean and retry
./scripts/quick-test-local.sh --clean -t all

# Setup only (no tests)
./scripts/quick-test-local.sh --setup-only
```

### Log Analysis

```bash
# Check server logs
tail -f test-results/raw-logs/server-logs.txt

# Monitor test progress
watch -n 1 'ls -la test-results/'

# Analyze failures
grep -r "ERROR\|FAILED" test-results/
```

## Best Practices

### Development Workflow

1. **Start with Functional Tests**: Ensure basic functionality works
2. **Add Security Testing**: Validate security posture
3. **Performance Baseline**: Establish performance benchmarks
4. **Continuous Integration**: Automate testing in CI/CD

### Test Configuration

1. **Environment Isolation**: Use containers for consistent testing
2. **Parallel Execution**: Leverage parallel testing for speed
3. **Confidence Thresholds**: Set appropriate confidence levels
4. **Regular Updates**: Keep test configurations current

### Monitoring and Maintenance

1. **Daily Benchmarks**: Run performance tests regularly
2. **Security Scans**: Regular security testing
3. **Issue Tracking**: Monitor and address detected issues
4. **Documentation**: Keep testing documentation updated

## Advanced Usage

### Custom Test Scenarios

```python
# Custom test implementation
from src.mcp_client_cli.testing import MCPServerTester

async def custom_pytest_test():
    tester = MCPServerTester()
    
    # Custom test logic
    result = await tester.test_tool_execution(
        tool_name="run_pytest",
        arguments={"test_file": "test_example.py"},
        expected_patterns=["PASSED", "FAILED"]
    )
    
    return result
```

### Integration with Other Tools

```bash
# Integration with pytest
pytest tests/ --mcp-server=../pytest-mcp-server

# Integration with coverage
coverage run --source=src scripts/test-pytest-mcp-server.py
coverage report
```

### Extending the Framework

```python
# Custom security tests
class CustomSecurityTester(MCPSecurityTester):
    async def test_pytest_specific_security(self):
        # Pytest-specific security tests
        pass

# Custom performance metrics
class CustomPerformanceTester(MCPPerformanceTester):
    async def test_pytest_performance(self):
        # Pytest-specific performance tests
        pass
```

## Contributing

To contribute improvements to pytest-mcp-server testing:

1. Fork both repositories
2. Create feature branches
3. Add comprehensive tests
4. Submit pull requests with test results
5. Update documentation

## Resources

- [pytest-mcp-server Repository](https://github.com/tosin2013/pytest-mcp-server)
- [MCP Protocol Specification](https://modelcontextprotocol.io/docs)
- [Dagger.io Documentation](https://docs.dagger.io/)
- [Testing Framework Documentation](../TESTING.md)
- [Methodological Pragmatism Guide](../examples/BEST_PRACTICES.md) 