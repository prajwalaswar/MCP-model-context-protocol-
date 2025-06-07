# Basic MCP Example Project

This project demonstrates the core concepts of the Model Context Protocol (MCP) in a simple, easy-to-understand way. It includes:
- An MCP server that exposes simple tools (functions)
- A client that interacts with the server
- (Optional) Integration with a language model (LLM) using Groq API

## What is MCP?
MCP (Model Context Protocol) is a standard for exposing tools and resources from an AI server so that clients (like apps or other agents) can use them easily and consistently.

## Project Structure
```
basic_mcp_example/
├── server.py         # MCP server with tools
├── client.py         # Example client that uses the tools
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## How to Run
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start the server:
   ```
   python server.py
   ```
3. In another terminal, run the client:
   ```
   python client.py
   ```

## Tools Exposed by the Server
- `add(a, b)`: Adds two numbers
- `greet(name)`: Returns a personalized greeting
- (Optional) `ask_llm(question)`: Uses Groq LLM to answer a question (requires API key)

## Key MCP Concepts Demonstrated
- **Server**: Hosts tools/resources
- **Host**: The environment (your computer)
- **Client**: Connects to the server to use tools

---
