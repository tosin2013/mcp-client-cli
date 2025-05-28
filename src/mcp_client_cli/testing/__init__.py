"""
MCP Server Testing Framework.

This package provides comprehensive testing capabilities for MCP servers,
including core testing, security validation, performance benchmarking,
issue detection, and automated remediation.
"""

from .mcp_tester import MCPServerTester, TestResult, TestStatus, TestSuite
from .test_storage import TestResultManager
from .cli_integration import MCPTestCLI
from .security_tester import MCPSecurityTester, SecurityTestConfig, SecurityVulnerability
from .performance_tester import MCPPerformanceTester, PerformanceTestConfig, PerformanceMetrics, LoadTestResult, ResourceMonitor
from .issue_detector import MCPIssueDetector, Issue, IssueType, IssueSeverity, HealthMetrics, IssuePattern
from .remediation import MCPRemediationEngine, RemediationResult, RemediationStatus, RemediationStrategy, RemediationAction, RetryConfig
from .issue_storage import IssueTrackingManager

__all__ = [
    # Core Testing
    "MCPServerTester",
    "TestResult", 
    "TestStatus",
    "TestSuite",
    "TestResultManager",
    "MCPTestCLI",
    
    # Security Testing
    "MCPSecurityTester",
    "SecurityTestConfig",
    "SecurityVulnerability",
    
    # Performance Testing
    "MCPPerformanceTester",
    "PerformanceTestConfig", 
    "PerformanceMetrics",
    "LoadTestResult",
    "ResourceMonitor",
    
    # Issue Detection
    "MCPIssueDetector",
    "Issue",
    "IssueType",
    "IssueSeverity", 
    "HealthMetrics",
    "IssuePattern",
    
    # Automated Remediation
    "MCPRemediationEngine",
    "RemediationResult",
    "RemediationStatus",
    "RemediationStrategy",
    "RemediationAction",
    "RetryConfig",
    
    # Issue Storage
    "IssueTrackingManager"
] 