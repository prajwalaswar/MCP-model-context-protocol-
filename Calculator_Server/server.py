#!/usr/bin/env python3
"""
Calculator MCP Server
A Model Context Protocol server that provides mathematical calculation capabilities.

This server implements:
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced mathematical functions (power, square root, factorial)
- Expression evaluation with proper error handling
- Mathematical constants (pi, e)
"""

import asyncio
import json
import math
import re
import sys
from typing import Any, Dict, List

from mcp.server import Server
from mcp.types import Tool, TextContent

# Create MCP server
server = Server("calculator")

# Mathematical constants
CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}

def safe_eval(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.
    Only allows basic math operations and functions.
    """
    # Remove whitespace
    expression = expression.replace(" ", "")
    
    # Replace constants
    for const, value in CONSTANTS.items():
        expression = expression.replace(const, str(value))
    
    # Allowed characters and functions
    allowed_chars = set("0123456789+-*/().^")
    allowed_functions = ["sin", "cos", "tan", "log", "sqrt", "abs", "pow"]
    
    # Check for dangerous patterns
    dangerous_patterns = [
        "__", "import", "exec", "eval", "open", "file", "input", "raw_input"
    ]
    
    for pattern in dangerous_patterns:
        if pattern in expression.lower():
            raise ValueError(f"Dangerous pattern detected: {pattern}")
    
    # Replace ^ with ** for Python power operator
    expression = expression.replace("^", "**")
    
    # Add math. prefix to allowed functions
    for func in allowed_functions:
        expression = re.sub(f"\\b{func}\\(", f"math.{func}(", expression)
    
    try:
        # Create a safe namespace with only math functions
        safe_dict = {
            "__builtins__": {},
            "math": math,
        }
        
        result = eval(expression, safe_dict)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available calculator tools."""
    return [
        Tool(
            name="calculate",
            description="Evaluate a mathematical expression safely",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4', 'sin(pi/2)', 'sqrt(16)')"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="subtract",
            description="Subtract two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number (minuend)"},
                    "b": {"type": "number", "description": "Second number (subtrahend)"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="divide",
            description="Divide two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Dividend"},
                    "b": {"type": "number", "description": "Divisor"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="power",
            description="Raise a number to a power",
            inputSchema={
                "type": "object",
                "properties": {
                    "base": {"type": "number", "description": "The base number"},
                    "exponent": {"type": "number", "description": "The exponent"}
                },
                "required": ["base", "exponent"]
            }
        ),
        Tool(
            name="square_root",
            description="Calculate the square root of a number",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {"type": "number", "description": "The number to find the square root of"}
                },
                "required": ["number"]
            }
        ),
        Tool(
            name="factorial",
            description="Calculate the factorial of a number",
            inputSchema={
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "description": "The number to calculate factorial for (must be non-negative integer)"}
                },
                "required": ["n"]
            }
        ),
        Tool(
            name="trigonometry",
            description="Calculate trigonometric functions",
            inputSchema={
                "type": "object",
                "properties": {
                    "function": {"type": "string", "description": "The trigonometric function (sin, cos, tan)"},
                    "angle": {"type": "number", "description": "The angle value"},
                    "unit": {"type": "string", "description": "The unit of the angle ('radians' or 'degrees')", "default": "radians"}
                },
                "required": ["function", "angle"]
            }
        ),
        Tool(
            name="get_constants",
            description="Get mathematical constants available in the calculator",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""

    if name == "calculate":
        return await calculate(arguments["expression"])
    elif name == "add":
        return await add(arguments["a"], arguments["b"])
    elif name == "subtract":
        return await subtract(arguments["a"], arguments["b"])
    elif name == "multiply":
        return await multiply(arguments["a"], arguments["b"])
    elif name == "divide":
        return await divide(arguments["a"], arguments["b"])
    elif name == "power":
        return await power(arguments["base"], arguments["exponent"])
    elif name == "square_root":
        return await square_root(arguments["number"])
    elif name == "factorial":
        return await factorial(arguments["n"])
    elif name == "trigonometry":
        unit = arguments.get("unit", "radians")
        return await trigonometry(arguments["function"], arguments["angle"], unit)
    elif name == "get_constants":
        return await get_constants()
    else:
        raise ValueError(f"Unknown tool: {name}")

async def calculate(expression: str) -> list[TextContent]:
    """
    Evaluate a mathematical expression safely.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4", "sin(pi/2)", "sqrt(16)")

    Returns:
        The result of the calculation as a string
    """
    try:
        result = safe_eval(expression)
        return [TextContent(type="text", text=f"{expression} = {result}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error calculating '{expression}': {str(e)}")]

async def add(a: float, b: float) -> list[TextContent]:
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    result = a + b
    return [TextContent(type="text", text=f"{a} + {b} = {result}")]

async def subtract(a: float, b: float) -> list[TextContent]:
    """
    Subtract two numbers.

    Args:
        a: First number (minuend)
        b: Second number (subtrahend)

    Returns:
        The difference of a and b
    """
    result = a - b
    return [TextContent(type="text", text=f"{a} - {b} = {result}")]

async def multiply(a: float, b: float) -> list[TextContent]:
    """
    Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The product of a and b
    """
    result = a * b
    return [TextContent(type="text", text=f"{a} × {b} = {result}")]

async def divide(a: float, b: float) -> list[TextContent]:
    """
    Divide two numbers.

    Args:
        a: Dividend
        b: Divisor

    Returns:
        The quotient of a and b
    """
    if b == 0:
        return [TextContent(type="text", text="Error: Division by zero is not allowed")]

    result = a / b
    return [TextContent(type="text", text=f"{a} ÷ {b} = {result}")]

async def power(base: float, exponent: float) -> list[TextContent]:
    """
    Raise a number to a power.

    Args:
        base: The base number
        exponent: The exponent

    Returns:
        The result of base raised to the power of exponent
    """
    try:
        result = base ** exponent
        return [TextContent(type="text", text=f"{base}^{exponent} = {result}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error calculating {base}^{exponent}: {str(e)}")]

async def square_root(number: float) -> list[TextContent]:
    """
    Calculate the square root of a number.

    Args:
        number: The number to find the square root of

    Returns:
        The square root of the number
    """
    if number < 0:
        return [TextContent(type="text", text="Error: Cannot calculate square root of negative number")]

    result = math.sqrt(number)
    return [TextContent(type="text", text=f"√{number} = {result}")]

async def factorial(n: int) -> list[TextContent]:
    """
    Calculate the factorial of a number.

    Args:
        n: The number to calculate factorial for (must be non-negative integer)

    Returns:
        The factorial of n
    """
    if n < 0:
        return [TextContent(type="text", text="Error: Factorial is not defined for negative numbers")]

    if n > 170:  # Prevent overflow
        return [TextContent(type="text", text="Error: Number too large for factorial calculation")]

    try:
        result = math.factorial(n)
        return [TextContent(type="text", text=f"{n}! = {result}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error calculating {n}!: {str(e)}")]

async def trigonometry(function: str, angle: float, unit: str = "radians") -> list[TextContent]:
    """
    Calculate trigonometric functions.

    Args:
        function: The trigonometric function (sin, cos, tan)
        angle: The angle value
        unit: The unit of the angle ("radians" or "degrees")

    Returns:
        The result of the trigonometric function
    """
    # Convert degrees to radians if needed
    if unit.lower() == "degrees":
        angle_rad = math.radians(angle)
    else:
        angle_rad = angle

    try:
        if function.lower() == "sin":
            result = math.sin(angle_rad)
        elif function.lower() == "cos":
            result = math.cos(angle_rad)
        elif function.lower() == "tan":
            result = math.tan(angle_rad)
        else:
            return [TextContent(type="text", text=f"Error: Unknown trigonometric function '{function}'")]

        return [TextContent(type="text", text=f"{function}({angle} {unit}) = {result}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error calculating {function}({angle}): {str(e)}")]

async def get_constants() -> list[TextContent]:
    """
    Get mathematical constants available in the calculator.

    Returns:
        A list of available mathematical constants
    """
    constants_info = []
    for name, value in CONSTANTS.items():
        constants_info.append(f"{name} = {value}")

    return [TextContent(type="text", text="Available constants:\n" + "\n".join(constants_info))]

async def main():
    """Main function to run the MCP server."""
    from mcp.server.stdio import stdio_server

    print("Starting Calculator MCP Server...")
    print("Available tools:")
    print("- calculate: Evaluate mathematical expressions")
    print("- add, subtract, multiply, divide: Basic arithmetic")
    print("- power, square_root, factorial: Advanced operations")
    print("- trigonometry: Sin, cos, tan functions")
    print("- get_constants: Available mathematical constants")
    print("\nServer running via stdio transport")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
