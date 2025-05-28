#!/usr/bin/env node
/**
 * Example Node.js MCP Server
 * 
 * This is a comprehensive example of a Node.js MCP server that demonstrates
 * all the features that can be tested by the universal MCP testing framework.
 * 
 * Features demonstrated:
 * - MCP protocol compliance
 * - Tool implementations
 * - Resource management
 * - Prompt handling
 * - Error handling
 * - Security features
 * - Performance optimization
 * - Health checks
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');
const http = require('http');

class NodejsMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'nodejs-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
          resources: {},
          prompts: {},
        },
      }
    );

    this.setupHandlers();
    this.setupHealthCheck();
  }

  setupHandlers() {
    // Tool handlers
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'calculate',
          description: 'Perform basic mathematical calculations',
          inputSchema: {
            type: 'object',
            properties: {
              expression: {
                type: 'string',
                description: 'Mathematical expression to evaluate',
              },
            },
            required: ['expression'],
          },
        },
        {
          name: 'file_operations',
          description: 'Perform file system operations',
          inputSchema: {
            type: 'object',
            properties: {
              operation: {
                type: 'string',
                enum: ['read', 'write', 'list', 'delete'],
                description: 'File operation to perform',
              },
              path: {
                type: 'string',
                description: 'File or directory path',
              },
              content: {
                type: 'string',
                description: 'Content to write (for write operation)',
              },
            },
            required: ['operation', 'path'],
          },
        },
        {
          name: 'hash_generator',
          description: 'Generate cryptographic hashes',
          inputSchema: {
            type: 'object',
            properties: {
              algorithm: {
                type: 'string',
                enum: ['md5', 'sha1', 'sha256', 'sha512'],
                description: 'Hash algorithm to use',
              },
              input: {
                type: 'string',
                description: 'Input string to hash',
              },
            },
            required: ['algorithm', 'input'],
          },
        },
        {
          name: 'system_info',
          description: 'Get system information',
          inputSchema: {
            type: 'object',
            properties: {
              info_type: {
                type: 'string',
                enum: ['platform', 'memory', 'cpu', 'uptime'],
                description: 'Type of system information to retrieve',
              },
            },
            required: ['info_type'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'calculate':
            return await this.handleCalculate(args);
          case 'file_operations':
            return await this.handleFileOperations(args);
          case 'hash_generator':
            return await this.handleHashGenerator(args);
          case 'system_info':
            return await this.handleSystemInfo(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error executing tool ${name}: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });

    // Resource handlers
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => ({
      resources: [
        {
          uri: 'file://config.json',
          name: 'Server Configuration',
          description: 'Current server configuration',
          mimeType: 'application/json',
        },
        {
          uri: 'file://logs/server.log',
          name: 'Server Logs',
          description: 'Current server logs',
          mimeType: 'text/plain',
        },
        {
          uri: 'memory://stats',
          name: 'Runtime Statistics',
          description: 'Current runtime statistics',
          mimeType: 'application/json',
        },
      ],
    }));

    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;

      try {
        switch (uri) {
          case 'file://config.json':
            return {
              contents: [
                {
                  uri,
                  mimeType: 'application/json',
                  text: JSON.stringify({
                    server: 'nodejs-mcp-server',
                    version: '1.0.0',
                    environment: process.env.NODE_ENV || 'development',
                    port: process.env.PORT || 3000,
                  }, null, 2),
                },
              ],
            };

          case 'file://logs/server.log':
            return {
              contents: [
                {
                  uri,
                  mimeType: 'text/plain',
                  text: `[${new Date().toISOString()}] Server started\n[${new Date().toISOString()}] Resource accessed: ${uri}`,
                },
              ],
            };

          case 'memory://stats':
            const memUsage = process.memoryUsage();
            return {
              contents: [
                {
                  uri,
                  mimeType: 'application/json',
                  text: JSON.stringify({
                    memory: memUsage,
                    uptime: process.uptime(),
                    pid: process.pid,
                    platform: process.platform,
                    nodeVersion: process.version,
                  }, null, 2),
                },
              ],
            };

          default:
            throw new Error(`Unknown resource: ${uri}`);
        }
      } catch (error) {
        throw new Error(`Error reading resource ${uri}: ${error.message}`);
      }
    });

    // Prompt handlers
    this.server.setRequestHandler(ListPromptsRequestSchema, async () => ({
      prompts: [
        {
          name: 'code_review',
          description: 'Generate a code review prompt',
          arguments: [
            {
              name: 'language',
              description: 'Programming language',
              required: true,
            },
            {
              name: 'complexity',
              description: 'Code complexity level',
              required: false,
            },
          ],
        },
        {
          name: 'documentation',
          description: 'Generate documentation prompt',
          arguments: [
            {
              name: 'type',
              description: 'Documentation type (API, user, developer)',
              required: true,
            },
            {
              name: 'format',
              description: 'Output format (markdown, html, plain)',
              required: false,
            },
          ],
        },
      ],
    }));

    this.server.setRequestHandler(GetPromptRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'code_review':
          const language = args?.language || 'javascript';
          const complexity = args?.complexity || 'medium';
          return {
            description: `Code review prompt for ${language}`,
            messages: [
              {
                role: 'user',
                content: {
                  type: 'text',
                  text: `Please review this ${language} code with ${complexity} complexity. Focus on:\n- Code quality and best practices\n- Security vulnerabilities\n- Performance optimizations\n- Maintainability\n- Documentation`,
                },
              },
            ],
          };

        case 'documentation':
          const type = args?.type || 'API';
          const format = args?.format || 'markdown';
          return {
            description: `Documentation prompt for ${type}`,
            messages: [
              {
                role: 'user',
                content: {
                  type: 'text',
                  text: `Generate comprehensive ${type} documentation in ${format} format. Include:\n- Overview and purpose\n- Installation instructions\n- Usage examples\n- API reference (if applicable)\n- Troubleshooting guide`,
                },
              },
            ],
          };

        default:
          throw new Error(`Unknown prompt: ${name}`);
      }
    });
  }

  async handleCalculate(args) {
    const { expression } = args;
    
    // Basic security: only allow safe mathematical expressions
    if (!/^[0-9+\-*/().\s]+$/.test(expression)) {
      throw new Error('Invalid expression: only numbers and basic operators allowed');
    }

    try {
      // Use Function constructor for safe evaluation (in real apps, use a proper math parser)
      const result = Function(`"use strict"; return (${expression})`)();
      
      return {
        content: [
          {
            type: 'text',
            text: `Result: ${expression} = ${result}`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Calculation error: ${error.message}`);
    }
  }

  async handleFileOperations(args) {
    const { operation, path: filePath, content } = args;

    // Security: restrict to safe directories
    const safePath = path.resolve('./sandbox', filePath);
    if (!safePath.startsWith(path.resolve('./sandbox'))) {
      throw new Error('Access denied: path outside sandbox');
    }

    try {
      switch (operation) {
        case 'read':
          const readContent = await fs.readFile(safePath, 'utf8');
          return {
            content: [
              {
                type: 'text',
                text: `File content:\n${readContent}`,
              },
            ],
          };

        case 'write':
          if (!content) {
            throw new Error('Content required for write operation');
          }
          await fs.mkdir(path.dirname(safePath), { recursive: true });
          await fs.writeFile(safePath, content, 'utf8');
          return {
            content: [
              {
                type: 'text',
                text: `File written successfully: ${filePath}`,
              },
            ],
          };

        case 'list':
          const entries = await fs.readdir(safePath);
          return {
            content: [
              {
                type: 'text',
                text: `Directory contents:\n${entries.join('\n')}`,
              },
            ],
          };

        case 'delete':
          await fs.unlink(safePath);
          return {
            content: [
              {
                type: 'text',
                text: `File deleted successfully: ${filePath}`,
              },
            ],
          };

        default:
          throw new Error(`Unknown operation: ${operation}`);
      }
    } catch (error) {
      throw new Error(`File operation failed: ${error.message}`);
    }
  }

  async handleHashGenerator(args) {
    const { algorithm, input } = args;

    try {
      const hash = crypto.createHash(algorithm).update(input).digest('hex');
      
      return {
        content: [
          {
            type: 'text',
            text: `${algorithm.toUpperCase()} hash: ${hash}`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Hash generation failed: ${error.message}`);
    }
  }

  async handleSystemInfo(args) {
    const { info_type } = args;

    try {
      let info;
      
      switch (info_type) {
        case 'platform':
          info = {
            platform: process.platform,
            arch: process.arch,
            nodeVersion: process.version,
          };
          break;

        case 'memory':
          info = process.memoryUsage();
          break;

        case 'cpu':
          info = {
            cpuUsage: process.cpuUsage(),
            loadAverage: require('os').loadavg(),
          };
          break;

        case 'uptime':
          info = {
            processUptime: process.uptime(),
            systemUptime: require('os').uptime(),
          };
          break;

        default:
          throw new Error(`Unknown info type: ${info_type}`);
      }

      return {
        content: [
          {
            type: 'text',
            text: `System ${info_type}:\n${JSON.stringify(info, null, 2)}`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`System info retrieval failed: ${error.message}`);
    }
  }

  setupHealthCheck() {
    // Create a simple HTTP health check endpoint
    const port = process.env.PORT || 3000;
    
    const server = http.createServer((req, res) => {
      if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          status: 'healthy',
          timestamp: new Date().toISOString(),
          uptime: process.uptime(),
          memory: process.memoryUsage(),
        }));
      } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
      }
    });

    server.listen(port, () => {
      console.error(`Health check server listening on port ${port}`);
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Node.js MCP Server running on stdio');
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.error('Received SIGINT, shutting down gracefully');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.error('Received SIGTERM, shutting down gracefully');
  process.exit(0);
});

// Start the server
if (require.main === module) {
  const server = new NodejsMCPServer();
  server.run().catch((error) => {
    console.error('Server error:', error);
    process.exit(1);
  });
}

module.exports = NodejsMCPServer; 