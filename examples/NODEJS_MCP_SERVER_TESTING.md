# Node.js MCP Server Testing Guide

This guide explains how to use the universal MCP testing framework with **Node.js MCP servers**, including GitHub Actions integration, security scanning, and performance benchmarking.

## 🚀 Quick Start

### 1. One-Command Testing

Test any Node.js MCP server repository:

```bash
# Auto-detect and test Node.js MCP server
./scripts/quick-test-local.sh --repo-url https://github.com/your-org/your-nodejs-mcp-server.git --server-type nodejs

# Test current Node.js repository
llm test-server --auto-detect --server-type nodejs

# Test with specific Node.js configuration
llm test-server --config examples/test-nodejs-mcp-server.json
```

### 2. GitHub Actions Integration

Copy the workflow file to your Node.js MCP server repository:

```bash
# In your Node.js MCP server repository
mkdir -p .github/workflows
curl -o .github/workflows/mcp-self-test.yml \
  https://raw.githubusercontent.com/your-org/mcp-client-cli/master/examples/github-actions/nodejs-mcp-server-self-test.yml
```

## 📋 Node.js-Specific Features

### Multi-Version Testing

The workflow tests across multiple Node.js versions:
- **Node.js 18.x** (LTS)
- **Node.js 20.x** (LTS)
- **Node.js 22.x** (Current)

### Security Tools Integration

#### npm audit
- Vulnerability scanning for dependencies
- HTML reports with `npm-audit-html`
- Configurable audit levels

#### ESLint Security Scanning
- `eslint-plugin-security` for security-focused linting
- `@microsoft/eslint-plugin-sdl` for SDL compliance
- Custom security-focused ESLint configuration

#### Semgrep Integration
- Advanced static analysis
- Node.js and TypeScript specific rules
- SARIF output for GitHub Security tab

### Performance Tools

#### Autocannon Load Testing
- HTTP load testing for MCP servers with HTTP endpoints
- Concurrent connection testing
- JSON output for analysis

#### Clinic.js Integration
- Performance profiling and diagnostics
- Memory leak detection
- CPU usage analysis

### Dependency Management

#### Package Analysis
- `npm outdated` for dependency updates
- License checking with `license-checker`
- Dependency vulnerability assessment

## 🔧 Configuration

### Basic Configuration

Create `examples/test-nodejs-mcp-server.json`:

```json
{
  "server": {
    "type": "nodejs",
    "command": "node",
    "args": ["server.js"],
    "cwd": "./",
    "env": {
      "NODE_ENV": "test",
      "PORT": "3000"
    },
    "startup_timeout": 10,
    "health_check": {
      "enabled": true,
      "endpoint": "http://localhost:3000/health",
      "timeout": 5
    }
  },
  "testing": {
    "types": ["functional", "security", "performance", "issue-detection"],
    "confidence_threshold": 0.8,
    "parallel_execution": true,
    "timeout": 300
  },
  "security": {
    "npm_audit": {
      "enabled": true,
      "audit_level": "moderate",
      "exclude_dev": false
    },
    "eslint_security": {
      "enabled": true,
      "config": ".eslintrc.security.json"
    },
    "semgrep": {
      "enabled": true,
      "config": ["p/security-audit", "p/nodejs", "p/typescript"]
    }
  },
  "performance": {
    "load_testing": {
      "enabled": true,
      "tool": "autocannon",
      "concurrent_connections": [1, 5, 10, 20],
      "duration": 10,
      "endpoint": "http://localhost:3000"
    },
    "profiling": {
      "enabled": true,
      "tools": ["clinic"],
      "memory_monitoring": true
    }
  }
}
```

### Advanced Configuration

For complex Node.js MCP servers:

```json
{
  "server": {
    "type": "nodejs",
    "command": "npm",
    "args": ["start"],
    "cwd": "./",
    "env": {
      "NODE_ENV": "test",
      "DEBUG": "mcp:*",
      "MCP_SERVER_PORT": "3000"
    },
    "build_command": "npm run build",
    "startup_timeout": 30,
    "health_check": {
      "enabled": true,
      "endpoint": "http://localhost:3000/health",
      "timeout": 10,
      "retries": 3
    }
  },
  "testing": {
    "types": ["functional", "security", "performance", "integration", "issue-detection"],
    "confidence_threshold": 0.85,
    "parallel_execution": true,
    "timeout": 600,
    "retry_failed": true,
    "retry_count": 2
  },
  "security": {
    "npm_audit": {
      "enabled": true,
      "audit_level": "low",
      "exclude_dev": true,
      "output_format": ["json", "html"]
    },
    "eslint_security": {
      "enabled": true,
      "config": ".eslintrc.security.json",
      "extensions": [".js", ".ts", ".mjs"],
      "ignore_patterns": ["node_modules/", "dist/", "build/"]
    },
    "semgrep": {
      "enabled": true,
      "config": [
        "p/security-audit",
        "p/nodejs",
        "p/typescript",
        "p/owasp-top-10"
      ],
      "exclude_patterns": ["test/", "*.test.js", "*.spec.ts"]
    },
    "custom_checks": {
      "enabled": true,
      "scripts": ["./scripts/security-check.js"]
    }
  },
  "performance": {
    "load_testing": {
      "enabled": true,
      "tool": "autocannon",
      "concurrent_connections": [1, 5, 10, 20, 50],
      "duration": 30,
      "endpoints": [
        "http://localhost:3000/",
        "http://localhost:3000/api/health",
        "http://localhost:3000/mcp/tools"
      ],
      "custom_headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer test-token"
      }
    },
    "profiling": {
      "enabled": true,
      "tools": ["clinic", "0x"],
      "memory_monitoring": true,
      "cpu_monitoring": true,
      "heap_snapshots": true
    },
    "benchmarks": {
      "enabled": true,
      "scenarios": [
        {
          "name": "tool_execution",
          "endpoint": "/mcp/tools/execute",
          "method": "POST",
          "payload": {"tool": "test_tool", "args": {}}
        }
      ]
    }
  },
  "integration": {
    "cross_language": {
      "enabled": true,
      "python_server": "./python_server.py",
      "test_interop": true
    },
    "external_services": {
      "enabled": false,
      "services": []
    }
  }
}
```

## 🔍 Testing Types

### 1. Functional Testing

Tests core MCP functionality:

```bash
# Test MCP protocol compliance
llm test-functional --server-type nodejs --test-mcp-protocol

# Test tool execution
llm test-functional --server-type nodejs --test-tools

# Test resource access
llm test-functional --server-type nodejs --test-resources
```

### 2. Security Testing

Comprehensive security analysis:

```bash
# Run all security tests
llm test-security --server-type nodejs

# npm audit only
llm test-security --server-type nodejs --npm-audit-only

# ESLint security scan
llm test-security --server-type nodejs --eslint-security-only

# Semgrep analysis
llm test-security --server-type nodejs --semgrep-only
```

### 3. Performance Testing

Performance benchmarking and profiling:

```bash
# Load testing with autocannon
llm test-performance --server-type nodejs --load-test

# Memory profiling
llm test-performance --server-type nodejs --memory-profile

# CPU profiling
llm test-performance --server-type nodejs --cpu-profile

# Full performance suite
llm test-performance --server-type nodejs --full-suite
```

### 4. Integration Testing

Cross-language and service integration:

```bash
# Test with Python MCP server
llm test-integration --nodejs-server ./server.js --python-server ./server.py

# Test external service integration
llm test-integration --server-type nodejs --external-services
```

## 📊 GitHub Actions Workflow

### Workflow Structure

The Node.js workflow includes 5 main jobs:

1. **self-test**: Core MCP testing across Node.js versions
2. **security-scan**: Security analysis with multiple tools
3. **performance-benchmark**: Performance testing and profiling
4. **dependency-check**: Dependency analysis and license checking
5. **generate-summary**: Comprehensive reporting

### Workflow Triggers

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:     # Manual trigger
```

### Customization

#### Environment Variables

```yaml
env:
  NODE_ENV: test
  MCP_SERVER_PORT: 3000
  DEBUG: mcp:*
  NPM_CONFIG_AUDIT_LEVEL: moderate
```

#### Matrix Strategy

```yaml
strategy:
  matrix:
    node-version: [18.x, 20.x, 22.x]
    os: [ubuntu-latest, windows-latest, macos-latest]  # Optional
```

#### Custom Test Types

```yaml
- name: Run Custom Tests
  run: |
    cd mcp-testing-framework
    python scripts/pytest-mcp-server-workflow.py \
      --path ../nodejs-mcp-server \
      --server-type nodejs \
      --test-types custom,integration \
      --custom-config ../nodejs-mcp-server/.mcp-test-config.json
```

## 🛠️ Development Integration

### Pre-commit Hooks

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: mcp-test
        name: MCP Server Testing
        entry: llm test-server --auto-detect --server-type nodejs --quick
        language: system
        pass_filenames: false
        always_run: true
```

### npm Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "test:mcp": "llm test-server --auto-detect --server-type nodejs",
    "test:mcp:security": "llm test-security --server-type nodejs",
    "test:mcp:performance": "llm test-performance --server-type nodejs",
    "test:mcp:full": "llm test-server --auto-detect --server-type nodejs --tests functional,security,performance"
  }
}
```

### VS Code Integration

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "MCP Test Server",
      "type": "shell",
      "command": "llm",
      "args": ["test-server", "--auto-detect", "--server-type", "nodejs"],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    }
  ]
}
```

## 📈 Results and Reporting

### Test Results Structure

```
test-results-node-20.x/
├── workflow_results_20241201_143022.json
├── functional_test_results.json
├── security_test_results.json
├── performance_test_results.json
├── integration_report.md
├── confidence_scores.json
└── recommendations.md
```

### Confidence Scoring

All results include confidence scores (0.0-1.0):

```json
{
  "test_type": "functional",
  "status": "PASSED",
  "confidence": 0.92,
  "details": {
    "mcp_protocol_compliance": {
      "score": 0.95,
      "tests_passed": 18,
      "tests_total": 19
    },
    "tool_execution": {
      "score": 0.89,
      "tests_passed": 8,
      "tests_total": 9
    }
  }
}
```

### Performance Metrics

```json
{
  "load_testing": {
    "autocannon_results": {
      "requests_per_second": 1250.5,
      "latency_p50": 12.3,
      "latency_p95": 45.7,
      "latency_p99": 89.2,
      "errors": 0
    }
  },
  "profiling": {
    "memory_usage": {
      "peak_heap": "45.2 MB",
      "heap_growth": "2.1 MB/min"
    },
    "cpu_usage": {
      "average": "15.3%",
      "peak": "67.8%"
    }
  }
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. npm audit Failures

```bash
# Fix vulnerabilities
npm audit fix

# Force fix (use with caution)
npm audit fix --force

# Skip audit in testing
export NPM_CONFIG_AUDIT_LEVEL=none
```

#### 2. ESLint Security Issues

```bash
# Install missing plugins
npm install --save-dev eslint-plugin-security @microsoft/eslint-plugin-sdl

# Fix auto-fixable issues
npx eslint . --fix --config .eslintrc.security.json
```

#### 3. Performance Test Failures

```bash
# Check server startup
npm start &
sleep 5
curl http://localhost:3000/health

# Increase timeouts
export MCP_TEST_TIMEOUT=60
```

#### 4. Dependency Issues

```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Debug Mode

Enable debug output:

```bash
export DEBUG=mcp:*,test:*
export MCP_TEST_VERBOSE=true
llm test-server --auto-detect --server-type nodejs --debug
```

## 🌟 Best Practices

### 1. Repository Structure

```
your-nodejs-mcp-server/
├── src/
│   ├── server.js
│   ├── tools/
│   └── resources/
├── test/
│   ├── unit/
│   ├── integration/
│   └── mcp/
├── .github/
│   └── workflows/
│       └── mcp-self-test.yml
├── .mcp-test-config.json
├── package.json
├── .eslintrc.security.json
└── README.md
```

### 2. Configuration Management

- Use environment-specific configs
- Separate test and production settings
- Include health check endpoints
- Configure proper timeouts

### 3. Security Considerations

- Regular dependency updates
- Security-focused linting
- Input validation testing
- Authentication/authorization testing

### 4. Performance Optimization

- Monitor memory usage
- Profile CPU-intensive operations
- Test under load
- Optimize startup time

### 5. CI/CD Integration

- Run tests on multiple Node.js versions
- Include security scans
- Generate comprehensive reports
- Fail fast on critical issues

## 📚 Additional Resources

- [Node.js MCP Server Examples](examples/nodejs_mcp_server.js)
- [Security Configuration Guide](examples/SECURITY_GUIDE.md)
- [Performance Tuning Guide](examples/PERFORMANCE_GUIDE.md)
- [Troubleshooting Guide](examples/TROUBLESHOOTING.md)
- [API Reference](examples/API_REFERENCE.md)

---

*This guide is part of the universal MCP testing framework. For Python servers, see [TESTING_PYTEST_MCP_SERVER.md](TESTING_PYTEST_MCP_SERVER.md).* 