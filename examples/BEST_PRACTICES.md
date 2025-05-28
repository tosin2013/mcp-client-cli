# MCP Testing Framework Best Practices

Comprehensive best practices guide for effective MCP server testing using methodological pragmatism principles.

## Testing Philosophy

### Methodological Pragmatism Approach

Our testing framework follows these core principles:

1. **Explicit Fallibilism**: Acknowledge limitations in both human understanding and AI systems
2. **Systematic Verification**: Establish structured processes for validating functionality
3. **Pragmatic Success Criteria**: Prioritize what works reliably in real-world conditions
4. **Cognitive Systematization**: Organize testing knowledge into coherent systems

### Confidence-Based Testing

```python
# Always consider confidence scores
result = await tester.test_tool_execution("echo", {"message": "test"})
if result.confidence >= 80:
    print("High confidence - reliable result")
elif result.confidence >= 60:
    print("Medium confidence - consider additional verification")
else:
    print("Low confidence - investigate further")
```

## Test Design Principles

### 1. Test Pyramid Structure

- **Unit Tests (70%)**: Individual tool/resource testing
- **Integration Tests (20%)**: Multi-component workflows
- **E2E Tests (10%)**: Complete user scenarios

### 2. Comprehensive Coverage

```python
class ComprehensiveTestSuite:
    async def test_basic_functionality(self):
        # Connection, tools, resources, prompts
        pass
        
    async def test_error_conditions(self):
        # Invalid inputs, failures, timeouts
        pass
        
    async def test_performance_characteristics(self):
        # Response times, concurrency, resources
        pass
        
    async def test_security_aspects(self):
        # Input validation, auth, authorization
        pass
```

### 3. Test Independence

```python
class IndependentTestExample:
    async def setUp(self):
        self.tester = MCPServerTester(timeout=30)
        await self.tester.connect(self.server_command)
        
    async def tearDown(self):
        await self.tester.disconnect()
        # Clean up resources
```

## Configuration Best Practices

### Environment-Specific Configurations

```json
// development.json
{
  "servers": {
    "dev-server": {
      "timeout": 60,
      "retry_attempts": 5,
      "env": {"DEBUG": "true"}
    }
  },
  "testing": {
    "performance": {"enabled": false},
    "security": {"enabled": false}
  }
}

// production.json
{
  "servers": {
    "prod-server": {
      "timeout": 30,
      "retry_attempts": 3,
      "env": {"DEBUG": "false"}
    }
  },
  "testing": {
    "performance": {"enabled": true},
    "security": {"enabled": true}
  }
}
```

### Configuration Validation

```python
def validate_test_config(config):
    errors = []
    
    if 'servers' not in config:
        errors.append("Missing 'servers' configuration")
    
    for name, server in config.get('servers', {}).items():
        if 'command' not in server:
            errors.append(f"Server '{name}' missing 'command'")
        if server.get('timeout', 0) < 5:
            errors.append(f"Server '{name}' timeout too low")
    
    return errors
```

## Performance Testing Guidelines

### 1. Baseline Establishment

```python
async def establish_baseline():
    tester = MCPPerformanceTester()
    baseline = await tester.benchmark_tool_execution(
        "echo", {"message": "baseline"}, iterations=100
    )
    await store_baseline(baseline)
    return baseline
```

### 2. Progressive Load Testing

```python
async def progressive_load_test():
    connection_counts = [1, 5, 10, 20, 50]
    results = {}
    
    for count in connection_counts:
        config = PerformanceTestConfig(concurrent_connections=count)
        result = await tester.test_concurrent_connections(config)
        results[count] = result
        
        if result.avg_response_time > 5.0:  # Stop if degraded
            break
    
    return results
```

### 3. Resource Monitoring

```python
async def test_with_monitoring():
    monitor = ResourceMonitor()
    await monitor.start_monitoring()
    
    try:
        result = await tester.run_performance_tests()
        resource_report = await monitor.get_report()
        
        if resource_report.memory_leak_detected:
            print("WARNING: Memory leak detected")
    finally:
        await monitor.stop_monitoring()
```

## Security Testing Standards

### 1. Input Validation Testing

```python
async def test_input_validation():
    # Test various attack vectors
    payloads = [
        "'; DROP TABLE users; --",  # SQL injection
        "<script>alert('xss')</script>",  # XSS
        "; rm -rf /",  # Command injection
    ]
    
    for payload in payloads:
        result = await tester.test_input_validation("tool", payload)
        assert result.status != TestStatus.ERROR, f"Server crashed on: {payload}"
```

### 2. Authentication Testing

```python
async def test_authentication():
    # Test no credentials
    result = await tester.test_authentication(None)
    assert result.status == TestStatus.FAILED
    
    # Test invalid credentials
    result = await tester.test_authentication({"user": "invalid"})
    assert result.status == TestStatus.FAILED
    
    # Test valid credentials
    result = await tester.test_authentication({"user": "valid"})
    assert result.status == TestStatus.PASSED
```

## Error Handling and Recovery

### 1. Graceful Degradation

```python
async def test_with_graceful_degradation():
    try:
        result = await tester.test_tool_execution("primary_tool", params)
    except ConnectionError:
        result = await tester.test_tool_execution("fallback_tool", params)
    except TimeoutError:
        simplified_params = simplify_parameters(params)
        result = await tester.test_tool_execution("primary_tool", simplified_params)
    
    return result
```

### 2. Retry Mechanisms

```python
async def test_with_retry(max_retries=3, backoff_factor=2):
    for attempt in range(max_retries):
        try:
            result = await tester.test_tool_execution("tool", params)
            if result.confidence >= 70:
                return result
        except (ConnectionError, TimeoutError) as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = backoff_factor ** attempt
            await asyncio.sleep(wait_time)
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: MCP Server Testing
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: pip install -e ".[testing]"
    
    - name: Run tests
      run: |
        llm test examples/test-config-basic.json --output-format junit
        llm test examples/test-config-security.json --output-format junit
```

### Quality Gates

```python
class QualityGates:
    def __init__(self):
        self.min_confidence = 80
        self.max_response_time = 2.0
        self.min_success_rate = 95.0
    
    def check_quality_gates(self, test_results):
        failures = []
        
        avg_confidence = sum(r.confidence for r in test_results) / len(test_results)
        if avg_confidence < self.min_confidence:
            failures.append(f"Low confidence: {avg_confidence}")
        
        avg_response_time = sum(r.execution_time for r in test_results) / len(test_results)
        if avg_response_time > self.max_response_time:
            failures.append(f"Slow response: {avg_response_time}s")
        
        success_count = sum(1 for r in test_results if r.status == TestStatus.PASSED)
        success_rate = (success_count / len(test_results)) * 100
        if success_rate < self.min_success_rate:
            failures.append(f"Low success rate: {success_rate}%")
        
        return failures
```

## Monitoring and Observability

### 1. Structured Logging

```python
import structlog

logger = structlog.get_logger()

async def test_with_logging():
    logger.info("Starting test", test_name="tool_execution", tool="echo")
    
    try:
        result = await tester.test_tool_execution("echo", {"message": "test"})
        logger.info(
            "Test completed",
            status=result.status.value,
            confidence=result.confidence,
            execution_time=result.execution_time
        )
    except Exception as e:
        logger.error("Test failed", error=str(e), exc_info=True)
        raise
```

### 2. Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

test_counter = Counter('mcp_tests_total', 'Total tests', ['test_type', 'status'])
test_duration = Histogram('mcp_test_duration_seconds', 'Test duration', ['test_type'])
confidence_gauge = Gauge('mcp_test_confidence', 'Test confidence', ['test_type'])

async def test_with_metrics():
    test_type = "tool_execution"
    
    with test_duration.labels(test_type=test_type).time():
        result = await tester.test_tool_execution("echo", {"message": "test"})
        test_counter.labels(test_type=test_type, status=result.status.value).inc()
        confidence_gauge.labels(test_type=test_type).set(result.confidence)
```

### 3. Health Checks

```python
async def health_check():
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check server connectivity
    try:
        result = await tester.test_connection("python examples/python_mcp_server.py")
        health_status["checks"]["server_connection"] = {
            "status": "healthy" if result.status == TestStatus.PASSED else "unhealthy",
            "confidence": result.confidence
        }
    except Exception as e:
        health_status["checks"]["server_connection"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    return health_status
```

## Code Quality Standards

### 1. Type Hints and Documentation

```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class TestConfiguration:
    """Configuration for MCP server testing.
    
    Attributes:
        server_command: Command to start the MCP server
        timeout: Maximum time to wait for responses
        retry_attempts: Number of retry attempts
        environment: Environment variables
    """
    server_command: str
    timeout: int = 30
    retry_attempts: int = 3
    environment: Optional[Dict[str, str]] = None

async def test_tool_execution(
    tool_name: str,
    parameters: Dict[str, Any],
    timeout: Optional[int] = None
) -> TestResult:
    """Execute a tool and return test results.
    
    Args:
        tool_name: Name of the tool to execute
        parameters: Parameters to pass to the tool
        timeout: Optional timeout override
        
    Returns:
        TestResult containing execution status and metrics
        
    Raises:
        ConnectionError: If server connection fails
        TimeoutError: If execution exceeds timeout
    """
    pass
```

### 2. Error Handling Standards

```python
class MCPTestingError(Exception):
    """Base exception for MCP testing framework"""
    pass

class ServerConnectionError(MCPTestingError):
    """Raised when server connection fails"""
    pass

class TestExecutionError(MCPTestingError):
    """Raised when test execution fails"""
    pass

# Use specific exception handling
async def robust_test_execution():
    try:
        result = await tester.test_tool_execution("tool", params)
        return result
    except ServerConnectionError as e:
        logger.error("Server connection failed", error=str(e))
        await tester.reconnect()
        return await tester.test_tool_execution("tool", params)
    except TestExecutionError as e:
        logger.error("Test execution failed", error=str(e))
        return TestResult(
            status=TestStatus.FAILED,
            confidence=0,
            error_message=str(e)
        )
```

## Maintenance and Updates

### Regular Maintenance Tasks

```python
async def daily_maintenance():
    """Daily maintenance tasks"""
    await cleanup_old_test_results(days=30)
    await update_performance_baselines()
    await check_security_updates()
    await validate_all_configurations()

async def weekly_maintenance():
    """Weekly maintenance tasks"""
    await analyze_test_trends()
    await update_documentation()
    await review_test_cases()

async def monthly_maintenance():
    """Monthly maintenance tasks"""
    await conduct_performance_review()
    await conduct_security_audit()
    await update_dependencies()
```

### Continuous Improvement

```python
class ContinuousImprovement:
    async def collect_feedback(self):
        # Analyze test results and user feedback
        pass
    
    async def identify_improvements(self):
        # Analyze failure patterns and bottlenecks
        pass
    
    async def implement_improvements(self):
        # Update strategies and optimize performance
        pass
```

---

This best practices guide provides essential guidance for effective MCP server testing using methodological pragmatism principles. Follow these practices to ensure reliable, maintainable, and effective testing of your MCP servers. 