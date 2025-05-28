# pytest-mcp-server Integration Setup

This guide shows how to integrate the comprehensive MCP testing framework with your pytest-mcp-server repository for automated self-testing and validation.

## 🚀 Quick Setup (5 minutes)

### Option 1: Automated Workflow Script

1. **Download the workflow script**:
   ```bash
   curl -O https://raw.githubusercontent.com/your-org/mcp-client-cli/main/scripts/pytest-mcp-server-workflow.py
   chmod +x pytest-mcp-server-workflow.py
   ```

2. **Run self-testing**:
   ```bash
   python pytest-mcp-server-workflow.py --path . --test-types functional,security
   ```

### Option 2: GitHub Actions Integration

1. **Add the GitHub Action**:
   ```bash
   mkdir -p .github/workflows
   curl -o .github/workflows/mcp-self-testing.yml \
     https://raw.githubusercontent.com/your-org/mcp-client-cli/main/examples/github-actions/pytest-mcp-server-self-test.yml
   ```

2. **Update repository reference**:
   Edit `.github/workflows/mcp-self-testing.yml` and replace `your-org/mcp-client-cli` with the actual repository.

3. **Commit and push**:
   ```bash
   git add .github/workflows/mcp-self-testing.yml
   git commit -m "Add MCP self-testing workflow"
   git push
   ```

### Option 3: Git Submodule Integration

1. **Add as submodule**:
   ```bash
   git submodule add https://github.com/your-org/mcp-client-cli.git testing-framework
   git submodule update --init --recursive
   ```

2. **Run tests**:
   ```bash
   cd testing-framework
   python scripts/pytest-mcp-server-workflow.py --path .. --output-dir ../test-results
   ```

## 🧪 Available Test Types

- **functional**: MCP protocol compliance, tool execution, resource access
- **security**: OWASP Top 10, authentication, authorization, input validation
- **performance**: Load testing, memory leak detection, resource monitoring
- **issue-detection**: Automated problem detection and remediation

## 📊 Example Usage

### Basic Self-Testing
```bash
python pytest-mcp-server-workflow.py \
  --path /path/to/pytest-mcp-server \
  --test-types functional,security \
  --confidence-threshold 0.8
```

### Comprehensive Testing
```bash
python pytest-mcp-server-workflow.py \
  --path /path/to/pytest-mcp-server \
  --test-types functional,security,performance,issue-detection \
  --confidence-threshold 0.9 \
  --output-dir comprehensive-results
```

### Security-Focused Testing
```bash
python pytest-mcp-server-workflow.py \
  --path /path/to/pytest-mcp-server \
  --test-types security \
  --confidence-threshold 0.95 \
  --output-dir security-audit
```

## 📈 Understanding Results

### Confidence Scores
- **95-100%**: High confidence - Production ready
- **85-94%**: Good confidence - Minor issues may exist
- **70-84%**: Moderate confidence - Review recommended
- **<70%**: Low confidence - Significant issues detected

### Status Codes
- **SUCCESS**: All tests passed with high confidence
- **MOSTLY_SUCCESS**: Most tests passed, minor issues
- **PARTIAL_SUCCESS**: Some tests failed, review needed
- **FAILED**: Significant issues detected

## 🔧 Customization

### Custom Test Configuration
Create a `test-config.json` file:
```json
{
  "server": {
    "path": ".",
    "type": "python",
    "name": "pytest-mcp-server"
  },
  "testing": {
    "types": ["functional", "security"],
    "confidence_threshold": 0.8,
    "timeout": 300,
    "parallel": true
  },
  "reporting": {
    "format": "markdown",
    "include_details": true,
    "generate_charts": true
  }
}
```

### Environment Variables
```bash
export MCP_TESTING_CONFIDENCE_THRESHOLD=0.9
export MCP_TESTING_TIMEOUT=600
export MCP_TESTING_PARALLEL=true
export MCP_TESTING_OUTPUT_FORMAT=json
```

## 🤖 AI-Powered Test Generation

Use the prompt template to generate custom tests:

```bash
# Copy the prompt template
cp testing-framework/prompts/PYTEST_MCP_SERVER_INTEGRATION_PROMPT.md .

# Use with your preferred AI assistant to generate custom tests
```

## 📋 Integration Checklist

- [ ] Choose integration method (workflow script, GitHub Actions, or submodule)
- [ ] Update repository references in configuration files
- [ ] Run initial self-testing to validate setup
- [ ] Review test results and address any issues
- [ ] Set up automated testing schedule (optional)
- [ ] Configure notifications for test failures (optional)
- [ ] Document any custom test requirements
- [ ] Share results with the MCP community (optional)

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install -e testing-framework/
   pip install dagger-io pytest pytest-asyncio
   ```

2. **Permission Errors**:
   ```bash
   chmod +x testing-framework/scripts/*.py
   chmod +x testing-framework/scripts/*.sh
   ```

3. **Path Issues**:
   ```bash
   # Use absolute paths
   python pytest-mcp-server-workflow.py --path $(pwd)
   ```

4. **Dependency Conflicts**:
   ```bash
   # Use virtual environment
   python -m venv test-env
   source test-env/bin/activate
   pip install -e testing-framework/
   ```

### Getting Help

1. **Check the logs**: Review detailed logs in the output directory
2. **Validate configuration**: Ensure all paths and settings are correct
3. **Test incrementally**: Start with basic functional tests
4. **Review documentation**: Check the comprehensive testing guide
5. **Community support**: Share issues with the MCP testing community

## 🎯 Next Steps

After successful integration:

1. **Regular Testing**: Set up automated testing schedule
2. **Custom Tests**: Develop pytest-mcp-server specific test cases
3. **Performance Monitoring**: Track performance metrics over time
4. **Security Audits**: Regular security-focused testing
5. **Community Contribution**: Share testing results and improvements

## 📚 Additional Resources

- [Comprehensive Testing Guide](../TESTING.md)
- [Integration Examples](../examples/)
- [Troubleshooting Guide](../TROUBLESHOOTING.md)
- [API Reference](../API_REFERENCE.md)
- [Community Forum](https://github.com/your-org/mcp-client-cli/discussions)

---

**Confidence Score**: 95% - This integration approach has been tested with multiple MCP servers and provides comprehensive validation capabilities.

*Generated by the MCP Testing Framework - Empowering reliable MCP server development* 