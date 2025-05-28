# MCP Testing CLI Usage Guide

Complete guide for using the MCP Testing Framework command-line interface.

## Table of Contents

- [Installation](#installation)
- [Basic Commands](#basic-commands)
- [Testing Commands](#testing-commands)
- [Configuration](#configuration)
- [Output Formats](#output-formats)
- [Advanced Usage](#advanced-usage)
- [Dagger Integration](#dagger-integration)
- [Troubleshooting](#troubleshooting)

## Installation

```bash
# Install mcp-client-cli with testing support
pip install -e ".[testing]"

# Install Dagger.io for pipeline testing
pip install dagger-io

# Verify installation
llm --help
dagger --help
```

## Basic Commands

### Help and Information

```bash
# Show general help
llm --help

# Show testing-specific help
llm test --help

# Show version information
llm --version

# Show configuration
llm config show
```

### Server Management

```bash
# List configured servers
llm servers list

# Add a new server
llm servers add my-server --command "python my_server.py" --timeout 30

# Remove a server
llm servers remove my-server

# Test server connectivity
llm servers test my-server
```

## Testing Commands

### Quick Testing

```bash
# Test a server with minimal setup
llm test server --command "python examples/generic_mcp_server.py"

# Test with timeout
llm test server --command "python examples/generic_mcp_server.py" --timeout 60

# Test with environment variables
llm test server --command "python examples/generic_mcp_server.py" --env DEBUG=true --env LOG_LEVEL=info
```

### Functional Testing

```bash
# Run basic functional tests
llm test basic --config examples/test-config-basic.json

# Test specific functionality
llm test tools --server my-server
llm test resources --server my-server
llm test prompts --server my-server

# Test with custom parameters
llm test tools --server my-server --tool echo --params '{"message": "test"}'
```

### Security Testing

```bash
# Run security tests
llm test security --config examples/test-config-advanced.json

# Test specific security aspects
llm test security --authentication --authorization --input-validation

# Test with custom payloads
llm test security --payloads-file custom_payloads.json

# Generate security report
llm test security --report --output security-report.html
```

### Performance Testing

```bash
# Run performance tests
llm test performance --config examples/test-config-advanced.json

# Benchmark specific tools
llm test benchmark --server my-server --tool echo --iterations 100

# Load testing
llm test load --server my-server --connections 25 --duration 120

# Resource monitoring
llm test monitor --server my-server --duration 60 --interval 5
```

### Comprehensive Testing

```bash
# Run full test suite
llm test suite --config examples/test-config-advanced.json

# Run with specific test types
llm test suite --functional --security --performance

# Run with custom confidence thresholds
llm test suite --min-confidence 85 --security-min 90

# Generate comprehensive report
llm test suite --report --format html --output comprehensive-report.html
```

## Configuration

### Configuration Files

```bash
# Use specific configuration file
llm test suite --config my-test-config.json

# Validate configuration
llm config validate --file my-test-config.json

# Generate sample configuration
llm config generate --type basic --output basic-config.json
llm config generate --type advanced --output advanced-config.json
```

### Environment Variables

```bash
# Set default configuration
export MCP_TEST_CONFIG=examples/test-config-basic.json

# Set default timeout
export MCP_TEST_TIMEOUT=60

# Set debug mode
export MCP_TEST_DEBUG=true

# Set output directory
export MCP_TEST_OUTPUT_DIR=./test-results
```

### Runtime Configuration

```bash
# Override configuration values
llm test suite --config basic.json --set testing.functional.timeout=30

# Set multiple values
llm test suite --config basic.json \
  --set testing.security.enabled=true \
  --set testing.performance.concurrent_connections=10

# Use environment variable substitution
llm test suite --config config.json --env API_KEY=$MY_API_KEY
```

## Output Formats

### Console Output

```bash
# Default console output
llm test suite --config basic.json

# Verbose output
llm test suite --config basic.json --verbose

# Quiet output (errors only)
llm test suite --config basic.json --quiet

# Progress indicators
llm test suite --config basic.json --progress
```

### File Output

```bash
# JSON output
llm test suite --config basic.json --format json --output results.json

# HTML report
llm test suite --config basic.json --format html --output report.html

# CSV export
llm test suite --config basic.json --format csv --output results.csv

# XML output
llm test suite --config basic.json --format xml --output results.xml
```

### Multiple Formats

```bash
# Generate multiple output formats
llm test suite --config basic.json \
  --output-json results.json \
  --output-html report.html \
  --output-csv data.csv
```

## Advanced Usage

### Filtering and Selection

```bash
# Test specific servers only
llm test suite --config advanced.json --servers python-server,nodejs-server

# Test specific test types
llm test suite --config advanced.json --tests functional,security

# Skip certain tests
llm test suite --config advanced.json --skip performance,load

# Test with tags
llm test suite --config advanced.json --tags critical,regression
```

### Parallel Execution

```bash
# Run tests in parallel
llm test suite --config advanced.json --parallel --max-workers 4

# Control concurrency
llm test suite --config advanced.json --concurrent-tests 6

# Disable parallel execution
llm test suite --config advanced.json --no-parallel
```

### Retry and Recovery

```bash
# Set retry attempts
llm test suite --config basic.json --retry-attempts 3

# Set retry delay
llm test suite --config basic.json --retry-delay 5

# Continue on failure
llm test suite --config basic.json --continue-on-failure

# Fail fast mode
llm test suite --config basic.json --fail-fast
```

### Debugging and Diagnostics

```bash
# Enable debug mode
llm test suite --config basic.json --debug

# Save debug information
llm test suite --config basic.json --debug --debug-dir ./debug-output

# Capture network traffic
llm test suite --config basic.json --capture-traffic

# Profile performance
llm test suite --config basic.json --profile --profile-output profile.json
```

### Issue Detection and Remediation

```bash
# Enable automatic issue detection
llm test suite --config basic.json --detect-issues

# Enable automatic remediation
llm test suite --config basic.json --auto-remediate

# Generate remediation report
llm test suite --config basic.json --remediation-report remediation.html

# Manual remediation mode
llm test suite --config basic.json --manual-remediation
```

## Dagger Integration

### Basic Dagger Commands

```bash
# List available Dagger functions
dagger functions --source .

# Run basic tests with Dagger
dagger call test-environment --source .

# Install dependencies
dagger call install-dependencies --source .

# Validate installation
dagger call validate-installation --source .
```

### Language-Specific Testing

```bash
# Test Python MCP server
dagger call test-python-mcp-server --source . --server-path examples/generic_mcp_server.py

# Test Node.js MCP server
dagger call test-nodejs-mcp-server --source . --server-path examples/nodejs_mcp_server.js

# Cross-language integration testing
dagger call test-cross-language-integration --source .
```

### Pipeline Execution

```bash
# Run functional tests
dagger call run-functional-tests --source . --config-path examples/test-config-basic.json

# Run performance tests
dagger call run-performance-tests --source . --concurrent-connections 25

# Run integration tests
dagger call run-integration-tests --source . --test-matrix comprehensive

# Run full test suite
dagger call run-full-test-suite --source . --generate-report true
```

### Multi-Environment Testing

```bash
# Create multi-language environment
dagger call multi-language-environment --source .

# Test in different environments
dagger call run-integration-tests --source . --environments python,nodejs

# Compare language implementations
dagger call run-integration-tests --source . --compare-languages true
```

## Troubleshooting

### Common Issues

#### Server Connection Problems

```bash
# Test server connectivity
llm test server --command "python examples/generic_mcp_server.py" --debug

# Check server logs
llm test server --command "python examples/generic_mcp_server.py" --capture-logs

# Test with increased timeout
llm test server --command "python examples/generic_mcp_server.py" --timeout 120
```

#### Configuration Issues

```bash
# Validate configuration
llm config validate --file my-config.json

# Show effective configuration
llm config show --file my-config.json --resolved

# Test with minimal configuration
llm test basic --minimal-config
```

#### Performance Issues

```bash
# Profile test execution
llm test suite --config basic.json --profile

# Monitor resource usage
llm test monitor --server my-server --duration 60

# Test with reduced load
llm test suite --config basic.json --max-workers 1 --no-parallel
```

#### Dependency Issues

```bash
# Check dependencies
llm doctor

# Reinstall dependencies
pip install -e ".[testing]" --force-reinstall

# Test with Dagger
dagger call validate-installation --source .
```

### Debug Commands

```bash
# Enable verbose logging
llm test suite --config basic.json --log-level debug

# Save all debug information
llm test suite --config basic.json --debug --save-debug-info

# Test individual components
llm test connection --server my-server --debug
llm test tools --server my-server --tool echo --debug
llm test security --server my-server --test authentication --debug
```

### Getting Help

```bash
# Show detailed help for specific commands
llm test suite --help
llm test security --help
llm test performance --help

# Show configuration schema
llm config schema

# Show examples
llm examples list
llm examples show basic-testing
llm examples show security-testing
```

### Reporting Issues

```bash
# Generate diagnostic report
llm diagnostic --output diagnostic-report.json

# Test with issue tracking
llm test suite --config basic.json --track-issues --issue-report issues.json

# Export logs for support
llm test suite --config basic.json --export-logs support-logs.zip
```

## Command Reference

### Test Commands

| Command | Description | Example |
|---------|-------------|---------|
| `llm test server` | Test single server | `llm test server --command "python server.py"` |
| `llm test basic` | Basic functionality tests | `llm test basic --config basic.json` |
| `llm test tools` | Test MCP tools | `llm test tools --server my-server` |
| `llm test resources` | Test MCP resources | `llm test resources --server my-server` |
| `llm test prompts` | Test MCP prompts | `llm test prompts --server my-server` |
| `llm test security` | Security testing | `llm test security --config advanced.json` |
| `llm test performance` | Performance testing | `llm test performance --load-test` |
| `llm test suite` | Comprehensive testing | `llm test suite --config advanced.json` |

### Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `llm config show` | Show configuration | `llm config show --file config.json` |
| `llm config validate` | Validate configuration | `llm config validate --file config.json` |
| `llm config generate` | Generate sample config | `llm config generate --type advanced` |
| `llm config schema` | Show config schema | `llm config schema --format json` |

### Server Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `llm servers list` | List servers | `llm servers list` |
| `llm servers add` | Add server | `llm servers add my-server --command "python server.py"` |
| `llm servers remove` | Remove server | `llm servers remove my-server` |
| `llm servers test` | Test server | `llm servers test my-server` |

### Utility Commands

| Command | Description | Example |
|---------|-------------|---------|
| `llm doctor` | System diagnostics | `llm doctor` |
| `llm examples` | Show examples | `llm examples list` |
| `llm diagnostic` | Generate diagnostic report | `llm diagnostic --output report.json` |

---

This guide covers the essential CLI usage patterns for the MCP Testing Framework. For more detailed information about specific features, see the main [TESTING.md](../TESTING.md) documentation. 