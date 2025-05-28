# MCP CLI client

A simple CLI program to run LLM prompt and implement [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) client.

You can use any [MCP-compatible servers](https://github.com/punkpeye/awesome-mcp-servers) from the convenience of your terminal.

This act as alternative client beside Claude Desktop. Additionally you can use any LLM provider like OpenAI, Groq, or local LLM model via [llama](https://github.com/ggerganov/llama.cpp).

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

This project includes a comprehensive testing framework for MCP servers, built with methodological pragmatism principles and powered by Dagger.io pipelines.

### Quick Start

1. **Install testing dependencies:**
   ```bash
   pip install -e ".[testing]"
   ```

2. **Run basic tests:**
   ```bash
   # Test a specific MCP server
   llm test-server --config examples/test-config-basic.json

   # Run comprehensive test suite
   llm test-suite --config examples/test-config-advanced.json

   # Run security tests
   llm test-security --server my-server --config examples/test-config-advanced.json
   ```

3. **Use Dagger.io pipelines:**
   ```bash
   # Run full test suite with Dagger
   dagger call run-full-test-suite --config-path examples/test-config-advanced.json

   # Run performance tests
   dagger call run-performance-tests --server-name my-server
   ```

### Testing Capabilities

- **Functional Testing**: Validate MCP server functionality, tool execution, and resource access
- **Security Testing**: Authentication, authorization, input validation, and vulnerability scanning
- **Performance Testing**: Load testing, response time measurement, and resource monitoring
- **Integration Testing**: Multi-environment testing with cross-language support
- **Automated Issue Detection**: Real-time monitoring with self-healing capabilities

### Configuration

Create test configurations using the provided examples:

- `examples/test-config-basic.json`: Basic testing setup
- `examples/test-config-advanced.json`: Comprehensive testing with security and performance

### Documentation

- **[TESTING.md](TESTING.md)**: Complete testing framework documentation
- **[examples/CLI_USAGE_GUIDE.md](examples/CLI_USAGE_GUIDE.md)**: CLI testing commands and usage
- **[examples/API_REFERENCE.md](examples/API_REFERENCE.md)**: Testing API reference
- **[examples/TESTING_EXAMPLES.md](examples/TESTING_EXAMPLES.md)**: Practical testing examples
- **[examples/BEST_PRACTICES.md](examples/BEST_PRACTICES.md)**: Testing best practices and guidelines
- **[examples/TROUBLESHOOTING.md](examples/TROUBLESHOOTING.md)**: Common issues and solutions

### Key Features

- **Confidence Scoring**: All test results include confidence scores (0-100%) for reliability assessment
- **Methodological Pragmatism**: Systematic verification with explicit fallibilism
- **Error Architecture Awareness**: Distinguishes between human-cognitive and artificial-stochastic errors
- **Multi-Language Support**: Test both Python and Node.js MCP servers
- **Container Isolation**: Dagger.io provides clean, reproducible test environments
- **Automated Remediation**: Self-healing capabilities for common issues

### Example Usage

```bash
# Basic server validation
llm test-server --server my-server --tests functional,security

# Performance benchmarking
llm test-performance --server my-server --concurrent-connections 10

# Issue detection and remediation
llm detect-issues --server my-server --auto-remediate

# Generate test reports
llm test-report --format html --output test-results.html
```

For detailed usage instructions, see the [CLI Usage Guide](examples/CLI_USAGE_GUIDE.md).

## Contributing

Feel free to submit issues and pull requests for improvements or bug fixes.
