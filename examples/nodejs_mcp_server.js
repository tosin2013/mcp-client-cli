#!/usr/bin/env node
/**
 * Example Node.js MCP Server for testing multi-language capabilities.
 * 
 * This is a simple MCP server implementation that demonstrates
 * how the Dagger testing infrastructure can test Node.js-based MCP servers.
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');

class NodeJSMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'nodejs-test-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );
    
    this.setupHandlers();
  }

  setupHandlers() {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: 'nodejs://test/resource1',
            name: 'Test Resource 1',
            description: 'A test resource from Node.js MCP server',
            mimeType: 'text/plain',
          },
        ],
      };
    });

    // Read a specific resource
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      
      if (uri === 'nodejs://test/resource1') {
        return {
          contents: [
            {
              uri,
              mimeType: 'text/plain',
              text: 'This is test content from Node.js MCP server',
            },
          ],
        };
      } else {
        throw new Error(`Unknown resource: ${uri}`);
      }
    });

    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'nodejs_echo',
            description: 'Echo back the input message with Node.js prefix',
            inputSchema: {
              type: 'object',
              properties: {
                message: {
                  type: 'string',
                  description: 'Message to echo back',
                },
              },
              required: ['message'],
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      if (name === 'nodejs_echo') {
        const message = args.message || '';
        const response = `[Node.js MCP Server] Echo: ${message}`;
        
        return {
          content: [
            {
              type: 'text',
              text: response,
            },
          ],
        };
      } else {
        throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    
    // Keep the server running
    console.error('Node.js MCP Server started');
  }
}

async function main() {
  const server = new NodeJSMCPServer();
  await server.run();
}

if (require.main === module) {
  main().catch((error) => {
    console.error('Server error:', error);
    process.exit(1);
  });
} 