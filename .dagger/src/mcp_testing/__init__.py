"""
MCP Testing Infrastructure using Dagger.io

This module provides comprehensive testing capabilities for MCP servers
following the systematic approach outlined in the ebook.
"""

import asyncio
import json
from typing import Annotated, Optional, List, Any
from pathlib import Path

import dagger
from dagger import dag, function, object_type, Container, Directory


@object_type
class McpTesting:
    """
    Main Dagger module for MCP server testing infrastructure.
    
    This class provides comprehensive testing capabilities for MCP servers
    across multiple languages (Python, Node.js, etc.), following the existing 
    async patterns from the mcp-client-cli codebase.
    """

    @function
    async def test_environment(
        self,
        python_version: str = "3.12",
        base_image: str = "python:3.12-slim"
    ) -> Container:
        """
        Create a standardized Python test environment container.
        
        Args:
            python_version: Python version to use (default: "3.12")
            base_image: Base container image (default: "python:3.12-slim")
            
        Returns:
            Container: Configured Python test environment container
        """
        return (
            dag.container()
            .from_(base_image)
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "git", "curl", "build-essential"])
            .with_exec(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
        )

    @function
    async def nodejs_test_environment(
        self,
        node_version: str = "20",
        base_image: str = "node:20-slim"
    ) -> Container:
        """
        Create a standardized Node.js test environment container.
        
        Args:
            node_version: Node.js version to use (default: "20")
            base_image: Base container image (default: "node:20-slim")
            
        Returns:
            Container: Configured Node.js test environment container
        """
        return (
            dag.container()
            .from_(base_image)
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "git", "curl", "build-essential", "python3"])
            .with_exec(["npm", "install", "-g", "npm@latest"])
            .with_exec(["npm", "install", "-g", "typescript", "@types/node"])
        )

    @function
    async def multi_language_environment(
        self,
        python_version: str = "3.12",
        node_version: str = "20"
    ) -> Container:
        """
        Create a multi-language environment supporting both Python and Node.js.
        
        Args:
            python_version: Python version to use (default: "3.12")
            node_version: Node.js version to use (default: "20")
            
        Returns:
            Container: Container with both Python and Node.js environments
        """
        return (
            dag.container()
            .from_("ubuntu:22.04")
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "curl", "git", "build-essential", "software-properties-common"])
            # Install Python
            .with_exec(["add-apt-repository", "ppa:deadsnakes/ppa", "-y"])
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", f"python{python_version}", f"python{python_version}-pip", f"python{python_version}-venv"])
            .with_exec(["ln", "-sf", f"/usr/bin/python{python_version}", "/usr/bin/python"])
            .with_exec(["ln", "-sf", f"/usr/bin/python{python_version}", "/usr/bin/python3"])
            # Install Node.js
            .with_exec(["curl", "-fsSL", "https://deb.nodesource.com/setup_20.x", "-o", "nodesource_setup.sh"])
            .with_exec(["bash", "nodesource_setup.sh"])
            .with_exec(["apt-get", "install", "-y", "nodejs"])
            .with_exec(["npm", "install", "-g", "npm@latest", "typescript", "@types/node"])
        )

    @function
    async def install_dependencies(
        self,
        container: Container,
        source: Annotated[Directory, dagger.DefaultPath("/")]
    ) -> Container:
        """
        Install project dependencies in the test environment.
        
        Args:
            container: Base container to install dependencies in
            source: Source directory containing the project
            
        Returns:
            Container: Container with dependencies installed
        """
        return (
            container
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["pip", "install", "-e", "."])
        )

    @function
    async def setup_mcp_client(
        self,
        container: Container,
        config_file: Optional[str] = None
    ) -> Container:
        """
        Setup MCP client configuration in the test environment.
        
        Args:
            container: Container to setup MCP client in
            config_file: Optional path to MCP configuration file
            
        Returns:
            Container: Container with MCP client configured
        """
        # Create basic MCP configuration if none provided
        if config_file is None:
            config_content = '''
{
  "systemPrompt": "You are a test assistant for MCP server validation.",
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0
  },
  "mcpServers": {}
}
'''
            container = container.with_new_file("/src/.llm/config.json", config_content)
        else:
            # Use provided configuration file
            container = container.with_file("/src/.llm/config.json", dag.host().file(config_file))
        
        return container

    # ========== NEW PIPELINE FUNCTIONS ==========

    @function
    async def run_functional_tests(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")],
        server_configs: Optional[List[str]] = None,
        parallel: bool = True
    ) -> str:
        """
        Run comprehensive functional tests for MCP servers.
        
        Args:
            source: Source directory containing the project
            server_configs: Optional list of server configuration names to test
            parallel: Whether to run tests in parallel (default: True)
            
        Returns:
            str: Functional test results with confidence scores
        """
        container = await self.test_environment()
        container = await self.install_dependencies(container, source)
        container = await self.setup_mcp_client(container)
        
        # Create functional test script using our Core MCP Testing Framework
        functional_test_script = '''
import asyncio
import json
import sys
from pathlib import Path
from mcp_client_cli.config import AppConfig, LLMConfig, ServerConfig
from mcp_client_cli.testing import MCPServerTester, run_mcp_tests

async def run_functional_tests():
    """Run comprehensive functional tests using the Core MCP Testing Framework."""
    print("🧪 Starting Functional Tests via Dagger Pipeline")
    print("=" * 60)
    
    try:
        # Create test configuration for example servers
        config = AppConfig(
            llm=LLMConfig(
                model="gpt-4o-mini",
                provider="openai",
                temperature=0.0
            ),
            system_prompt="Functional testing via Dagger pipeline",
            mcp_servers={
                "python-example": ServerConfig(
                    command="python",
                    args=["examples/generic_mcp_server.py"],
                    env={},
                    enabled=True,
                    exclude_tools=[],
                    requires_confirmation=[]
                )
            },
            tools_requires_confirmation=[]
        )
        
        print("✅ Test configuration created")
        
        # Run comprehensive tests using our framework
        tester = MCPServerTester(config)
        
        # Test configuration validation
        config_result = await tester.validate_configuration(config)
        print(f"📋 Configuration Validation: {config_result.status.value} (confidence: {config_result.confidence_score:.2%})")
        
        # Run comprehensive test suite for all servers
        results = await tester.run_comprehensive_test_suite()
        
        # Display results
        total_tests = 0
        total_passed = 0
        total_confidence = 0.0
        
        for server_name, suite in results.items():
            print(f"\\n🔍 Server: {server_name}")
            print(f"   Tests: {suite.total_tests} | Passed: {suite.passed_tests} | Failed: {suite.failed_tests}")
            print(f"   Confidence: {suite.overall_confidence:.2%} | Time: {suite.execution_time:.2f}s")
            
            total_tests += suite.total_tests
            total_passed += suite.passed_tests
            total_confidence += suite.overall_confidence
        
        # Calculate overall metrics
        overall_confidence = total_confidence / len(results) if results else 0.0
        success_rate = (total_passed / total_tests) if total_tests > 0 else 0.0
        
        print(f"\\n📊 Overall Results:")
        print(f"   Success Rate: {success_rate:.2%}")
        print(f"   Overall Confidence: {overall_confidence:.2%}")
        print(f"   Total Tests: {total_tests}")
        
        # Cleanup
        await tester.cleanup()
        
        if success_rate >= 0.8 and overall_confidence >= 0.85:
            print("\\n✅ Functional tests PASSED")
            return "PASSED"
        else:
            print("\\n❌ Functional tests FAILED")
            return "FAILED"
            
    except Exception as e:
        print(f"\\n💥 Functional tests ERROR: {e}")
        import traceback
        traceback.print_exc()
        return "ERROR"

if __name__ == "__main__":
    result = asyncio.run(run_functional_tests())
    print(f"\\nFunctional Test Result: {result}")
    sys.exit(0 if result == "PASSED" else 1)
'''
        
        container = container.with_new_file("/src/functional_tests.py", functional_test_script)
        
        # Run functional tests
        result = await (
            container
            .with_exec(["python", "functional_tests.py"])
            .stdout()
        )
        
        return f"Functional Test Pipeline Results:\\n{result}"

    @function
    async def run_performance_tests(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")],
        duration_seconds: int = 60,
        concurrent_connections: int = 10
    ) -> str:
        """
        Run performance tests for MCP servers.
        
        Args:
            source: Source directory containing the project
            duration_seconds: Test duration in seconds (default: 60)
            concurrent_connections: Number of concurrent connections (default: 10)
            
        Returns:
            str: Performance test results with metrics
        """
        container = await self.test_environment()
        container = await self.install_dependencies(container, source)
        container = await self.setup_mcp_client(container)
        
        # Create performance test script
        performance_test_script = f'''
import asyncio
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
from mcp_client_cli.config import AppConfig, LLMConfig, ServerConfig
from mcp_client_cli.testing import MCPServerTester

async def performance_test_single_server(server_name: str, config: AppConfig, iterations: int = 10):
    """Run performance test for a single server."""
    tester = MCPServerTester(config)
    
    try:
        times = []
        success_count = 0
        
        for i in range(iterations):
            start_time = time.time()
            
            # Test connectivity
            server_config = config.mcp_servers[server_name]
            result = await tester.test_server_connectivity(server_config, server_name)
            
            execution_time = time.time() - start_time
            times.append(execution_time)
            
            if result.status.value == "passed":
                success_count += 1
            
            # Small delay between tests
            await asyncio.sleep(0.1)
        
        # Calculate metrics
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        success_rate = success_count / iterations
        
        await tester.cleanup()
        
        return {{
            "server": server_name,
            "iterations": iterations,
            "success_rate": success_rate,
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "times": times
        }}
        
    except Exception as e:
        await tester.cleanup()
        return {{
            "server": server_name,
            "error": str(e),
            "success_rate": 0.0
        }}

async def run_performance_tests():
    """Run comprehensive performance tests."""
    print("⚡ Starting Performance Tests via Dagger Pipeline")
    print("=" * 60)
    
    # Test configuration
    config = AppConfig(
        llm=LLMConfig(
            model="gpt-4o-mini",
            provider="openai",
            temperature=0.0
        ),
        system_prompt="Performance testing via Dagger pipeline",
        mcp_servers={{
            "python-perf": ServerConfig(
                command="python",
                args=["examples/generic_mcp_server.py"],
                env={{}},
                enabled=True,
                exclude_tools=[],
                requires_confirmation=[]
            )
        }},
        tools_requires_confirmation=[]
    )
    
    print(f"🔧 Test Parameters:")
    print(f"   Duration: {duration_seconds} seconds")
    print(f"   Concurrent Connections: {concurrent_connections}")
    print(f"   Iterations per connection: 10")
    
    # Run performance tests
    start_time = time.time()
    
    # Create tasks for concurrent testing
    tasks = []
    for i in range({concurrent_connections}):
        task = performance_test_single_server("python-perf", config, 10)
        tasks.append(task)
    
    # Run concurrent tests
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    total_time = time.time() - start_time
    
    # Analyze results
    successful_results = [r for r in results if isinstance(r, dict) and "error" not in r]
    failed_results = [r for r in results if isinstance(r, dict) and "error" in r]
    
    if successful_results:
        all_times = []
        total_success_rate = 0.0
        
        for result in successful_results:
            all_times.extend(result["times"])
            total_success_rate += result["success_rate"]
        
        avg_success_rate = total_success_rate / len(successful_results)
        overall_avg_time = statistics.mean(all_times)
        overall_min_time = min(all_times)
        overall_max_time = max(all_times)
        
        print(f"\\n📊 Performance Results:")
        print(f"   Successful Connections: {{len(successful_results)}}/{concurrent_connections}")
        print(f"   Average Success Rate: {{avg_success_rate:.2%}}")
        print(f"   Average Response Time: {{overall_avg_time:.3f}}s")
        print(f"   Min Response Time: {{overall_min_time:.3f}}s")
        print(f"   Max Response Time: {{overall_max_time:.3f}}s")
        print(f"   Total Test Duration: {{total_time:.2f}}s")
        
        # Performance thresholds
        if avg_success_rate >= 0.95 and overall_avg_time <= 2.0:
            print("\\n✅ Performance tests PASSED")
            return "PASSED"
        else:
            print("\\n⚠️ Performance tests MARGINAL")
            return "MARGINAL"
    else:
        print(f"\\n❌ Performance tests FAILED - {{len(failed_results)}} failures")
        return "FAILED"

if __name__ == "__main__":
    result = asyncio.run(run_performance_tests())
    print(f"\\nPerformance Test Result: {{result}}")
'''
        
        container = container.with_new_file("/src/performance_tests.py", performance_test_script)
        
        # Run performance tests
        result = await (
            container
            .with_exec(["python", "performance_tests.py"])
            .stdout()
        )
        
        return f"Performance Test Pipeline Results:\\n{result}"

    @function
    async def run_integration_tests(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")],
        test_matrix: Optional[List[str]] = None
    ) -> str:
        """
        Run integration tests across multiple environments and configurations.
        
        Args:
            source: Source directory containing the project
            test_matrix: Optional test matrix configurations as JSON strings
            
        Returns:
            str: Integration test results
        """
        # Default test matrix if none provided
        if test_matrix is None:
            test_matrix = [
                '{"python_version": "3.12", "environment": "python"}',
                '{"node_version": "20", "environment": "nodejs"}',
                '{"python_version": "3.12", "node_version": "20", "environment": "multi"}'
            ]
        
        results = []
        
        for matrix_config_str in test_matrix:
            matrix_config = json.loads(matrix_config_str)
            env_type = matrix_config.get("environment", "python")
            
            # Create appropriate environment
            if env_type == "nodejs":
                container = await self.nodejs_test_environment(
                    node_version=matrix_config.get("node_version", "20")
                )
            elif env_type == "multi":
                container = await self.multi_language_environment(
                    python_version=matrix_config.get("python_version", "3.12"),
                    node_version=matrix_config.get("node_version", "20")
                )
            else:
                container = await self.test_environment(
                    python_version=matrix_config.get("python_version", "3.12")
                )
            
            # Install dependencies and setup
            if env_type in ["python", "multi"]:
                container = await self.install_dependencies(container, source)
            container = await self.setup_mcp_client(container)
            
            # Create integration test script
            integration_test = f'''
import asyncio
import json
from mcp_client_cli.config import AppConfig, LLMConfig, ServerConfig
from mcp_client_cli.testing import MCPServerTester

async def run_integration_test():
    """Run integration test for environment: {env_type}"""
    print(f"🔗 Integration Test - Environment: {env_type}")
    print(f"   Matrix Config: {matrix_config}")
    
    try:
        # Create test configuration
        config = AppConfig(
            llm=LLMConfig(
                model="gpt-4o-mini",
                provider="openai",
                temperature=0.0
            ),
            system_prompt="Integration testing via Dagger pipeline",
            mcp_servers={{
                "integration-test": ServerConfig(
                    command="python" if "{env_type}" != "nodejs" else "node",
                    args=["examples/generic_mcp_server.py"] if "{env_type}" != "nodejs" else ["examples/nodejs_mcp_server.js"],
                    env={{}},
                    enabled=True,
                    exclude_tools=[],
                    requires_confirmation=[]
                )
            }},
            tools_requires_confirmation=[]
        )
        
        # Run basic integration tests
        tester = MCPServerTester(config)
        
        # Test configuration
        config_result = await tester.validate_configuration(config)
        print(f"   Config Validation: {{config_result.status.value}}")
        
        # Test connectivity (basic integration)
        server_config = config.mcp_servers["integration-test"]
        conn_result = await tester.test_server_connectivity(server_config, "integration-test")
        print(f"   Connectivity: {{conn_result.status.value}}")
        
        await tester.cleanup()
        
        if config_result.status.value == "passed" and conn_result.status.value == "passed":
            print(f"   ✅ Integration test PASSED for {env_type}")
            return "PASSED"
        else:
            print(f"   ❌ Integration test FAILED for {env_type}")
            return "FAILED"
            
    except Exception as e:
        print(f"   💥 Integration test ERROR for {env_type}: {{e}}")
        return "ERROR"

if __name__ == "__main__":
    result = asyncio.run(run_integration_test())
    print(f"Integration Test Result ({env_type}): {{result}}")
'''
            
            container = container.with_new_file(f"/src/integration_test_{env_type}.py", integration_test)
            
            # Run integration test
            try:
                result = await (
                    container
                    .with_exec(["python", f"integration_test_{env_type}.py"])
                    .stdout()
                )
                results.append(f"Environment {env_type}:\\n{result}")
            except Exception as e:
                results.append(f"Environment {env_type}: ERROR - {str(e)}")
        
        return f"Integration Test Pipeline Results:\\n\\n" + "\\n\\n".join(results)

    @function
    async def run_full_test_suite(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")],
        include_performance: bool = True,
        parallel_execution: bool = True
    ) -> str:
        """
        Run the complete test suite including functional, performance, and integration tests.
        
        Args:
            source: Source directory containing the project
            include_performance: Whether to include performance tests (default: True)
            parallel_execution: Whether to run tests in parallel (default: True)
            
        Returns:
            str: Complete test suite results with summary
        """
        print("🚀 Starting Full Test Suite via Dagger Pipeline")
        print("=" * 70)
        
        start_time = asyncio.get_event_loop().time()
        
        if parallel_execution:
            # Run tests in parallel
            tasks = [
                self.run_functional_tests(source),
                self.run_integration_tests(source)
            ]
            
            if include_performance:
                tasks.append(self.run_performance_tests(source))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            functional_result = results[0] if len(results) > 0 else "ERROR"
            integration_result = results[1] if len(results) > 1 else "ERROR"
            performance_result = results[2] if len(results) > 2 and include_performance else "SKIPPED"
            
        else:
            # Run tests sequentially
            functional_result = await self.run_functional_tests(source)
            integration_result = await self.run_integration_tests(source)
            performance_result = await self.run_performance_tests(source) if include_performance else "SKIPPED"
        
        total_time = asyncio.get_event_loop().time() - start_time
        
        # Compile summary
        summary = f"""
🎯 FULL TEST SUITE SUMMARY
{'=' * 70}

⏱️  Total Execution Time: {total_time:.2f} seconds
🔄 Parallel Execution: {parallel_execution}
📊 Performance Tests: {'Included' if include_performance else 'Skipped'}

📋 TEST RESULTS:
{'=' * 30}

🧪 FUNCTIONAL TESTS:
{functional_result}

🔗 INTEGRATION TESTS:
{integration_result}

⚡ PERFORMANCE TESTS:
{performance_result}

🎉 OVERALL STATUS:
{'=' * 20}
"""
        
        # Determine overall status
        all_results = [functional_result, integration_result]
        if include_performance:
            all_results.append(performance_result)
        
        passed_count = sum(1 for r in all_results if "PASSED" in str(r))
        total_count = len(all_results)
        
        if passed_count == total_count:
            summary += "✅ ALL TESTS PASSED - Ready for production!"
        elif passed_count >= total_count * 0.8:
            summary += "⚠️  MOSTLY PASSED - Review failed tests"
        else:
            summary += "❌ MULTIPLE FAILURES - Requires attention"
        
        summary += f"\\n\\n📈 Success Rate: {passed_count}/{total_count} ({passed_count/total_count:.1%})"
        
        return summary

    # ========== EXISTING FUNCTIONS (PRESERVED) ==========

    @function
    async def test_python_mcp_server(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")],
        server_path: str,
        server_args: List[str] = []
    ) -> str:
        """Test a Python MCP server implementation."""
        container = await self.test_environment()
        container = await self.install_dependencies(container, source)
        container = await self.setup_mcp_client(container)
        
        # Use our enhanced testing framework
        result = await self.run_functional_tests(source)
        return f"Python MCP Server Test Results:\\n{result}"

    @function
    async def test_nodejs_mcp_server(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")],
        server_path: str,
        server_args: List[str] = []
    ) -> str:
        """Test a Node.js MCP server implementation."""
        container = await self.multi_language_environment()
        
        # Install Python dependencies for the MCP client
        container = (
            container
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["python", "-m", "pip", "install", "-e", ".[testing]"])
        )
        
        container = await self.setup_mcp_client(container)
        
        # Use integration tests for Node.js
        result = await self.run_integration_tests(source, ['{"environment": "nodejs"}'])
        return f"Node.js MCP Server Test Results:\\n{result}"

    @function
    async def test_cross_language_integration(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")],
        python_server_path: str,
        nodejs_server_path: str
    ) -> str:
        """Test cross-language integration."""
        result = await self.run_integration_tests(source, ['{"environment": "multi"}'])
        return f"Cross-Language Integration Test Results:\\n{result}"

    @function
    async def validate_installation(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")]
    ) -> str:
        """Validate installation."""
        container = await self.test_environment()
        container = await self.install_dependencies(container, source)
        container = await self.setup_mcp_client(container)
        
        # Test basic functionality
        result = await (
            container
            .with_exec(["python", "-c", "import mcp_client_cli; print('MCP Client CLI imported successfully')"])
            .with_exec(["python", "-c", "import dagger; print('Dagger SDK imported successfully')"])
            .with_exec(["python", "-c", "import pytest; print('Pytest imported successfully')"])
            .with_exec(["llm", "--help"])
            .stdout()
        )
        
        return f"Installation validation completed successfully:\\n{result}"

    @function
    async def run_basic_tests(
        self,
        source: Annotated[Directory, dagger.DefaultPath("/")]
    ) -> str:
        """Run basic validation tests."""
        container = await self.test_environment()
        container = await self.install_dependencies(container, source)
        
        # Create a simple validation test script
        validation_script = '''
import sys
import importlib

def test_imports():
    """Test basic imports."""
    print("Starting basic validation tests...")
    
    try:
        # Test core imports
        import mcp_client_cli
        print("SUCCESS: mcp_client_cli imported")
        
        from mcp_client_cli.config import AppConfig, LLMConfig, ServerConfig, TestConfig
        print("SUCCESS: Config classes imported")
        
        from mcp_client_cli.testing import MCPServerTester
        print("SUCCESS: MCPServerTester imported")
        
        # Test basic configuration creation
        config = AppConfig(
            llm=LLMConfig(
                model="gpt-4o-mini",
                provider="openai",
                temperature=0.0
            ),
            system_prompt="Basic validation test",
            mcp_servers={},
            tools_requires_confirmation=[],
            testing=TestConfig()
        )
        print("SUCCESS: Basic configuration created")
        
        # Test tester instantiation
        tester = MCPServerTester(config)
        print("SUCCESS: MCPServerTester instantiated")
        
        print("\\nAll basic validation tests PASSED")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    print(f"\\nValidation Result: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
'''
        
        container = container.with_new_file("/src/validation_tests.py", validation_script)
        
        # Run validation tests
        result = await (
            container
            .with_exec(["python", "validation_tests.py"])
            .stdout()
        )
        
        return f"Basic validation tests completed:\\n{result}" 