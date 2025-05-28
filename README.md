# MCP CLI client

A simple CLI program to run LLM prompt and implement [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) client, **featuring a universal testing framework for any MCP server repository**.

You can use any [MCP-compatible servers](https://github.com/punkpeye/awesome-mcp-servers) from the convenience of your terminal.

This act as alternative client beside Claude Desktop. Additionally you can use any LLM provider like OpenAI, Groq, or local LLM model via [llama](https://github.com/ggerganov/llama.cpp).

**🧪 Universal MCP Testing**: Includes a comprehensive testing framework that works with any MCP server implementation (Python, Node.js, Go, Rust, etc.) with automated detection, security testing, performance benchmarking, and CI/CD integration.

![C4 Diagram](https://raw.githubusercontent.com/adhikasp/mcp-client-cli/refs/heads/master/c4_diagram.png)

## Setup

1. Install via pip:
   ```bash
   pip install mcp-client-cli
   ```

2. Create a `~/.llm/config.json` file to configure your LLM and MCP servers:
   ```json
   {
     "systemPrompt": "You are an AI assistant helping a software engineer...",
     "llm": {
       "provider": "openai",
       "model": "gpt-4",
       "api_key": "your-openai-api-key",
       "temperature": 0.7,
       "base_url": "https://api.openai.com/v1"  // Optional, for OpenRouter or other providers
     },
     "mcpServers": {
       "fetch": {
         "command": "uvx",
         "args": ["mcp-server-fetch"],
         "requires_confirmation": ["fetch"],
         "enabled": true,  // Optional, defaults to true
         "exclude_tools": []  // Optional, list of tool names to exclude
       },
       "brave-search": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-brave-search"],
         "env": {
           "BRAVE_API_KEY": "your-brave-api-key"
         },
         "requires_confirmation": ["brave_web_search"]
       },
       "youtube": {
         "command": "uvx",
         "args": ["--from", "git+https://github.com/adhikasp/mcp-youtube", "mcp-youtube"]
       }
     }
   }
   ```

   Note:
   - See [CONFIG.md](CONFIG.md) for complete documentation of the configuration format
   - Use `requires_confirmation` to specify which tools need user confirmation before execution
   - The LLM API key can also be set via environment variables `LLM_API_KEY` or `OPENAI_API_KEY`
   - The config file can be placed in either `~/.llm/config.json` or `$PWD/.llm/config.json`
   - You can comment the JSON config file with `//` if you like to switch around the configuration

3. Run the CLI:
   ```bash
   llm "What is the capital city of North Sumatra?"
   ```

## Usage

### Basic Usage

```bash
$ llm What is the capital city of North Sumatra?
The capital city of North Sumatra is Medan.
```

You can omit the quotes, but be careful with bash special characters like `&`, `|`, `;` that might be interpreted by your shell.

You can also pipe input from other commands or files:

```bash
$ echo "What is the capital city of North Sumatra?" | llm
The capital city of North Sumatra is Medan.

$ echo "Given a location, tell me its capital city." > instructions.txt
$ cat instruction.txt | llm "West Java"
The capital city of West Java is Bandung.
```

### Image Input

You can pipe image files to analyze them with multimodal LLMs:

```bash
$ cat image.jpg | llm "What do you see in this image?"
[LLM will analyze and describe the image]

$ cat screenshot.png | llm "Is there any error in this screenshot?"
[LLM will analyze the screenshot and point out any errors]
```

### Using Prompt Templates

You can use predefined prompt templates by using the `p` prefix followed by the template name and its arguments:

```bash
# List available prompt templates
$ llm --list-prompts

# Use a template
$ llm p review  # Review git changes
$ llm p commit  # Generate commit message
$ llm p yt url=https://youtube.com/...  # Summarize YouTube video
```

### Triggering a tool

```bash
$ llm What is the top article on hackernews today?

================================== Ai Message ==================================
Tool Calls:
  brave_web_search (call_eXmFQizLUp8TKBgPtgFo71et)
 Call ID: call_eXmFQizLUp8TKBgPtgFo71et
  Args:
    query: site:news.ycombinator.com
    count: 1
Brave Search MCP Server running on stdio

# If the tool requires confirmation, you'll be prompted:
Confirm tool call? [y/n]: y

================================== Ai Message ==================================
Tool Calls:
  fetch (call_xH32S0QKqMfudgN1ZGV6vH1P)
 Call ID: call_xH32S0QKqMfudgN1ZGV6vH1P
  Args:
    url: https://news.ycombinator.com/
================================= Tool Message =================================
Name: fetch

[TextContent(type='text', text='Contents [REDACTED]]
================================== Ai Message ==================================

The top article on Hacker News today is:

### [Why pipes sometimes get "stuck": buffering](https://jvns.ca)
- **Points:** 31
- **Posted by:** tanelpoder
- **Posted:** 1 hour ago

You can view the full list of articles on [Hacker News](https://news.ycombinator.com/)
```

To bypass tool confirmation requirements, use the `--no-confirmations` flag:

```bash
$ llm --no-confirmations "What is the top article on hackernews today?"
```

To use in bash scripts, add the --no-intermediates, so it doesn't print intermediate messages, only the concluding end message.
```bash
$ llm --no-intermediates "What is the time in Tokyo right now?"
```

### Continuation

Add a `c ` prefix to your message to continue the last conversation.

```bash
$ llm asldkfjasdfkl
It seems like your message might have been a typo or an error. Could you please clarify or provide more details about what you need help with?
$ llm c what did i say previously?
You previously typed "asldkfjasdfkl," which appears to be a random string of characters. If you meant to ask something specific or if you have a question, please let me know!
```

### Clipboard Support

You can use content from your clipboard using the `cb` command:

```bash
# After copying text to clipboard
$ llm cb
[LLM will process the clipboard text]

$ llm cb "What language is this code written in?"
[LLM will analyze the clipboard text with your question]

# After copying an image to clipboard
$ llm cb "What do you see in this image?"
[LLM will analyze the clipboard image]

# You can combine it with continuation
$ llm cb c "Tell me more about what you see"
[LLM will continue the conversation about the clipboard content]
```

The clipboard feature works in:
- Native Windows/macOS/Linux environments
  - Windows: Uses PowerShell
  - macOS: Uses `pbpaste` for text, `pngpaste` for images (optional)
  - Linux: Uses `xclip` (required for clipboard support)
- Windows Subsystem for Linux (WSL)
  - Accesses the Windows clipboard through PowerShell
  - Works with both text and images
  - Make sure you have access to `powershell.exe` from WSL

Required tools for clipboard support:
- Windows: PowerShell (built-in)
- macOS: 
  - `pbpaste` (built-in) for text
  - `pngpaste` (optional) for images: `brew install pngpaste`
- Linux: 
  - `xclip`: `sudo apt install xclip` or equivalent

The CLI automatically detects if the clipboard content is text or image and handles it appropriately.

### Additional Options

```bash
$ llm --list-tools                # List all available tools
$ llm --list-prompts              # List available prompt templates
$ llm --no-tools                  # Run without any tools
$ llm --force-refresh             # Force refresh tool capabilities cache
$ llm --text-only                 # Output raw text without markdown formatting
$ llm --show-memories             # Show user memories
$ llm --model gpt-4               # Override the model specified in config
```

## MCP Testing Framework

This project includes a **universal, comprehensive testing framework** for MCP servers, designed to work with **any MCP server repository** regardless of implementation language or framework. Built with methodological pragmatism principles and powered by Dagger.io pipelines.

### 🌟 Universal Compatibility

The testing framework automatically detects and adapts to:
- **Any MCP server implementation** (Python, Node.js, Go, Rust, etc.)
- **Any repository structure** with intelligent auto-discovery
- **Multiple testing environments** (local, containerized, CI/CD)
- **Various MCP protocol versions** and extensions

### Quick Start

1. **Install testing dependencies:**
   ```bash
   pip install -e ".[testing]"
   ```

2. **One-command testing for any repository:**
   ```bash
   # Auto-detect and test any MCP server repository
   ./scripts/quick-test-local.sh --repo-url https://github.com/your-org/your-mcp-server.git

   # Test current repository
   llm test-server --auto-detect

   # Test with specific configuration
   llm test-server --config examples/test-config-basic.json
   ```

3. **Universal self-testing workflow:**
   ```bash
   # Generate and run tests for any MCP server
   python scripts/pytest-mcp-server-workflow.py --repo-url https://github.com/your-org/your-mcp-server.git
   ```

4. **Use Dagger.io pipelines:**
   ```bash
   # Run full test suite with automatic environment detection
   dagger call run-full-test-suite --auto-detect

   # Multi-language testing
   dagger call multi-language-environment --test-python --test-nodejs
   ```

### Testing Capabilities

- **🔍 Functional Testing**: Validate MCP server functionality, tool execution, and resource access
- **🔒 Security Testing**: Authentication, authorization, input validation, OWASP compliance
- **⚡ Performance Testing**: Load testing, response time measurement, memory leak detection
- **🔗 Integration Testing**: Multi-environment testing with cross-language support
- **🤖 Automated Issue Detection**: Real-time monitoring with self-healing capabilities
- **📊 Confidence Scoring**: All results include reliability scores (0-100%)
- **🌐 Universal Compatibility**: Works with any MCP server implementation

### Configuration

The framework provides intelligent defaults and auto-configuration:

- **Auto-Detection**: Automatically discovers MCP server type and configuration
- **Smart Defaults**: Generates appropriate test configurations based on repository structure
- **Example Configurations**: Pre-built configs for common scenarios
  - `examples/test-config-basic.json`: Basic testing setup
  - `examples/test-config-advanced.json`: Comprehensive testing with security and performance
  - `examples/MCP_SERVER_INTEGRATION.md`: Integration guide for any repository

### Documentation

#### Universal Guides
- **[examples/UNIVERSAL_SELF_TESTING_GUIDE.md](examples/UNIVERSAL_SELF_TESTING_GUIDE.md)**: Complete guide for testing any MCP server repository
- **[examples/MCP_SERVER_SETUP.md](examples/MCP_SERVER_SETUP.md)**: 5-minute setup for any repository
- **[examples/MCP_SERVER_INTEGRATION.md](examples/MCP_SERVER_INTEGRATION.md)**: Integration patterns and examples

#### Framework Documentation
- **[TESTING.md](TESTING.md)**: Complete testing framework documentation
- **[examples/CLI_USAGE_GUIDE.md](examples/CLI_USAGE_GUIDE.md)**: CLI testing commands and usage
- **[examples/API_REFERENCE.md](examples/API_REFERENCE.md)**: Testing API reference
- **[examples/TESTING_EXAMPLES.md](examples/TESTING_EXAMPLES.md)**: Practical testing examples
- **[examples/BEST_PRACTICES.md](examples/BEST_PRACTICES.md)**: Testing best practices and guidelines
- **[examples/TROUBLESHOOTING.md](examples/TROUBLESHOOTING.md)**: Common issues and solutions

#### Advanced Features
- **[MULTI_LANGUAGE_TESTING.md](MULTI_LANGUAGE_TESTING.md)**: Multi-language testing capabilities
- **[REVERSE_INTEGRATION_SUMMARY.md](REVERSE_INTEGRATION_SUMMARY.md)**: Reverse integration workflows
- **[prompts/MCP_SERVER_TESTING_PROMPT.md](prompts/MCP_SERVER_TESTING_PROMPT.md)**: AI-powered test generation

### Key Features

- **🎯 Universal Compatibility**: Test any MCP server repository without modification
- **📈 Confidence Scoring**: All test results include confidence scores (0-100%) for reliability assessment
- **🧠 Methodological Pragmatism**: Systematic verification with explicit fallibilism
- **⚠️ Error Architecture Awareness**: Distinguishes between human-cognitive and artificial-stochastic errors
- **🌍 Multi-Language Support**: Test Python, Node.js, Go, Rust, and other MCP servers
- **🐳 Container Isolation**: Dagger.io provides clean, reproducible test environments
- **🔧 Automated Remediation**: Self-healing capabilities for common issues
- **🔄 CI/CD Integration**: GitHub Actions workflows for automated testing

### Example Usage

```bash
# Test any MCP server repository
llm test-server --repo-url https://github.com/your-org/your-mcp-server.git

# Auto-detect and test current repository
llm test-server --auto-detect --tests functional,security,performance

# Performance benchmarking with auto-scaling
llm test-performance --auto-detect --concurrent-connections 10

# Issue detection with automated remediation
llm detect-issues --auto-detect --auto-remediate

# Generate comprehensive test reports
llm test-report --format html --output test-results.html --include-confidence-scores

# Multi-language integration testing
llm test-integration --python-server ./server.py --nodejs-server ./server.js

# AI-powered test generation
llm generate-tests --repo-url https://github.com/your-org/your-mcp-server.git --ai-enhanced
```

### Universal Repository Integration

The framework can be integrated into **any MCP server repository** with minimal setup:

1. **One-Command Setup**: `./scripts/quick-test-local.sh --setup`
2. **GitHub Actions Integration**: Copy `.github/workflows/test-mcp-server.yml`
3. **Custom Test Generation**: Use AI prompts to generate repository-specific tests
4. **Reverse Integration**: Enable your repository to self-test using this framework

For detailed integration instructions, see the [Universal Self-Testing Guide](examples/UNIVERSAL_SELF_TESTING_GUIDE.md).

### Confidence and Reliability

All testing operations include:
- **Confidence Scores**: 0-100% reliability indicators
- **Error Classification**: Human-cognitive vs. artificial-stochastic error detection
- **Systematic Verification**: Methodological pragmatism principles
- **Fallibilism Awareness**: Explicit acknowledgment of limitations and uncertainties

## Contributing

Feel free to submit issues and pull requests for improvements or bug fixes.
