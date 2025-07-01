# Calculator MCP Server 🧮

A **Model Context Protocol (MCP) server** that provides comprehensive mathematical calculation capabilities for AI assistants. This intermediate-level implementation demonstrates proper MCP protocol usage with multiple tools, error handling, and security considerations.

## 🌟 Features

### 🔢 Basic Arithmetic
- **Addition**: Add two numbers
- **Subtraction**: Subtract two numbers  
- **Multiplication**: Multiply two numbers
- **Division**: Divide two numbers (with zero-division protection)

### 🧮 Advanced Operations
- **Power**: Raise numbers to any power
- **Square Root**: Calculate square roots (with negative number protection)
- **Factorial**: Calculate factorials (with overflow protection)

### 📐 Trigonometry
- **Sin, Cos, Tan**: Support for both radians and degrees
- **Angle conversion**: Automatic degree-to-radian conversion

### 🔍 Expression Evaluation
- **Safe Expression Parser**: Evaluate complex mathematical expressions
- **Security**: Protected against code injection
- **Constants**: Built-in mathematical constants (π, e, τ)

### 🛡️ Safety Features
- Input validation and sanitization
- Protection against dangerous code execution
- Proper error handling and user-friendly messages
- Overflow protection for large calculations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd Calculator_Server
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python server.py
```

The server will start on `http://0.0.0.0:8001` with SSE transport.

### 3. Test with Client
```bash
python client.py
```

## 🛠️ Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `calculate` | Evaluate mathematical expressions | `"2 + 3 * 4"` → `14` |
| `add` | Add two numbers | `add(5, 3)` → `8` |
| `subtract` | Subtract two numbers | `subtract(10, 4)` → `6` |
| `multiply` | Multiply two numbers | `multiply(6, 7)` → `42` |
| `divide` | Divide two numbers | `divide(15, 3)` → `5` |
| `power` | Raise to power | `power(2, 8)` → `256` |
| `square_root` | Calculate square root | `square_root(64)` → `8` |
| `factorial` | Calculate factorial | `factorial(5)` → `120` |
| `trigonometry` | Trig functions | `sin(90°)` → `1` |
| `get_constants` | List available constants | `π, e, τ` |

## 📝 Usage Examples

### Basic Calculations
```python
# Simple arithmetic
add(10, 5)          # "10 + 5 = 15"
multiply(7, 8)      # "7 × 8 = 56"
divide(20, 4)       # "20 ÷ 4 = 5"

# Advanced operations
power(2, 10)        # "2^10 = 1024"
square_root(144)    # "√144 = 12"
factorial(6)        # "6! = 720"
```

### Expression Evaluation
```python
# Complex expressions
calculate("2 + 3 * 4")              # "2 + 3 * 4 = 14"
calculate("sqrt(16) + pow(2, 3)")   # "sqrt(16) + pow(2, 3) = 12"
calculate("sin(pi/2)")              # "sin(pi/2) = 1"
calculate("2^3 + sqrt(9)")          # "2^3 + sqrt(9) = 11"
```

### Trigonometry
```python
# Degrees and radians
trigonometry("sin", 90, "degrees")   # "sin(90 degrees) = 1"
trigonometry("cos", 0, "radians")    # "cos(0 radians) = 1"
trigonometry("tan", 45, "degrees")   # "tan(45 degrees) = 1"
```

## 🔧 Integration with MCP Clients

### Claude Desktop Configuration
Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["path/to/Calculator_Server/server.py"],
      "env": {}
    }
  }
}
```

### Cursor IDE Configuration
Add to your Cursor MCP config:
```json
{
  "calculator-server": {
    "command": "python",
    "args": ["server.py"],
    "cwd": "path/to/Calculator_Server"
  }
}
```

## 🛡️ Security Features

- **Safe Expression Evaluation**: Only allows mathematical operations
- **Input Sanitization**: Removes dangerous patterns and functions
- **Error Boundaries**: Graceful error handling with informative messages
- **Overflow Protection**: Prevents calculations that could cause system issues

## 🎯 Why This is Intermediate Level

1. **Multiple Tool Types**: Implements 9 different calculation tools
2. **Complex Logic**: Safe expression parsing with security considerations
3. **Error Handling**: Comprehensive error management for edge cases
4. **Type Safety**: Proper type hints and validation
5. **Real-world Utility**: Actually useful for AI assistants
6. **MCP Best Practices**: Follows official MCP protocol standards

## 🔄 Transport Protocols

- **SSE (Server-Sent Events)**: Default transport for web integration
- **Stdio**: Available for command-line integration

## 📊 Example Output

```
🧮 Testing Calculator MCP Server...
==================================================
📋 Available tools: 9
  • calculate: Evaluate a mathematical expression safely
  • add: Add two numbers
  • subtract: Subtract two numbers
  • multiply: Multiply two numbers
  • divide: Divide two numbers
  • power: Raise a number to a power
  • square_root: Calculate the square root of a number
  • factorial: Calculate the factorial of a number
  • trigonometry: Calculate trigonometric functions

🧪 Test 1: add({'a': 5, 'b': 3})
✅ Result: 5 + 3 = 8

🧪 Test 2: calculate({'expression': 'sin(pi/2)'})
✅ Result: sin(pi/2) = 1.0

🎉 Calculator MCP Server testing completed!
```

## 🤝 Contributing

This calculator server demonstrates intermediate MCP development concepts. Feel free to extend it with:
- More mathematical functions (logarithms, hyperbolic functions)
- Unit conversions
- Statistical calculations
- Matrix operations

---

**Built with ❤️ using the Model Context Protocol**
