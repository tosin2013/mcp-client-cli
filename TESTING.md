# MCP Testing Framework Documentation

A comprehensive testing infrastructure for MCP (Model Context Protocol) servers using mcp-client-cli and Dagger.io pipelines, following methodological pragmatism principles.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Testing Framework Components](#testing-framework-components)
- [Configuration](#configuration)
- [Testing Types](#testing-types)
- [CLI Testing Commands](#cli-testing-commands)
- [Dagger.io Pipelines](#daggerio-pipelines)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Performance Tuning](#performance-tuning)
- [Security Testing Guidelines](#security-testing-guidelines)
- [Confidence Scoring](#confidence-scoring)
- [Methodological Pragmatism](#methodological-pragmatism)

## Overview

The MCP Testing Framework provides systematic testing capabilities for MCP servers with:

- **Functional Testing**: Validate MCP server functionality, tool execution, and configuration
- **Security Testing**: Authentication, authorization, input validation, and data sanitization
- **Performance Testing**: Benchmarking, load testing, and resource monitoring
- **Issue Detection**: Automated problem identification and remediation
- **Multi-Language Support**: Python and Node.js MCP server testing
- **CI/CD Integration**: Dagger.io pipelines for automated testing workflows

### Key Features

- ✅ **Systematic Verification**: Following methodological pragmatism principles
- ✅ **Error Architecture Awareness**: Distinguishing human-cognitive vs artificial-stochastic errors
- ✅ **Confidence Scoring**: Quantified reliability assessment for test results
- ✅ **Automated Remediation**: Self-healing mechanisms for common issues
- ✅ **Comprehensive Reporting**: Detailed test results with actionable insights

## Quick Start

### 1. Install Dependencies

```bash
# Install the MCP client CLI with testing dependencies
pip install -e ".[testing]"

# Install Dagger.io for pipeline testing
pip install dagger-io
```

### 2. Basic Testing

```bash
# Run basic MCP server tests
llm test basic --server-config examples/test-config-basic.json

# Run comprehensive test suite
llm test suite --config examples/test-config-advanced.json

# Run security tests
llm test security --server-config examples/test-config-basic.json
```

### 3. Dagger Pipeline Testing

```bash
# Run functional tests via Dagger
dagger call run-functional-tests --source .

# Run full test suite with reporting
dagger call run-full-test-suite --source . --generate-report true

# Run performance benchmarks
dagger call run-performance-tests --source . --benchmark-mode true
```

## Testing Framework Components

### Core Testing Framework

Located in `src/mcp_client_cli/testing/`:

- **`mcp_tester.py`**: Core MCPServerTester class with async testing capabilities
- **`test_storage.py`**: TestResultManager for persistent test result storage
- **`cli_integration.py`**: MCPTestCLI for rich command-line integration

### Security Testing

- **`security_tester.py`**: MCPSecurityTester for comprehensive security validation
- Authentication testing (credentials, tokens, headers)
- Authorization testing (privilege escalation, access controls)
- Input validation and data sanitization testing

### Performance Testing

- **`performance_tester.py`**: MCPPerformanceTester for benchmarking and profiling
- Tool execution benchmarking with response time measurement
- Concurrent connection testing and scalability analysis
- Resource usage monitoring with memory leak detection

### Issue Detection and Remediation

- **`issue_detector.py`**: MCPIssueDetector for automated problem identification
- **`remediation.py`**: MCPRemediationEngine for self-healing mechanisms
- **`issue_storage.py`**: IssueTrackingManager for issue persistence and analytics

## Configuration

### Basic Test Configuration

Create a test configuration file (e.g., `test-config.json`):

```json
{
  "servers": {
    "test-server": {
      "command": "python",
      "args": ["examples/generic_mcp_server.py"],
      "timeout": 30,
      "retry_attempts": 3
    }
  },
  "testing": {
    "functional": {
      "enabled": true,
      "test_tools": true,
      "test_resources": true,
      "test_prompts": true
    },
    "security": {
      "enabled": true,
      "test_authentication": true,
      "test_authorization": true,
      "test_input_validation": true
    },
    "performance": {
      "enabled": true,
      "benchmark_tools": true,
      "concurrent_connections": 10,
      "test_duration": 60
    }
  },
  "confidence_thresholds": {
    "minimum_pass": 80,
    "high_confidence": 95
  }
}
```

### Advanced Configuration

For complex testing scenarios, see `examples/test-config-advanced.json`:

```json
{
  "servers": {
    "python-server": {
      "command": "python",
      "args": ["examples/generic_mcp_server.py"],
      "env": {
        "DEBUG": "true"
      },
      "timeout": 30
    },
    "nodejs-server": {
      "command": "node",
      "args": ["examples/nodejs_mcp_server.js"],
      "timeout": 30
    }
  },
  "testing": {
    "functional": {
      "enabled": true,
      "test_tools": true,
      "test_resources": true,
      "test_prompts": true,
      "custom_tests": [
        "test_tool_echo",
        "test_resource_list",
        "test_prompt_generation"
      ]
    },
    "security": {
      "enabled": true,
      "test_authentication": true,
      "test_authorization": true,
      "test_input_validation": true,
      "malicious_payloads": true,
      "custom_security_tests": [
        "test_sql_injection",
        "test_xss_prevention",
        "test_command_injection"
      ]
    },
    "performance": {
      "enabled": true,
      "benchmark_tools": true,
      "concurrent_connections": 50,
      "test_duration": 300,
      "memory_monitoring": true,
      "resource_limits": {
        "max_memory_mb": 512,
        "max_cpu_percent": 80
      }
    },
    "issue_detection": {
      "enabled": true,
      "auto_remediation": true,
      "monitoring_interval": 5,
      "health_checks": true
    }
  },
  "reporting": {
    "format": "html",
    "include_charts": true,
    "confidence_analysis": true,
    "remediation_suggestions": true
  },
  "confidence_thresholds": {
    "minimum_pass": 85,
    "high_confidence": 95,
    "security_minimum": 90,
    "performance_minimum": 80
  }
}
```

## Testing Types

### 1. Functional Testing

Tests core MCP server functionality:

```python
from mcp_client_cli.testing import MCPServerTester

async def test_functional():
    tester = MCPServerTester()
    
    # Test server connection
    result = await tester.test_connection("python examples/generic_mcp_server.py")
    print(f"Connection test: {result.status} (confidence: {result.confidence}%)")
    
    # Test tool execution
    result = await tester.test_tool_execution("echo", {"message": "Hello, World!"})
    print(f"Tool test: {result.status} (confidence: {result.confidence}%)")
```

### 2. Security Testing

Validates security aspects:

```python
from mcp_client_cli.testing import MCPSecurityTester

async def test_security():
    tester = MCPSecurityTester()
    
    # Test authentication
    auth_results = await tester.test_authentication()
    
    # Test input validation
    validation_results = await tester.test_input_validation()
    
    # Generate security report
    report = tester.generate_security_report()
    print(f"Security score: {report.overall_score}%")
```

### 3. Performance Testing

Benchmarks and profiling:

```python
from mcp_client_cli.testing import MCPPerformanceTester

async def test_performance():
    tester = MCPPerformanceTester()
    
    # Benchmark tool execution
    benchmark = await tester.benchmark_tool_execution("echo", {"message": "test"})
    print(f"Average response time: {benchmark.avg_response_time}ms")
    
    # Test concurrent connections
    load_test = await tester.test_concurrent_connections(connections=10)
    print(f"Concurrent test grade: {load_test.grade}")
```

### 4. Issue Detection and Remediation

Automated problem resolution:

```python
from mcp_client_cli.testing import MCPIssueDetector, MCPRemediationEngine

async def test_issue_detection():
    detector = MCPIssueDetector()
    remediation = MCPRemediationEngine()
    
    # Detect issues
    issues = await detector.analyze_server_health("python examples/generic_mcp_server.py")
    
    # Auto-remediate if possible
    for issue in issues:
        if issue.severity.value >= 3:  # High severity
            result = await remediation.remediate_issue(issue)
            print(f"Remediation: {result.status}")
```

## CLI Testing Commands

### Basic Commands

```bash
# Test a single MCP server
llm test server --command "python examples/generic_mcp_server.py"

# Run functional tests
llm test functional --config test-config.json

# Run security tests
llm test security --config test-config.json --include-malicious-payloads

# Run performance tests
llm test performance --config test-config.json --duration 60
```

### Advanced Commands

```bash
# Run comprehensive test suite
llm test suite --config test-config.json --parallel --generate-report

# Test with issue detection
llm test suite --config test-config.json --auto-remediation

# Multi-language testing
llm test multi-lang --python-server "python examples/generic_mcp_server.py" \
                    --nodejs-server "node examples/nodejs_mcp_server.js"

# Custom confidence thresholds
llm test suite --config test-config.json --min-confidence 90
```

### Reporting Commands

```bash
# Generate HTML report
llm test report --format html --output test-report.html

# View test history
llm test history --days 7

# Export test results
llm test export --format json --output results.json
```

## Dagger.io Pipelines

### Available Pipeline Functions

```bash
# List all available functions
dagger functions

# Basic environment setup
dagger call test-environment
dagger call nodejs-test-environment
dagger call multi-language-environment

# Dependency management
dagger call install-dependencies --source .
dagger call setup-mcp-client --source .

# Testing functions
dagger call run-functional-tests --source . --include-security true
dagger call run-performance-tests --source . --benchmark-mode true
dagger call run-integration-tests --source .

# Comprehensive testing
dagger call run-full-test-suite --source . --parallel true --generate-report true
```

### Pipeline Configuration

Create `.dagger/pipeline-config.json`:

```json
{
  "environments": {
    "python": {
      "version": "3.12",
      "dependencies": ["mcp", "langchain", "rich"]
    },
    "nodejs": {
      "version": "18",
      "dependencies": ["@modelcontextprotocol/sdk"]
    }
  },
  "testing": {
    "parallel_execution": true,
    "timeout_seconds": 300,
    "retry_attempts": 3
  },
  "reporting": {
    "generate_html": true,
    "include_performance_charts": true,
    "confidence_analysis": true
  }
}
```

## Best Practices

### 1. Test Organization

- **Separate test configurations** for different environments (dev, staging, prod)
- **Use descriptive test names** that clearly indicate what's being tested
- **Group related tests** into test suites for better organization
- **Maintain test data** separately from test logic

### 2. Confidence Scoring

- **Set appropriate thresholds** based on your quality requirements
- **Monitor confidence trends** over time to identify degradation
- **Use high confidence tests** for critical functionality
- **Review low confidence results** manually for potential issues

### 3. Security Testing

- **Test with realistic payloads** that match your threat model
- **Include both positive and negative test cases**
- **Regularly update malicious payload databases**
- **Test authentication and authorization separately**

### 4. Performance Testing

- **Establish baseline metrics** before making changes
- **Test under realistic load conditions**
- **Monitor resource usage** during performance tests
- **Use consistent test environments** for reliable comparisons

### 5. Issue Detection

- **Enable auto-remediation** for well-understood issues
- **Monitor remediation success rates** and adjust strategies
- **Maintain issue pattern databases** for better detection
- **Review unresolved issues** regularly for manual intervention

## Troubleshooting

### Common Issues

#### 1. Server Connection Failures

**Symptoms**: Connection timeout, server not responding
**Solutions**:
- Check server command and arguments
- Verify environment variables are set correctly
- Increase timeout values in configuration
- Check server logs for startup errors

```bash
# Debug server startup
llm test server --command "python examples/generic_mcp_server.py" --debug --timeout 60
```

#### 2. Tool Execution Failures

**Symptoms**: Tool calls fail, unexpected responses
**Solutions**:
- Validate tool parameters and types
- Check tool implementation for errors
- Test tools individually before integration testing
- Review tool documentation for correct usage

```bash
# Test individual tool
llm test tool --server-config test-config.json --tool-name "echo" --params '{"message": "test"}'
```

#### 3. Performance Issues

**Symptoms**: Slow response times, high resource usage
**Solutions**:
- Profile server performance under load
- Check for memory leaks or resource exhaustion
- Optimize tool implementations
- Adjust concurrent connection limits

```bash
# Performance profiling
llm test performance --config test-config.json --profile --duration 30
```

#### 4. Security Test Failures

**Symptoms**: Authentication/authorization failures, input validation issues
**Solutions**:
- Review security configuration
- Check credential management
- Validate input sanitization logic
- Test with known-good security configurations

```bash
# Security debugging
llm test security --config test-config.json --verbose --include-details
```

### Debugging Commands

```bash
# Enable debug logging
export MCP_TEST_DEBUG=true
llm test suite --config test-config.json

# Verbose output
llm test functional --config test-config.json --verbose

# Save debug information
llm test suite --config test-config.json --save-debug-info debug-output/
```

## Performance Tuning

### 1. Test Execution Optimization

```json
{
  "testing": {
    "parallel_execution": true,
    "max_concurrent_tests": 4,
    "test_timeout": 30,
    "retry_strategy": {
      "max_attempts": 3,
      "backoff_factor": 2,
      "jitter": true
    }
  }
}
```

### 2. Resource Management

```json
{
  "performance": {
    "resource_limits": {
      "max_memory_mb": 512,
      "max_cpu_percent": 80,
      "max_open_files": 1024
    },
    "monitoring": {
      "sample_interval": 1,
      "memory_leak_detection": true,
      "resource_cleanup": true
    }
  }
}
```

### 3. Caching and Optimization

```json
{
  "optimization": {
    "cache_test_results": true,
    "cache_duration": 3600,
    "reuse_connections": true,
    "connection_pooling": {
      "max_connections": 10,
      "idle_timeout": 30
    }
  }
}
```

## Security Testing Guidelines

### 1. Authentication Testing

Test various authentication scenarios:

```json
{
  "security": {
    "authentication": {
      "test_no_credentials": true,
      "test_invalid_credentials": true,
      "test_expired_credentials": true,
      "test_malformed_headers": true,
      "custom_auth_tests": [
        "test_token_validation",
        "test_session_management"
      ]
    }
  }
}
```

### 2. Input Validation Testing

Comprehensive input validation:

```json
{
  "security": {
    "input_validation": {
      "test_sql_injection": true,
      "test_xss_prevention": true,
      "test_command_injection": true,
      "test_path_traversal": true,
      "custom_payloads": [
        "'; DROP TABLE users; --",
        "<script>alert('xss')</script>",
        "$(rm -rf /)"
      ]
    }
  }
}
```

### 3. Authorization Testing

Access control validation:

```json
{
  "security": {
    "authorization": {
      "test_privilege_escalation": true,
      "test_unauthorized_access": true,
      "test_resource_isolation": true,
      "role_based_tests": {
        "admin": ["all_tools", "all_resources"],
        "user": ["limited_tools", "user_resources"],
        "guest": ["public_tools", "public_resources"]
      }
    }
  }
}
```

## Confidence Scoring

### Understanding Confidence Scores

Confidence scores (0-100%) indicate the reliability of test results:

- **95-100%**: High confidence - Results are highly reliable
- **85-94%**: Good confidence - Results are generally reliable
- **70-84%**: Moderate confidence - Results should be reviewed
- **50-69%**: Low confidence - Results require manual verification
- **0-49%**: Very low confidence - Results are unreliable

### Factors Affecting Confidence

1. **Test Execution Success**: Clean execution without errors
2. **Response Consistency**: Consistent results across multiple runs
3. **Error Handling**: Proper error detection and reporting
4. **Resource Availability**: Adequate system resources during testing
5. **Network Stability**: Stable network conditions for remote servers

### Confidence Configuration

```json
{
  "confidence": {
    "thresholds": {
      "minimum_pass": 80,
      "high_confidence": 95,
      "security_minimum": 90,
      "performance_minimum": 75
    },
    "factors": {
      "execution_success": 40,
      "response_consistency": 30,
      "error_handling": 20,
      "resource_availability": 10
    }
  }
}
```

## Methodological Pragmatism

This testing framework follows methodological pragmatism principles:

### 1. Explicit Fallibilism

- **Acknowledge limitations** of both human and AI understanding
- **Provide confidence scores** rather than absolute certainty
- **Enable manual review** of uncertain results
- **Document known limitations** and edge cases

### 2. Systematic Verification

- **Structured testing processes** with clear verification steps
- **Reproducible test procedures** with consistent environments
- **Comprehensive test coverage** across multiple dimensions
- **Automated validation** with human oversight capabilities

### 3. Pragmatic Success Criteria

- **Focus on practical outcomes** rather than theoretical perfection
- **Prioritize reliability** over comprehensive coverage
- **Adapt testing strategies** based on real-world constraints
- **Balance thoroughness** with execution efficiency

### 4. Error Architecture Awareness

#### Human-Cognitive Errors
- **Knowledge gaps** in domain understanding
- **Attention limitations** leading to inconsistencies
- **Cognitive biases** affecting judgment

#### Artificial-Stochastic Errors
- **Pattern completion errors** merging incompatible patterns
- **Context window limitations** affecting consistency
- **Training data artifacts** leading to outdated practices

### Implementation in Testing

```python
class TestResult:
    """Test result with methodological pragmatism principles."""
    
    def __init__(self, status: TestStatus, confidence: float, 
                 error_type: Optional[ErrorType] = None):
        self.status = status
        self.confidence = confidence  # Explicit fallibilism
        self.error_type = error_type  # Error architecture awareness
        self.verification_steps = []  # Systematic verification
        self.practical_impact = None  # Pragmatic success criteria
```

### Best Practices for Pragmatic Testing

1. **Always include confidence scores** in test results
2. **Distinguish between error types** when failures occur
3. **Provide actionable remediation suggestions**
4. **Enable iterative improvement** based on test outcomes
5. **Document assumptions and limitations** clearly
6. **Focus on practical reliability** over theoretical completeness

---

## Getting Help

- **Documentation**: See this file and CONFIG.md for detailed configuration
- **Examples**: Check the `examples/` directory for practical configurations
- **Issues**: Report bugs and feature requests on GitHub
- **Community**: Join discussions about MCP testing best practices

For more information about the Model Context Protocol, visit [modelcontextprotocol.io](https://modelcontextprotocol.io/). 