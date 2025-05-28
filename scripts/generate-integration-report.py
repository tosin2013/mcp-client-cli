#!/usr/bin/env python3
"""
Generate Integration Report for pytest-mcp-server Testing

This script generates comprehensive integration reports for pytest-mcp-server
testing using the mcp-client-cli testing framework.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3


class IntegrationReportGenerator:
    """Generate comprehensive integration reports for MCP testing."""
    
    def __init__(self, target: str, results_dir: str, output_path: str):
        self.target = target
        self.results_dir = Path(results_dir)
        self.output_path = Path(output_path)
        self.timestamp = datetime.now().isoformat()
        
    def generate_report(self) -> None:
        """Generate the complete integration report."""
        print(f"🔍 Generating integration report for {self.target}")
        
        # Collect test results
        results = self._collect_test_results()
        
        # Generate report sections
        report_sections = {
            "header": self._generate_header(),
            "executive_summary": self._generate_executive_summary(results),
            "functional_tests": self._generate_functional_section(results),
            "security_tests": self._generate_security_section(results),
            "performance_tests": self._generate_performance_section(results),
            "issue_detection": self._generate_issue_detection_section(results),
            "recommendations": self._generate_recommendations(results),
            "confidence_analysis": self._generate_confidence_analysis(results),
            "next_steps": self._generate_next_steps(results),
            "appendix": self._generate_appendix(results)
        }
        
        # Write report
        self._write_report(report_sections)
        print(f"✅ Integration report generated: {self.output_path}")
    
    def _collect_test_results(self) -> Dict[str, Any]:
        """Collect all test results from the results directory."""
        results = {
            "functional": [],
            "security": [],
            "performance": [],
            "issue_detection": [],
            "metadata": {}
        }
        
        # Collect JSON results
        for json_file in self.results_dir.glob("*.json"):
            try:
                with open(json_file) as f:
                    data = json.load(f)
                    
                if "functional" in json_file.name:
                    results["functional"].extend(data.get("tests", []))
                elif "security" in json_file.name:
                    results["security"].extend(data.get("tests", []))
                elif "performance" in json_file.name:
                    results["performance"].extend(data.get("tests", []))
                elif "issue" in json_file.name:
                    results["issue_detection"].extend(data.get("issues", []))
                    
            except Exception as e:
                print(f"⚠️  Warning: Could not parse {json_file}: {e}")
        
        # Collect SQLite results if available
        db_path = self.results_dir / "test_results.db"
        if db_path.exists():
            results.update(self._collect_sqlite_results(db_path))
        
        return results
    
    def _collect_sqlite_results(self, db_path: Path) -> Dict[str, Any]:
        """Collect results from SQLite database."""
        results = {}
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            
            # Get test results
            cursor = conn.execute("""
                SELECT test_name, test_type, status, confidence, 
                       execution_time, error_message, created_at
                FROM test_results 
                ORDER BY created_at DESC
            """)
            
            test_results = []
            for row in cursor.fetchall():
                test_results.append({
                    "name": row["test_name"],
                    "type": row["test_type"],
                    "status": row["status"],
                    "confidence": row["confidence"],
                    "execution_time": row["execution_time"],
                    "error_message": row["error_message"],
                    "timestamp": row["created_at"]
                })
            
            results["all_tests"] = test_results
            
            # Get summary statistics
            cursor = conn.execute("""
                SELECT test_type, 
                       COUNT(*) as total,
                       SUM(CASE WHEN status = 'PASSED' THEN 1 ELSE 0 END) as passed,
                       AVG(confidence) as avg_confidence,
                       AVG(execution_time) as avg_time
                FROM test_results 
                GROUP BY test_type
            """)
            
            summary_stats = {}
            for row in cursor.fetchall():
                summary_stats[row["test_type"]] = {
                    "total": row["total"],
                    "passed": row["passed"],
                    "failed": row["total"] - row["passed"],
                    "pass_rate": row["passed"] / row["total"] if row["total"] > 0 else 0,
                    "avg_confidence": row["avg_confidence"] or 0,
                    "avg_time": row["avg_time"] or 0
                }
            
            results["summary_stats"] = summary_stats
            conn.close()
            
        except Exception as e:
            print(f"⚠️  Warning: Could not read SQLite results: {e}")
        
        return results
    
    def _generate_header(self) -> str:
        """Generate report header."""
        return f"""# MCP Testing Integration Report: {self.target}

**Generated**: {self.timestamp}  
**Target**: {self.target}  
**Testing Framework**: mcp-client-cli comprehensive testing suite  
**Methodology**: Methodological Pragmatism with Confidence Scoring  

---
"""
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> str:
        """Generate executive summary section."""
        summary_stats = results.get("summary_stats", {})
        all_tests = results.get("all_tests", [])
        
        total_tests = len(all_tests)
        passed_tests = len([t for t in all_tests if t["status"] == "PASSED"])
        avg_confidence = sum(t["confidence"] for t in all_tests) / total_tests if total_tests > 0 else 0
        
        # Determine overall status
        pass_rate = passed_tests / total_tests if total_tests > 0 else 0
        if pass_rate >= 0.95 and avg_confidence >= 0.9:
            overall_status = "🟢 EXCELLENT"
        elif pass_rate >= 0.85 and avg_confidence >= 0.8:
            overall_status = "🟡 GOOD"
        elif pass_rate >= 0.7 and avg_confidence >= 0.7:
            overall_status = "🟠 MODERATE"
        else:
            overall_status = "🔴 NEEDS ATTENTION"
        
        return f"""## 📊 Executive Summary

**Overall Status**: {overall_status}

### Key Metrics
- **Total Tests**: {total_tests}
- **Passed**: {passed_tests} ({pass_rate:.1%})
- **Failed**: {total_tests - passed_tests}
- **Average Confidence**: {avg_confidence:.2f}

### Test Coverage
{self._format_test_coverage(summary_stats)}

### Critical Findings
{self._generate_critical_findings(results)}

### Confidence Assessment
- **Methodology**: Systematic verification with explicit fallibilism
- **Reliability**: {self._assess_reliability(avg_confidence)}
- **Limitations**: {self._identify_limitations(results)}

"""
    
    def _format_test_coverage(self, summary_stats: Dict[str, Any]) -> str:
        """Format test coverage information."""
        if not summary_stats:
            return "- No detailed coverage data available"
        
        coverage = []
        for test_type, stats in summary_stats.items():
            coverage.append(
                f"- **{test_type.title()}**: {stats['passed']}/{stats['total']} "
                f"({stats['pass_rate']:.1%}) - Confidence: {stats['avg_confidence']:.2f}"
            )
        
        return "\n".join(coverage)
    
    def _generate_critical_findings(self, results: Dict[str, Any]) -> str:
        """Generate critical findings summary."""
        all_tests = results.get("all_tests", [])
        failed_tests = [t for t in all_tests if t["status"] == "FAILED"]
        
        if not failed_tests:
            return "- ✅ No critical issues identified"
        
        findings = ["**Critical Issues Identified:**"]
        for test in failed_tests[:5]:  # Top 5 failures
            findings.append(f"- ❌ {test['name']}: {test.get('error_message', 'Unknown error')}")
        
        if len(failed_tests) > 5:
            findings.append(f"- ... and {len(failed_tests) - 5} more failures")
        
        return "\n".join(findings)
    
    def _assess_reliability(self, avg_confidence: float) -> str:
        """Assess reliability based on confidence score."""
        if avg_confidence >= 0.9:
            return "High - Comprehensive verification with strong methodological foundation"
        elif avg_confidence >= 0.8:
            return "Good - Solid verification with minor gaps"
        elif avg_confidence >= 0.7:
            return "Moderate - Basic verification with some assumptions"
        else:
            return "Low - Limited verification, significant assumptions"
    
    def _identify_limitations(self, results: Dict[str, Any]) -> str:
        """Identify testing limitations."""
        limitations = []
        
        if not results.get("security"):
            limitations.append("Security testing data incomplete")
        
        if not results.get("performance"):
            limitations.append("Performance testing data incomplete")
        
        all_tests = results.get("all_tests", [])
        if len(all_tests) < 10:
            limitations.append("Limited test coverage")
        
        if not limitations:
            return "Comprehensive testing with minimal limitations"
        
        return "; ".join(limitations)
    
    def _generate_functional_section(self, results: Dict[str, Any]) -> str:
        """Generate functional testing section."""
        functional_tests = [t for t in results.get("all_tests", []) if t["type"] == "functional"]
        
        if not functional_tests:
            return """## 🔧 Functional Testing

**Status**: No functional test data available

"""
        
        passed = len([t for t in functional_tests if t["status"] == "PASSED"])
        total = len(functional_tests)
        avg_confidence = sum(t["confidence"] for t in functional_tests) / total
        
        return f"""## 🔧 Functional Testing

**Status**: {passed}/{total} tests passed ({passed/total:.1%})  
**Confidence**: {avg_confidence:.2f}

### Protocol Compliance
{self._analyze_protocol_compliance(functional_tests)}

### Tool Execution
{self._analyze_tool_execution(functional_tests)}

### Resource Access
{self._analyze_resource_access(functional_tests)}

### Detailed Results
{self._format_test_details(functional_tests)}

"""
    
    def _generate_security_section(self, results: Dict[str, Any]) -> str:
        """Generate security testing section."""
        security_tests = [t for t in results.get("all_tests", []) if t["type"] == "security"]
        
        if not security_tests:
            return """## 🔒 Security Testing

**Status**: No security test data available

"""
        
        passed = len([t for t in security_tests if t["status"] == "PASSED"])
        total = len(security_tests)
        avg_confidence = sum(t["confidence"] for t in security_tests) / total
        
        # Calculate security score
        security_score = (passed / total) * avg_confidence if total > 0 else 0
        
        return f"""## 🔒 Security Testing

**Status**: {passed}/{total} tests passed ({passed/total:.1%})  
**Security Score**: {security_score:.2f}  
**Confidence**: {avg_confidence:.2f}

### OWASP Top 10 Assessment
{self._analyze_owasp_compliance(security_tests)}

### Authentication & Authorization
{self._analyze_auth_security(security_tests)}

### Input Validation
{self._analyze_input_validation(security_tests)}

### Detailed Results
{self._format_test_details(security_tests)}

"""
    
    def _generate_performance_section(self, results: Dict[str, Any]) -> str:
        """Generate performance testing section."""
        performance_tests = [t for t in results.get("all_tests", []) if t["type"] == "performance"]
        
        if not performance_tests:
            return """## ⚡ Performance Testing

**Status**: No performance test data available

"""
        
        passed = len([t for t in performance_tests if t["status"] == "PASSED"])
        total = len(performance_tests)
        avg_time = sum(t["execution_time"] for t in performance_tests) / total if total > 0 else 0
        
        return f"""## ⚡ Performance Testing

**Status**: {passed}/{total} tests passed ({passed/total:.1%})  
**Average Response Time**: {avg_time:.2f}ms

### Load Testing
{self._analyze_load_performance(performance_tests)}

### Memory Usage
{self._analyze_memory_performance(performance_tests)}

### Scalability
{self._analyze_scalability(performance_tests)}

### Detailed Results
{self._format_test_details(performance_tests)}

"""
    
    def _generate_issue_detection_section(self, results: Dict[str, Any]) -> str:
        """Generate issue detection section."""
        issues = results.get("issue_detection", [])
        
        if not issues:
            return """## 🔍 Issue Detection

**Status**: No issues detected or no issue detection data available

"""
        
        critical_issues = [i for i in issues if i.get("severity") == "critical"]
        high_issues = [i for i in issues if i.get("severity") == "high"]
        
        return f"""## 🔍 Issue Detection

**Total Issues**: {len(issues)}  
**Critical**: {len(critical_issues)}  
**High**: {len(high_issues)}

### Critical Issues
{self._format_issues(critical_issues)}

### High Priority Issues
{self._format_issues(high_issues)}

### Automated Remediation
{self._analyze_remediation(issues)}

"""
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> str:
        """Generate recommendations section."""
        all_tests = results.get("all_tests", [])
        failed_tests = [t for t in all_tests if t["status"] == "FAILED"]
        
        recommendations = []
        
        # Security recommendations
        security_tests = [t for t in all_tests if t["type"] == "security"]
        security_failures = [t for t in security_tests if t["status"] == "FAILED"]
        if security_failures:
            recommendations.append("🔒 **Security**: Address failed security tests, particularly authentication and input validation")
        
        # Performance recommendations
        performance_tests = [t for t in all_tests if t["type"] == "performance"]
        slow_tests = [t for t in performance_tests if t["execution_time"] > 1000]  # > 1 second
        if slow_tests:
            recommendations.append("⚡ **Performance**: Optimize response times for slow operations")
        
        # General recommendations
        if len(failed_tests) > len(all_tests) * 0.1:  # > 10% failure rate
            recommendations.append("🔧 **Quality**: High failure rate indicates need for code review and testing improvements")
        
        if not recommendations:
            recommendations.append("✅ **Excellent**: No major issues identified, continue current practices")
        
        return f"""## 💡 Recommendations

### Immediate Actions
{chr(10).join(f"- {rec}" for rec in recommendations)}

### Long-term Improvements
- 📊 **Monitoring**: Implement continuous testing and monitoring
- 📚 **Documentation**: Update documentation based on test findings
- 🔄 **CI/CD**: Integrate testing framework into development workflow
- 🎯 **Coverage**: Expand test coverage for edge cases and error conditions

### Methodological Pragmatism Application
- **Systematic Verification**: Implement structured validation processes
- **Confidence Tracking**: Monitor confidence scores over time
- **Fallibilism**: Acknowledge and document testing limitations
- **Pragmatic Focus**: Prioritize tests based on real-world impact

"""
    
    def _generate_confidence_analysis(self, results: Dict[str, Any]) -> str:
        """Generate confidence analysis section."""
        all_tests = results.get("all_tests", [])
        
        if not all_tests:
            return """## 📈 Confidence Analysis

**Status**: No confidence data available

"""
        
        confidence_scores = [t["confidence"] for t in all_tests]
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        high_confidence = len([c for c in confidence_scores if c >= 0.9])
        good_confidence = len([c for c in confidence_scores if 0.8 <= c < 0.9])
        moderate_confidence = len([c for c in confidence_scores if 0.7 <= c < 0.8])
        low_confidence = len([c for c in confidence_scores if c < 0.7])
        
        return f"""## 📈 Confidence Analysis

**Average Confidence**: {avg_confidence:.2f}

### Confidence Distribution
- **High (0.9-1.0)**: {high_confidence} tests ({high_confidence/len(all_tests):.1%})
- **Good (0.8-0.9)**: {good_confidence} tests ({good_confidence/len(all_tests):.1%})
- **Moderate (0.7-0.8)**: {moderate_confidence} tests ({moderate_confidence/len(all_tests):.1%})
- **Low (<0.7)**: {low_confidence} tests ({low_confidence/len(all_tests):.1%})

### Methodological Foundation
- **Explicit Fallibilism**: Testing limitations acknowledged and documented
- **Systematic Verification**: Structured validation processes applied
- **Pragmatic Success**: Focus on practical, real-world outcomes
- **Cognitive Systematization**: Organized approach to knowledge validation

### Confidence Factors
- **Test Coverage**: {self._assess_coverage(results)}
- **Verification Depth**: {self._assess_verification_depth(results)}
- **Methodology Rigor**: {self._assess_methodology_rigor(avg_confidence)}

"""
    
    def _generate_next_steps(self, results: Dict[str, Any]) -> str:
        """Generate next steps section."""
        all_tests = results.get("all_tests", [])
        failed_tests = [t for t in all_tests if t["status"] == "FAILED"]
        
        next_steps = []
        
        if failed_tests:
            next_steps.append("1. **Address Failed Tests**: Review and fix failing test cases")
            next_steps.append("2. **Root Cause Analysis**: Investigate underlying causes of failures")
        
        next_steps.extend([
            "3. **Continuous Integration**: Set up automated testing in CI/CD pipeline",
            "4. **Monitoring**: Implement ongoing test result monitoring",
            "5. **Documentation**: Update project documentation with test findings",
            "6. **Team Training**: Share testing methodology with development team"
        ])
        
        return f"""## 🚀 Next Steps

### Immediate (1-2 days)
{chr(10).join(next_steps[:2]) if failed_tests else "1. **Maintain Quality**: Continue current testing practices"}

### Short-term (1-2 weeks)
{chr(10).join(next_steps[2:4])}

### Long-term (1-2 months)
{chr(10).join(next_steps[4:])}

### Integration with pytest-mcp-server
- **Self-Testing**: Implement regular self-testing using this framework
- **Cross-Testing**: Test against other MCP servers for compatibility
- **Community**: Share testing results and methodologies with MCP community

"""
    
    def _generate_appendix(self, results: Dict[str, Any]) -> str:
        """Generate appendix section."""
        return f"""## 📎 Appendix

### Testing Framework Details
- **Framework**: mcp-client-cli comprehensive testing suite
- **Version**: Latest
- **Methodology**: Methodological Pragmatism
- **Confidence Scoring**: 0.0-1.0 scale with explicit limitations

### Test Environment
- **Target**: {self.target}
- **Timestamp**: {self.timestamp}
- **Results Directory**: {self.results_dir}

### Raw Data
- **Test Results Database**: Available in SQLite format
- **JSON Reports**: Individual test type reports available
- **Logs**: Detailed execution logs available

### Contact and Support
- **Framework Repository**: https://github.com/your-org/mcp-client-cli
- **Documentation**: Comprehensive guides and examples available
- **Community**: GitHub issues and discussions for support

---

*This report was generated using methodological pragmatism principles with explicit acknowledgment of limitations and systematic verification processes.*
"""
    
    def _analyze_protocol_compliance(self, tests: List[Dict]) -> str:
        """Analyze protocol compliance from functional tests."""
        protocol_tests = [t for t in tests if "protocol" in t["name"].lower()]
        if not protocol_tests:
            return "- No specific protocol compliance tests found"
        
        passed = len([t for t in protocol_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(protocol_tests)} protocol tests passed"
    
    def _analyze_tool_execution(self, tests: List[Dict]) -> str:
        """Analyze tool execution from functional tests."""
        tool_tests = [t for t in tests if "tool" in t["name"].lower()]
        if not tool_tests:
            return "- No specific tool execution tests found"
        
        passed = len([t for t in tool_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(tool_tests)} tool execution tests passed"
    
    def _analyze_resource_access(self, tests: List[Dict]) -> str:
        """Analyze resource access from functional tests."""
        resource_tests = [t for t in tests if "resource" in t["name"].lower()]
        if not resource_tests:
            return "- No specific resource access tests found"
        
        passed = len([t for t in resource_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(resource_tests)} resource access tests passed"
    
    def _analyze_owasp_compliance(self, tests: List[Dict]) -> str:
        """Analyze OWASP compliance from security tests."""
        owasp_tests = [t for t in tests if "owasp" in t["name"].lower()]
        if not owasp_tests:
            return "- No specific OWASP tests found"
        
        passed = len([t for t in owasp_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(owasp_tests)} OWASP tests passed"
    
    def _analyze_auth_security(self, tests: List[Dict]) -> str:
        """Analyze authentication security from security tests."""
        auth_tests = [t for t in tests if any(keyword in t["name"].lower() 
                                            for keyword in ["auth", "login", "token"])]
        if not auth_tests:
            return "- No specific authentication tests found"
        
        passed = len([t for t in auth_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(auth_tests)} authentication tests passed"
    
    def _analyze_input_validation(self, tests: List[Dict]) -> str:
        """Analyze input validation from security tests."""
        validation_tests = [t for t in tests if any(keyword in t["name"].lower() 
                                                  for keyword in ["input", "validation", "sanitiz"])]
        if not validation_tests:
            return "- No specific input validation tests found"
        
        passed = len([t for t in validation_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(validation_tests)} input validation tests passed"
    
    def _analyze_load_performance(self, tests: List[Dict]) -> str:
        """Analyze load performance from performance tests."""
        load_tests = [t for t in tests if "load" in t["name"].lower()]
        if not load_tests:
            return "- No specific load tests found"
        
        passed = len([t for t in load_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(load_tests)} load tests passed"
    
    def _analyze_memory_performance(self, tests: List[Dict]) -> str:
        """Analyze memory performance from performance tests."""
        memory_tests = [t for t in tests if "memory" in t["name"].lower()]
        if not memory_tests:
            return "- No specific memory tests found"
        
        passed = len([t for t in memory_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(memory_tests)} memory tests passed"
    
    def _analyze_scalability(self, tests: List[Dict]) -> str:
        """Analyze scalability from performance tests."""
        scalability_tests = [t for t in tests if any(keyword in t["name"].lower() 
                                                   for keyword in ["scalab", "concurrent", "throughput"])]
        if not scalability_tests:
            return "- No specific scalability tests found"
        
        passed = len([t for t in scalability_tests if t["status"] == "PASSED"])
        return f"- {passed}/{len(scalability_tests)} scalability tests passed"
    
    def _format_test_details(self, tests: List[Dict]) -> str:
        """Format detailed test results."""
        if not tests:
            return "- No test details available"
        
        details = []
        for test in tests[:10]:  # Limit to first 10 tests
            status_icon = "✅" if test["status"] == "PASSED" else "❌"
            details.append(
                f"- {status_icon} **{test['name']}** "
                f"(Confidence: {test['confidence']:.2f}, "
                f"Time: {test['execution_time']:.1f}ms)"
            )
        
        if len(tests) > 10:
            details.append(f"- ... and {len(tests) - 10} more tests")
        
        return "\n".join(details)
    
    def _format_issues(self, issues: List[Dict]) -> str:
        """Format issue list."""
        if not issues:
            return "- No issues in this category"
        
        formatted = []
        for issue in issues[:5]:  # Limit to first 5 issues
            formatted.append(f"- **{issue.get('title', 'Unknown Issue')}**: {issue.get('description', 'No description')}")
        
        if len(issues) > 5:
            formatted.append(f"- ... and {len(issues) - 5} more issues")
        
        return "\n".join(formatted)
    
    def _analyze_remediation(self, issues: List[Dict]) -> str:
        """Analyze automated remediation capabilities."""
        if not issues:
            return "- No remediation data available"
        
        remediated = len([i for i in issues if i.get("remediated", False)])
        return f"- {remediated}/{len(issues)} issues automatically remediated"
    
    def _assess_coverage(self, results: Dict[str, Any]) -> str:
        """Assess test coverage."""
        all_tests = results.get("all_tests", [])
        test_types = set(t["type"] for t in all_tests)
        
        if len(test_types) >= 4:
            return "Comprehensive coverage across multiple test types"
        elif len(test_types) >= 2:
            return "Good coverage with some gaps"
        else:
            return "Limited coverage, expansion recommended"
    
    def _assess_verification_depth(self, results: Dict[str, Any]) -> str:
        """Assess verification depth."""
        all_tests = results.get("all_tests", [])
        
        if len(all_tests) >= 50:
            return "Deep verification with extensive test suite"
        elif len(all_tests) >= 20:
            return "Good verification depth"
        else:
            return "Basic verification, deeper testing recommended"
    
    def _assess_methodology_rigor(self, avg_confidence: float) -> str:
        """Assess methodology rigor."""
        if avg_confidence >= 0.9:
            return "High rigor with systematic verification"
        elif avg_confidence >= 0.8:
            return "Good rigor with structured approach"
        else:
            return "Moderate rigor, methodology improvements recommended"
    
    def _write_report(self, sections: Dict[str, str]) -> None:
        """Write the complete report to file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_path, 'w') as f:
            for section in sections.values():
                f.write(section)
                f.write("\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate integration report for pytest-mcp-server testing"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target server name (e.g., pytest-mcp-server)"
    )
    parser.add_argument(
        "--results",
        required=True,
        help="Path to test results directory"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the integration report"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    results_dir = Path(args.results)
    if not results_dir.exists():
        print(f"❌ Error: Results directory does not exist: {results_dir}")
        sys.exit(1)
    
    # Generate report
    generator = IntegrationReportGenerator(args.target, args.results, args.output)
    generator.generate_report()


if __name__ == "__main__":
    main() 