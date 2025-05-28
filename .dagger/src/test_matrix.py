"""
Test Matrix Configuration and Execution for MCP Testing.

This module provides test matrix configuration and execution utilities
for comprehensive MCP testing scenarios across different environments,
Python versions, and server configurations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class TestEnvironment(Enum):
    """Test environment types."""
    PYTHON_ONLY = "python"
    NODEJS_ONLY = "nodejs"
    MULTI_LANGUAGE = "multi"


class TestType(Enum):
    """Test types for matrix execution."""
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"


@dataclass
class TestMatrixConfig:
    """
    Configuration for a single test matrix entry.
    
    This defines a specific test environment and configuration
    that should be tested as part of the comprehensive test suite.
    """
    environment: TestEnvironment
    python_version: Optional[str] = None
    node_version: Optional[str] = None
    test_types: List[TestType] = field(default_factory=lambda: [TestType.FUNCTIONAL])
    server_configs: List[str] = field(default_factory=list)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 300
    retry_count: int = 2
    parallel_execution: bool = True
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.environment == TestEnvironment.PYTHON_ONLY and not self.python_version:
            self.python_version = "3.12"
        elif self.environment == TestEnvironment.NODEJS_ONLY and not self.node_version:
            self.node_version = "20"
        elif self.environment == TestEnvironment.MULTI_LANGUAGE:
            if not self.python_version:
                self.python_version = "3.12"
            if not self.node_version:
                self.node_version = "20"


@dataclass
class TestResult:
    """Result of a single test matrix execution."""
    config: TestMatrixConfig
    success: bool
    execution_time: float
    output: str
    error_message: Optional[str] = None
    confidence_score: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)


class TestMatrixBuilder:
    """
    Builder for creating comprehensive test matrices.
    
    This class provides a fluent interface for building test matrices
    that cover various combinations of environments, versions, and test types.
    """
    
    def __init__(self):
        self.configs: List[TestMatrixConfig] = []
    
    def add_python_environments(
        self, 
        versions: List[str] = None,
        test_types: List[TestType] = None
    ) -> 'TestMatrixBuilder':
        """
        Add Python-only test environments to the matrix.
        
        Args:
            versions: Python versions to test (default: ["3.11", "3.12"])
            test_types: Test types to run (default: [FUNCTIONAL])
            
        Returns:
            TestMatrixBuilder: Self for method chaining
        """
        if versions is None:
            versions = ["3.11", "3.12"]
        if test_types is None:
            test_types = [TestType.FUNCTIONAL]
        
        for version in versions:
            config = TestMatrixConfig(
                environment=TestEnvironment.PYTHON_ONLY,
                python_version=version,
                test_types=test_types.copy()
            )
            self.configs.append(config)
        
        return self
    
    def add_nodejs_environments(
        self,
        versions: List[str] = None,
        test_types: List[TestType] = None
    ) -> 'TestMatrixBuilder':
        """
        Add Node.js-only test environments to the matrix.
        
        Args:
            versions: Node.js versions to test (default: ["18", "20"])
            test_types: Test types to run (default: [FUNCTIONAL])
            
        Returns:
            TestMatrixBuilder: Self for method chaining
        """
        if versions is None:
            versions = ["18", "20"]
        if test_types is None:
            test_types = [TestType.FUNCTIONAL]
        
        for version in versions:
            config = TestMatrixConfig(
                environment=TestEnvironment.NODEJS_ONLY,
                node_version=version,
                test_types=test_types.copy()
            )
            self.configs.append(config)
        
        return self
    
    def add_multi_language_environments(
        self,
        python_versions: List[str] = None,
        node_versions: List[str] = None,
        test_types: List[TestType] = None
    ) -> 'TestMatrixBuilder':
        """
        Add multi-language test environments to the matrix.
        
        Args:
            python_versions: Python versions to test (default: ["3.12"])
            node_versions: Node.js versions to test (default: ["20"])
            test_types: Test types to run (default: [INTEGRATION])
            
        Returns:
            TestMatrixBuilder: Self for method chaining
        """
        if python_versions is None:
            python_versions = ["3.12"]
        if node_versions is None:
            node_versions = ["20"]
        if test_types is None:
            test_types = [TestType.INTEGRATION]
        
        for py_version in python_versions:
            for node_version in node_versions:
                config = TestMatrixConfig(
                    environment=TestEnvironment.MULTI_LANGUAGE,
                    python_version=py_version,
                    node_version=node_version,
                    test_types=test_types.copy()
                )
                self.configs.append(config)
        
        return self
    
    def add_performance_matrix(
        self,
        environments: List[TestEnvironment] = None
    ) -> 'TestMatrixBuilder':
        """
        Add performance testing configurations to the matrix.
        
        Args:
            environments: Environments to test (default: all)
            
        Returns:
            TestMatrixBuilder: Self for method chaining
        """
        if environments is None:
            environments = [TestEnvironment.PYTHON_ONLY, TestEnvironment.MULTI_LANGUAGE]
        
        for env in environments:
            if env == TestEnvironment.PYTHON_ONLY:
                config = TestMatrixConfig(
                    environment=env,
                    python_version="3.12",
                    test_types=[TestType.PERFORMANCE],
                    timeout_seconds=600  # Longer timeout for performance tests
                )
            elif env == TestEnvironment.NODEJS_ONLY:
                config = TestMatrixConfig(
                    environment=env,
                    node_version="20",
                    test_types=[TestType.PERFORMANCE],
                    timeout_seconds=600
                )
            else:  # MULTI_LANGUAGE
                config = TestMatrixConfig(
                    environment=env,
                    python_version="3.12",
                    node_version="20",
                    test_types=[TestType.PERFORMANCE],
                    timeout_seconds=600
                )
            
            self.configs.append(config)
        
        return self
    
    def add_compatibility_matrix(self) -> 'TestMatrixBuilder':
        """
        Add compatibility testing configurations.
        
        Returns:
            TestMatrixBuilder: Self for method chaining
        """
        # Test multiple Python versions for compatibility
        python_versions = ["3.11", "3.12", "3.13"]
        
        for version in python_versions:
            config = TestMatrixConfig(
                environment=TestEnvironment.PYTHON_ONLY,
                python_version=version,
                test_types=[TestType.COMPATIBILITY],
                timeout_seconds=180
            )
            self.configs.append(config)
        
        return self
    
    def with_custom_config(self, config: TestMatrixConfig) -> 'TestMatrixBuilder':
        """
        Add a custom test configuration to the matrix.
        
        Args:
            config: Custom test matrix configuration
            
        Returns:
            TestMatrixBuilder: Self for method chaining
        """
        self.configs.append(config)
        return self
    
    def build(self) -> List[TestMatrixConfig]:
        """
        Build and return the complete test matrix.
        
        Returns:
            List[TestMatrixConfig]: Complete test matrix configurations
        """
        return self.configs.copy()


class DefaultTestMatrices:
    """
    Predefined test matrices for common testing scenarios.
    
    This class provides factory methods for creating standard test matrices
    that cover the most common MCP testing scenarios.
    """
    
    @staticmethod
    def basic_functional() -> List[TestMatrixConfig]:
        """
        Create a basic functional test matrix.
        
        Returns:
            List[TestMatrixConfig]: Basic functional test configurations
        """
        return (
            TestMatrixBuilder()
            .add_python_environments(["3.12"], [TestType.FUNCTIONAL])
            .add_multi_language_environments(["3.12"], ["20"], [TestType.INTEGRATION])
            .build()
        )
    
    @staticmethod
    def comprehensive() -> List[TestMatrixConfig]:
        """
        Create a comprehensive test matrix covering all scenarios.
        
        Returns:
            List[TestMatrixConfig]: Comprehensive test configurations
        """
        return (
            TestMatrixBuilder()
            .add_python_environments(["3.11", "3.12"], [TestType.FUNCTIONAL])
            .add_nodejs_environments(["18", "20"], [TestType.FUNCTIONAL])
            .add_multi_language_environments(["3.12"], ["20"], [TestType.INTEGRATION])
            .add_performance_matrix()
            .add_compatibility_matrix()
            .build()
        )
    
    @staticmethod
    def performance_focused() -> List[TestMatrixConfig]:
        """
        Create a performance-focused test matrix.
        
        Returns:
            List[TestMatrixConfig]: Performance test configurations
        """
        return (
            TestMatrixBuilder()
            .add_python_environments(["3.12"], [TestType.FUNCTIONAL, TestType.PERFORMANCE])
            .add_performance_matrix([TestEnvironment.PYTHON_ONLY, TestEnvironment.MULTI_LANGUAGE])
            .build()
        )
    
    @staticmethod
    def compatibility_focused() -> List[TestMatrixConfig]:
        """
        Create a compatibility-focused test matrix.
        
        Returns:
            List[TestMatrixConfig]: Compatibility test configurations
        """
        return (
            TestMatrixBuilder()
            .add_python_environments(["3.11", "3.12", "3.13"], [TestType.FUNCTIONAL])
            .add_nodejs_environments(["18", "20", "22"], [TestType.FUNCTIONAL])
            .add_compatibility_matrix()
            .build()
        )


def get_test_matrix_for_scenario(scenario: str) -> List[TestMatrixConfig]:
    """
    Get a predefined test matrix for a specific scenario.
    
    Args:
        scenario: Test scenario name ("basic", "comprehensive", "performance", "compatibility")
        
    Returns:
        List[TestMatrixConfig]: Test matrix configurations for the scenario
        
    Raises:
        ValueError: If scenario is not recognized
    """
    scenarios = {
        "basic": DefaultTestMatrices.basic_functional,
        "comprehensive": DefaultTestMatrices.comprehensive,
        "performance": DefaultTestMatrices.performance_focused,
        "compatibility": DefaultTestMatrices.compatibility_focused
    }
    
    if scenario not in scenarios:
        available = ", ".join(scenarios.keys())
        raise ValueError(f"Unknown scenario '{scenario}'. Available: {available}")
    
    return scenarios[scenario]()


def format_test_matrix_summary(configs: List[TestMatrixConfig]) -> str:
    """
    Format a test matrix summary for display.
    
    Args:
        configs: Test matrix configurations
        
    Returns:
        str: Formatted summary of the test matrix
    """
    if not configs:
        return "No test configurations in matrix"
    
    summary = f"Test Matrix Summary ({len(configs)} configurations):\n"
    summary += "=" * 50 + "\n\n"
    
    # Group by environment
    env_groups = {}
    for config in configs:
        env_name = config.environment.value
        if env_name not in env_groups:
            env_groups[env_name] = []
        env_groups[env_name].append(config)
    
    for env_name, env_configs in env_groups.items():
        summary += f"🔧 {env_name.upper()} Environment ({len(env_configs)} configs):\n"
        
        for i, config in enumerate(env_configs, 1):
            summary += f"   {i}. "
            
            if config.python_version:
                summary += f"Python {config.python_version} "
            if config.node_version:
                summary += f"Node.js {config.node_version} "
            
            test_types = [t.value for t in config.test_types]
            summary += f"- Tests: {', '.join(test_types)}"
            
            if config.timeout_seconds != 300:
                summary += f" (timeout: {config.timeout_seconds}s)"
            
            summary += "\n"
        
        summary += "\n"
    
    # Overall statistics
    total_tests = sum(len(config.test_types) for config in configs)
    unique_envs = len(env_groups)
    
    summary += f"📊 Statistics:\n"
    summary += f"   Total Configurations: {len(configs)}\n"
    summary += f"   Total Test Types: {total_tests}\n"
    summary += f"   Unique Environments: {unique_envs}\n"
    
    return summary 