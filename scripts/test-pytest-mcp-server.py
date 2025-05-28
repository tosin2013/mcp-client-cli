#!/usr/bin/env python3
"""
Test script for validating our MCP testing framework against pytest-mcp-server.

This script demonstrates how to use our comprehensive testing infrastructure
to validate a real MCP server implementation.
"""

import asyncio
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, Optional

from src.mcp_client_cli.config import AppConfig, LLMConfig, ServerConfig
from src.mcp_client_cli.testing import (
    MCPServerTester, 
    MCPSecurityTester, 
    MCPPerformanceTester,
    MCPIssueDetector,
    TestResult,
    TestStatus
)


class PytestMCPServerTestRunner:
    """
    Comprehensive test runner for pytest-mcp-server integration.
    
    This class demonstrates the full capabilities of our MCP testing framework
    by testing against a real, production MCP server.
    """
    
    def __init__(self, pytest_server_path: str):
        self.pytest_server_path = Path(pytest_server_path)
        self.test_data_dir = Path("./test-data")
        self.test_data_dir.mkdir(exist_ok=True)
        
        # Load configuration
        config_path = Path("examples/test-pytest-mcp-server.json")
        with open(config_path) as f:
            config_data = json.load(f)
        
        self.config = AppConfig(
            llm=LLMConfig(**config_data["llm"]),
            system_prompt=config_data["systemPrompt"],
            mcp_servers={
                name: ServerConfig(**server_config)
                for name, server_config in config_data["mcpServers"].items()
            },
            tools_requires_confirmation=config_data.get("toolsRequiresConfirmation", [])
        )
        
        self.testing_config = config_data.get("testingConfig", {})
        
    async def setup_pytest_server(self) -> bool:
        """Clone and setup the pytest-mcp-server if not already present."""
        print("🔧 Setting up pytest-mcp-server...")
        
        if not self.pytest_server_path.exists():
            print(f"   Cloning pytest-mcp-server to {self.pytest_server_path}")
            try:
                subprocess.run([
                    "git", "clone", 
                    "https://github.com/tosin2013/pytest-mcp-server.git",
                    str(self.pytest_server_path)
                ], check=True, capture_output=True)
                print("   ✅ Repository cloned successfully")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to clone repository: {e}")
                return False
        
        # Install dependencies
        print("   Installing Node.js dependencies...")
        try:
            subprocess.run([
                "npm", "install"
            ], cwd=self.pytest_server_path, check=True, capture_output=True)
            print("   ✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install dependencies: {e}")
            return False
        
        # Build the project
        print("   Building TypeScript project...")
        try:
            subprocess.run([
                "npm", "run", "build"
            ], cwd=self.pytest_server_path, check=True, capture_output=True)
            print("   ✅ Project built successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Build failed, continuing with source files: {e}")
        
        return True
    
    async def run_functional_tests(self) -> Dict[str, TestResult]:
        """Run comprehensive functional tests against pytest-mcp-server."""
        print("\n🧪 Running Functional Tests")
        print("=" * 50)
        
        tester = MCPServerTester(self.config)
        results = {}
        
        try:
            # Test 1: Configuration Validation
            print("📋 Testing configuration validation...")
            config_result = await tester.validate_configuration(self.config)
            results["config_validation"] = config_result
            print(f"   Status: {config_result.status.value} (confidence: {config_result.confidence_score:.2%})")
            
            # Test 2: Server Connectivity
            print("🔌 Testing server connectivity...")
            server_config = self.config.mcp_servers["pytest-mcp-server"]
            conn_result = await tester.test_server_connectivity(server_config, "pytest-mcp-server")
            results["connectivity"] = conn_result
            print(f"   Status: {conn_result.status.value} (confidence: {conn_result.confidence_score:.2%})")
            
            # Test 3: Tool Discovery
            print("🔍 Testing tool discovery...")
            tools_result = await tester.test_tool_discovery(server_config, "pytest-mcp-server")
            results["tool_discovery"] = tools_result
            print(f"   Status: {tools_result.status.value} (confidence: {tools_result.confidence_score:.2%})")
            
            # Test 4: Specific Tool Tests
            expected_tools = self.testing_config.get("functionalTesting", {}).get("toolTests", [])
            for tool_name in expected_tools:
                print(f"🛠️  Testing tool: {tool_name}")
                tool_result = await tester.test_tool_execution(
                    server_config, "pytest-mcp-server", tool_name, {}
                )
                results[f"tool_{tool_name}"] = tool_result
                print(f"   Status: {tool_result.status.value} (confidence: {tool_result.confidence_score:.2%})")
            
            # Test 5: Resource Discovery (if enabled)
            if self.testing_config.get("functionalTesting", {}).get("resourceTests", False):
                print("📚 Testing resource discovery...")
                resource_result = await tester.test_resource_discovery(server_config, "pytest-mcp-server")
                results["resource_discovery"] = resource_result
                print(f"   Status: {resource_result.status.value} (confidence: {resource_result.confidence_score:.2%})")
            
        except Exception as e:
            print(f"💥 Functional testing error: {e}")
            results["error"] = TestResult(
                test_name="functional_tests",
                status=TestStatus.ERROR,
                message=str(e),
                confidence_score=0.0
            )
        finally:
            await tester.cleanup()
        
        return results
    
    async def run_security_tests(self) -> Dict[str, TestResult]:
        """Run security tests against pytest-mcp-server."""
        print("\n🔒 Running Security Tests")
        print("=" * 50)
        
        security_config = self.testing_config.get("securityTesting", {})
        if not security_config.get("enabled", False):
            print("   Security testing disabled in configuration")
            return {}
        
        tester = MCPSecurityTester(self.config)
        results = {}
        
        try:
            server_config = self.config.mcp_servers["pytest-mcp-server"]
            
            # Authentication Tests
            if security_config.get("authenticationTests", False):
                print("🔐 Testing authentication security...")
                auth_result = await tester.test_authentication_security(server_config, "pytest-mcp-server")
                results["authentication"] = auth_result
                print(f"   Status: {auth_result.status.value} (confidence: {auth_result.confidence_score:.2%})")
            
            # Input Validation Tests
            if security_config.get("inputValidationTests", False):
                print("🛡️  Testing input validation...")
                validation_result = await tester.test_input_validation(server_config, "pytest-mcp-server")
                results["input_validation"] = validation_result
                print(f"   Status: {validation_result.status.value} (confidence: {validation_result.confidence_score:.2%})")
            
            # Data Sanitization Tests
            if security_config.get("dataSanitizationTests", False):
                print("🧹 Testing data sanitization...")
                sanitization_result = await tester.test_data_sanitization(server_config, "pytest-mcp-server")
                results["data_sanitization"] = sanitization_result
                print(f"   Status: {sanitization_result.status.value} (confidence: {sanitization_result.confidence_score:.2%})")
            
        except Exception as e:
            print(f"💥 Security testing error: {e}")
            results["error"] = TestResult(
                test_name="security_tests",
                status=TestStatus.ERROR,
                message=str(e),
                confidence_score=0.0
            )
        finally:
            await tester.cleanup()
        
        return results
    
    async def run_performance_tests(self) -> Dict[str, TestResult]:
        """Run performance tests against pytest-mcp-server."""
        print("\n⚡ Running Performance Tests")
        print("=" * 50)
        
        perf_config = self.testing_config.get("performanceTesting", {})
        if not perf_config.get("enabled", False):
            print("   Performance testing disabled in configuration")
            return {}
        
        tester = MCPPerformanceTester(self.config)
        results = {}
        
        try:
            server_config = self.config.mcp_servers["pytest-mcp-server"]
            
            # Response Time Tests
            print("⏱️  Testing response times...")
            response_result = await tester.test_response_times(server_config, "pytest-mcp-server")
            results["response_times"] = response_result
            print(f"   Status: {response_result.status.value} (confidence: {response_result.confidence_score:.2%})")
            
            # Concurrent Connection Tests
            concurrent_connections = perf_config.get("concurrentConnections", 5)
            print(f"🔄 Testing concurrent connections ({concurrent_connections})...")
            concurrent_result = await tester.test_concurrent_connections(
                server_config, "pytest-mcp-server", concurrent_connections
            )
            results["concurrent_connections"] = concurrent_result
            print(f"   Status: {concurrent_result.status.value} (confidence: {concurrent_result.confidence_score:.2%})")
            
            # Memory Leak Detection
            if perf_config.get("memoryLeakDetection", False):
                print("🧠 Testing for memory leaks...")
                memory_result = await tester.test_memory_usage(server_config, "pytest-mcp-server")
                results["memory_usage"] = memory_result
                print(f"   Status: {memory_result.status.value} (confidence: {memory_result.confidence_score:.2%})")
            
        except Exception as e:
            print(f"💥 Performance testing error: {e}")
            results["error"] = TestResult(
                test_name="performance_tests",
                status=TestStatus.ERROR,
                message=str(e),
                confidence_score=0.0
            )
        finally:
            await tester.cleanup()
        
        return results
    
    async def run_issue_detection_tests(self) -> Dict[str, Any]:
        """Run issue detection and analysis tests."""
        print("\n🔍 Running Issue Detection Tests")
        print("=" * 50)
        
        detector = MCPIssueDetector()
        results = {}
        
        try:
            # Simulate some test failures for analysis
            test_failures = [
                {
                    "server": "pytest-mcp-server",
                    "error": "Connection timeout after 30 seconds",
                    "timestamp": time.time() - 3600,
                    "context": {"tool": "register_pytest_failure"}
                },
                {
                    "server": "pytest-mcp-server", 
                    "error": "Tool execution failed: Invalid parameter type",
                    "timestamp": time.time() - 1800,
                    "context": {"tool": "debug_with_principle"}
                }
            ]
            
            # Detect issues
            print("🔎 Analyzing test failures...")
            issues = await detector.detect_issues(test_failures)
            results["detected_issues"] = len(issues)
            
            for issue in issues:
                print(f"   Issue: {issue.issue_type.value} - {issue.description}")
                print(f"   Confidence: {issue.confidence:.2%}")
            
            # Health monitoring
            print("📊 Monitoring server health...")
            health_metrics = await detector.monitor_health("pytest-mcp-server", test_failures)
            results["health_metrics"] = {
                "success_rate": health_metrics.success_rate,
                "avg_response_time": health_metrics.avg_response_time,
                "error_rate": health_metrics.error_rate
            }
            print(f"   Success Rate: {health_metrics.success_rate:.2%}")
            print(f"   Error Rate: {health_metrics.error_rate:.2%}")
            
        except Exception as e:
            print(f"💥 Issue detection error: {e}")
            results["error"] = str(e)
        
        return results
    
    def generate_test_report(self, all_results: Dict[str, Dict[str, Any]]) -> str:
        """Generate a comprehensive test report."""
        report = []
        report.append("# pytest-mcp-server Integration Test Report")
        report.append("=" * 60)
        report.append("")
        
        # Summary
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        for test_type, results in all_results.items():
            if isinstance(results, dict):
                for test_name, result in results.items():
                    if isinstance(result, TestResult):
                        total_tests += 1
                        if result.status == TestStatus.PASSED:
                            passed_tests += 1
                        elif result.status == TestStatus.FAILED:
                            failed_tests += 1
                        elif result.status == TestStatus.ERROR:
                            error_tests += 1
        
        report.append(f"## Summary")
        report.append(f"- Total Tests: {total_tests}")
        report.append(f"- Passed: {passed_tests}")
        report.append(f"- Failed: {failed_tests}")
        report.append(f"- Errors: {error_tests}")
        report.append(f"- Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "- Success Rate: N/A")
        report.append("")
        
        # Detailed Results
        for test_type, results in all_results.items():
            report.append(f"## {test_type.replace('_', ' ').title()}")
            report.append("")
            
            if isinstance(results, dict):
                for test_name, result in results.items():
                    if isinstance(result, TestResult):
                        status_emoji = {
                            TestStatus.PASSED: "✅",
                            TestStatus.FAILED: "❌", 
                            TestStatus.ERROR: "💥"
                        }.get(result.status, "❓")
                        
                        report.append(f"### {status_emoji} {test_name}")
                        report.append(f"- Status: {result.status.value}")
                        report.append(f"- Confidence: {result.confidence_score:.2%}")
                        if result.message:
                            report.append(f"- Message: {result.message}")
                        if result.details:
                            report.append(f"- Details: {result.details}")
                        report.append("")
            else:
                report.append(f"Results: {results}")
                report.append("")
        
        return "\n".join(report)
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites against pytest-mcp-server."""
        print("🚀 Starting Comprehensive pytest-mcp-server Integration Tests")
        print("=" * 70)
        
        # Setup
        setup_success = await self.setup_pytest_server()
        if not setup_success:
            print("❌ Setup failed, aborting tests")
            return {"error": "Setup failed"}
        
        all_results = {}
        
        # Run test suites
        all_results["functional"] = await self.run_functional_tests()
        all_results["security"] = await self.run_security_tests()
        all_results["performance"] = await self.run_performance_tests()
        all_results["issue_detection"] = await self.run_issue_detection_tests()
        
        # Generate report
        report = self.generate_test_report(all_results)
        
        # Save report
        report_path = Path("test-results/pytest-mcp-server-report.md")
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, "w") as f:
            f.write(report)
        
        print(f"\n📄 Test report saved to: {report_path}")
        print("\n" + "=" * 70)
        print("🎉 Integration testing completed!")
        
        return all_results


async def main():
    """Main entry point for the test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MCP framework against pytest-mcp-server")
    parser.add_argument(
        "--server-path", 
        default="../pytest-mcp-server",
        help="Path to pytest-mcp-server repository"
    )
    parser.add_argument(
        "--test-type",
        choices=["all", "functional", "security", "performance", "issue-detection"],
        default="all",
        help="Type of tests to run"
    )
    
    args = parser.parse_args()
    
    runner = PytestMCPServerTestRunner(args.server_path)
    
    if args.test_type == "all":
        results = await runner.run_all_tests()
    elif args.test_type == "functional":
        results = await runner.run_functional_tests()
    elif args.test_type == "security":
        results = await runner.run_security_tests()
    elif args.test_type == "performance":
        results = await runner.run_performance_tests()
    elif args.test_type == "issue-detection":
        results = await runner.run_issue_detection_tests()
    
    print(f"\nTest Results: {json.dumps(results, indent=2, default=str)}")


if __name__ == "__main__":
    asyncio.run(main()) 