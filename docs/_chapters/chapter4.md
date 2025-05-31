---
layout: chapter
title: "Basic Usage and Commands"
chapter_number: 4
description: "Essential commands and basic usage patterns for MCP-Client-CLI"
---

# Chapter 4: Basic Usage and Commands

## Command Line Interface Overview

The mcp-client-cli provides a powerful and flexible command-line interface for testing and validating MCP servers. Understanding this interface is essential for effective testing workflows. As documented in the [Quick Reference guide](https://github.com/tosin2013/mcp-client-cli/blob/main/QUICK_REFERENCE.md), the tool offers multiple entry points and a rich set of commands.

### Multiple Entry Points

The mcp-client-cli provides several command-line entry points to accommodate different workflows and preferences:

- **`mcp-test`**: The primary testing interface, focused on comprehensive MCP server validation
- **`mcp-testing`**: An alternative testing command with similar functionality
- **`mcp-client`**: Client interaction mode for direct communication with MCP servers
- **`llm`**: Legacy compatibility mode supporting older command structures

These entry points share core functionality but may offer slightly different command structures or default behaviors. For consistency, this chapter will focus on the `mcp-test` command, which is the recommended entry point for most testing scenarios.

### Command Structure

The general structure of mcp-client-cli commands follows a consistent pattern:

```
mcp-test [global-options] command [command-options]
```

Where:
- **global-options**: Apply to all commands (e.g., `--verbose`, `--config`)
- **command**: Specifies the action to perform (e.g., `test-server`, `run-suite`)
- **command-options**: Specific to the selected command

This hierarchical structure allows for intuitive and flexible command composition, making it easy to express complex testing requirements.

### Getting Help

The mcp-client-cli includes comprehensive built-in help documentation. To access this information:

```bash
# Display general help
mcp-test --help

# Get help for a specific command
mcp-test test-server --help

# Show version information
mcp-test --version
```

These help commands provide detailed information about available options, arguments, and usage examples, making them valuable references during testing.

## Core Commands and Syntax

The mcp-client-cli offers a wide range of commands for different testing scenarios. Let's explore the most important ones:

### Server Testing Commands

The primary purpose of the mcp-client-cli is to test MCP servers. Several commands facilitate this:

#### Basic Server Testing

```bash
# Test a specific MCP server
mcp-test test-server --command "python examples/generic_mcp_server.py"

# Test a server defined in the configuration file
mcp-test test-server --server-name your-server

# Test with specific test types
mcp-test test-server --server-name your-server --test-types functional,security
```

These commands initiate testing against the specified MCP server, running the default or specified test types.

#### Comprehensive Test Suites

For more thorough testing, you can run complete test suites:

```bash
# Run the default test suite
mcp-test run-suite --server-name your-server

# Run a specific test suite
mcp-test run-suite --suite-name comprehensive --server-name your-server

# Run a suite with custom parameters
mcp-test run-suite --suite-name security --server-name your-server --parameters '{"depth": "high"}'
```

Test suites combine multiple test types and scenarios, providing comprehensive validation of MCP server functionality.

### Specific Test Type Commands

The tool also offers commands for running specific types of tests:

#### Functional Testing

```bash
# Run functional tests
mcp-test functional --server-name your-server

# Test specific tools
mcp-test functional --server-name your-server --tools echo,file_read

# Test with custom parameters
mcp-test functional --server-name your-server --parameters '{"timeout": 30}'
```

Functional tests verify that the MCP server correctly implements the protocol and that its tools perform as expected.

#### Security Testing

```bash
# Run security tests
mcp-test security --server-name your-server

# Run specific security test categories
mcp-test security --server-name your-server --categories authentication,input-validation

# Include malicious payload testing
mcp-test security --server-name your-server --include-malicious-payloads
```

Security tests evaluate the server's resistance to various attacks and its adherence to security best practices.

#### Performance Testing

```bash
# Run performance tests
mcp-test performance --server-name your-server

# Specify test duration and concurrency
mcp-test performance --server-name your-server --duration 60 --concurrent-connections 10

# Enable resource monitoring
mcp-test performance --server-name your-server --monitor-resources
```

Performance tests assess the server's efficiency, responsiveness, and resource utilization under various conditions.

### Utility Commands

Beyond testing, the mcp-client-cli includes several utility commands:

#### Configuration Management

```bash
# Validate configuration
mcp-test validate-config

# Generate a sample configuration
mcp-test generate-config --output sample-config.json

# Update existing configuration
mcp-test update-config --set "testing.timeout=60"
```

These commands help manage your testing configuration, ensuring it's valid and up-to-date.

#### Reporting Commands

```bash
# Generate a test report
mcp-test generate-report --format html --output report.html

# View test history
mcp-test history --days 7

# Export test results
mcp-test export-results --format json --output results.json
```

Reporting commands provide insights into test results and history, facilitating analysis and documentation.

#### Tool Management

```bash
# List available tools
mcp-test list-tools

# Describe a specific tool
mcp-test describe-tool --tool-name echo

# Test a specific tool
mcp-test test-tool --server-name your-server --tool-name echo --parameters '{"message": "test"}'
```

These commands help you work with the tools provided by MCP servers, understanding their capabilities and testing their functionality.

## Configuration Files

While the mcp-client-cli can be used with command-line arguments alone, configuration files provide a more convenient and reproducible way to define testing parameters.

### Configuration File Formats

The tool supports configuration in multiple formats:

- **JSON**: The default and most common format
- **YAML**: An alternative format with more readable syntax
- **TOML**: Another alternative with a different structure

For consistency, this chapter focuses on JSON configuration, which is the format used in the official documentation.

### Basic Configuration Structure

As described in the [CONFIG.md](https://github.com/tosin2013/mcp-client-cli/blob/main/CONFIG.md) file, a typical configuration includes several sections:

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "api_key": "your-api-key"
  },
  "mcpServers": {
    "your-server": {
      "command": "python",
      "args": ["examples/generic_mcp_server.py"],
      "enabled": true
    }
  },
  "testing": {
    "timeout": 30,
    "retries": 3,
    "parallel": true
  }
}
```

This structure defines the LLM provider, MCP servers to test, and general testing parameters.

### Configuration File Location

By default, the mcp-client-cli looks for configuration in specific locations:

- **Primary location**: `~/.llm/config.json` (or equivalent for YAML/TOML)
- **Secondary location**: `./.llm/config.json` in the current directory

You can also specify a custom configuration file with the `--config` option:

```bash
mcp-test test-server --config custom-config.json
```

### Environment Variable Expansion

The configuration file supports environment variable expansion, allowing you to reference sensitive information without hardcoding it:

```json
{
  "llm": {
    "api_key": "${OPENAI_API_KEY}"
  }
}
```

In this example, the tool will replace `${OPENAI_API_KEY}` with the value of the corresponding environment variable.

### Configuration Inheritance and Overrides

The mcp-client-cli implements a hierarchical configuration system:

1. **Default values**: Built-in defaults for all settings
2. **Configuration file**: Values from your configuration file
3. **Environment variables**: Settings defined in environment variables
4. **Command-line arguments**: Options specified on the command line

Each level overrides the previous ones, with command-line arguments taking the highest precedence. This allows for flexible configuration management across different environments and use cases.

## Basic Testing Workflows

Now that we understand the commands and configuration options, let's explore some common testing workflows.

### Quick Server Validation

For a quick check of an MCP server's basic functionality:

```bash
# Define the server in your configuration file
# Then run:
mcp-test test-server --server-name your-server --test-types basic

# Or test directly without configuration:
mcp-test test-server --command "python examples/generic_mcp_server.py" --test-types basic
```

This workflow runs a minimal set of tests to verify that the server starts correctly, responds to basic requests, and implements the core protocol features.

### Comprehensive Server Testing

For thorough validation before deployment:

```bash
# Define the server and testing parameters in your configuration file
# Then run:
mcp-test run-suite --suite-name comprehensive --server-name your-server

# Generate a detailed report:
mcp-test generate-report --format html --output comprehensive-report.html
```

This workflow runs a complete test suite covering functional, security, and performance aspects, followed by report generation for documentation and analysis.

### Focused Testing

When addressing specific concerns or validating particular features:

```bash
# Test specific functionality:
mcp-test functional --server-name your-server --tools echo,file_read

# Focus on security aspects:
mcp-test security --server-name your-server --categories authentication,input-validation

# Evaluate performance under load:
mcp-test performance --server-name your-server --duration 60 --concurrent-connections 20
```

These focused workflows allow you to concentrate on specific aspects of your MCP server, streamlining the testing process when you don't need comprehensive validation.

### Continuous Integration

For automated testing in CI/CD pipelines:

```bash
# Typically run from a CI script:
mcp-test run-suite --suite-name ci --server-name your-server --format json --output results.json

# Check the exit code for pass/fail status:
if [ $? -eq 0 ]; then
  echo "Tests passed"
else
  echo "Tests failed"
  exit 1
fi
```

This workflow is designed for automation, using a CI-specific test suite and producing machine-readable output that can be easily integrated with CI/CD systems.

## Output Formats and Interpretation

The mcp-client-cli provides test results in various formats, each suited to different use cases.

### Console Output

By default, test results are displayed in the console with color-coding and formatting for readability:

```
✅ Connection test: PASSED
✅ Tool discovery: PASSED
✅ Echo tool test: PASSED
⚠️ File read tool test: WARNING (slow response time)
❌ Security test: FAILED (input validation issue)
```

This format is ideal for interactive use, providing immediate feedback during testing.

### Structured Output Formats

For programmatic processing or integration with other tools, structured output formats are available:

#### JSON Format

```bash
mcp-test test-server --server-name your-server --output-format json
```

Produces output like:

```json
{
  "status": "partial_success",
  "tests": [
    {
      "name": "connection_test",
      "status": "passed",
      "duration_ms": 127,
      "confidence": 100
    },
    {
      "name": "tool_discovery",
      "status": "passed",
      "duration_ms": 215,
      "confidence": 100
    },
    {
      "name": "echo_tool_test",
      "status": "passed",
      "duration_ms": 189,
      "confidence": 95
    },
    {
      "name": "file_read_tool_test",
      "status": "warning",
      "duration_ms": 1250,
      "confidence": 80,
      "message": "Slow response time detected"
    },
    {
      "name": "security_test",
      "status": "failed",
      "duration_ms": 312,
      "confidence": 90,
      "message": "Input validation issue detected",
      "details": {
        "vulnerability": "sql_injection",
        "severity": "high",
        "location": "query parameter"
      }
    }
  ],
  "summary": {
    "total": 5,
    "passed": 3,
    "warning": 1,
    "failed": 1,
    "overall_confidence": 93
  }
}
```

This format is ideal for programmatic processing and integration with other tools.

#### XML Format

```bash
mcp-test test-server --server-name your-server --output-format xml
```

Produces structured XML output suitable for integration with tools that expect XML data.

#### CSV Format

```bash
mcp-test test-server --server-name your-server --output-format csv
```

Generates comma-separated values, useful for importing into spreadsheets or data analysis tools.

### Report Formats

For documentation and presentation, the tool can generate formatted reports:

#### HTML Reports

```bash
mcp-test generate-report --format html --output report.html
```

Creates a comprehensive HTML report with test results, charts, and detailed information. This format is ideal for sharing with team members or stakeholders who need a clear overview of test results.

#### Markdown Reports

```bash
mcp-test generate-report --format markdown --output report.md
```

Produces a Markdown document that can be easily included in project documentation or converted to other formats.

#### PDF Reports

```bash
mcp-test generate-report --format pdf --output report.pdf
```

Generates a professional PDF report suitable for formal documentation or presentation.

### Interpreting Test Results

Test results include several key components that help you understand the state of your MCP server:

#### Status Indicators

- **PASSED**: The test completed successfully with no issues
- **WARNING**: The test completed but identified potential concerns
- **FAILED**: The test identified critical issues that need to be addressed
- **ERROR**: The test could not be completed due to an error in the testing process

#### Confidence Scores

Many tests include confidence scores (0-100%) indicating the reliability of the test results. As explained in the [TESTING.md](https://github.com/tosin2013/mcp-client-cli/blob/main/TESTING.md) documentation, these scores help you assess the certainty of the findings:

- **90-100%**: High confidence, very reliable results
- **70-89%**: Good confidence, generally reliable results
- **50-69%**: Moderate confidence, results should be verified
- **Below 50%**: Low confidence, results require manual verification

#### Performance Metrics

Performance tests include metrics such as:

- **Response Time**: How quickly the server responds to requests
- **Throughput**: How many requests the server can handle per second
- **Resource Usage**: CPU, memory, and other resource utilization
- **Scalability**: How performance changes under increasing load

These metrics help you assess the efficiency and capacity of your MCP server.

#### Security Findings

Security tests report findings with severity levels:

- **Critical**: Severe vulnerabilities requiring immediate attention
- **High**: Significant issues that should be addressed promptly
- **Medium**: Moderate concerns that should be addressed
- **Low**: Minor issues that pose limited risk
- **Info**: Informational findings with no direct security impact

Each finding includes details about the vulnerability, its location, and potential impact.

## Advanced Command Features

Beyond the basic commands, the mcp-client-cli offers several advanced features for more sophisticated testing scenarios.

### Parallel Testing

For testing multiple servers or running multiple test types simultaneously:

```bash
# Test multiple servers in parallel
mcp-test test-servers --server-names server1,server2,server3 --parallel

# Run multiple test types in parallel
mcp-test run-suite --suite-name comprehensive --server-name your-server --parallel-tests
```

Parallel testing can significantly reduce overall testing time, especially for comprehensive test suites.

### Filtering and Selection

To focus on specific aspects of your testing:

```bash
# Test specific tools
mcp-test functional --server-name your-server --include-tools echo,file_read

# Exclude certain tests
mcp-test security --server-name your-server --exclude-categories dos,csrf

# Filter by tags
mcp-test run-suite --suite-name comprehensive --server-name your-server --tags critical,regression
```

These filtering options allow you to customize your testing to focus on the most relevant aspects for your current needs.

### Custom Test Parameters

For fine-tuning test behavior:

```bash
# Set custom timeout
mcp-test test-server --server-name your-server --timeout 60

# Configure retry behavior
mcp-test test-server --server-name your-server --retries 5 --retry-delay 2

# Set custom thresholds
mcp-test performance --server-name your-server --max-response-time 500 --max-memory-usage 256
```

These parameters allow you to adapt the testing process to your specific requirements and constraints.

### Interactive Mode

For exploratory testing and debugging:

```bash
# Start interactive testing session
mcp-test interactive --server-name your-server
```

Interactive mode provides a REPL (Read-Eval-Print Loop) interface for directly interacting with the MCP server, sending custom requests, and examining responses in real-time.

## Practical Examples

Let's explore some practical examples that demonstrate how to use the mcp-client-cli in real-world scenarios.

### Example 1: Basic Server Validation

Scenario: You've developed a simple MCP server and want to verify its basic functionality.

```bash
# Create a minimal configuration file
cat > ~/.llm/config.json << EOF
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["my_mcp_server.py"],
      "enabled": true
    }
  }
}
EOF

# Run basic validation
mcp-test test-server --server-name my-server --test-types basic

# Check specific tools
mcp-test test-tool --server-name my-server --tool-name echo --parameters '{"message": "Hello, world!"}'
```

This example demonstrates a simple workflow for validating a new MCP server, focusing on basic functionality and specific tool testing.

### Example 2: Comprehensive Testing for Production

Scenario: You're preparing to deploy an MCP server to production and need thorough validation.

```bash
# Create a comprehensive configuration
cat > production-test-config.json << EOF
{
  "mcpServers": {
    "production-server": {
      "command": "node",
      "args": ["dist/server.js"],
      "env": {
        "NODE_ENV": "production",
        "LOG_LEVEL": "error"
      },
      "enabled": true
    }
  },
  "testing": {
    "timeout": 60,
    "retries": 3,
    "parallel": true,
    "confidence_threshold": 90
  },
  "security": {
    "enable_advanced_tests": true
  },
  "performance": {
    "duration": 300,
    "concurrent_connections": 50,
    "monitor_resources": true
  }
}
EOF

# Run comprehensive testing
mcp-test run-suite --suite-name production --config production-test-config.json

# Generate detailed report
mcp-test generate-report --format html --output production-readiness-report.html
```

This example shows a more comprehensive testing approach suitable for production deployment, including advanced security and performance testing.

### Example 3: CI/CD Integration

Scenario: You want to integrate MCP server testing into your CI/CD pipeline.

```bash
#!/bin/bash
# ci-test-script.sh

# Install the testing framework
pip install mcp-testing-framework

# Create configuration from environment variables
cat > ci-config.json << EOF
{
  "mcpServers": {
    "ci-server": {
      "command": "${SERVER_COMMAND}",
      "args": ${SERVER_ARGS},
      "env": {
        "CI": "true"
      },
      "enabled": true
    }
  }
}
EOF

# Run CI test suite
mcp-test run-suite --suite-name ci --config ci-config.json --output-format json --output results.json

# Check exit code
if [ $? -eq 0 ]; then
  echo "Tests passed"
  exit 0
else
  echo "Tests failed"
  exit 1
fi
```

This example demonstrates how to integrate the mcp-client-cli into a CI/CD pipeline, using environment variables for configuration and producing machine-readable output.

### Example 4: Security Audit

Scenario: You need to perform a security audit of an existing MCP server.

```bash
# Create security-focused configuration
cat > security-audit-config.json << EOF
{
  "mcpServers": {
    "audit-target": {
      "command": "python",
      "args": ["target_server.py"],
      "enabled": true
    }
  },
  "security": {
    "enable_advanced_tests": true,
    "include_malicious_payloads": true,
    "authentication_tests": true,
    "authorization_tests": true,
    "input_validation_tests": true,
    "data_protection_tests": true
  }
}
EOF

# Run security audit
mcp-test security --config security-audit-config.json --comprehensive

# Generate security report
mcp-test generate-report --format pdf --output security-audit-report.pdf
```

This example shows how to configure and run a comprehensive security audit, focusing exclusively on security aspects of the MCP server.

## Conclusion

This chapter has provided a comprehensive overview of the mcp-client-cli's command-line interface, covering core commands, configuration options, output formats, and practical examples. With this knowledge, you're well-equipped to begin testing your MCP servers using the tool's powerful capabilities.

In the next chapter, we'll delve deeper into the fundamentals of MCP server testing, exploring the principles and methodologies that underpin effective validation strategies.
