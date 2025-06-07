import requests

SERVER_URL = "http://localhost:8000"

# --- MCP Client: Connects to the MCP Server to use tools ---

def demo_add():
    resp = requests.get(f"{SERVER_URL}/add", params={"a": 2, "b": 3})
    print("Add (2 + 3):", resp.json())

def demo_greet():
    resp = requests.get(f"{SERVER_URL}/greet", params={"name": "Alice"})
    print("Greet (Alice):", resp.json())

def demo_ask_llm():
    question = "What is the Model Context Protocol?"
    resp = requests.post(f"{SERVER_URL}/ask_llm", json={"question": question})
    print("Ask LLM:", resp.json())

if __name__ == "__main__":
    print("--- MCP Client Demo ---")
    demo_add()
    demo_greet()
    print("(Optional) LLM Tool (requires GROQ_API_KEY on server):")
    demo_ask_llm() 