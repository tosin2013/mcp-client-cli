# Testing pytest-mcp-server with MCP Testing Framework

## 🎯 Quick Start Guide

Our comprehensive MCP testing framework is now ready to test against the [pytest-mcp-server](https://github.com/tosin2013/pytest-mcp-server). Here are the three main ways to run tests:

### 1. 🚀 One-Command Local Testing (Recommended)

```bash
# Clone and test in one command
./scripts/quick-test-local.sh

# Run all test types
./scripts/quick-test-local.sh -t all

# Security-focused testing
./scripts/quick-test-local.sh -t security

# Performance benchmarking
./scripts/quick-test-local.sh -t performance
```

### 2. 🐳 Containerized Testing with Dagger

```bash
# Install Dagger CLI (if not already installed)
curl -L https://dl.dagger.io/dagger/install.sh | sh

# Run containerized tests
./scripts/quick-test-local.sh --dagger -t all

# Or use Dagger directly
dagger call run-full-test-suite \
  --server-path ../pytest-mcp-server \
  --config-path examples/test-pytest-mcp-server.json \
  --parallel true
```

### 3. ⚙️ Manual Python Testing

```bash
# Setup
pip install -e ".[testing]"
git clone https://github.com/tosin2013/pytest-mcp-server.git ../pytest-mcp-server

# Run tests
python scripts/test-pytest-mcp-server.py \
  --server-path ../pytest-mcp-server \
  --test-type all
```

## 🧪 Available Test Types

| Test Type | Description | Command |
|-----------|-------------|---------|
| **functional** | Core MCP protocol compliance and pytest functionality | `-t functional` |
| **security** | OWASP-based security testing (auth, input validation, etc.) | `-t security` |
| **performance** | Load testing, response times, memory leak detection | `-t performance` |
| **issue-detection** | Automated issue detection and remediation | `-t issue-detection` |
| **all** | Complete test suite with all types | `-t all` |

## 📊 What Gets Tested

### Functional Testing ✅
- **MCP Protocol Compliance**: Handshake, capabilities, message format
- **Tool Execution**: pytest command invocation and result handling
- **Resource Access**: Test file and result resource validation
- **Error Handling**: Error scenarios and recovery mechanisms

### Security Testing 🔒
- **Authentication**: No credentials, invalid credentials, expired tokens
- **Authorization**: Privilege escalation, unauthorized access attempts
- **Input Validation**: XSS, SQL injection, command injection prevention
- **Data Sanitization**: Path traversal, malicious payload handling

### Performance Testing ⚡
- **Response Time Analysis**: Cold start, warm sequential, burst scenarios
- **Concurrent Connections**: Scalability testing (1, 5, 10, 20 connections)
- **Resource Monitoring**: Memory, CPU, file descriptor usage
- **Memory Leak Detection**: Long-running stability analysis

### Issue Detection 🔍
- **Pattern Recognition**: Common failure patterns and root causes
- **Health Monitoring**: Server health metrics and trend analysis
- **Automated Remediation**: Configuration fixes and dependency resolution
- **Failure Analysis**: Systematic categorization with confidence scoring

## 🎛️ Configuration Options

### Basic Configuration
```json
{
  "mcpServers": {
    "pytest-mcp-server": {
      "command": "node",
      "args": ["../pytest-mcp-server/src/index.ts"],
      "env": {"NODE_ENV": "test"}
    }
  },
  "testingConfig": {
    "timeout": 30,
    "retries": 3,
    "confidenceThreshold": 0.85
  }
}
```

### Advanced Configuration
```json
{
  "testingConfig": {
    "securityTesting": {
      "enabled": true,
      "maliciousPayloads": ["<script>", "'; DROP TABLE", "../../../etc/passwd"]
    },
    "performanceTesting": {
      "concurrentConnections": [1, 5, 10, 20],
      "memoryLeakDetection": true
    },
    "issueDetection": {
      "autoRemediation": false,
      "healthMonitoring": true
    }
  }
}
```

## 🤖 GitHub Actions Integration

### Automated Testing
The framework includes a comprehensive GitHub Actions workflow that:

- **Multi-Environment**: Tests across Python 3.12 and Node.js 18/20
- **Cross-Platform**: Ubuntu, macOS, Windows validation
- **Parallel Execution**: All test types run simultaneously
- **Daily Benchmarks**: Automated performance regression testing

### Trigger Tests
```bash
# Manual workflow dispatch
gh workflow run test-pytest-mcp-server.yml -f test_type=all

# Security-focused run
gh workflow run test-pytest-mcp-server.yml -f test_type=security
```

## 📈 Test Results and Reporting

### Result Structure
```
test-results/
├── pytest-mcp-server-report.md     # Comprehensive report
├── functional-tests.json           # Functional test results
├── security-tests.json             # Security test results
├── performance-tests.json          # Performance benchmarks
├── issue-detection.json            # Issues and remediation
└── test-summary.html               # HTML report
```

### Confidence Scoring
All results include confidence scores based on methodological pragmatism:
- **95-100%**: High confidence, systematic verification
- **85-94%**: Good confidence, minor uncertainties
- **70-84%**: Moderate confidence, some assumptions
- **Below 70%**: Low confidence, manual review needed

## 🛠️ Troubleshooting

### Common Issues and Solutions

1. **Node.js Version**
   ```bash
   node --version  # Should be 18+
   nvm install 18 && nvm use 18
   ```

2. **Python Dependencies**
   ```bash
   pip install -e ".[testing]" --force-reinstall
   ```

3. **Dagger Issues**
   ```bash
   dagger version  # Verify installation
   dagger functions  # Check available functions
   ```

### Debug Mode
```bash
# Verbose output
./scripts/quick-test-local.sh -v -t functional

# Clean and retry
./scripts/quick-test-local.sh --clean -t all

# Setup only (no tests)
./scripts/quick-test-local.sh --setup-only
```

## 🎯 Testing Scenarios

### Development Workflow
```bash
# 1. Quick functional check
./scripts/quick-test-local.sh -t functional

# 2. Security validation
./scripts/quick-test-local.sh -t security

# 3. Performance baseline
./scripts/quick-test-local.sh -t performance

# 4. Full validation
./scripts/quick-test-local.sh -t all
```

### CI/CD Integration
```bash
# In GitHub Actions
- name: Test MCP Server
  run: ./scripts/quick-test-local.sh --dagger -t all

# Local CI simulation
./scripts/quick-test-local.sh --dagger -t all --clean
```

### Production Validation
```bash
# Comprehensive testing
./scripts/quick-test-local.sh -t all -v

# Security audit
./scripts/quick-test-local.sh -t security -v

# Performance benchmarking
./scripts/quick-test-local.sh -t performance -v
```

## 📚 Documentation

- **[Complete Testing Guide](TESTING.md)**: Comprehensive framework documentation
- **[MCP Server Integration](examples/MCP_SERVER_INTEGRATION.md)**: Detailed integration guide
- **[API Reference](examples/API_REFERENCE.md)**: Testing API documentation
- **[Best Practices](examples/BEST_PRACTICES.md)**: Methodological pragmatism guidelines
- **[Troubleshooting](examples/TROUBLESHOOTING.md)**: Common issues and solutions

## 🚀 Next Steps

1. **Run Your First Test**:
   ```bash
   ./scripts/quick-test-local.sh
   ```

2. **Review Results**:
   ```bash
   cat test-results/pytest-mcp-server-report.md
   ```

3. **Explore Advanced Features**:
   ```bash
   ./scripts/quick-test-local.sh --help
   ```

4. **Set Up CI/CD**:
   - Configure GitHub Actions workflow
   - Add required secrets (API keys)
   - Enable automated testing

## 🎉 Success Metrics

After running tests, you should see:
- ✅ **Functional Tests**: MCP protocol compliance verified
- ✅ **Security Tests**: No critical vulnerabilities found
- ✅ **Performance Tests**: Response times within acceptable ranges
- ✅ **Issue Detection**: No critical issues detected
- ✅ **Confidence Scores**: 85%+ across all test categories

## 🤝 Contributing

To improve pytest-mcp-server testing:
1. Fork both repositories
2. Add new test scenarios
3. Submit pull requests with test results
4. Update documentation

---

**Ready to test?** Start with: `./scripts/quick-test-local.sh`

For questions or issues, refer to the [troubleshooting guide](examples/TROUBLESHOOTING.md) or open an issue. 