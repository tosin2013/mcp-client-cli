# MCP Testing Framework Troubleshooting Guide

Comprehensive troubleshooting guide for common issues with the MCP Testing Framework.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Connection Problems](#connection-problems)
- [Testing Failures](#testing-failures)
- [Performance Issues](#performance-issues)
- [Security Testing Problems](#security-testing-problems)
- [Dagger.io Pipeline Issues](#daggerio-pipeline-issues)
- [Configuration Problems](#configuration-problems)
- [Error Messages and Solutions](#error-messages-and-solutions)
- [Debugging Techniques](#debugging-techniques)
- [Getting Help](#getting-help)

## Installation Issues

### Problem: pip install fails with dependency conflicts

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently consider all the packages that are installed
```

**Solutions:**

1. **Use virtual environment:**
```bash
python -m venv mcp-testing-env
source mcp-testing-env/bin/activate  # On Windows: mcp-testing-env\Scripts\activate
pip install -e ".[testing]"
```

2. **Update pip and setuptools:**
```bash
pip install --upgrade pip setuptools wheel
pip install -e ".[testing]"
```

3. **Install with --force-reinstall:**
```bash
pip install --force-reinstall -e ".[testing]"
```

### Problem: Dagger.io installation fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement dagger-io
```

**Solutions:**

1. **Check Python version (requires 3.8+):**
```bash
python --version
```

2. **Install from specific index:**
```bash
pip install dagger-io --extra-index-url https://pypi.org/simple/
```

3. **Install development version:**
```bash
pip install git+https://github.com/dagger/dagger.git#subdirectory=sdk/python
```

### Problem: Import errors after installation

**Symptoms:**
```python
ImportError: No module named 'mcp_client_cli.testing'
```

**Solutions:**

1. **Verify installation:**
```bash
pip list | grep mcp-client-cli
```

2. **Reinstall in development mode:**
```bash
pip uninstall mcp-client-cli
pip install -e ".[testing]"
```

3. **Check Python path:**
```python
import sys
print(sys.path)
```

## Connection Problems

### Problem: Server connection timeout

**Symptoms:**
```
TimeoutError: Server connection timed out after 30 seconds
```

**Solutions:**

1. **Increase timeout:**
```python
tester = MCPServerTester(timeout=60)
```

2. **Check server startup time:**
```bash
time python examples/generic_mcp_server.py
```

3. **Verify server command:**
```bash
# Test server manually
python examples/generic_mcp_server.py
# Should start without errors
```

4. **Check system resources:**
```bash
# Monitor CPU and memory
top
# Or on Windows
taskmgr
```

### Problem: Server process fails to start

**Symptoms:**
```
ProcessError: Failed to start server process
```

**Solutions:**

1. **Check executable permissions:**
```bash
chmod +x examples/generic_mcp_server.py
```

2. **Verify Python path:**
```bash
which python
python --version
```

3. **Test server independently:**
```bash
python examples/generic_mcp_server.py --help
```

4. **Check environment variables:**
```python
import os
print(os.environ.get('PATH'))
```

### Problem: Connection refused

**Symptoms:**
```
ConnectionRefusedError: [Errno 61] Connection refused
```

**Solutions:**

1. **Check if server is listening:**
```bash
# For stdio servers, this shouldn't apply
# For TCP servers, check port availability
netstat -an | grep :8080
```

2. **Verify server configuration:**
```json
{
  "servers": {
    "test-server": {
      "command": "python",
      "args": ["examples/generic_mcp_server.py"],
      "timeout": 30
    }
  }
}
```

3. **Check firewall settings:**
```bash
# On macOS
sudo pfctl -sr
# On Linux
sudo iptables -L
```

## Testing Failures

### Problem: Tool execution tests fail

**Symptoms:**
```
TestResult(status=FAILED, confidence=25, error_message="Tool 'echo' not found")
```

**Solutions:**

1. **Verify tool availability:**
```python
# List available tools first
result = await tester.test_tool_listing()
print(result.data.get('tools', []))
```

2. **Check tool parameters:**
```python
# Use correct parameter format
await tester.test_tool_execution("echo", {"message": "test"})
# Not: {"text": "test"}
```

3. **Validate server implementation:**
```python
# Check server logs for tool registration
```

### Problem: Resource access tests fail

**Symptoms:**
```
TestResult(status=FAILED, confidence=30, error_message="Resource not accessible")
```

**Solutions:**

1. **Check resource URI format:**
```python
# Correct format
await tester.test_resource_access("file:///path/to/resource")
# Not: "/path/to/resource"
```

2. **Verify resource permissions:**
```bash
ls -la /path/to/resource
```

3. **Test resource listing first:**
```python
result = await tester.test_resource_listing()
print(result.data.get('resources', []))
```

### Problem: Low confidence scores

**Symptoms:**
```
TestResult(status=PASSED, confidence=45, ...)
```

**Solutions:**

1. **Improve response times:**
   - Optimize server code
   - Reduce startup time
   - Use connection pooling

2. **Reduce error patterns:**
   - Fix warning messages
   - Handle exceptions properly
   - Improve error messages

3. **Increase success rate:**
   - Add retry logic
   - Improve error handling
   - Validate inputs

## Performance Issues

### Problem: Slow test execution

**Symptoms:**
- Tests take longer than expected
- High CPU usage during testing
- Memory usage increases over time

**Solutions:**

1. **Optimize test configuration:**
```python
config = PerformanceTestConfig(
    concurrent_connections=5,  # Reduce from default
    test_duration=30,          # Reduce duration
    iterations=50              # Reduce iterations
)
```

2. **Use connection pooling:**
```python
# Reuse connections when possible
tester = MCPServerTester(timeout=30)
await tester.connect(command)
# Run multiple tests
await tester.disconnect()
```

3. **Monitor resource usage:**
```python
monitor = ResourceMonitor()
await monitor.start_monitoring()
# Run tests
report = await monitor.get_report()
```

### Problem: Memory leaks detected

**Symptoms:**
```
MemoryLeakDetected: Linear trend in memory usage detected
```

**Solutions:**

1. **Check server implementation:**
```python
# Ensure proper cleanup in server code
def cleanup():
    # Close connections
    # Free resources
    # Clear caches
```

2. **Reduce test duration:**
```python
config = PerformanceTestConfig(test_duration=60)  # Reduce from 300
```

3. **Monitor specific operations:**
```python
# Test individual operations for leaks
await tester.benchmark_tool_execution("tool", {}, iterations=10)
```

## Security Testing Problems

### Problem: Authentication tests not working

**Symptoms:**
```
SecurityTestResult(status=SKIPPED, message="Authentication not supported")
```

**Solutions:**

1. **Enable authentication in server:**
```python
# Server must implement authentication
class AuthenticatedMCPServer:
    def __init__(self):
        self.auth_required = True
```

2. **Configure authentication testing:**
```json
{
  "testing": {
    "security": {
      "enabled": true,
      "test_authentication": true,
      "auth_methods": ["basic", "token"]
    }
  }
}
```

3. **Provide test credentials:**
```python
config = SecurityTestConfig(
    test_credentials={
        "valid": {"username": "test", "password": "test"},
        "invalid": {"username": "bad", "password": "bad"}
    }
)
```

### Problem: Input validation tests fail

**Symptoms:**
```
SecurityTestResult(status=ERROR, message="Server crashed during input validation test")
```

**Solutions:**

1. **Implement proper input validation:**
```python
def validate_input(input_data):
    # Sanitize input
    # Check for malicious patterns
    # Return validated data
```

2. **Add error handling:**
```python
try:
    result = process_input(data)
except ValidationError:
    return error_response("Invalid input")
```

3. **Use gradual testing:**
```python
# Start with simple payloads
await tester.test_input_validation("tool", "simple_test")
# Then try more complex ones
await tester.test_input_validation("tool", "'; DROP TABLE users; --")
```

## Dagger.io Pipeline Issues

### Problem: Dagger functions not found

**Symptoms:**
```
dagger call --help
# No functions listed
```

**Solutions:**

1. **Check Dagger configuration:**
```bash
cat .dagger/dagger.json
```

2. **Verify module structure:**
```bash
ls -la .dagger/src/
```

3. **Reinstall Dagger module:**
```bash
cd .dagger
dagger develop
```

### Problem: Container build failures

**Symptoms:**
```
BuildError: Failed to build container
```

**Solutions:**

1. **Check Dockerfile syntax:**
```dockerfile
# Ensure proper syntax in container definitions
FROM python:3.12-slim
RUN pip install --no-cache-dir requirements.txt
```

2. **Verify base images:**
```python
# Use stable base images
container = dag.container().from_("python:3.12-slim")
```

3. **Check network connectivity:**
```bash
# Test Docker connectivity
docker pull python:3.12-slim
```

### Problem: Pipeline execution timeout

**Symptoms:**
```
TimeoutError: Pipeline execution exceeded timeout
```

**Solutions:**

1. **Increase pipeline timeout:**
```python
@function
async def run_tests(self, timeout: int = 600) -> str:
    # Increased from default 300
```

2. **Optimize pipeline steps:**
```python
# Cache dependencies
container = container.with_mounted_cache("/root/.cache/pip", cache_volume)
```

3. **Parallelize operations:**
```python
# Run tests in parallel
tasks = [
    self.test_python_server(),
    self.test_nodejs_server()
]
results = await asyncio.gather(*tasks)
```

## Configuration Problems

### Problem: Invalid JSON configuration

**Symptoms:**
```
JSONDecodeError: Expecting ',' delimiter
```

**Solutions:**

1. **Validate JSON syntax:**
```bash
python -m json.tool test-config.json
```

2. **Use JSON linter:**
```bash
# Install jsonlint
npm install -g jsonlint
jsonlint test-config.json
```

3. **Check for common issues:**
   - Trailing commas
   - Missing quotes
   - Incorrect nesting

### Problem: Configuration not loaded

**Symptoms:**
```
ConfigurationError: No configuration found
```

**Solutions:**

1. **Check file path:**
```python
import os
print(os.path.exists("test-config.json"))
```

2. **Verify file permissions:**
```bash
ls -la test-config.json
```

3. **Use absolute path:**
```python
config_path = os.path.abspath("test-config.json")
```

## Error Messages and Solutions

### Common Error Patterns

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | Missing MCP dependency | `pip install mcp` |
| `AttributeError: 'NoneType' object has no attribute` | Uninitialized object | Check object initialization |
| `asyncio.TimeoutError` | Operation timeout | Increase timeout values |
| `ConnectionResetError` | Server disconnection | Implement reconnection logic |
| `PermissionError: [Errno 13]` | File permissions | `chmod +r filename` |
| `OSError: [Errno 48] Address already in use` | Port conflict | Use different port or kill process |

### Debugging Error Messages

1. **Enable debug logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Use verbose output:**
```bash
llm test --verbose --debug
```

3. **Check server logs:**
```python
# Add logging to server
import logging
logger = logging.getLogger(__name__)
logger.info("Server started")
```

## Debugging Techniques

### 1. Enable Comprehensive Logging

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_testing.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Enable MCP client logging
logging.getLogger('mcp').setLevel(logging.DEBUG)
```

### 2. Use Test Isolation

```python
# Test components individually
async def debug_connection():
    tester = MCPServerTester(timeout=60)
    result = await tester.test_connection("python examples/generic_mcp_server.py")
    print(f"Connection: {result}")
    
async def debug_tools():
    # Test after successful connection
    result = await tester.test_tool_listing()
    print(f"Tools: {result}")
```

### 3. Monitor System Resources

```bash
# Monitor during testing
# Terminal 1: Run tests
llm test examples/test-config-basic.json

# Terminal 2: Monitor resources
top -p $(pgrep -f generic_mcp_server)
```

### 4. Use Confidence Analysis

```python
# Analyze confidence factors
result = await tester.test_tool_execution("echo", {"message": "test"})
print(f"Confidence: {result.confidence}")
print(f"Execution time: {result.execution_time}")
print(f"Error patterns: {result.data.get('error_patterns', [])}")
```

### 5. Test with Minimal Configuration

```json
{
  "servers": {
    "minimal": {
      "command": "python",
      "args": ["-c", "print('Hello MCP')"],
      "timeout": 10
    }
  },
  "testing": {
    "functional": {
      "enabled": true,
      "test_tools": false,
      "test_resources": false,
      "test_prompts": false
    }
  }
}
```

## Getting Help

### 1. Check Documentation

- [TESTING.md](../TESTING.md) - Main documentation
- [API_REFERENCE.md](API_REFERENCE.md) - API documentation
- [TESTING_EXAMPLES.md](TESTING_EXAMPLES.md) - Usage examples

### 2. Enable Verbose Output

```bash
# Get detailed output
llm test --verbose --debug examples/test-config-basic.json
```

### 3. Collect Diagnostic Information

```bash
# System information
python --version
pip list | grep -E "(mcp|dagger)"
uname -a

# Test environment
python -c "import mcp_client_cli.testing; print('Testing module loaded')"
dagger version
```

### 4. Create Minimal Reproduction

```python
# Minimal test case
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def minimal_test():
    tester = MCPServerTester(timeout=30)
    try:
        result = await tester.test_connection("echo 'test'")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(minimal_test())
```

### 5. Report Issues

When reporting issues, include:

1. **Environment information:**
   - Operating system
   - Python version
   - Package versions

2. **Configuration:**
   - Test configuration file
   - Server command and arguments

3. **Error details:**
   - Full error message
   - Stack trace
   - Log files

4. **Reproduction steps:**
   - Minimal code to reproduce
   - Expected vs actual behavior

### 6. Community Resources

- GitHub Issues: Report bugs and feature requests
- Documentation: Check for updates and examples
- Stack Overflow: Search for similar issues

---

This troubleshooting guide covers the most common issues with the MCP Testing Framework. For additional help, refer to the [API Reference](API_REFERENCE.md) and [Testing Examples](TESTING_EXAMPLES.md). 