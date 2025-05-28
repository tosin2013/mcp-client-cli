#!/usr/bin/env python3
"""
Generic Python MCP Server Example

This is a template/example for creating a Python-based MCP server that can be tested
with the comprehensive MCP testing framework.

This example demonstrates:
- Basic MCP server structure
- Tool implementation
- Resource handling
- Error handling
- Testing integration
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional, Sequence

from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenericMCPServer:
    """Generic MCP Server implementation."""
    
    def __init__(self):
        self.server = Server("generic-mcp-server")
        self.data_store = {}
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="echo",
                    description="Echo back the provided text",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to echo back"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                Tool(
                    name="calculate",
                    description="Perform basic mathematical calculations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate (e.g., '2 + 2')"
                            }
                        },
                        "required": ["expression"]
                    }
                ),
                Tool(
                    name="store_data",
                    description="Store data with a key",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Key to store data under"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value to store"
                            }
                        },
                        "required": ["key", "value"]
                    }
                ),
                Tool(
                    name="get_data",
                    description="Retrieve stored data by key",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Key to retrieve data for"
                            }
                        },
                        "required": ["key"]
                    }
                ),
                Tool(
                    name="list_keys",
                    description="List all stored data keys",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool execution."""
            try:
                if name == "echo":
                    text = arguments.get("text", "")
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Echo: {text}")]
                    )
                
                elif name == "calculate":
                    expression = arguments.get("expression", "")
                    # Simple evaluation (in production, use a safer approach)
                    try:
                        # Only allow basic math operations for safety
                        allowed_chars = set("0123456789+-*/.() ")
                        if all(c in allowed_chars for c in expression):
                            result = eval(expression)
                            return CallToolResult(
                                content=[TextContent(type="text", text=f"Result: {result}")]
                            )
                        else:
                            return CallToolResult(
                                content=[TextContent(type="text", text="Error: Invalid characters in expression")]
                            )
                    except Exception as e:
                        return CallToolResult(
                            content=[TextContent(type="text", text=f"Calculation error: {str(e)}")]
                        )
                
                elif name == "store_data":
                    key = arguments.get("key")
                    value = arguments.get("value")
                    self.data_store[key] = value
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Stored '{value}' under key '{key}'")]
                    )
                
                elif name == "get_data":
                    key = arguments.get("key")
                    if key in self.data_store:
                        value = self.data_store[key]
                        return CallToolResult(
                            content=[TextContent(type="text", text=f"Value for '{key}': {value}")]
                        )
                    else:
                        return CallToolResult(
                            content=[TextContent(type="text", text=f"No data found for key '{key}'")]
                        )
                
                elif name == "list_keys":
                    keys = list(self.data_store.keys())
                    if keys:
                        return CallToolResult(
                            content=[TextContent(type="text", text=f"Stored keys: {', '.join(keys)}")]
                        )
                    else:
                        return CallToolResult(
                            content=[TextContent(type="text", text="No data stored")]
                        )
                
                else:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                        isError=True
                    )
            
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Tool execution error: {str(e)}")],
                    isError=True
                )
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="memory://data",
                    name="Data Store",
                    description="Current data store contents",
                    mimeType="application/json"
                ),
                Resource(
                    uri="memory://stats",
                    name="Server Statistics",
                    description="Server runtime statistics",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Read resource content."""
            try:
                if uri == "memory://data":
                    content = json.dumps(self.data_store, indent=2)
                    return ReadResourceResult(
                        contents=[TextContent(type="text", text=content)]
                    )
                
                elif uri == "memory://stats":
                    stats = {
                        "data_items": len(self.data_store),
                        "server_name": "generic-mcp-server",
                        "status": "running"
                    }
                    content = json.dumps(stats, indent=2)
                    return ReadResourceResult(
                        contents=[TextContent(type="text", text=content)]
                    )
                
                else:
                    return ReadResourceResult(
                        contents=[TextContent(type="text", text=f"Resource not found: {uri}")],
                        isError=True
                    )
            
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return ReadResourceResult(
                    contents=[TextContent(type="text", text=f"Resource read error: {str(e)}")],
                    isError=True
                )

async def main():
    """Main server entry point."""
    # Check if running in test mode
    test_mode = sys.argv[1:] and sys.argv[1] == "--test"
    
    if test_mode:
        logger.info("Starting server in test mode")
    
    # Create and run server
    server_instance = GenericMCPServer()
    
    # Configure server parameters
    server_params = StdioServerParameters(
        server_name="generic-mcp-server",
        server_version="1.0.0"
    )
    
    try:
        # Run the server
        async with server_instance.server.stdio_server() as (read_stream, write_stream):
            await server_instance.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="generic-mcp-server",
                    server_version="1.0.0",
                    capabilities=server_instance.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None
                    )
                )
            )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Generic MCP Server")
            print("Usage:")
            print("  python server.py          # Run normally")
            print("  python server.py --test   # Run in test mode")
            print("  python server.py --help   # Show this help")
            sys.exit(0)
    
    # Run the server
    asyncio.run(main()) 