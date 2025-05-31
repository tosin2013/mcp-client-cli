---
layout: chapter
title: "CI/CD Integration"
chapter_number: 8
description: "Continuous integration and deployment pipeline integration"
---

# Chapter 8: CI/CD Integration

## GitHub Actions Integration

Continuous Integration and Continuous Deployment (CI/CD) are essential practices for modern software development. Integrating MCP server testing into CI/CD pipelines ensures that your servers are automatically validated with every code change. The mcp-client-cli provides robust support for CI/CD integration, with particular emphasis on GitHub Actions.

### Basic GitHub Actions Workflow

According to the [mcp-client-cli documentation](https://github.com/tosin2013/mcp-client-cli), a basic GitHub Actions workflow for MCP server testing looks like this:

```yaml
# .github/workflows/mcp-testing.yml
name: MCP Server Testing
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install mcp-testing-framework
      - run: mcp-test --test-mcp-servers
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

This simple workflow:
1. Triggers on push and pull request events
2. Sets up a Python environment
3. Installs the mcp-testing-framework
4. Runs the basic MCP server tests

As noted in the [official MCP documentation](https://modelcontextprotocol.io/introduction), this integration ensures that your MCP server is tested with every code change, maintaining consistent quality and compliance with the protocol specification.

### Advanced GitHub Actions Configuration

For more comprehensive testing, you can create a more sophisticated workflow:

```yaml
# .github/workflows/comprehensive-mcp-testing.yml
name: Comprehensive MCP Server Testing
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
        exclude:
          - os: macos-latest
            python-version: '3.9'
          - os: windows-latest
            python-version: '3.9'
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install mcp-testing-framework[all]
      
      - name: Cache test results
        uses: actions/cache@v3
        with:
          path: ~/.mcp-test-cache
          key: ${{ runner.os }}-python-${{ matrix.python-version }}-${{ hashFiles('**/*.py') }}
      
      - name: Run functional tests
        run: mcp-test functional --server-name mcp-server --config test-config.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Run security tests
        run: mcp-test security --server-name mcp-server --config test-config.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Run performance tests
        run: mcp-test performance --server-name mcp-server --config test-config.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      
      - name: Generate test report
        run: mcp-test generate-report --format html --output test-report.html
      
      - name: Upload test report
        uses: actions/upload-artifact@v3
        with:
          name: test-report-${{ matrix.os }}-python-${{ matrix.python-version }}
          path: test-report.html
```

This advanced workflow provides:
1. **Matrix Testing**: Across multiple operating systems and Python versions
2. **Scheduled Testing**: Daily runs in addition to push/PR triggers
3. **Dependency Caching**: For faster workflow execution
4. **Comprehensive Testing**: Separate steps for functional, security, and performance tests
5. **Report Generation**: Creating and uploading HTML test reports

According to the [Spring AI Reference documentation](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-overview.html), this kind of comprehensive testing is essential for ensuring MCP server compatibility across different environments.

### GitHub Actions Workflow Templates

The mcp-client-cli provides several pre-configured workflow templates for different testing scenarios:

#### Basic Testing Template

```bash
# Generate a basic testing workflow
mcp-test generate-workflow --type github-actions --template basic --output .github/workflows/basic-testing.yml
```

This command generates a simple workflow for basic MCP server testing.

#### Comprehensive Testing Template

```bash
# Generate a comprehensive testing workflow
mcp-test generate-workflow --type github-actions --template comprehensive --output .github/workflows/comprehensive-testing.yml
```

This command generates a more sophisticated workflow with matrix testing and multiple test types.

#### Security-Focused Template

```bash
# Generate a security-focused workflow
mcp-test generate-workflow --type github-actions --template security --output .github/workflows/security-testing.yml
```

This command generates a workflow focused specifically on security testing.

#### Performance-Focused Template

```bash
# Generate a performance-focused workflow
mcp-test generate-workflow --type github-actions --template performance --output .github/workflows/performance-testing.yml
```

This command generates a workflow focused on performance testing and benchmarking.

### GitHub Actions Best Practices

When integrating MCP server testing with GitHub Actions, several best practices enhance effectiveness:

1. **Secret Management**: Store API keys and sensitive configuration in GitHub Secrets
   ```yaml
   env:
     OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
     MCP_SERVER_TOKEN: ${{ secrets.MCP_SERVER_TOKEN }}
   ```

2. **Artifact Management**: Save test reports and logs as artifacts
   ```yaml
   - name: Upload test artifacts
     uses: actions/upload-artifact@v3
     with:
       name: test-results
       path: |
         test-report.html
         test-logs/
         performance-data/
   ```

3. **Conditional Testing**: Run different tests based on context
   ```yaml
   - name: Run comprehensive tests
     if: github.event_name == 'schedule' || github.ref == 'refs/heads/main'
     run: mcp-test run-suite --suite-name comprehensive
   
   - name: Run basic tests
     if: github.event_name == 'pull_request'
     run: mcp-test run-suite --suite-name basic
   ```

4. **Workflow Optimization**: Use caching and selective testing
   ```yaml
   - name: Cache dependencies
     uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
   ```

5. **Status Checks**: Configure required status checks for protected branches
   ```yaml
   - name: Report status
     run: |
       if [ $TEST_EXIT_CODE -ne 0 ]; then
         echo "Tests failed with exit code $TEST_EXIT_CODE"
         exit 1
       fi
     env:
       TEST_EXIT_CODE: ${{ steps.run_tests.outputs.exit_code }}
   ```

These practices help ensure reliable, efficient, and secure CI/CD integration for your MCP server testing.

## Automated Testing Pipelines

Beyond GitHub Actions, the mcp-client-cli supports integration with various CI/CD systems through automated testing pipelines.

### Jenkins Integration

For organizations using Jenkins, the mcp-client-cli can be integrated into Jenkins pipelines:

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'python:3.11'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install mcp-testing-framework[all]'
            }
        }
        
        stage('Functional Testing') {
            steps {
                sh 'mcp-test functional --server-name mcp-server --config test-config.json'
            }
        }
        
        stage('Security Testing') {
            steps {
                sh 'mcp-test security --server-name mcp-server --config test-config.json'
            }
        }
        
        stage('Performance Testing') {
            steps {
                sh 'mcp-test performance --server-name mcp-server --config test-config.json'
            }
        }
        
        stage('Report Generation') {
            steps {
                sh 'mcp-test generate-report --format html --output test-report.html'
                archiveArtifacts artifacts: 'test-report.html', fingerprint: true
            }
        }
    }
    
    post {
        always {
            junit 'test-results/*.xml'
        }
    }
}
```

According to the [mcp-client-cli documentation](https://github.com/tosin2013/mcp-client-cli), this pipeline provides comprehensive testing with result reporting and artifact archiving.

### GitLab CI Integration

For GitLab users, the mcp-client-cli can be integrated with GitLab CI:

```yaml
# .gitlab-ci.yml
image: python:3.11

stages:
  - setup
  - test
  - report

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

cache:
  paths:
    - .pip-cache/

setup:
  stage: setup
  script:
    - pip install mcp-testing-framework[all]
  artifacts:
    paths:
      - .pip-cache/

functional_testing:
  stage: test
  script:
    - mcp-test functional --server-name mcp-server --config test-config.json
  artifacts:
    paths:
      - test-results/functional/

security_testing:
  stage: test
  script:
    - mcp-test security --server-name mcp-server --config test-config.json
  artifacts:
    paths:
      - test-results/security/

performance_testing:
  stage: test
  script:
    - mcp-test performance --server-name mcp-server --config test-config.json
  artifacts:
    paths:
      - test-results/performance/

generate_report:
  stage: report
  script:
    - mcp-test generate-report --format html --output test-report.html
  artifacts:
    paths:
      - test-report.html
```

This configuration provides a multi-stage pipeline with dependency caching and artifact management.

### Azure DevOps Integration

For Azure DevOps users, the mcp-client-cli can be integrated with Azure Pipelines:

```yaml
# azure-pipelines.yml
trigger:
  - main
  - develop

pool:
  vmImage: 'ubuntu-latest'

strategy:
  matrix:
    Python39:
      pythonVersion: '3.9'
    Python310:
      pythonVersion: '3.10'
    Python311:
      pythonVersion: '3.11'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '$(pythonVersion)'
    addToPath: true

- script: |
    python -m pip install --upgrade pip
    pip install mcp-testing-framework[all]
  displayName: 'Install dependencies'

- script: |
    mcp-test functional --server-name mcp-server --config test-config.json
  displayName: 'Run functional tests'

- script: |
    mcp-test security --server-name mcp-server --config test-config.json
  displayName: 'Run security tests'

- script: |
    mcp-test performance --server-name mcp-server --config test-config.json
  displayName: 'Run performance tests'

- script: |
    mcp-test generate-report --format html --output $(Build.ArtifactStagingDirectory)/test-report.html
  displayName: 'Generate test report'

- task: PublishBuildArtifacts@1
  inputs:
    pathtoPublish: '$(Build.ArtifactStagingDirectory)'
    artifactName: 'test-results'
```

This configuration provides matrix testing across Python versions with artifact publishing.

### CircleCI Integration

For CircleCI users, the mcp-client-cli can be integrated with CircleCI workflows:

```yaml
# .circleci/config.yml
version: 2.1

orbs:
  python: circleci/python@1.5

jobs:
  test:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          packages:
            - mcp-testing-framework[all]
      - run:
          name: Run functional tests
          command: mcp-test functional --server-name mcp-server --config test-config.json
      - run:
          name: Run security tests
          command: mcp-test security --server-name mcp-server --config test-config.json
      - run:
          name: Run performance tests
          command: mcp-test performance --server-name mcp-server --config test-config.json
      - run:
          name: Generate test report
          command: mcp-test generate-report --format html --output test-report.html
      - store_artifacts:
          path: test-report.html
          destination: test-report.html

workflows:
  version: 2
  test:
    jobs:
      - test
```

This configuration provides a complete testing workflow with artifact storage.

## Dagger.io Pipelines

The mcp-client-cli includes special integration with [Dagger.io](https://dagger.io/), a powerful tool for creating portable CI/CD pipelines. This integration provides enhanced capabilities for MCP server testing.

### Dagger.io Overview

According to the [TESTING.md](https://github.com/tosin2013/mcp-client-cli/blob/master/TESTING.md) documentation, Dagger.io offers several advantages for MCP server testing:

1. **Portability**: Pipelines run consistently across different environments
2. **Containerization**: Tests run in isolated containers
3. **Caching**: Intelligent caching improves performance
4. **Parallelism**: Efficient parallel execution
5. **Reproducibility**: Consistent results across runs

These advantages make Dagger.io an excellent choice for MCP server testing pipelines.

### Basic Dagger.io Pipeline

A basic Dagger.io pipeline for MCP server testing looks like this:

```bash
# Run functional tests via Dagger
dagger call run-functional-tests --source .

# Run full test suite with reporting
dagger call run-full-test-suite --source . --generate-report true

# Run performance benchmarks
dagger call run-performance-tests --source . --benchmark-mode true
```

These commands leverage pre-defined Dagger.io functions in the mcp-client-cli to execute different types of tests.

### Dagger.io Pipeline Configuration

Dagger.io pipelines can be configured through a `.dagger/pipeline-config.json` file:

```json
{
  "environments": {
    "python": {
      "version": "3.12",
      "dependencies": ["mcp", "langchain", "rich"]
    },
    "nodejs": {
      "version": "18",
      "dependencies": ["@modelcontextprotocol/sdk"]
    }
  },
  "testing": {
    "parallel_execution": true,
    "timeout_seconds": 300,
    "retry_attempts": 3
  },
  "reporting": {
    "generate_html": true,
    "include_performance_charts": true,
    "confidence_analysis": true
  }
}
```

This configuration defines testing environments, execution parameters, and reporting options.

### Custom Dagger.io Functions

You can define custom Dagger.io functions for specialized testing needs:

```go
// .dagger/main.go
package main

import (
	"context"
	"fmt"
)

type MCP struct{}

// RunCustomTests runs specialized MCP server tests
func (m *MCP) RunCustomTests(
	ctx context.Context,
	source *Directory,
	testType string,
	parameters *Optional[string],
) (*Container, error) {
	container := dag.Container().
		From("python:3.11").
		WithDirectory("/src", source).
		WithWorkdir("/src").
		WithExec([]string{"pip", "install", "mcp-testing-framework[all]"})

	paramStr := ""
	if parameters != nil && parameters.Value != "" {
		paramStr = fmt.Sprintf("--parameters '%s'", parameters.Value)
	}

	return container.WithExec([]string{
		"sh", "-c",
		fmt.Sprintf("mcp-test custom --test-type %s %s", testType, paramStr),
	}), nil
}
```

This custom function allows you to run specialized tests with configurable parameters.

### Dagger.io CI Integration

Dagger.io pipelines can be integrated with CI systems:

```yaml
# .github/workflows/dagger-mcp-testing.yml
name: Dagger MCP Testing
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Dagger
        uses: dagger/dagger-for-github@v5
      
      - name: Run MCP tests with Dagger
        run: |
          dagger call run-full-test-suite --source . --generate-report true
      
      - name: Upload test report
        uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: test-report.html
```

This workflow uses Dagger.io to run MCP server tests, providing consistent results across different environments.

## Multi-Environment Testing

Comprehensive MCP server testing requires validation across multiple environments. The mcp-client-cli provides robust support for multi-environment testing.

### Environment Matrix Definition

According to the [mcp-client-cli documentation](https://github.com/tosin2013/mcp-client-cli), you can define an environment matrix for testing:

```json
{
  "environments": {
    "python-3.9": {
      "image": "python:3.9",
      "setup": "pip install -r requirements.txt"
    },
    "python-3.10": {
      "image": "python:3.10",
      "setup": "pip install -r requirements.txt"
    },
    "python-3.11": {
      "image": "python:3.11",
      "setup": "pip install -r requirements.txt"
    },
    "nodejs-16": {
      "image": "node:16",
      "setup": "npm ci"
    },
    "nodejs-18": {
      "image": "node:18",
      "setup": "npm ci"
    }
  }
}
```

This matrix defines different environments for testing, each with its own configuration.

### Matrix Testing Command

To run tests across the environment matrix:

```bash
# Run matrix testing
mcp-test matrix --config matrix-config.json --test-type functional
```

This command executes the specified tests across all defined environments, providing comprehensive validation.

### Environment-Specific Configuration

You can provide environment-specific test configurations:

```json
{
  "environments": {
    "python-3.11": {
      "image": "python:3.11",
      "setup": "pip install -r requirements.txt",
      "config": {
        "testing": {
          "timeout": 60,
          "retries": 3
        }
      }
    },
    "nodejs-18": {
      "image": "node:18",
      "setup": "npm ci",
      "config": {
        "testing": {
          "timeout": 30,
          "retries": 5
        }
      }
    }
  }
}
```

This approach allows you to customize testing parameters for each environment.

### Cross-Environment Compatibility Testing

To validate compatibility across different environments:

```bash
# Run cross-environment compatibility tests
mcp-test cross-compatibility --environments python-3.11,nodejs-18 --config matrix-config.json
```

This command tests interactions between different environments, ensuring that MCP servers and clients can communicate effectively regardless of their implementation language.

### Environment Reporting

To generate reports that compare results across environments:

```bash
# Generate environment comparison report
mcp-test generate-environment-report --environments all --format html --output environment-report.html
```

This command creates a report that highlights differences in test results across environments, helping identify environment-specific issues.

## Continuous Validation Strategies

Beyond basic CI/CD integration, the mcp-client-cli supports sophisticated continuous validation strategies that ensure ongoing quality and compliance.

### Scheduled Testing

According to the [mcp-client-cli documentation](https://github.com/tosin2013/mcp-client-cli), scheduled testing helps identify issues that might not appear in regular CI runs:

```yaml
# .github/workflows/scheduled-testing.yml
name: Scheduled MCP Testing
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  comprehensive-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install mcp-testing-framework[all]
      - run: mcp-test run-suite --suite-name comprehensive --extended-duration
```

Scheduled testing can include extended test durations, more comprehensive test suites, and additional validation that might be too time-consuming for regular CI runs.

### Regression Testing

To ensure that previously fixed issues don't reappear:

```bash
# Run regression tests
mcp-test regression --issue-ids issue-123,issue-456 --config test-config.json
```

This command runs tests specifically designed to verify that previously identified issues remain fixed, providing an additional layer of quality assurance.

### Canary Testing

For early detection of issues in new code:

```bash
# Run canary tests
mcp-test canary --branch feature/new-functionality --config test-config.json
```

Canary testing runs a subset of tests against new code branches, providing early feedback before full testing in the main CI pipeline.

### A/B Testing

To compare different implementations or configurations:

```bash
# Run A/B testing
mcp-test compare --config-a config-a.json --config-b config-b.json --output comparison-report.html
```

This command runs the same tests against different configurations or implementations, generating a comparison report that highlights differences in functionality, performance, or other aspects.

### Continuous Benchmarking

To track performance over time:

```bash
# Run continuous benchmarking
mcp-test benchmark --historical --days 30 --output benchmark-trends.html
```

Continuous benchmarking tracks performance metrics over time, helping identify performance regressions or improvements as the code evolves.

### Notification and Alerting

To ensure timely response to issues:

```yaml
# .github/workflows/mcp-testing-with-alerts.yml
name: MCP Testing with Alerts
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install mcp-testing-framework[all]
      - run: mcp-test run-suite --suite-name comprehensive
      
      - name: Send notification on failure
        if: failure()
        uses: rtCamp/action-slack-notify@v2
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
          SLACK_CHANNEL: mcp-testing-alerts
          SLACK_TITLE: MCP Testing Failed
          SLACK_MESSAGE: 'MCP tests failed in ${{ github.repository }} on branch ${{ github.ref }}'
          SLACK_COLOR: danger
```

This workflow sends notifications when tests fail, ensuring that issues are promptly addressed.

## Conclusion

Integrating MCP server testing into CI/CD pipelines is essential for maintaining quality and compliance with the MCP specification. The mcp-client-cli provides robust support for various CI/CD systems, including GitHub Actions, Jenkins, GitLab CI, Azure DevOps, CircleCI, and Dagger.io.

By implementing automated testing pipelines, multi-environment testing, and continuous validation strategies, you can ensure that your MCP server implementations remain functional, secure, and performant as they evolve. These practices help identify issues early in the development process, reducing the cost and impact of fixes.

Whether you're using simple GitHub Actions workflows or sophisticated Dagger.io pipelines, the mcp-client-cli provides the tools and capabilities you need to implement effective CI/CD integration for your MCP server testing.

In the next chapter, we'll explore multi-language testing, which is particularly important for organizations that implement MCP servers in multiple programming languages.
