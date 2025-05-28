"""
Pipeline Result Aggregation and Reporting.

This module provides utilities for aggregating, analyzing, and reporting
test results from Dagger pipeline executions, following methodological
pragmatism principles with confidence scoring and systematic verification.
"""

import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

from .test_matrix import TestMatrixConfig, TestResult, TestType, TestEnvironment


class PipelineStatus(Enum):
    """Overall pipeline execution status."""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    ERROR = "error"


@dataclass
class PipelineMetrics:
    """
    Comprehensive metrics for pipeline execution.
    
    This class captures detailed metrics about test execution performance,
    success rates, and confidence levels across the entire pipeline.
    """
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    error_tests: int = 0
    skipped_tests: int = 0
    
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    min_execution_time: float = 0.0
    max_execution_time: float = 0.0
    
    overall_confidence: float = 0.0
    confidence_distribution: Dict[str, int] = field(default_factory=dict)
    
    success_rate: float = 0.0
    error_rate: float = 0.0
    
    environment_breakdown: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    test_type_breakdown: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def calculate_derived_metrics(self, results: List[TestResult]):
        """Calculate derived metrics from test results."""
        if not results:
            return
        
        # Basic counts
        self.total_tests = len(results)
        self.passed_tests = sum(1 for r in results if r.success)
        self.failed_tests = sum(1 for r in results if not r.success and r.error_message is None)
        self.error_tests = sum(1 for r in results if r.error_message is not None)
        
        # Execution time metrics
        execution_times = [r.execution_time for r in results]
        self.total_execution_time = sum(execution_times)
        self.average_execution_time = statistics.mean(execution_times)
        self.min_execution_time = min(execution_times)
        self.max_execution_time = max(execution_times)
        
        # Confidence metrics
        confidence_scores = [r.confidence_score for r in results if r.confidence_score > 0]
        if confidence_scores:
            self.overall_confidence = statistics.mean(confidence_scores)
            
            # Confidence distribution
            self.confidence_distribution = {
                "high (>0.9)": sum(1 for c in confidence_scores if c > 0.9),
                "medium (0.7-0.9)": sum(1 for c in confidence_scores if 0.7 <= c <= 0.9),
                "low (<0.7)": sum(1 for c in confidence_scores if c < 0.7)
            }
        
        # Success and error rates
        self.success_rate = self.passed_tests / self.total_tests if self.total_tests > 0 else 0.0
        self.error_rate = self.error_tests / self.total_tests if self.total_tests > 0 else 0.0
        
        # Environment breakdown
        env_groups = {}
        for result in results:
            env_name = result.config.environment.value
            if env_name not in env_groups:
                env_groups[env_name] = []
            env_groups[env_name].append(result)
        
        for env_name, env_results in env_groups.items():
            env_passed = sum(1 for r in env_results if r.success)
            env_total = len(env_results)
            env_avg_time = statistics.mean([r.execution_time for r in env_results])
            env_confidence = statistics.mean([r.confidence_score for r in env_results if r.confidence_score > 0])
            
            self.environment_breakdown[env_name] = {
                "total": env_total,
                "passed": env_passed,
                "success_rate": env_passed / env_total if env_total > 0 else 0.0,
                "avg_execution_time": env_avg_time,
                "avg_confidence": env_confidence if env_confidence else 0.0
            }
        
        # Test type breakdown
        type_groups = {}
        for result in results:
            for test_type in result.config.test_types:
                type_name = test_type.value
                if type_name not in type_groups:
                    type_groups[type_name] = []
                type_groups[type_name].append(result)
        
        for type_name, type_results in type_groups.items():
            type_passed = sum(1 for r in type_results if r.success)
            type_total = len(type_results)
            type_avg_time = statistics.mean([r.execution_time for r in type_results])
            
            self.test_type_breakdown[type_name] = {
                "total": type_total,
                "passed": type_passed,
                "success_rate": type_passed / type_total if type_total > 0 else 0.0,
                "avg_execution_time": type_avg_time
            }


@dataclass
class PipelineReport:
    """
    Comprehensive pipeline execution report.
    
    This class provides a complete report of pipeline execution including
    metrics, analysis, and recommendations following methodological pragmatism.
    """
    pipeline_id: str
    execution_start: datetime
    execution_end: datetime
    status: PipelineStatus
    metrics: PipelineMetrics
    results: List[TestResult]
    
    # Analysis and recommendations
    confidence_assessment: str = ""
    performance_analysis: str = ""
    failure_analysis: str = ""
    recommendations: List[str] = field(default_factory=list)
    
    # Metadata
    dagger_version: Optional[str] = None
    environment_info: Dict[str, str] = field(default_factory=dict)
    
    @property
    def execution_duration(self) -> timedelta:
        """Get total pipeline execution duration."""
        return self.execution_end - self.execution_start
    
    def generate_analysis(self):
        """Generate comprehensive analysis and recommendations."""
        self._analyze_confidence()
        self._analyze_performance()
        self._analyze_failures()
        self._generate_recommendations()
    
    def _analyze_confidence(self):
        """Analyze confidence scores and provide assessment."""
        if self.metrics.overall_confidence >= 0.9:
            self.confidence_assessment = (
                f"HIGH CONFIDENCE ({self.metrics.overall_confidence:.2%}) - "
                "Results are highly reliable with strong systematic verification."
            )
        elif self.metrics.overall_confidence >= 0.8:
            self.confidence_assessment = (
                f"GOOD CONFIDENCE ({self.metrics.overall_confidence:.2%}) - "
                "Results are generally reliable with adequate verification."
            )
        elif self.metrics.overall_confidence >= 0.7:
            self.confidence_assessment = (
                f"MODERATE CONFIDENCE ({self.metrics.overall_confidence:.2%}) - "
                "Results require additional verification and review."
            )
        else:
            self.confidence_assessment = (
                f"LOW CONFIDENCE ({self.metrics.overall_confidence:.2%}) - "
                "Results require significant review and re-testing."
            )
    
    def _analyze_performance(self):
        """Analyze performance metrics and identify bottlenecks."""
        avg_time = self.metrics.average_execution_time
        max_time = self.metrics.max_execution_time
        
        if avg_time <= 30.0:
            perf_rating = "EXCELLENT"
        elif avg_time <= 60.0:
            perf_rating = "GOOD"
        elif avg_time <= 120.0:
            perf_rating = "ACCEPTABLE"
        else:
            perf_rating = "NEEDS IMPROVEMENT"
        
        self.performance_analysis = (
            f"Performance Rating: {perf_rating} "
            f"(Avg: {avg_time:.1f}s, Max: {max_time:.1f}s, Total: {self.metrics.total_execution_time:.1f}s)"
        )
        
        # Identify slow environments
        slow_envs = []
        for env_name, env_data in self.metrics.environment_breakdown.items():
            if env_data["avg_execution_time"] > avg_time * 1.5:
                slow_envs.append(f"{env_name} ({env_data['avg_execution_time']:.1f}s)")
        
        if slow_envs:
            self.performance_analysis += f" | Slow environments: {', '.join(slow_envs)}"
    
    def _analyze_failures(self):
        """Analyze failure patterns and identify common issues."""
        if self.metrics.failed_tests == 0 and self.metrics.error_tests == 0:
            self.failure_analysis = "No failures detected - all tests passed successfully."
            return
        
        # Categorize failures
        failure_patterns = {}
        error_patterns = {}
        
        for result in self.results:
            if not result.success:
                if result.error_message:
                    # Categorize errors by type
                    error_type = self._categorize_error(result.error_message)
                    if error_type not in error_patterns:
                        error_patterns[error_type] = []
                    error_patterns[error_type].append(result)
                else:
                    # Categorize failures by environment/test type
                    failure_key = f"{result.config.environment.value}_{result.config.test_types[0].value if result.config.test_types else 'unknown'}"
                    if failure_key not in failure_patterns:
                        failure_patterns[failure_key] = []
                    failure_patterns[failure_key].append(result)
        
        analysis_parts = []
        
        if failure_patterns:
            analysis_parts.append(f"Test failures: {len(failure_patterns)} patterns identified")
            for pattern, failures in failure_patterns.items():
                analysis_parts.append(f"  - {pattern}: {len(failures)} failures")
        
        if error_patterns:
            analysis_parts.append(f"Execution errors: {len(error_patterns)} error types")
            for error_type, errors in error_patterns.items():
                analysis_parts.append(f"  - {error_type}: {len(errors)} occurrences")
        
        self.failure_analysis = " | ".join(analysis_parts) if analysis_parts else "No specific failure patterns identified."
    
    def _categorize_error(self, error_message: str) -> str:
        """Categorize error message into common error types."""
        error_lower = error_message.lower()
        
        if "timeout" in error_lower:
            return "timeout"
        elif "connection" in error_lower or "connect" in error_lower:
            return "connection"
        elif "import" in error_lower or "module" in error_lower:
            return "dependency"
        elif "permission" in error_lower or "access" in error_lower:
            return "permission"
        elif "memory" in error_lower or "oom" in error_lower:
            return "memory"
        elif "syntax" in error_lower or "parse" in error_lower:
            return "syntax"
        else:
            return "other"
    
    def _generate_recommendations(self):
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # Confidence-based recommendations
        if self.metrics.overall_confidence < 0.8:
            recommendations.append(
                "Improve test reliability: Review test implementations and add more robust error handling"
            )
        
        # Performance-based recommendations
        if self.metrics.average_execution_time > 60.0:
            recommendations.append(
                "Optimize test performance: Consider parallel execution or test optimization"
            )
        
        # Success rate recommendations
        if self.metrics.success_rate < 0.9:
            recommendations.append(
                "Address test failures: Investigate and fix failing tests to improve reliability"
            )
        
        # Environment-specific recommendations
        for env_name, env_data in self.metrics.environment_breakdown.items():
            if env_data["success_rate"] < 0.8:
                recommendations.append(
                    f"Fix {env_name} environment issues: Success rate is {env_data['success_rate']:.1%}"
                )
        
        # Error-specific recommendations
        if self.metrics.error_rate > 0.1:
            recommendations.append(
                "Reduce execution errors: Review infrastructure and dependency management"
            )
        
        # General recommendations
        if self.metrics.total_tests < 10:
            recommendations.append(
                "Expand test coverage: Add more comprehensive test scenarios"
            )
        
        self.recommendations = recommendations


class PipelineReportGenerator:
    """
    Generator for comprehensive pipeline reports.
    
    This class provides utilities for creating detailed reports from
    pipeline execution results with analysis and recommendations.
    """
    
    @staticmethod
    def create_report(
        pipeline_id: str,
        results: List[TestResult],
        execution_start: datetime,
        execution_end: datetime,
        environment_info: Optional[Dict[str, str]] = None
    ) -> PipelineReport:
        """
        Create a comprehensive pipeline report.
        
        Args:
            pipeline_id: Unique identifier for the pipeline execution
            results: List of test results from pipeline execution
            execution_start: Pipeline start time
            execution_end: Pipeline end time
            environment_info: Optional environment information
            
        Returns:
            PipelineReport: Comprehensive pipeline report
        """
        # Calculate metrics
        metrics = PipelineMetrics()
        metrics.calculate_derived_metrics(results)
        
        # Determine overall status
        if metrics.error_rate > 0.2:
            status = PipelineStatus.ERROR
        elif metrics.success_rate < 0.7:
            status = PipelineStatus.FAILURE
        elif metrics.success_rate < 0.9:
            status = PipelineStatus.PARTIAL_SUCCESS
        else:
            status = PipelineStatus.SUCCESS
        
        # Create report
        report = PipelineReport(
            pipeline_id=pipeline_id,
            execution_start=execution_start,
            execution_end=execution_end,
            status=status,
            metrics=metrics,
            results=results,
            environment_info=environment_info or {}
        )
        
        # Generate analysis
        report.generate_analysis()
        
        return report
    
    @staticmethod
    def format_report(report: PipelineReport, format_type: str = "detailed") -> str:
        """
        Format a pipeline report for display.
        
        Args:
            report: Pipeline report to format
            format_type: Format type ("summary", "detailed", "json")
            
        Returns:
            str: Formatted report
        """
        if format_type == "json":
            return PipelineReportGenerator._format_json(report)
        elif format_type == "summary":
            return PipelineReportGenerator._format_summary(report)
        else:
            return PipelineReportGenerator._format_detailed(report)
    
    @staticmethod
    def _format_detailed(report: PipelineReport) -> str:
        """Format detailed report."""
        duration = report.execution_duration
        
        output = f"""
🚀 MCP TESTING PIPELINE REPORT
{'=' * 70}

📋 EXECUTION SUMMARY
Pipeline ID: {report.pipeline_id}
Status: {report.status.value.upper()}
Duration: {duration.total_seconds():.1f} seconds
Start Time: {report.execution_start.strftime('%Y-%m-%d %H:%M:%S')}
End Time: {report.execution_end.strftime('%Y-%m-%d %H:%M:%S')}

📊 TEST METRICS
{'=' * 30}
Total Tests: {report.metrics.total_tests}
✅ Passed: {report.metrics.passed_tests} ({report.metrics.success_rate:.1%})
❌ Failed: {report.metrics.failed_tests}
💥 Errors: {report.metrics.error_tests}
⏭️  Skipped: {report.metrics.skipped_tests}

⏱️  PERFORMANCE METRICS
{'=' * 30}
Total Execution Time: {report.metrics.total_execution_time:.1f}s
Average Test Time: {report.metrics.average_execution_time:.1f}s
Fastest Test: {report.metrics.min_execution_time:.1f}s
Slowest Test: {report.metrics.max_execution_time:.1f}s

🎯 CONFIDENCE ANALYSIS
{'=' * 30}
Overall Confidence: {report.metrics.overall_confidence:.2%}
{report.confidence_assessment}

Confidence Distribution:
"""
        
        for level, count in report.metrics.confidence_distribution.items():
            output += f"  {level}: {count} tests\n"
        
        output += f"""
🔧 ENVIRONMENT BREAKDOWN
{'=' * 30}
"""
        
        for env_name, env_data in report.metrics.environment_breakdown.items():
            output += f"""
{env_name.upper()}:
  Tests: {env_data['total']} | Passed: {env_data['passed']} ({env_data['success_rate']:.1%})
  Avg Time: {env_data['avg_execution_time']:.1f}s | Confidence: {env_data['avg_confidence']:.2%}
"""
        
        output += f"""
🧪 TEST TYPE BREAKDOWN
{'=' * 30}
"""
        
        for type_name, type_data in report.metrics.test_type_breakdown.items():
            output += f"""
{type_name.upper()}:
  Tests: {type_data['total']} | Passed: {type_data['passed']} ({type_data['success_rate']:.1%})
  Avg Time: {type_data['avg_execution_time']:.1f}s
"""
        
        output += f"""
📈 PERFORMANCE ANALYSIS
{'=' * 30}
{report.performance_analysis}

🔍 FAILURE ANALYSIS
{'=' * 30}
{report.failure_analysis}

💡 RECOMMENDATIONS
{'=' * 30}
"""
        
        if report.recommendations:
            for i, rec in enumerate(report.recommendations, 1):
                output += f"{i}. {rec}\n"
        else:
            output += "No specific recommendations - pipeline executed successfully.\n"
        
        return output
    
    @staticmethod
    def _format_summary(report: PipelineReport) -> str:
        """Format summary report."""
        duration = report.execution_duration
        
        return f"""
🚀 Pipeline {report.pipeline_id} - {report.status.value.upper()}
⏱️  Duration: {duration.total_seconds():.1f}s | Tests: {report.metrics.total_tests}
✅ Success: {report.metrics.success_rate:.1%} | 🎯 Confidence: {report.metrics.overall_confidence:.2%}
📊 Passed: {report.metrics.passed_tests} | Failed: {report.metrics.failed_tests} | Errors: {report.metrics.error_tests}
"""
    
    @staticmethod
    def _format_json(report: PipelineReport) -> str:
        """Format JSON report."""
        data = {
            "pipeline_id": report.pipeline_id,
            "status": report.status.value,
            "execution_start": report.execution_start.isoformat(),
            "execution_end": report.execution_end.isoformat(),
            "duration_seconds": report.execution_duration.total_seconds(),
            "metrics": {
                "total_tests": report.metrics.total_tests,
                "passed_tests": report.metrics.passed_tests,
                "failed_tests": report.metrics.failed_tests,
                "error_tests": report.metrics.error_tests,
                "success_rate": report.metrics.success_rate,
                "overall_confidence": report.metrics.overall_confidence,
                "total_execution_time": report.metrics.total_execution_time,
                "average_execution_time": report.metrics.average_execution_time,
                "environment_breakdown": report.metrics.environment_breakdown,
                "test_type_breakdown": report.metrics.test_type_breakdown
            },
            "analysis": {
                "confidence_assessment": report.confidence_assessment,
                "performance_analysis": report.performance_analysis,
                "failure_analysis": report.failure_analysis
            },
            "recommendations": report.recommendations
        }
        
        return json.dumps(data, indent=2) 