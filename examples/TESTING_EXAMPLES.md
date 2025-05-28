# MCP Testing Framework Examples

This document provides practical examples for using the MCP Testing Framework with real-world scenarios.

## Table of Contents

- [Quick Start Examples](#quick-start-examples)
- [Functional Testing Examples](#functional-testing-examples)
- [Security Testing Examples](#security-testing-examples)
- [Performance Testing Examples](#performance-testing-examples)
- [Issue Detection Examples](#issue-detection-examples)
- [Multi-Language Testing Examples](#multi-language-testing-examples)
- [CI/CD Integration Examples](#cicd-integration-examples)
- [Custom Test Scenarios](#custom-test-scenarios)

## Quick Start Examples

### 1. Basic Server Testing

Test a simple MCP server with minimal configuration:

```bash
# Test the example Python server
llm test server --command "python examples/python_mcp_server.py" --timeout 30

# Test with basic configuration
llm test basic --config examples/test-config-basic.json
```

### 2. Quick Functional Test

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def quick_test():
    tester = MCPServerTester()
    
    # Test server startup and basic functionality
    result = await tester.test_connection("python examples/python_mcp_server.py")
    print(f"Server connection: {result.status} (confidence: {result.confidence}%)")
    
    if result.status == "PASSED":
        # Test a simple tool
        tool_result = await tester.test_tool_execution("echo", {"message": "Hello, MCP!"})
        print(f"Tool test: {tool_result.status} (confidence: {tool_result.confidence}%)")

# Run the test
asyncio.run(quick_test())
```

## Functional Testing Examples

### 1. Comprehensive Tool Testing

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def test_all_tools():
    tester = MCPServerTester()
    
    # Connect to server
    await tester.connect("python examples/python_mcp_server.py")
    
    # Test each tool individually
    tools_to_test = [
        ("echo", {"message": "test"}),
        ("calculate", {"expression": "2 + 2"}),
        ("get_time", {}),
    ]
    
    for tool_name, params in tools_to_test:
        result = await tester.test_tool_execution(tool_name, params)
        print(f"{tool_name}: {result.status} (confidence: {result.confidence}%)")
        
        if result.status == "FAILED":
            print(f"  Error: {result.error_message}")
            print(f"  Suggestions: {result.remediation_suggestions}")

asyncio.run(test_all_tools())
```

### 2. Resource Testing

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def test_resources():
    tester = MCPServerTester()
    await tester.connect("python examples/python_mcp_server.py")
    
    # Test resource listing
    resources_result = await tester.test_resource_listing()
    print(f"Resource listing: {resources_result.status}")
    
    # Test individual resource access
    if resources_result.status == "PASSED":
        for resource in resources_result.data.get("resources", []):
            resource_result = await tester.test_resource_access(resource["uri"])
            print(f"Resource {resource['uri']}: {resource_result.status}")

asyncio.run(test_resources())
```

### 3. Prompt Testing

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def test_prompts():
    tester = MCPServerTester()
    await tester.connect("python examples/python_mcp_server.py")
    
    # Test prompt listing
    prompts_result = await tester.test_prompt_listing()
    print(f"Prompt listing: {prompts_result.status}")
    
    # Test prompt execution
    if prompts_result.status == "PASSED":
        for prompt in prompts_result.data.get("prompts", []):
            prompt_result = await tester.test_prompt_execution(
                prompt["name"], 
                {"topic": "testing"}
            )
            print(f"Prompt {prompt['name']}: {prompt_result.status}")

asyncio.run(test_prompts())
```

## Security Testing Examples

### 1. Authentication Testing

```python
import asyncio
from mcp_client_cli.testing import MCPSecurityTester

async def test_authentication():
    tester = MCPSecurityTester()
    
    # Test various authentication scenarios
    auth_tests = [
        ("no_credentials", {}),
        ("invalid_credentials", {"token": "invalid_token"}),
        ("malformed_headers", {"authorization": "malformed"}),
    ]
    
    for test_name, credentials in auth_tests:
        result = await tester.test_authentication_scenario(test_name, credentials)
        print(f"Auth test {test_name}: {result.status}")
        
        if result.vulnerabilities:
            for vuln in result.vulnerabilities:
                print(f"  Vulnerability: {vuln.description} (severity: {vuln.severity})")

asyncio.run(test_authentication())
```

### 2. Input Validation Testing

```python
import asyncio
from mcp_client_cli.testing import MCPSecurityTester

async def test_input_validation():
    tester = MCPSecurityTester()
    
    # Test with malicious payloads
    malicious_payloads = [
        "'; DROP TABLE users; --",  # SQL injection
        "<script>alert('xss')</script>",  # XSS
        "$(rm -rf /)",  # Command injection
        "../../../etc/passwd",  # Path traversal
    ]
    
    for payload in malicious_payloads:
        result = await tester.test_input_validation("echo", {"message": payload})
        print(f"Payload test: {result.status}")
        
        if result.status == "FAILED":
            print(f"  Server vulnerable to: {payload}")

asyncio.run(test_input_validation())
```

### 3. Authorization Testing

```python
import asyncio
from mcp_client_cli.testing import MCPSecurityTester

async def test_authorization():
    tester = MCPSecurityTester()
    
    # Test privilege escalation
    escalation_result = await tester.test_privilege_escalation()
    print(f"Privilege escalation test: {escalation_result.status}")
    
    # Test unauthorized tool access
    unauthorized_result = await tester.test_unauthorized_tool_access()
    print(f"Unauthorized access test: {unauthorized_result.status}")
    
    # Generate security report
    report = tester.generate_security_report()
    print(f"Overall security score: {report.overall_score}%")

asyncio.run(test_authorization())
```

## Performance Testing Examples

### 1. Tool Benchmarking

```python
import asyncio
from mcp_client_cli.testing import MCPPerformanceTester

async def benchmark_tools():
    tester = MCPPerformanceTester()
    
    # Benchmark individual tools
    tools = ["echo", "calculate", "get_time"]
    
    for tool_name in tools:
        benchmark = await tester.benchmark_tool_execution(
            tool_name, 
            {"message": "benchmark"} if tool_name == "echo" else {}
        )
        
        print(f"{tool_name} benchmark:")
        print(f"  Average response time: {benchmark.avg_response_time:.2f}ms")
        print(f"  95th percentile: {benchmark.p95_response_time:.2f}ms")
        print(f"  Throughput: {benchmark.throughput:.2f} req/s")

asyncio.run(benchmark_tools())
```

### 2. Load Testing

```python
import asyncio
from mcp_client_cli.testing import MCPPerformanceTester

async def load_test():
    tester = MCPPerformanceTester()
    
    # Test with increasing load
    connection_counts = [1, 5, 10, 25, 50]
    
    for connections in connection_counts:
        result = await tester.test_concurrent_connections(connections)
        
        print(f"Load test with {connections} connections:")
        print(f"  Success rate: {result.success_rate:.1f}%")
        print(f"  Average response time: {result.avg_response_time:.2f}ms")
        print(f"  Grade: {result.grade}")
        
        if result.grade in ["D", "F"]:
            print(f"  Performance degraded at {connections} connections")
            break

asyncio.run(load_test())
```

### 3. Resource Monitoring

```python
import asyncio
from mcp_client_cli.testing import MCPPerformanceTester

async def monitor_resources():
    tester = MCPPerformanceTester()
    
    # Start resource monitoring
    monitor = await tester.start_resource_monitoring()
    
    # Run some load
    await tester.test_concurrent_connections(10)
    
    # Get resource usage
    usage = await monitor.get_usage_stats()
    
    print(f"Resource usage during test:")
    print(f"  Peak memory: {usage.peak_memory_mb:.1f} MB")
    print(f"  Average CPU: {usage.avg_cpu_percent:.1f}%")
    print(f"  Memory leak detected: {usage.memory_leak_detected}")

asyncio.run(monitor_resources())
```

## Issue Detection Examples

### 1. Health Monitoring

```python
import asyncio
from mcp_client_cli.testing import MCPIssueDetector

async def monitor_health():
    detector = MCPIssueDetector()
    
    # Analyze server health
    issues = await detector.analyze_server_health("python examples/python_mcp_server.py")
    
    print(f"Found {len(issues)} issues:")
    for issue in issues:
        print(f"  {issue.type}: {issue.description}")
        print(f"    Severity: {issue.severity}")
        print(f"    Confidence: {issue.confidence}%")

asyncio.run(monitor_health())
```

### 2. Automated Remediation

```python
import asyncio
from mcp_client_cli.testing import MCPIssueDetector, MCPRemediationEngine

async def auto_remediate():
    detector = MCPIssueDetector()
    remediation = MCPRemediationEngine()
    
    # Detect and remediate issues
    issues = await detector.analyze_server_health("python examples/python_mcp_server.py")
    
    for issue in issues:
        if issue.severity.value >= 3:  # High severity
            print(f"Attempting to remediate: {issue.description}")
            
            result = await remediation.remediate_issue(issue)
            print(f"Remediation result: {result.status}")
            
            if result.status == "SUCCESS":
                print(f"  Actions taken: {result.actions_taken}")
            else:
                print(f"  Manual intervention required: {result.manual_steps}")

asyncio.run(auto_remediate())
```

## Multi-Language Testing Examples

### 1. Cross-Language Compatibility

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def test_cross_language():
    tester = MCPServerTester()
    
    servers = [
        ("Python", "python examples/python_mcp_server.py"),
        ("Node.js", "node examples/nodejs_mcp_server.js"),
    ]
    
    results = {}
    
    for name, command in servers:
        print(f"Testing {name} server...")
        
        # Test basic functionality
        connection_result = await tester.test_connection(command)
        tool_result = await tester.test_tool_execution("echo", {"message": "test"})
        
        results[name] = {
            "connection": connection_result.status,
            "tool_execution": tool_result.status,
            "confidence": (connection_result.confidence + tool_result.confidence) / 2
        }
    
    # Compare results
    print("\nCross-language compatibility:")
    for name, result in results.items():
        print(f"  {name}: {result['confidence']:.1f}% confidence")

asyncio.run(test_cross_language())
```

### 2. Protocol Compliance Testing

```bash
# Test both servers with Dagger
dagger call test-cross-language-integration --source .

# Compare implementations
dagger call run-integration-tests --source . --compare-languages true
```

## CI/CD Integration Examples

### 1. GitHub Actions Workflow

```yaml
# .github/workflows/mcp-testing.yml
name: MCP Server Testing

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -e ".[testing]"
        pip install dagger-io
    
    - name: Run MCP tests
      run: |
        llm test suite --config examples/test-config-basic.json --format json --output test-results.json
    
    - name: Run Dagger pipeline
      run: |
        dagger call run-full-test-suite --source . --generate-report true
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: |
          test-results.json
          test-report.html
```

### 2. Docker Testing

```dockerfile
# Dockerfile.test
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install -e ".[testing]"
RUN pip install dagger-io

# Run tests
CMD ["llm", "test", "suite", "--config", "examples/test-config-basic.json"]
```

```bash
# Build and run tests in Docker
docker build -f Dockerfile.test -t mcp-tests .
docker run --rm mcp-tests
```

## Custom Test Scenarios

### 1. Custom Test Configuration

```json
{
  "servers": {
    "custom-server": {
      "command": "python",
      "args": ["my_custom_server.py"],
      "env": {
        "API_KEY": "${API_KEY}",
        "DEBUG": "true"
      }
    }
  },
  "testing": {
    "functional": {
      "enabled": true,
      "custom_tests": [
        "test_custom_tool",
        "test_api_integration",
        "test_data_processing"
      ]
    }
  }
}
```

### 2. Custom Test Implementation

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

class CustomMCPTester(MCPServerTester):
    """Custom tester with domain-specific tests."""
    
    async def test_custom_tool(self):
        """Test a custom tool specific to your domain."""
        result = await self.test_tool_execution("custom_tool", {
            "input_data": "test_data",
            "options": {"format": "json"}
        })
        
        # Custom validation logic
        if result.status == "PASSED":
            response_data = result.data.get("response", {})
            if "processed_data" not in response_data:
                result.status = "FAILED"
                result.error_message = "Missing processed_data in response"
        
        return result
    
    async def test_api_integration(self):
        """Test integration with external APIs."""
        # Custom integration testing logic
        pass

# Usage
async def run_custom_tests():
    tester = CustomMCPTester()
    await tester.connect("python my_custom_server.py")
    
    custom_result = await tester.test_custom_tool()
    print(f"Custom tool test: {custom_result.status}")

asyncio.run(run_custom_tests())
```

### 3. Test Data Management

```python
import json
from pathlib import Path

class TestDataManager:
    """Manage test data for MCP testing."""
    
    def __init__(self, data_dir: str = "test_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load_test_cases(self, test_type: str):
        """Load test cases from JSON files."""
        file_path = self.data_dir / f"{test_type}_test_cases.json"
        if file_path.exists():
            with open(file_path) as f:
                return json.load(f)
        return []
    
    def save_test_results(self, test_type: str, results: dict):
        """Save test results for analysis."""
        file_path = self.data_dir / f"{test_type}_results.json"
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2)

# Usage
data_manager = TestDataManager()

# Load custom test cases
security_cases = data_manager.load_test_cases("security")
performance_cases = data_manager.load_test_cases("performance")

# Run tests with custom data
# ... test execution ...

# Save results
data_manager.save_test_results("security", security_results)
```

## Best Practices for Examples

### 1. Error Handling

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def robust_testing():
    tester = MCPServerTester()
    
    try:
        await tester.connect("python examples/python_mcp_server.py")
        
        # Test with proper error handling
        result = await tester.test_tool_execution("echo", {"message": "test"})
        
        if result.confidence < 80:
            print(f"Low confidence result: {result.confidence}%")
            print("Consider manual review")
        
    except Exception as e:
        print(f"Test execution failed: {e}")
        # Implement fallback or retry logic
    
    finally:
        await tester.disconnect()

asyncio.run(robust_testing())
```

### 2. Test Organization

```python
import asyncio
from dataclasses import dataclass
from typing import List
from mcp_client_cli.testing import MCPServerTester

@dataclass
class TestSuite:
    name: str
    tests: List[str]
    config: dict

class TestRunner:
    """Organized test execution."""
    
    def __init__(self):
        self.tester = MCPServerTester()
        self.results = {}
    
    async def run_suite(self, suite: TestSuite):
        """Run a complete test suite."""
        print(f"Running test suite: {suite.name}")
        
        suite_results = []
        for test_name in suite.tests:
            result = await self.run_test(test_name, suite.config)
            suite_results.append(result)
        
        self.results[suite.name] = suite_results
        return suite_results
    
    async def run_test(self, test_name: str, config: dict):
        """Run an individual test."""
        # Implement test execution logic
        pass

# Usage
runner = TestRunner()

functional_suite = TestSuite(
    name="Functional Tests",
    tests=["test_connection", "test_tools", "test_resources"],
    config={"timeout": 30}
)

asyncio.run(runner.run_suite(functional_suite))
```

---

These examples demonstrate practical usage of the MCP Testing Framework across different scenarios. Start with the basic examples and gradually move to more advanced testing as your needs grow.

For more detailed information, see the main [TESTING.md](../TESTING.md) documentation. 