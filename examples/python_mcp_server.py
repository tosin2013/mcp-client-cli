#!/usr/bin/env python3
"""
Example Python MCP Server for testing multi-language capabilities.

This is a simple MCP server implementation that demonstrates
how the Dagger testing infrastructure can test Python-based MCP servers.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List

from mcp import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)


class PythonMCPServer:
    """Simple Python MCP Server for testing purposes."""
    
    def __init__(self):
        self.server = Server("python-test-server")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup MCP server handlers."""
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="python://test/resource1",
                    name="Test Resource 1",
                    description="A test resource from Python MCP server",
                    mimeType="text/plain"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read a specific resource."""
            if uri == "python://test/resource1":
                return "This is test content from Python MCP server"
            else:
                raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="python_echo",
                    description="Echo back the input message with Python prefix",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message to echo back"
                            }
                        },
                        "required": ["message"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            if name == "python_echo":
                message = arguments.get("message", "")
                response = f"[Python MCP Server] Echo: {message}"
                return [TextContent(type="text", text=response)]
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="python-test-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )


async def main():
    """Main entry point."""
    server = PythonMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main()) 