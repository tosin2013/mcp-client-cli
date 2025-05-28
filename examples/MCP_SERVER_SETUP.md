# MCP Server Testing Setup Guide

Quick 5-minute setup guide for testing any MCP server with the comprehensive testing framework.

## Prerequisites

- Python 3.9+ or Node.js 18+
- Git
- Your MCP server repository

## Quick Setup (5 Minutes)

### Step 1: Clone Your MCP Server Repository

```bash
# Clone your MCP server repository
git clone <your-mcp-server-repo-url>
cd <your-mcp-server-directory>

# Or if you're already in your MCP server directory
pwd  # Confirm you're in the right directory
```

### Step 2: Install MCP Testing Framework

```bash
# Option A: Install from PyPI (when available)
pip install mcp-client-cli[testing]

# Option B: Install from GitHub (current)
pip install git+https://github.com/tosin2013/mcp-client-cli.git[testing]

# Option C: Clone and install locally
git clone https://github.com/tosin2013/mcp-client-cli.git ../mcp-client-cli
pip install -e "../mcp-client-cli[testing]"
```

### Step 3: Create Test Configuration

Create a `test-config.json` file in your MCP server repository:

```bash
# Auto-detect and create configuration
cat > test-config.json << 'EOF'
{
  "test_server": {
    "command": "python",
    "args": ["server.py"],
    "env": {
      "TEST_MODE": "true",
      "LOG_LEVEL": "DEBUG"
    },
    "enabled": true
  }
}
EOF
```

**Customize for your server:**

- **Python servers**: `"command": "python", "args": ["your_server.py"]`
- **Node.js servers**: `"command": "node", "args": ["dist/server.js"]`
- **Rust servers**: `"command": "./target/release/server"`
- **Go servers**: `"command": "./server"`

### Step 4: Run Basic Tests

```bash
# Quick functional test
mcp-client-cli test --config test-config.json

# Comprehensive testing (all test types)
mcp-client-cli test --config test-config.json --comprehensive

# Specific test types
mcp-client-cli test --config test-config.json --security
mcp-client-cli test --config test-config.json --performance
```

### Step 5: View Results

```bash
# View test results
ls -la test-results/

# Read summary report
cat test-results/test-summary.md

# Check specific results
cat test-results/functional-tests.json
```

## Advanced Setup Options

### Option 1: One-Command Setup Script

Create `setup-testing.sh` in your repository:

```bash
#!/bin/bash
# setup-testing.sh - One-command MCP server testing setup

set -e

echo "🚀 Setting up MCP server testing..."

# Install testing framework
pip install git+https://github.com/tosin2013/mcp-client-cli.git[testing]

# Auto-detect server configuration
if [ -f "server.py" ]; then
    SERVER_CMD="python"
    SERVER_ARGS='["server.py"]'
elif [ -f "src/server.py" ]; then
    SERVER_CMD="python"
    SERVER_ARGS='["src/server.py"]'
elif [ -f "dist/server.js" ]; then
    SERVER_CMD="node"
    SERVER_ARGS='["dist/server.js"]'
elif [ -f "server.js" ]; then
    SERVER_CMD="node"
    SERVER_ARGS='["server.js"]'
else
    echo "❌ Could not auto-detect server. Please create test-config.json manually."
    exit 1
fi

# Create configuration
cat > test-config.json << EOF
{
  "test_server": {
    "command": "$SERVER_CMD",
    "args": $SERVER_ARGS,
    "env": {
      "TEST_MODE": "true",
      "LOG_LEVEL": "DEBUG"
    },
    "enabled": true
  }
}
EOF

echo "✅ Configuration created: test-config.json"

# Run basic tests
echo "🧪 Running basic tests..."
mcp-client-cli test --config test-config.json

echo "🎉 Setup complete! Check test-results/ for detailed results."
```

Make it executable and run:

```bash
chmod +x setup-testing.sh
./setup-testing.sh
```

### Option 2: GitHub Actions Integration

Create `.github/workflows/mcp-testing.yml`:

```yaml
name: MCP Server Testing

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  test-mcp-server:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.11, 3.12]
        test-type: [functional, security, performance]
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install git+https://github.com/tosin2013/mcp-client-cli.git[testing]
        
        # Install your server dependencies
        if [ -f requirements.txt ]; then
          pip install -r requirements.txt
        elif [ -f pyproject.toml ]; then
          pip install -e .
        fi
    
    - name: Create test configuration
      run: |
        cat > test-config.json << 'EOF'
        {
          "test_server": {
            "command": "python",
            "args": ["server.py"],
            "env": {
              "TEST_MODE": "true",
              "CI": "true"
            },
            "enabled": true
          }
        }
        EOF
    
    - name: Run MCP tests
      run: |
        case "${{ matrix.test-type }}" in
          functional)
            mcp-client-cli test --config test-config.json --functional
            ;;
          security)
            mcp-client-cli test --config test-config.json --security
            ;;
          performance)
            mcp-client-cli test --config test-config.json --performance
            ;;
        esac
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results-${{ matrix.python-version }}-${{ matrix.test-type }}
        path: test-results/
        retention-days: 30
    
    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          if (fs.existsSync('test-results/test-summary.md')) {
            const summary = fs.readFileSync('test-results/test-summary.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## MCP Testing Results (${{ matrix.test-type }})\n\n${summary}`
            });
          }
```

### Option 3: Docker Integration

Create `Dockerfile.testing`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install testing framework
RUN pip install git+https://github.com/tosin2013/mcp-client-cli.git[testing]

# Copy your server code
COPY . .

# Install server dependencies
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
RUN if [ -f pyproject.toml ]; then pip install -e .; fi

# Create test configuration
RUN echo '{\
  "test_server": {\
    "command": "python",\
    "args": ["server.py"],\
    "env": {"TEST_MODE": "true"},\
    "enabled": true\
  }\
}' > test-config.json

# Run tests by default
CMD ["mcp-client-cli", "test", "--config", "test-config.json", "--comprehensive"]
```

Build and run:

```bash
# Build testing image
docker build -f Dockerfile.testing -t my-mcp-server-test .

# Run comprehensive tests
docker run --rm -v $(pwd)/test-results:/app/test-results my-mcp-server-test

# Run specific test types
docker run --rm my-mcp-server-test mcp-client-cli test --config test-config.json --security
```

## Configuration Examples

### Python MCP Server

```json
{
  "python_server": {
    "command": "python",
    "args": ["-m", "my_package.server"],
    "env": {
      "PYTHONPATH": "src",
      "LOG_LEVEL": "DEBUG",
      "TEST_MODE": "true"
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
    "args": ["dist/index.js"],
    "env": {
      "NODE_ENV": "test",
      "DEBUG": "*",
      "LOG_LEVEL": "debug"
    },
    "enabled": true
  }
}
```

### Multi-Server Testing

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

## Troubleshooting

### Common Issues

1. **Server won't start**
   ```bash
   # Check if server runs manually
   python server.py
   
   # Verify dependencies
   pip list | grep -E "(mcp|langchain)"
   ```

2. **Tests timeout**
   ```bash
   # Increase timeout in configuration
   {
     "test_server": {
       "command": "python",
       "args": ["server.py"],
       "timeout": 60,
       "enabled": true
     }
   }
   ```

3. **Permission errors**
   ```bash
   # Make server executable
   chmod +x server.py
   
   # Check file permissions
   ls -la server.py
   ```

### Debug Mode

```bash
# Enable verbose output
mcp-client-cli test --config test-config.json --verbose

# Save debug logs
mcp-client-cli test --config test-config.json --debug > debug.log 2>&1
```

## Next Steps

1. **Customize Configuration**: Adjust test-config.json for your specific server
2. **Add CI/CD**: Set up automated testing with GitHub Actions
3. **Monitor Performance**: Regular performance testing
4. **Security Hardening**: Regular security testing
5. **Documentation**: Document your testing setup

## Resources

- [Main Testing Documentation](../TESTING.md)
- [Configuration Reference](CONFIG_REFERENCE.md)
- [API Documentation](API_REFERENCE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## Support

If you encounter issues:

1. Check the [troubleshooting guide](TROUBLESHOOTING.md)
2. Review [common configurations](CONFIG_EXAMPLES.md)
3. Open an issue on [GitHub](https://github.com/tosin2013/mcp-client-cli/issues)

**Setup time: ~5 minutes | First test run: ~2 minutes | Full test suite: ~10 minutes** 