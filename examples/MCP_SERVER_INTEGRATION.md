# MCP Server Integration Testing Guide

This guide shows how to integrate the MCP testing framework with any MCP server repository for comprehensive testing.

## Quick Start

### 1. Basic Integration

For any MCP server repository, create a test configuration file:

```json
{
  "test_server": {
    "command": "python",
    "args": ["your_server.py"],
    "env": {
      "TEST_MODE": "true"
    },
    "enabled": true
  }
}
```

### 2. One-Command Testing

```bash
# Clone and test any MCP server
git clone <your-mcp-server-repo>
cd <your-mcp-server-repo>

# Run comprehensive testing
curl -sSL https://raw.githubusercontent.com/tosin2013/mcp-client-cli/master/scripts/quick-test-local.sh | bash
```

## Integration Approaches

### Approach 1: Local Testing Script

Create a simple test script in your MCP server repository:

```python
#!/usr/bin/env python3
"""
Test script for MCP server using mcp-client-cli testing framework.
"""

import asyncio
import json
from pathlib import Path

async def test_mcp_server():
    """Test the MCP server with comprehensive testing."""
    
    # Auto-detect server configuration
    config = {
        "test_server": {
            "command": "python",
            "args": ["server.py"],  # Adjust to your server file
            "env": {"TEST_MODE": "true"},
            "enabled": True
        }
    }
    
    # Save configuration
    config_path = Path("test-config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print("🧪 Running comprehensive MCP server tests...")
    
    # Import and run tests
    from mcp_client_cli.testing.mcp_tester import MCPServerTester
    from mcp_client_cli.testing.security_tester import MCPSecurityTester
    from mcp_client_cli.testing.performance_tester import MCPPerformanceTester
    
    # Run all test suites
    tester = MCPServerTester()
    security_tester = MCPSecurityTester()
    performance_tester = MCPPerformanceTester()
    
    # Test results will be displayed with confidence scores
    print("✅ Testing complete! Check results above.")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
```

### Approach 2: GitHub Actions Integration

Add to `.github/workflows/mcp-testing.yml`:

```yaml
name: MCP Server Testing

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test-mcp-server:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install MCP Testing Framework
      run: |
        pip install git+https://github.com/tosin2013/mcp-client-cli.git
    
    - name: Run MCP Server Tests
      run: |
        # Create test configuration
        cat > test-config.json << EOF
        {
          "test_server": {
            "command": "python",
            "args": ["your_server.py"],
            "env": {"TEST_MODE": "true"},
            "enabled": true
          }
        }
        EOF
        
        # Run comprehensive tests
        mcp-client-cli test --config test-config.json --comprehensive
    
    - name: Upload Test Results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results-${{ matrix.python-version }}
        path: test-results/
```

### Approach 3: Containerized Testing with Dagger

```python
import dagger

async def test_with_dagger():
    """Test MCP server using Dagger containerized environment."""
    
    async with dagger.Connection() as client:
        # Load the MCP testing module
        mcp_testing = client.module("github.com/tosin2013/mcp-client-cli/.dagger")
        
        # Run comprehensive test suite
        result = await mcp_testing.run_full_test_suite(
            server_config="test-config.json",
            server_name="test_server"
        )
        
        print(f"Test results: {result}")
```

## Configuration Examples

### Python MCP Server

```json
{
  "python_server": {
    "command": "python",
    "args": ["-m", "your_package.server"],
    "env": {
      "PYTHONPATH": "src",
      "LOG_LEVEL": "DEBUG"
    },
    "enabled": true
  }
}
```

### Node.js MCP Server

```json
{
  "nodejs_server": {
    "command": "node",
    "args": ["dist/server.js"],
    "env": {
      "NODE_ENV": "test",
      "DEBUG": "*"
    },
    "enabled": true
  }
}
```

### Rust MCP Server

```json
{
  "rust_server": {
    "command": "./target/release/mcp-server",
    "args": ["--config", "test-config.toml"],
    "env": {
      "RUST_LOG": "debug"
    },
    "enabled": true
  }
}
```

## Test Types Available

### 1. Functional Testing
- MCP protocol compliance
- Tool execution validation
- Resource access testing
- Error handling verification

### 2. Security Testing
- Authentication mechanisms
- Authorization controls
- Input validation
- Data sanitization

### 3. Performance Testing
- Response time measurement
- Concurrent connection handling
- Resource usage monitoring
- Load testing

### 4. Issue Detection
- Automated problem detection
- Pattern recognition
- Health monitoring
- Remediation suggestions

## Advanced Configuration

### Custom Test Scenarios

```json
{
  "test_server": {
    "command": "python",
    "args": ["server.py"],
    "env": {"TEST_MODE": "true"},
    "enabled": true,
    "test_config": {
      "security": {
        "test_authentication": true,
        "test_authorization": true,
        "timeout_seconds": 30
      },
      "performance": {
        "max_concurrent_connections": 20,
        "test_duration_seconds": 60,
        "max_response_time_ms": 1000
      }
    }
  }
}
```

### Multi-Environment Testing

```json
{
  "development": {
    "command": "python",
    "args": ["server.py", "--dev"],
    "env": {"ENV": "development"},
    "enabled": true
  },
  "production": {
    "command": "python",
    "args": ["server.py", "--prod"],
    "env": {"ENV": "production"},
    "enabled": true
  }
}
```

## Best Practices

1. **Start Simple**: Begin with basic functional testing
2. **Add Security**: Include security testing for production servers
3. **Monitor Performance**: Regular performance testing prevents issues
4. **Automate**: Use CI/CD for continuous testing
5. **Document**: Keep test configurations in version control

## Troubleshooting

### Common Issues

1. **Server Won't Start**
   - Check command and arguments
   - Verify environment variables
   - Ensure dependencies are installed

2. **Tests Timeout**
   - Increase timeout values in configuration
   - Check server responsiveness
   - Monitor resource usage

3. **Security Tests Fail**
   - Review authentication implementation
   - Check input validation
   - Verify authorization controls

### Getting Help

- Check the [main documentation](../TESTING.md)
- Review [troubleshooting guide](TROUBLESHOOTING.md)
- See [API reference](API_REFERENCE.md)

## Next Steps

1. Set up basic testing for your MCP server
2. Add security and performance testing
3. Integrate with your CI/CD pipeline
4. Monitor and improve based on test results

This framework works with any MCP server implementation, providing comprehensive testing capabilities with minimal configuration required. 