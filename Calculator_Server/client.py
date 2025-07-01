#!/usr/bin/env python3
"""
Calculator MCP Client
A simple client to test the Calculator MCP Server.
"""

import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

async def test_calculator_stdio():
    """Test the calculator MCP server via stdio transport."""

    # Server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["server.py", "--transport", "stdio"],
        env=None
    )

    print("🧮 Testing Calculator MCP Server (stdio)...")
    print("=" * 50)

    try:
        # Connect to the server
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the session
                await session.initialize()
                await run_tests(session)

    except Exception as e:
        print(f"❌ Failed to connect via stdio: {e}")
        return False
    return True

async def test_calculator_sse():
    """Test the calculator MCP server via SSE transport."""

    print("🧮 Testing Calculator MCP Server (SSE)...")
    print("=" * 50)

    try:
        # Connect to the SSE server
        async with sse_client("http://localhost:8001/sse") as session:
            # Initialize the session
            await session.initialize()
            await run_tests(session)

    except Exception as e:
        print(f"❌ Failed to connect via SSE: {e}")
        return False
    return True

async def run_tests(session):
    """Run the test cases on the given session."""
    # List available tools
    tools = await session.list_tools()
    print(f"📋 Available tools: {len(tools.tools)}")
    for tool in tools.tools:
        print(f"  • {tool.name}: {tool.description}")
    print()

    # Test cases
    test_cases = [
        # Basic arithmetic
        ("add", {"a": 5, "b": 3}),
        ("subtract", {"a": 10, "b": 4}),
        ("multiply", {"a": 6, "b": 7}),
        ("divide", {"a": 15, "b": 3}),

        # Advanced operations
        ("power", {"base": 2, "exponent": 8}),
        ("square_root", {"number": 64}),
        ("factorial", {"n": 5}),

        # Trigonometry
        ("trigonometry", {"function": "sin", "angle": 90, "unit": "degrees"}),
        ("trigonometry", {"function": "cos", "angle": 0, "unit": "radians"}),

        # Expression evaluation
        ("calculate", {"expression": "2 + 3 * 4"}),
        ("calculate", {"expression": "sqrt(16) + pow(2, 3)"}),
        ("calculate", {"expression": "sin(pi/2)"}),

        # Constants
        ("get_constants", {}),

        # Error cases
        ("divide", {"a": 10, "b": 0}),
        ("square_root", {"number": -4}),
        ("factorial", {"n": -1}),
    ]

    # Execute test cases
    for i, (tool_name, arguments) in enumerate(test_cases, 1):
        print(f"🧪 Test {i}: {tool_name}({arguments})")
        try:
            result = await session.call_tool(tool_name, arguments)
            print(f"✅ Result: {result.content[0].text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()

    print("🎉 Calculator MCP Server testing completed!")

async def main():
    """Main function to test both transport methods."""

    # Try SSE first (since server is running on SSE)
    print("Attempting to connect to running SSE server...")
    sse_success = await test_calculator_sse()

    if not sse_success:
        print("\nSSE connection failed. Trying stdio transport...")
        stdio_success = await test_calculator_stdio()

        if not stdio_success:
            print("\n❌ Both connection methods failed!")
            print("Make sure the server is running with: python server.py")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
