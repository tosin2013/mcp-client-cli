# Reverse Integration: pytest-mcp-server → MCP Testing Framework

## Overview

This guide shows how the [pytest-mcp-server](https://github.com/tosin2013/pytest-mcp-server) can leverage our comprehensive MCP testing framework to generate, execute, and analyze tests. This creates a powerful self-testing and cross-testing ecosystem.

## 🎯 Integration Scenarios

### 1. Self-Testing (pytest-mcp-server testing itself)
### 2. Cross-Testing (pytest-mcp-server testing other MCP servers)
### 3. Test Generation (AI-powered test case generation)
### 4. Continuous Validation (Automated testing workflows)

## 🚀 Quick Start Integration

### Option A: Git Submodule Integration

```bash
# In pytest-mcp-server repository
git submodule add https://github.com/your-org/mcp-client-cli.git testing-framework
git submodule update --init --recursive

# Create integration script
cat > scripts/run-mcp-tests.sh << 'EOF'
#!/bin/bash
cd testing-framework
./scripts/quick-test-local.sh --path .. --type all
EOF

chmod +x scripts/run-mcp-tests.sh
```

### Option B: NPM Package Integration

```bash
# In pytest-mcp-server package.json
npm install --save-dev mcp-testing-framework

# Add test scripts
{
  "scripts": {
    "test:mcp": "mcp-test --server-path . --type all",
    "test:mcp:security": "mcp-test --server-path . --type security",
    "test:mcp:performance": "mcp-test --server-path . --type performance"
  }
}
```

### Option C: Docker Integration

```dockerfile
# In pytest-mcp-server Dockerfile.test
FROM node:20-alpine

# Install Python for MCP testing framework
RUN apk add --no-cache python3 py3-pip git

# Clone testing framework
RUN git clone https://github.com/your-org/mcp-client-cli.git /mcp-testing

# Install dependencies
WORKDIR /mcp-testing
RUN pip install -e ".[testing]"

# Copy pytest-mcp-server
COPY . /app
WORKDIR /app

# Run tests
CMD ["/mcp-testing/scripts/quick-test-local.sh", "--path", "/app", "--type", "all"]
```

## 🛠️ MCP Tool Integration

### New MCP Tool: `generate_mcp_tests`

Add this tool to pytest-mcp-server to generate tests using our framework:

```typescript
// src/tools/GenerateMCPTestsTool.ts
import { MCPTool } from "mcp-framework";
import { z } from "zod";
import { exec } from "child_process";
import { promisify } from "util";

interface GenerateMCPTestsInput {
  target_server?: string;
  test_types: string[];
  output_format: "json" | "markdown" | "html";
  confidence_threshold: number;
}

class GenerateMCPTestsTool extends MCPTool<GenerateMCPTestsInput> {
  name = "generate_mcp_tests";
  description = "Generate comprehensive MCP tests using the mcp-client-cli testing framework";

  schema = {
    target_server: {
      type: z.string().optional(),
      description: "Path to target MCP server (default: self)",
    },
    test_types: {
      type: z.array(z.enum(["functional", "security", "performance", "issue-detection", "all"])),
      description: "Types of tests to generate and run",
    },
    output_format: {
      type: z.enum(["json", "markdown", "html"]),
      description: "Format for test results",
    },
    confidence_threshold: {
      type: z.number().min(0).max(1),
      description: "Minimum confidence threshold for test results",
    },
  };

  async execute(input: GenerateMCPTestsInput) {
    const execAsync = promisify(exec);
    
    try {
      // Determine target server path
      const serverPath = input.target_server || ".";
      
      // Build command
      const testTypes = input.test_types.join(",");
      const command = `cd mcp-testing-framework && ./scripts/quick-test-local.sh --path ${serverPath} --type ${testTypes}`;
      
      // Execute tests
      const { stdout, stderr } = await execAsync(command);
      
      // Parse results
      const resultsPath = `mcp-testing-framework/test-results/pytest-mcp-server-report.${input.output_format}`;
      const results = await this.parseResults(resultsPath, input.output_format);
      
      // Filter by confidence threshold
      const filteredResults = this.filterByConfidence(results, input.confidence_threshold);
      
      return {
        success: true,
        test_results: filteredResults,
        summary: {
          total_tests: filteredResults.length,
          passed: filteredResults.filter(r => r.status === "PASSED").length,
          failed: filteredResults.filter(r => r.status === "FAILED").length,
          avg_confidence: filteredResults.reduce((sum, r) => sum + r.confidence, 0) / filteredResults.length
        },
        output_path: resultsPath
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        suggestion: "Ensure mcp-testing-framework is properly installed and configured"
      };
    }
  }

  private async parseResults(path: string, format: string) {
    // Implementation for parsing different result formats
    // ...
  }

  private filterByConfidence(results: any[], threshold: number) {
    return results.filter(result => result.confidence >= threshold);
  }
}

export default GenerateMCPTestsTool;
```

### New MCP Tool: `validate_mcp_server`

```typescript
// src/tools/ValidateMCPServerTool.ts
class ValidateMCPServerTool extends MCPTool<ValidateMCPServerInput> {
  name = "validate_mcp_server";
  description = "Validate any MCP server using comprehensive testing framework";

  async execute(input: ValidateMCPServerInput) {
    // Generate configuration for target server
    const config = await this.generateTestConfig(input);
    
    // Run validation tests
    const results = await this.runValidationTests(config);
    
    // Generate recommendations
    const recommendations = await this.generateRecommendations(results);
    
    return {
      validation_results: results,
      recommendations: recommendations,
      compliance_score: this.calculateComplianceScore(results),
      next_steps: this.suggestNextSteps(results)
    };
  }
}
```

## 📋 Workflow Templates

### 1. Self-Testing Workflow

```yaml
# .github/workflows/self-test-with-mcp-framework.yml
name: Self-Test with MCP Framework

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM

jobs:
  self-test:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout pytest-mcp-server
      uses: actions/checkout@v4
      with:
        path: pytest-mcp-server

    - name: Checkout MCP Testing Framework
      uses: actions/checkout@v4
      with:
        repository: your-org/mcp-client-cli
        path: mcp-testing-framework

    - name: Setup Environment
      run: |
        cd mcp-testing-framework
        pip install -e ".[testing]"

    - name: Run Self-Tests
      run: |
        cd mcp-testing-framework
        ./scripts/quick-test-local.sh \
          --path ../pytest-mcp-server \
          --type all \
          --clean

    - name: Generate Test Report
      run: |
        cd mcp-testing-framework
        python scripts/generate-integration-report.py \
          --target pytest-mcp-server \
          --results test-results/ \
          --output ../pytest-mcp-server/SELF_TEST_REPORT.md

    - name: Upload Results
      uses: actions/upload-artifact@v4
      with:
        name: self-test-results
        path: |
          mcp-testing-framework/test-results/
          pytest-mcp-server/SELF_TEST_REPORT.md
```

### 2. Cross-Testing Workflow

```yaml
# .github/workflows/cross-test-mcp-servers.yml
name: Cross-Test MCP Servers

on:
  workflow_dispatch:
    inputs:
      target_servers:
        description: 'Comma-separated list of MCP server repositories'
        required: true
        default: 'anthropic/mcp-server-example,other-org/mcp-server'

jobs:
  cross-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        target: ${{ fromJson(github.event.inputs.target_servers) }}
    
    steps:
    - name: Checkout pytest-mcp-server
      uses: actions/checkout@v4

    - name: Checkout MCP Testing Framework
      uses: actions/checkout@v4
      with:
        repository: your-org/mcp-client-cli
        path: mcp-testing-framework

    - name: Checkout Target Server
      uses: actions/checkout@v4
      with:
        repository: ${{ matrix.target }}
        path: target-server

    - name: Run Cross-Tests
      run: |
        cd mcp-testing-framework
        ./scripts/quick-test-local.sh \
          --path ../target-server \
          --type all \
          --output-prefix ${{ matrix.target }}
```

## 🎯 Prompt Templates

### Test Generation Prompt

```markdown
# MCP Server Test Generation Prompt

You are an expert MCP (Model Context Protocol) testing specialist. Generate comprehensive tests for the target MCP server using the mcp-client-cli testing framework.

## Context
- **Target Server**: {server_name}
- **Server Type**: {server_type}
- **Available Tools**: {tools_list}
- **Resources**: {resources_list}

## Testing Requirements
1. **Functional Testing**: Validate MCP protocol compliance and tool functionality
2. **Security Testing**: Check for vulnerabilities and security best practices
3. **Performance Testing**: Benchmark response times and resource usage
4. **Integration Testing**: Test with various client configurations

## Generate Tests For:
- [ ] Protocol handshake and capabilities exchange
- [ ] Tool execution with valid/invalid parameters
- [ ] Resource access and permissions
- [ ] Error handling and recovery
- [ ] Security vulnerabilities (OWASP Top 10)
- [ ] Performance under load
- [ ] Memory leak detection
- [ ] Cross-platform compatibility

## Output Format
Provide test configuration in JSON format compatible with mcp-client-cli testing framework.

## Confidence Scoring
Include confidence scores (0.0-1.0) for each test based on:
- Test coverage completeness
- Verification methodology strength
- Expected result reliability
```

### Validation Prompt

```markdown
# MCP Server Validation Prompt

Analyze the MCP server test results and provide comprehensive validation assessment.

## Test Results Summary
- **Total Tests**: {total_tests}
- **Passed**: {passed_tests}
- **Failed**: {failed_tests}
- **Average Confidence**: {avg_confidence}

## Analysis Required
1. **Compliance Assessment**: MCP protocol adherence
2. **Security Posture**: Vulnerability analysis
3. **Performance Characteristics**: Bottlenecks and optimization opportunities
4. **Reliability Metrics**: Error rates and stability
5. **Best Practice Adherence**: Industry standards compliance

## Provide Recommendations For:
- Critical issues requiring immediate attention
- Performance optimization opportunities
- Security hardening suggestions
- Code quality improvements
- Documentation updates

## Confidence Methodology
Apply methodological pragmatism principles:
- Explicit fallibilism acknowledgment
- Systematic verification processes
- Pragmatic success criteria
- Cognitive systematization
```

## 🔧 Integration Scripts

### Self-Test Integration Script

```bash
#!/bin/bash
# scripts/self-test-integration.sh

set -e

echo "🧪 pytest-mcp-server Self-Testing with MCP Framework"
echo "=================================================="

# Configuration
MCP_FRAMEWORK_PATH="${MCP_FRAMEWORK_PATH:-../mcp-client-cli}"
TEST_TYPE="${TEST_TYPE:-all}"
OUTPUT_DIR="${OUTPUT_DIR:-./test-results}"

# Ensure MCP testing framework is available
if [[ ! -d "$MCP_FRAMEWORK_PATH" ]]; then
    echo "📥 Cloning MCP testing framework..."
    git clone https://github.com/your-org/mcp-client-cli.git "$MCP_FRAMEWORK_PATH"
fi

# Setup testing framework
echo "🔧 Setting up testing framework..."
cd "$MCP_FRAMEWORK_PATH"
pip install -e ".[testing]" > /dev/null 2>&1

# Return to pytest-mcp-server directory
cd - > /dev/null

# Run self-tests
echo "🚀 Running self-tests..."
"$MCP_FRAMEWORK_PATH/scripts/quick-test-local.sh" \
    --path . \
    --type "$TEST_TYPE" \
    --clean

# Copy results to our directory
mkdir -p "$OUTPUT_DIR"
cp -r "$MCP_FRAMEWORK_PATH/test-results/"* "$OUTPUT_DIR/"

# Generate summary
echo "📊 Generating test summary..."
python3 << 'EOF'
import json
import os
from pathlib import Path

results_dir = Path(os.environ.get('OUTPUT_DIR', './test-results'))
summary = {
    "timestamp": "$(date -Iseconds)",
    "test_type": os.environ.get('TEST_TYPE', 'all'),
    "server": "pytest-mcp-server",
    "results": {}
}

# Parse test results
for result_file in results_dir.glob("*.json"):
    with open(result_file) as f:
        data = json.load(f)
        summary["results"][result_file.stem] = data

# Save summary
with open(results_dir / "self-test-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"✅ Self-test completed! Results in {results_dir}")
EOF
```

### Cross-Test Integration Script

```bash
#!/bin/bash
# scripts/cross-test-integration.sh

set -e

TARGET_REPO="$1"
TARGET_BRANCH="${2:-main}"

if [[ -z "$TARGET_REPO" ]]; then
    echo "Usage: $0 <target-repo> [branch]"
    echo "Example: $0 anthropic/mcp-server-example main"
    exit 1
fi

echo "🔄 Cross-testing against $TARGET_REPO ($TARGET_BRANCH)"
echo "=================================================="

# Clone target repository
TARGET_DIR="./cross-test-targets/$(basename "$TARGET_REPO")"
mkdir -p "$(dirname "$TARGET_DIR")"

if [[ ! -d "$TARGET_DIR" ]]; then
    git clone "https://github.com/$TARGET_REPO.git" "$TARGET_DIR"
fi

cd "$TARGET_DIR"
git checkout "$TARGET_BRANCH"
git pull origin "$TARGET_BRANCH"

# Setup target server if needed
if [[ -f "package.json" ]]; then
    npm ci
    npm run build 2>/dev/null || echo "Build failed, continuing..."
elif [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
elif [[ -f "pyproject.toml" ]]; then
    pip install -e .
fi

cd - > /dev/null

# Run cross-tests using our MCP framework
echo "🧪 Running cross-tests..."
../mcp-client-cli/scripts/quick-test-local.sh \
    --path "$TARGET_DIR" \
    --type all \
    --output-prefix "cross-test-$(basename "$TARGET_REPO")"

echo "✅ Cross-test completed for $TARGET_REPO"
```

## 📊 Integration Dashboard

### Test Results Dashboard

```html
<!-- dashboard/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>pytest-mcp-server Testing Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>MCP Testing Dashboard</h1>
    
    <div class="dashboard-grid">
        <div class="card">
            <h2>Self-Test Results</h2>
            <canvas id="selfTestChart"></canvas>
        </div>
        
        <div class="card">
            <h2>Cross-Test Results</h2>
            <canvas id="crossTestChart"></canvas>
        </div>
        
        <div class="card">
            <h2>Performance Trends</h2>
            <canvas id="performanceChart"></canvas>
        </div>
        
        <div class="card">
            <h2>Security Score</h2>
            <canvas id="securityChart"></canvas>
        </div>
    </div>

    <script>
        // Load and display test results
        fetch('./test-results/self-test-summary.json')
            .then(response => response.json())
            .then(data => {
                // Render charts with test data
                renderSelfTestChart(data);
            });
    </script>
</body>
</html>
```

## 🚀 Getting Started

### 1. Add to pytest-mcp-server

```bash
# In pytest-mcp-server repository
mkdir -p scripts
curl -o scripts/self-test-integration.sh \
    https://raw.githubusercontent.com/your-org/mcp-client-cli/main/examples/self-test-integration.sh
chmod +x scripts/self-test-integration.sh

# Add to package.json
{
  "scripts": {
    "test:self": "./scripts/self-test-integration.sh",
    "test:cross": "./scripts/cross-test-integration.sh"
  }
}
```

### 2. Run Self-Tests

```bash
npm run test:self
# or
./scripts/self-test-integration.sh
```

### 3. Run Cross-Tests

```bash
npm run test:cross anthropic/mcp-server-example
# or
./scripts/cross-test-integration.sh anthropic/mcp-server-example
```

## 🎯 Benefits

1. **Bidirectional Testing**: Both repositories can test each other
2. **Continuous Validation**: Automated testing workflows
3. **Cross-Compatibility**: Test against multiple MCP servers
4. **Quality Assurance**: Comprehensive test coverage
5. **Performance Monitoring**: Continuous performance tracking
6. **Security Validation**: Regular security assessments

## 📚 Next Steps

1. **Implement MCP Tools**: Add `generate_mcp_tests` and `validate_mcp_server` tools
2. **Setup Workflows**: Configure GitHub Actions for automated testing
3. **Create Dashboard**: Build testing results dashboard
4. **Documentation**: Update pytest-mcp-server documentation
5. **Community**: Share integration patterns with MCP community

This reverse integration creates a powerful ecosystem where MCP servers can leverage our comprehensive testing framework for self-validation and cross-testing capabilities. 