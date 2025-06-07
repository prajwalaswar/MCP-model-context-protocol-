from fastapi import FastAPI, Query
from pydantic import BaseModel
import os
import groq

app = FastAPI(title="Basic MCP Example Server")

# --- Tool 1: Add two numbers ---
@app.get("/add")
def add(a: int = Query(...), b: int = Query(...)):
    """Add two numbers and return the result."""
    return {"result": a + b}

# --- Tool 2: Greet a user ---
@app.get("/greet")
def greet(name: str = Query(...)):
    """Return a personalized greeting."""
    return {"greeting": f"Hello, {name}! Welcome to MCP."}

# --- Tool 3: Ask LLM (Groq) ---
class LLMRequest(BaseModel):
    question: str

@app.post("/ask_llm")
def ask_llm(req: LLMRequest):
    """Use Groq LLM to answer a question (requires GROQ_API_KEY env variable)."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "GROQ_API_KEY not set in environment."}
    client = groq.Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": req.question}]
    )
    answer = chat_completion.choices[0].message.content
    return {"answer": answer}

# --- MCP Concepts ---
# This server is the "MCP Server" (the power strip analogy)
# It exposes tools (add, greet, ask_llm) as API endpoints
# Clients can connect and use these tools

# To run: uvicorn server:app --reload 