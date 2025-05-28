# MCP Testing Framework API Reference

Complete API reference for the MCP Testing Framework Python modules.

## Table of Contents

- [Core Testing Module](#core-testing-module)
- [Security Testing Module](#security-testing-module)
- [Performance Testing Module](#performance-testing-module)
- [Issue Detection Module](#issue-detection-module)
- [Remediation Engine Module](#remediation-engine-module)
- [Storage Module](#storage-module)
- [CLI Integration Module](#cli-integration-module)
- [Data Classes](#data-classes)
- [Enums](#enums)
- [Exceptions](#exceptions)
- [Utilities](#utilities)

## Core Testing Module

### MCPServerTester

Main class for testing MCP servers with comprehensive functionality.

```python
from mcp_client_cli.testing import MCPServerTester

class MCPServerTester:
    """Comprehensive MCP server testing with confidence scoring."""
```

#### Constructor

```python
def __init__(self, 
             timeout: int = 30,
             retry_attempts: int = 3,
             confidence_threshold: int = 80):
    """
    Initialize the MCP server tester.
    
    Args:
        timeout: Default timeout for operations (seconds)
        retry_attempts: Number of retry attempts for failed operations
        confidence_threshold: Minimum confidence score for passing tests
    """
```

#### Connection Methods

```python
async def connect(self, command: str, args: List[str] = None, 
                 env: Dict[str, str] = None) -> TestResult:
    """
    Connect to an MCP server.
    
    Args:
        command: Server command to execute
        args: Command arguments
        env: Environment variables
        
    Returns:
        TestResult with connection status and confidence score
    """

async def disconnect(self) -> None:
    """Disconnect from the MCP server."""

async def test_connection(self, command: str, **kwargs) -> TestResult:
    """Test server connection without maintaining the connection."""
```

#### Tool Testing Methods

```python
async def test_tool_execution(self, tool_name: str, 
                             parameters: Dict[str, Any]) -> TestResult:
    """
    Test execution of a specific tool.
    
    Args:
        tool_name: Name of the tool to test
        parameters: Tool parameters
        
    Returns:
        TestResult with execution status and confidence score
    """

async def test_tool_listing(self) -> TestResult:
    """Test listing available tools."""

async def benchmark_tool(self, tool_name: str, parameters: Dict[str, Any],
                        iterations: int = 10) -> TestResult:
    """Benchmark tool execution performance."""
```

#### Resource Testing Methods

```python
async def test_resource_listing(self) -> TestResult:
    """Test listing available resources."""

async def test_resource_access(self, resource_uri: str) -> TestResult:
    """
    Test access to a specific resource.
    
    Args:
        resource_uri: URI of the resource to test
        
    Returns:
        TestResult with access status and confidence score
    """

async def test_resource_content(self, resource_uri: str) -> TestResult:
    """Test resource content retrieval."""
```

#### Prompt Testing Methods

```python
async def test_prompt_listing(self) -> TestResult:
    """Test listing available prompts."""

async def test_prompt_execution(self, prompt_name: str,
                               arguments: Dict[str, Any]) -> TestResult:
    """
    Test execution of a specific prompt.
    
    Args:
        prompt_name: Name of the prompt to test
        arguments: Prompt arguments
        
    Returns:
        TestResult with execution status and confidence score
    """
```

#### Comprehensive Testing Methods

```python
async def run_comprehensive_test(self, command: str, **kwargs) -> TestSuite:
    """
    Run comprehensive test suite on an MCP server.
    
    Args:
        command: Server command
        **kwargs: Additional configuration options
        
    Returns:
        TestSuite with all test results
    """

async def validate_mcp_compliance(self, command: str) -> TestResult:
    """Validate MCP protocol compliance."""
```

## Security Testing Module

### MCPSecurityTester

Specialized class for security testing of MCP servers.

```python
from mcp_client_cli.testing import MCPSecurityTester

class MCPSecurityTester:
    """Security testing for MCP servers with vulnerability detection."""
```

#### Constructor

```python
def __init__(self, config: SecurityTestConfig = None):
    """
    Initialize security tester.
    
    Args:
        config: Security testing configuration
    """
```

#### Authentication Testing

```python
async def test_authentication_scenario(self, scenario: str,
                                     credentials: Dict[str, Any]) -> SecurityTestResult:
    """
    Test authentication scenarios.
    
    Args:
        scenario: Authentication scenario name
        credentials: Credentials to test
        
    Returns:
        SecurityTestResult with vulnerabilities found
    """

async def test_no_credentials(self) -> SecurityTestResult:
    """Test server behavior with no credentials."""

async def test_invalid_credentials(self) -> SecurityTestResult:
    """Test server behavior with invalid credentials."""

async def test_expired_credentials(self) -> SecurityTestResult:
    """Test server behavior with expired credentials."""
```

#### Authorization Testing

```python
async def test_privilege_escalation(self) -> SecurityTestResult:
    """Test for privilege escalation vulnerabilities."""

async def test_unauthorized_tool_access(self) -> SecurityTestResult:
    """Test unauthorized access to tools."""

async def test_resource_access_controls(self) -> SecurityTestResult:
    """Test resource access control mechanisms."""
```

#### Input Validation Testing

```python
async def test_input_validation(self, tool_name: str,
                               malicious_input: str) -> SecurityTestResult:
    """
    Test input validation with malicious payloads.
    
    Args:
        tool_name: Tool to test
        malicious_input: Malicious payload
        
    Returns:
        SecurityTestResult with vulnerability assessment
    """

async def test_sql_injection(self) -> SecurityTestResult:
    """Test for SQL injection vulnerabilities."""

async def test_xss_prevention(self) -> SecurityTestResult:
    """Test for XSS prevention mechanisms."""

async def test_command_injection(self) -> SecurityTestResult:
    """Test for command injection vulnerabilities."""

async def test_path_traversal(self) -> SecurityTestResult:
    """Test for path traversal vulnerabilities."""
```

#### Security Reporting

```python
def generate_security_report(self) -> SecurityReport:
    """Generate comprehensive security report."""

def get_vulnerability_summary(self) -> Dict[str, int]:
    """Get summary of vulnerabilities by severity."""
```

## Performance Testing Module

### MCPPerformanceTester

Specialized class for performance testing and benchmarking.

```python
from mcp_client_cli.testing import MCPPerformanceTester

class MCPPerformanceTester:
    """Performance testing and benchmarking for MCP servers."""
```

#### Constructor

```python
def __init__(self, config: PerformanceTestConfig = None):
    """
    Initialize performance tester.
    
    Args:
        config: Performance testing configuration
    """
```

#### Benchmarking Methods

```python
async def benchmark_tool_execution(self, tool_name: str,
                                  parameters: Dict[str, Any],
                                  iterations: int = 100) -> PerformanceMetrics:
    """
    Benchmark tool execution performance.
    
    Args:
        tool_name: Tool to benchmark
        parameters: Tool parameters
        iterations: Number of iterations
        
    Returns:
        PerformanceMetrics with timing statistics
    """

async def benchmark_connection_setup(self, iterations: int = 50) -> PerformanceMetrics:
    """Benchmark connection setup time."""

async def benchmark_resource_access(self, resource_uri: str,
                                   iterations: int = 50) -> PerformanceMetrics:
    """Benchmark resource access performance."""
```

#### Load Testing Methods

```python
async def test_concurrent_connections(self, connection_count: int,
                                    duration: int = 60) -> LoadTestResult:
    """
    Test server performance under concurrent connections.
    
    Args:
        connection_count: Number of concurrent connections
        duration: Test duration in seconds
        
    Returns:
        LoadTestResult with performance metrics
    """

async def test_sustained_load(self, requests_per_second: int,
                             duration: int = 300) -> LoadTestResult:
    """Test server performance under sustained load."""

async def test_burst_load(self, burst_size: int,
                         burst_interval: int = 10) -> LoadTestResult:
    """Test server performance under burst load."""
```

#### Resource Monitoring

```python
async def start_resource_monitoring(self) -> ResourceMonitor:
    """Start monitoring system resources."""

async def monitor_memory_usage(self, duration: int = 60) -> MemoryUsageReport:
    """Monitor memory usage during testing."""

async def monitor_cpu_usage(self, duration: int = 60) -> CPUUsageReport:
    """Monitor CPU usage during testing."""

def detect_memory_leaks(self, usage_data: List[float]) -> bool:
    """Detect memory leaks from usage data."""
```

#### Performance Analysis

```python
def calculate_performance_grade(self, metrics: PerformanceMetrics) -> str:
    """Calculate performance grade (A-F) from metrics."""

def identify_bottlenecks(self, metrics: PerformanceMetrics) -> List[str]:
    """Identify performance bottlenecks."""

def generate_performance_report(self) -> PerformanceReport:
    """Generate comprehensive performance report."""
```

## Issue Detection Module

### MCPIssueDetector

Automated issue detection and health monitoring.

```python
from mcp_client_cli.testing import MCPIssueDetector

class MCPIssueDetector:
    """Automated issue detection and health monitoring for MCP servers."""
```

#### Constructor

```python
def __init__(self, patterns_file: str = None):
    """
    Initialize issue detector.
    
    Args:
        patterns_file: Path to custom issue patterns file
    """
```

#### Issue Detection Methods

```python
async def analyze_server_health(self, command: str) -> List[Issue]:
    """
    Analyze server health and detect issues.
    
    Args:
        command: Server command to analyze
        
    Returns:
        List of detected issues
    """

async def detect_connection_issues(self, command: str) -> List[Issue]:
    """Detect connection-related issues."""

async def detect_performance_issues(self, metrics: PerformanceMetrics) -> List[Issue]:
    """Detect performance-related issues."""

async def detect_security_issues(self, security_results: List[SecurityTestResult]) -> List[Issue]:
    """Detect security-related issues."""
```

#### Pattern Matching

```python
def match_error_patterns(self, error_message: str) -> List[IssuePattern]:
    """
    Match error messages against known patterns.
    
    Args:
        error_message: Error message to analyze
        
    Returns:
        List of matching issue patterns
    """

def add_custom_pattern(self, pattern: IssuePattern) -> None:
    """Add custom issue detection pattern."""

def update_pattern_confidence(self, pattern_id: str, confidence: int) -> None:
    """Update pattern confidence based on feedback."""
```

#### Health Monitoring

```python
async def monitor_health_continuously(self, command: str,
                                    interval: int = 60) -> AsyncIterator[HealthMetrics]:
    """
    Continuously monitor server health.
    
    Args:
        command: Server command to monitor
        interval: Monitoring interval in seconds
        
    Yields:
        HealthMetrics for each monitoring cycle
    """

def calculate_health_score(self, metrics: HealthMetrics) -> int:
    """Calculate overall health score (0-100)."""
```

## Remediation Engine Module

### MCPRemediationEngine

Automated issue remediation and recovery.

```python
from mcp_client_cli.testing import MCPRemediationEngine

class MCPRemediationEngine:
    """Automated remediation engine for MCP server issues."""
```

#### Constructor

```python
def __init__(self, config: RemediationConfig = None):
    """
    Initialize remediation engine.
    
    Args:
        config: Remediation configuration
    """
```

#### Remediation Methods

```python
async def remediate_issue(self, issue: Issue) -> RemediationResult:
    """
    Attempt to remediate a detected issue.
    
    Args:
        issue: Issue to remediate
        
    Returns:
        RemediationResult with outcome and actions taken
    """

async def remediate_connection_issue(self, issue: Issue) -> RemediationResult:
    """Remediate connection-related issues."""

async def remediate_performance_issue(self, issue: Issue) -> RemediationResult:
    """Remediate performance-related issues."""

async def remediate_configuration_issue(self, issue: Issue) -> RemediationResult:
    """Remediate configuration-related issues."""
```

#### Strategy Management

```python
def add_remediation_strategy(self, issue_type: IssueType,
                           strategy: RemediationStrategy) -> None:
    """Add custom remediation strategy."""

def get_available_strategies(self, issue_type: IssueType) -> List[RemediationStrategy]:
    """Get available strategies for issue type."""

async def validate_remediation(self, issue: Issue,
                              result: RemediationResult) -> bool:
    """Validate that remediation was successful."""
```

#### Retry and Recovery

```python
async def retry_with_backoff(self, operation: Callable,
                           max_attempts: int = 3) -> Any:
    """Retry operation with exponential backoff."""

async def rollback_changes(self, actions: List[RemediationAction]) -> bool:
    """Rollback remediation actions if needed."""
```

## Storage Module

### TestResultManager

Persistent storage for test results and analytics.

```python
from mcp_client_cli.testing import TestResultManager

class TestResultManager:
    """Manage persistent storage of test results."""
```

#### Constructor

```python
def __init__(self, db_path: str = "test_results.db"):
    """
    Initialize test result manager.
    
    Args:
        db_path: Path to SQLite database file
    """
```

#### Storage Methods

```python
async def save_test_result(self, result: TestResult) -> str:
    """
    Save test result to database.
    
    Args:
        result: Test result to save
        
    Returns:
        Unique ID of saved result
    """

async def save_test_suite(self, suite: TestSuite) -> str:
    """Save complete test suite results."""

async def get_test_result(self, result_id: str) -> TestResult:
    """Retrieve test result by ID."""

async def get_test_history(self, server_name: str,
                          limit: int = 100) -> List[TestResult]:
    """Get test history for a server."""
```

#### Analytics Methods

```python
async def get_test_statistics(self, server_name: str = None) -> Dict[str, Any]:
    """Get test statistics and analytics."""

async def get_confidence_trends(self, server_name: str,
                               days: int = 30) -> List[Tuple[datetime, float]]:
    """Get confidence score trends over time."""

async def get_failure_patterns(self, server_name: str = None) -> Dict[str, int]:
    """Get common failure patterns."""
```

#### Data Management

```python
async def cleanup_old_results(self, days: int = 90) -> int:
    """Clean up old test results."""

async def export_results(self, format: str = "json",
                        output_file: str = None) -> str:
    """Export test results to file."""

async def import_results(self, input_file: str) -> int:
    """Import test results from file."""
```

## CLI Integration Module

### MCPTestCLI

Rich command-line interface integration.

```python
from mcp_client_cli.testing import MCPTestCLI

class MCPTestCLI:
    """Rich CLI integration for MCP testing framework."""
```

#### Constructor

```python
def __init__(self, console: Console = None):
    """
    Initialize CLI integration.
    
    Args:
        console: Rich console instance
    """
```

#### Display Methods

```python
def display_test_results(self, results: List[TestResult]) -> None:
    """Display test results with rich formatting."""

def display_test_suite(self, suite: TestSuite) -> None:
    """Display complete test suite results."""

def display_progress(self, current: int, total: int, description: str) -> None:
    """Display progress indicator."""

def display_confidence_chart(self, confidence_data: List[Tuple[str, float]]) -> None:
    """Display confidence scores as chart."""
```

#### Interactive Methods

```python
def prompt_for_configuration(self) -> Dict[str, Any]:
    """Interactive configuration prompts."""

def confirm_action(self, message: str) -> bool:
    """Confirm user action."""

def select_from_options(self, options: List[str], message: str) -> str:
    """Select from multiple options."""
```

## Data Classes

### TestResult

```python
@dataclass
class TestResult:
    """Result of a single test operation."""
    
    test_name: str
    status: TestStatus
    confidence: int
    execution_time: float
    timestamp: datetime
    error_message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    remediation_suggestions: Optional[List[str]] = None
```

### TestSuite

```python
@dataclass
class TestSuite:
    """Collection of test results."""
    
    name: str
    results: List[TestResult]
    overall_confidence: float
    execution_time: float
    timestamp: datetime
    summary: Optional[str] = None
```

### SecurityTestResult

```python
@dataclass
class SecurityTestResult:
    """Result of security testing."""
    
    test_name: str
    status: TestStatus
    confidence: int
    vulnerabilities: List[SecurityVulnerability]
    risk_level: RiskLevel
    recommendations: List[str]
```

### PerformanceMetrics

```python
@dataclass
class PerformanceMetrics:
    """Performance testing metrics."""
    
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    p95_response_time: float
    p99_response_time: float
    throughput: float
    error_rate: float
    concurrent_connections: int
```

### Issue

```python
@dataclass
class Issue:
    """Detected issue information."""
    
    id: str
    type: IssueType
    severity: IssueSeverity
    description: str
    confidence: int
    server: str
    timestamp: datetime
    pattern_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
```

## Enums

### TestStatus

```python
class TestStatus(Enum):
    """Test execution status."""
    
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
```

### IssueType

```python
class IssueType(Enum):
    """Types of issues that can be detected."""
    
    CONNECTION = "connection"
    TIMEOUT = "timeout"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    TOOL_EXECUTION = "tool_execution"
    RESOURCE_ACCESS = "resource_access"
    CONFIGURATION = "configuration"
    PERFORMANCE = "performance"
    SECURITY = "security"
    PROTOCOL = "protocol"
```

### IssueSeverity

```python
class IssueSeverity(Enum):
    """Issue severity levels."""
    
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
```

## Exceptions

### MCPTestingError

```python
class MCPTestingError(Exception):
    """Base exception for MCP testing framework."""
    
    def __init__(self, message: str, confidence: int = 0):
        super().__init__(message)
        self.confidence = confidence
```

### ConnectionError

```python
class ConnectionError(MCPTestingError):
    """Raised when server connection fails."""
    pass
```

### TimeoutError

```python
class TimeoutError(MCPTestingError):
    """Raised when operation times out."""
    pass
```

### ValidationError

```python
class ValidationError(MCPTestingError):
    """Raised when validation fails."""
    pass
```

## Utilities

### Confidence Calculation

```python
def calculate_confidence(success_rate: float,
                        response_time: float,
                        error_patterns: List[str]) -> int:
    """
    Calculate confidence score based on multiple factors.
    
    Args:
        success_rate: Success rate (0.0-1.0)
        response_time: Average response time
        error_patterns: List of error patterns found
        
    Returns:
        Confidence score (0-100)
    """
```

### Pattern Matching

```python
def match_error_pattern(error_message: str,
                       patterns: List[IssuePattern]) -> Optional[IssuePattern]:
    """
    Match error message against known patterns.
    
    Args:
        error_message: Error message to match
        patterns: List of patterns to check
        
    Returns:
        Matching pattern or None
    """
```

### Retry Utilities

```python
async def retry_with_exponential_backoff(operation: Callable,
                                       max_attempts: int = 3,
                                       base_delay: float = 1.0) -> Any:
    """
    Retry operation with exponential backoff.
    
    Args:
        operation: Async operation to retry
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        
    Returns:
        Operation result
    """
```

## Usage Examples

### Basic Testing

```python
import asyncio
from mcp_client_cli.testing import MCPServerTester

async def basic_test():
    tester = MCPServerTester(timeout=30, confidence_threshold=85)
    
    # Test server connection
    result = await tester.test_connection("python examples/generic_mcp_server.py")
    print(f"Connection test: {result.status} (confidence: {result.confidence}%)")
    
    # Test tool execution
    if result.status == TestStatus.PASSED:
        tool_result = await tester.test_tool_execution("echo", {"message": "test"})
        print(f"Tool test: {tool_result.status} (confidence: {tool_result.confidence}%)")

asyncio.run(basic_test())
```

### Security Testing

```python
import asyncio
from mcp_client_cli.testing import MCPSecurityTester

async def security_test():
    tester = MCPSecurityTester()
    
    # Test authentication
    auth_result = await tester.test_authentication_scenario("no_credentials", {})
    print(f"Auth test: {auth_result.status}")
    
    # Test input validation
    validation_result = await tester.test_input_validation("echo", "'; DROP TABLE users; --")
    print(f"Validation test: {validation_result.status}")
    
    # Generate security report
    report = tester.generate_security_report()
    print(f"Security score: {report.overall_score}%")

asyncio.run(security_test())
```

### Performance Testing

```python
import asyncio
from mcp_client_cli.testing import MCPPerformanceTester

async def performance_test():
    tester = MCPPerformanceTester()
    
    # Benchmark tool execution
    metrics = await tester.benchmark_tool_execution("echo", {"message": "benchmark"}, iterations=100)
    print(f"Average response time: {metrics.avg_response_time:.2f}ms")
    
    # Load testing
    load_result = await tester.test_concurrent_connections(10, duration=60)
    print(f"Load test grade: {load_result.grade}")

asyncio.run(performance_test())
```

---

This API reference provides comprehensive documentation for all classes, methods, and interfaces in the MCP Testing Framework. For practical usage examples, see [TESTING_EXAMPLES.md](TESTING_EXAMPLES.md). 