---
layout: chapter
title: "Setting Up the MCP-Client-CLI"
chapter_number: 3
description: "Installation, configuration, and initial setup of the MCP-Client-CLI tool"
---

# Chapter 3: Setting Up the MCP-Client-CLI

## Installation Requirements and Dependencies

Before diving into MCP server testing, you'll need to properly set up the mcp-client-cli tool. This chapter walks through the installation process, requirements, and initial configuration steps to ensure you have a functional testing environment.

### System Requirements

The mcp-client-cli tool is designed to run on multiple platforms with minimal system requirements. According to the [repository documentation](https://github.com/tosin2013/mcp-client-cli), the tool supports:

- **Operating Systems**: 
  - Linux (Ubuntu, Debian, CentOS, etc.)
  - macOS (10.15 Catalina or newer)
  - Windows 10/11 with WSL (Windows Subsystem for Linux)

- **Python Requirements**:
  - Python 3.9 or newer
  - pip package manager

- **Additional Dependencies**:
  - Git (for repository cloning and version control)
  - A working internet connection (for package installation and external API access)

For optimal performance, especially when running comprehensive test suites or performance testing, the following specifications are recommended:

- 4GB RAM or more
- 2 CPU cores or more
- 1GB free disk space

### Python Environment Setup

The mcp-client-cli tool relies on Python, so ensuring you have a proper Python environment is the first step. If you don't already have Python installed, you can download it from the [official Python website](https://www.python.org/downloads/).

To verify your Python installation, open a terminal or command prompt and run:

```bash
python --version
# or
python3 --version
```

You should see output indicating Python 3.9 or newer. If you receive an error or have an older version, you'll need to install or update Python before proceeding.

### Virtual Environment (Recommended)

While not strictly required, using a virtual environment is highly recommended to avoid dependency conflicts with other Python projects. As noted in the [Python documentation](https://docs.python.org/3/library/venv.html), virtual environments provide isolated spaces for Python projects, ensuring clean and reproducible installations.

To create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv mcp-testing-env

# Activate the environment (Linux/macOS)
source mcp-testing-env/bin/activate

# Activate the environment (Windows)
mcp-testing-env\Scripts\activate
```

Once activated, your command prompt should show the environment name, indicating that any Python packages you install will be contained within this environment.

## Installation Methods

The mcp-client-cli tool can be installed through several methods, depending on your specific needs and preferences.

### Installation via pip (Recommended)

The simplest and most straightforward installation method is using pip, Python's package manager. As documented in the [README.md](https://github.com/tosin2013/mcp-client-cli), you can install the package with:

```bash
pip install mcp-testing-framework
```

This command installs the latest stable release from the Python Package Index (PyPI). For those who need specific versions, you can specify the version number:

```bash
pip install mcp-testing-framework==1.0.0
```

### Installation from Source

For users who need the latest features or want to contribute to the project, installing from source is the preferred method:

```bash
# Clone the repository
git clone https://github.com/tosin2013/mcp-client-cli.git

# Navigate to the project directory
cd mcp-client-cli

# Install in development mode
pip install -e ".[dev]"
```

Installing in development mode (`-e`) creates a link to the source code, allowing you to modify the code and immediately see the effects without reinstalling.

### Installation with Additional Features

The mcp-client-cli supports optional feature sets for different testing scenarios. These can be installed using pip's extras syntax:

```bash
# Install with testing extras
pip install mcp-testing-framework[testing]

# Install with development extras
pip install mcp-testing-framework[dev]

# Install with all extras
pip install mcp-testing-framework[all]
```

Each feature set includes additional dependencies tailored to specific use cases:

- **testing**: Includes pytest, coverage tools, and other testing utilities
- **dev**: Adds development tools like black, isort, and mypy
- **all**: Installs all available extras

### Docker Installation (Alternative)

For users who prefer containerized environments, the mcp-client-cli can also be run using Docker. While not explicitly documented in the repository, this approach offers several advantages, including isolation from the host system and consistent environments across different machines.

To use Docker:

1. Create a Dockerfile:
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   RUN pip install mcp-testing-framework
   
   ENTRYPOINT ["mcp-test"]
   ```

2. Build the Docker image:
   ```bash
   docker build -t mcp-testing .
   ```

3. Run the container:
   ```bash
   docker run -it --rm mcp-testing --help
   ```

This containerized approach is particularly useful for CI/CD environments or when testing across multiple systems.

## Basic Configuration

After installation, you'll need to configure the mcp-client-cli to work with your specific environment and testing needs.

### Configuration File Location

The mcp-client-cli uses a configuration file to store settings and preferences. By default, this file is located at:

- **Linux/macOS**: `~/.llm/config.json`
- **Windows**: `%USERPROFILE%\.llm\config.json`

If the directory doesn't exist, you'll need to create it:

```bash
# Linux/macOS
mkdir -p ~/.llm

# Windows (Command Prompt)
mkdir %USERPROFILE%\.llm
```

### Creating a Basic Configuration

As detailed in the [CONFIG.md](https://github.com/tosin2013/mcp-client-cli/blob/master/CONFIG.md) documentation, the configuration file uses JSON format and supports various settings. A minimal configuration might look like:

```json
{
  "systemPrompt": "You are an AI assistant helping with MCP server testing.",
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "api_key": "your-api-key",
    "temperature": 0.7
  },
  "mcpServers": {
    "your-server": {
      "command": "node",
      "args": ["path/to/your/server.js", "--stdio"],
      "env": {
        "DEBUG": "*"
      },
      "enabled": true
    }
  }
}
```

This configuration includes:

1. **System Prompt**: Instructions for the LLM when interacting with MCP servers
2. **LLM Settings**: Configuration for the language model provider
3. **MCP Server Definitions**: Specifications for the servers you want to test

You can create this file manually or use the tool's interactive configuration feature (if available in your version).

### Configuration Sections Explained

Let's examine each section of the configuration file in more detail:

#### LLM Configuration

The `llm` section configures the language model that will be used for testing:

```json
"llm": {
  "provider": "openai",
  "model": "gpt-4o-mini",
  "api_key": "your-api-key",
  "temperature": 0.7
}
```

Key parameters include:

- **provider**: The LLM service provider (e.g., "openai", "anthropic", "local")
- **model**: The specific model to use
- **api_key**: Your authentication key for the provider
- **temperature**: Controls randomness in model outputs (0.0-1.0)

You'll need to obtain an API key from your chosen provider. For OpenAI, you can get a key from the [OpenAI platform](https://platform.openai.com/), while Anthropic keys are available from the [Anthropic console](https://console.anthropic.com/).

#### MCP Server Configuration

The `mcpServers` section defines the servers you want to test:

```json
"mcpServers": {
  "your-server": {
    "command": "node",
    "args": ["path/to/your/server.js", "--stdio"],
    "env": {
      "DEBUG": "*"
    },
    "enabled": true
  }
}
```

Each server entry includes:

- **command**: The executable to run (e.g., "node", "python")
- **args**: Command-line arguments for the server
- **env**: Environment variables to set
- **enabled**: Whether this server should be included in testing

You can define multiple servers in this section, allowing you to test different implementations or configurations simultaneously.

#### Advanced Configuration Options

For more complex testing scenarios, the configuration file supports additional options:

```json
{
  "testing": {
    "parallel": true,
    "timeout": 30,
    "retries": 3,
    "reportFormat": "html"
  },
  "security": {
    "enableAdvancedTests": true,
    "maliciousPayloads": ["sql_injection", "xss"]
  },
  "performance": {
    "concurrentConnections": 10,
    "duration": 60,
    "monitorResources": true
  }
}
```

These advanced options allow you to customize the testing process to match your specific requirements and constraints.

## Environment Setup

Beyond the basic configuration file, you may need to set up additional environment components for effective MCP server testing.

### API Keys and Authentication

Many MCP servers interact with external services that require authentication. To test these servers properly, you'll need to configure the appropriate API keys and credentials.

For security reasons, it's recommended to use environment variables for sensitive information rather than hardcoding them in configuration files. The mcp-client-cli supports reading environment variables through the configuration:

```json
"mcpServers": {
  "github-server": {
    "command": "node",
    "args": ["github-mcp-server.js"],
    "env": {
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

In this example, the `${GITHUB_TOKEN}` syntax tells the tool to use the value of the `GITHUB_TOKEN` environment variable.

### Setting Up Test Data

Some MCP server tests require specific data or resources. The mcp-client-cli documentation recommends creating a dedicated directory for test data:

```bash
mkdir -p ~/mcp-test-data
```

You can then reference this location in your tests or configuration files.

### Network Configuration

If your MCP servers communicate with external services, you may need to configure network settings such as proxies or firewall rules. The specific requirements will depend on your environment and the servers you're testing.

For corporate environments with proxies, you can configure the tool to use them through environment variables:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### Git Configuration (for Repository-Based Testing)

When testing MCP servers that interact with Git repositories, you'll need proper Git configuration:

```bash
# Configure Git user information
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set up SSH keys if needed
ssh-keygen -t ed25519 -C "your.email@example.com"
```

For GitHub integration, you may also need to configure a personal access token as described in the [GitHub documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

## Verifying Installation

After completing the installation and configuration steps, it's important to verify that everything is working correctly before proceeding with actual testing.

### Basic Verification Commands

The mcp-client-cli provides several commands for verifying your installation:

```bash
# Check the installed version
mcp-test --version

# List available tools
mcp-test --list-tools

# Display help information
mcp-test --help
```

These commands should run without errors and provide the expected output. If you encounter any issues, check the troubleshooting section later in this book.

### Testing a Simple MCP Server

To verify that the tool can properly interact with MCP servers, you can test with a simple example server:

```bash
# Run a basic test against the example server
mcp-test --test-server examples/generic_mcp_server.py
```

This command should start the example server, run basic tests, and report the results. A successful output indicates that your installation is working correctly.

### Validating Configuration

To ensure your configuration file is correctly formatted and contains all required information:

```bash
# Validate configuration
mcp-test --validate-config
```

This command checks your configuration file for syntax errors and missing required fields, helping you identify and fix issues before they affect your testing.

## Troubleshooting Common Installation Issues

Despite careful installation, you might encounter some common issues. Here are solutions to frequently reported problems:

### Python Version Conflicts

**Issue**: Error messages about incompatible Python versions.

**Solution**: Verify your Python version and upgrade if necessary:

```bash
python --version
# If below 3.9, upgrade Python or use a version manager like pyenv
```

### Dependency Conflicts

**Issue**: Errors about conflicting dependencies or missing packages.

**Solution**: Use a virtual environment and reinstall:

```bash
python -m venv fresh-env
source fresh-env/bin/activate
pip install mcp-testing-framework
```

### Permission Issues

**Issue**: Permission denied errors during installation or execution.

**Solution**: For Linux/macOS, you may need to use sudo or fix permissions:

```bash
# Option 1: Use sudo (not recommended for pip)
sudo pip install mcp-testing-framework

# Option 2: Fix permissions (preferred)
mkdir -p ~/.local/bin
pip install --user mcp-testing-framework
export PATH="$HOME/.local/bin:$PATH"
```

### Configuration File Not Found

**Issue**: Errors about missing configuration files.

**Solution**: Create the configuration directory and file:

```bash
mkdir -p ~/.llm
touch ~/.llm/config.json
# Edit the file with your preferred text editor
```

### API Key Issues

**Issue**: Authentication failures with LLM providers.

**Solution**: Verify your API keys and provider settings:

```bash
# Test API key validity (for OpenAI)
curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Next Steps

With the mcp-client-cli successfully installed and configured, you're now ready to begin testing MCP servers. The following chapters will guide you through:

1. Basic usage and commands for everyday testing
2. Fundamental testing principles and workflows
3. Advanced testing capabilities for comprehensive validation
4. Integration with CI/CD systems for automated testing
5. Troubleshooting and best practices for effective testing

By following these steps, you'll be well-equipped to validate your MCP server implementations and ensure they meet the protocol's requirements for functionality, security, and performance.

Remember that the mcp-client-cli is actively developed, so it's a good practice to periodically check for updates:

```bash
pip install --upgrade mcp-testing-framework
```

This ensures you have access to the latest features, bug fixes, and security improvements as the tool and the MCP ecosystem continue to evolve.
