# MCP AI Configuration - Quick Reference

## 🚀 One-Command Setup

```bash
llm --ai-configure setup-testing --repo-url https://github.com/user/my-mcp-server
```

## 🔧 Common Commands

### Basic Configuration
```bash
# Full setup (recommended)
llm --ai-configure setup-testing --repo-url <url>

# Preview before applying
llm --ai-configure setup-testing --repo-url <url> --config-preview

# CI/CD pipeline only
llm --ai-configure add-ci --repo-url <url>

# Security testing focus
llm --ai-configure enable-security --repo-url <url>
```

### Authentication Options
```bash
# SSH (default)
llm --ai-configure setup-testing --repo-url <url> --auth-method ssh

# GitHub Token
llm --ai-configure setup-testing --repo-url <url> --auth-method token

# Interactive
llm --ai-configure setup-testing --repo-url <url> --auth-method interactive
```

### Batch Operations
```bash
# Multiple repositories
llm --ai-configure batch-setup --repo-list repositories.txt

# Merge with existing
llm --ai-configure add-ci --repo-url <url> --merge-existing
```

## 🤖 AI Assistant Prompts

### Cursor/Claude
```
Configure MCP testing for https://github.com/user/my-mcp-server

Use the MCP Client CLI AI configuration system to set up comprehensive testing.
```

### GitHub Copilot
```
@terminal Set up MCP testing for my repository using the AI configuration system
```

### Claude (Standalone)
```
I need to configure MCP testing for my repository at https://github.com/user/my-server. 
Please use the MCP Client CLI AI configuration system.
```

## 📋 What Gets Created

### Python Servers
- `.github/workflows/mcp-testing.yml`
- `test-config.json`
- `TESTING.md`
- `requirements-test.txt` (if needed)

### Node.js Servers
- `.github/workflows/mcp-testing.yml`
- `test-config.json`
- `TESTING.md`
- Updated `package.json` scripts

## 🔍 Troubleshooting

### Authentication Issues
```bash
# Check SSH
ssh -T git@github.com

# Verify token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### Debug Mode
```bash
llm --ai-configure setup-testing --repo-url <url> --verbose --debug
```

### Validation
```bash
llm --validate-config --config-file test-config.json
llm --validate-workflow --workflow-file .github/workflows/mcp-testing.yml
```

## ⚙️ Environment Setup

### Prerequisites
```bash
# Install
pip install mcp-client-cli

# SSH setup
ssh-add ~/.ssh/id_rsa

# Token setup
export GITHUB_TOKEN="your_token_here"

# Verify
llm --version
```

## 📊 Migration from Legacy

### Automatic Migration
```bash
llm --migrate-from-reverse-integration --repo-url <url>
```

### Manual Cleanup
```bash
# Remove old files
rm -rf .github/workflows/pytest-mcp-server-self-test.yml
rm -rf scripts/test-pytest-mcp-server.py
rm -rf test-pytest-mcp-server.json

# Apply new config
llm --ai-configure setup-testing --repo-url <current-repo>
```

## 🆘 Help Commands

```bash
llm --ai-configure --help
llm --ai-configure setup-testing --help
```

## 🔗 Links

- [Full Documentation](./AI_CONFIGURATION_GUIDE.md)
- [Technical Architecture](./TECHNICAL_ARCHITECTURE.md)
- [MCP Client CLI](https://github.com/user/mcp-client-cli)

---

**💡 Pro Tip**: Use `--config-preview` to see what will be configured before applying changes! 