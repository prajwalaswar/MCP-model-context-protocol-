# Advanced MCP Research Assistant

A sophisticated implementation of Model Context Protocol (MCP) for an AI-powered research assistant.

## Features

- **Advanced Context Management**: Maintains conversation history with topic tracking, research integration, and context summarization
- **Research Paper Integration**: Search for, analyze, and manage research papers
- **Citation Management**: Automatically extracts and manages citations
- **Literature Review Generation**: Creates comprehensive literature reviews based on research context
- **Topic Detection**: Automatically detects and tracks conversation topics
- **Groq API Integration**: Uses Llama 3 for high-quality responses
- **Modern UI**: Clean, responsive interface with multiple views

## What is MCP?

Model Context Protocol (MCP) is a framework for managing and structuring context in AI model interactions. It provides:

- Structured context management
- Session-based conversation tracking
- Topic detection and tracking
- Context persistence and retrieval
- Enhanced AI responses through context awareness

## Project Structure

```
mcp_advanced/
├── api/                    # API endpoints
│   ├── __init__.py
│   └── endpoints.py        # REST API implementation
├── core/                   # Core MCP components
│   ├── __init__.py
│   ├── context_manager.py  # Advanced context management
│   ├── model_interface.py  # Interface for AI models
│   └── research_utils.py   # Research utilities
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       ├── app.js          # Main application JavaScript
│       ├── research.js     # Research page JavaScript
│       └── papers.js       # Papers page JavaScript
├── templates/              # HTML templates
│   ├── index.html          # Main chat interface
│   ├── research.html       # Research interface
│   └── papers.html         # Papers management interface
├── data/                   # Data storage
│   └── contexts/           # Context storage
├── app.py                  # Main application
├── .env                    # Environment variables
└── requirements.txt        # Project dependencies
```

## Key MCP Components

### Research Context Manager

The `ResearchContextManager` class in `core/context_manager.py` implements sophisticated context management:

- Maintains conversation history with metadata
- Tracks topics automatically
- Stores research papers, findings, and citations
- Manages user preferences
- Provides context summarization
- Implements context persistence with YAML storage

### Research Model Interface

The `ResearchModelInterface` class in `core/model_interface.py` provides an interface to AI models:

- Formats context for model consumption
- Supports different interaction modes (research, paper analysis, literature review)
- Implements prompt engineering with templates
- Processes responses and extracts citations
- Analyzes research papers

### API Endpoints

The API endpoints in `api/endpoints.py` expose the MCP functionality:

- Chat endpoint for conversation
- Context management endpoints
- Research paper search and analysis
- Literature review generation
- Citation management

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   GROQ_API_KEY=your_api_key
   DEFAULT_MODEL=llama3-8b-8192
   MAX_CONTEXT_LENGTH=30
   DEBUG=True
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Future Enhancements

- Database integration for persistent storage
- User authentication and multi-user support
- Advanced NLP for better topic detection and citation extraction
- Integration with academic APIs like Semantic Scholar or Google Scholar
- Collaborative research features
