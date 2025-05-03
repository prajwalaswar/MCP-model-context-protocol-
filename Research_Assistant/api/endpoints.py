"""
API Endpoints for the MCP Research Assistant
This module provides the API endpoints for interacting with the research assistant.
"""

from flask import Blueprint, request, jsonify, session
import json
import os

from core.context_manager import ResearchContextManager
from core.model_interface import ResearchModelInterface
from core.research_utils import search_papers, extract_key_findings, generate_citation

# Create Blueprint
api = Blueprint('api', __name__)

# Initialize the context manager and model interface
context_manager = ResearchContextManager(
    max_context_length=int(os.getenv("MAX_CONTEXT_LENGTH", 30))
)
model_interface = ResearchModelInterface()

# Helper function to generate a session ID
def generate_session_id():
    """Generate a unique session ID."""
    import uuid
    return str(uuid.uuid4())

@api.route('/chat', methods=['POST'])
def chat():
    """Handle chat API requests."""
    data = request.json
    user_input = data.get('message', '')
    mode = data.get('mode', 'default')
    parameters = data.get('parameters', {})
    
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    session_id = session['session_id']
    
    # Process the input and get a response
    response = model_interface.process_input(
        user_input, 
        context_manager, 
        session_id,
        mode=mode,
        parameters=parameters
    )
    
    return jsonify({
        'response': response,
        'session_id': session_id
    })

@api.route('/context', methods=['GET'])
def get_context():
    """Get the current context for the session."""
    if 'session_id' not in session:
        return jsonify({'error': 'No session ID'}), 400
    
    session_id = session['session_id']
    context = context_manager.get_context(session_id)
    if not context:
        return jsonify({'error': 'No context found for this session'}), 404
    
    return jsonify(context)

@api.route('/clear-context', methods=['POST'])
def clear_context():
    """Clear the context for the session."""
    if 'session_id' not in session:
        return jsonify({'error': 'No session ID'}), 400
    
    session_id = session['session_id']
    context_manager.clear_context(session_id)
    return jsonify({'status': 'success', 'message': 'Context cleared'})

@api.route('/summary', methods=['GET'])
def get_summary():
    """Generate and return a summary of the current context."""
    if 'session_id' not in session:
        return jsonify({'error': 'No session ID'}), 400
    
    session_id = session['session_id']
    summary = context_manager.generate_summary(session_id)
    return jsonify({'summary': summary})

@api.route('/topics', methods=['GET'])
def get_topics():
    """Get the topics for the current session."""
    if 'session_id' not in session:
        return jsonify({'error': 'No session ID'}), 400
    
    session_id = session['session_id']
    topics = context_manager.get_topics(session_id)
    return jsonify({'topics': topics})

@api.route('/search-papers', methods=['POST'])
def search_research_papers():
    """Search for research papers on a topic."""
    data = request.json
    query = data.get('query', '')
    max_results = data.get('max_results', 3)
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Search for papers
    papers = search_papers(query, max_results=max_results)
    
    # Get session ID
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    session_id = session['session_id']
    
    # Add papers to context
    for paper in papers:
        context_manager.add_research_paper(
            session_id,
            paper['title'],
            paper['authors'],
            paper['abstract'],
            url=paper.get('url'),
            year=paper.get('year'),
            relevance=paper.get('relevance', 1.0)
        )
        
        # Add a finding from the paper
        finding = extract_key_findings(paper['abstract'])
        context_manager.add_research_finding(
            session_id,
            finding,
            source=paper['title'],
            relevance=paper.get('relevance', 1.0)
        )
    
    # Add topic to context
    context_manager.add_topic(session_id, query)
    
    return jsonify({
        'status': 'success',
        'message': f'Found {len(papers)} papers on {query}',
        'papers': papers
    })

@api.route('/analyze-paper', methods=['POST'])
def analyze_paper():
    """Analyze a research paper and add it to the context."""
    data = request.json
    title = data.get('title', '')
    authors = data.get('authors', [])
    abstract = data.get('abstract', '')
    
    if not title or not abstract:
        return jsonify({'error': 'Title and abstract are required'}), 400
    
    # Get session ID
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    session_id = session['session_id']
    
    # Analyze the paper
    analysis = model_interface.analyze_paper(
        context_manager,
        session_id,
        title,
        authors,
        abstract
    )
    
    return jsonify({
        'status': 'success',
        'message': f'Paper "{title}" analyzed',
        'analysis': analysis
    })

@api.route('/literature-review', methods=['POST'])
def generate_literature_review():
    """Generate a literature review based on the research in the context."""
    data = request.json
    topic = data.get('topic', '')
    
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
    
    # Get session ID
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    session_id = session['session_id']
    
    # Generate a literature review
    review = model_interface.generate_literature_review(
        context_manager,
        session_id,
        topic
    )
    
    return jsonify({
        'status': 'success',
        'message': f'Literature review on {topic} generated',
        'review': review
    })

@api.route('/research-papers', methods=['GET'])
def get_research_papers():
    """Get research papers for the current session."""
    if 'session_id' not in session:
        return jsonify({'error': 'No session ID'}), 400
    
    session_id = session['session_id']
    papers = context_manager.get_research_papers(session_id)
    return jsonify({'papers': papers})

@api.route('/research-findings', methods=['GET'])
def get_research_findings():
    """Get research findings for the current session."""
    if 'session_id' not in session:
        return jsonify({'error': 'No session ID'}), 400
    
    session_id = session['session_id']
    findings = context_manager.get_research_findings(session_id)
    return jsonify({'findings': findings})

@api.route('/citations', methods=['GET'])
def get_citations():
    """Get citations for the current session."""
    if 'session_id' not in session:
        return jsonify({'error': 'No session ID'}), 400
    
    session_id = session['session_id']
    citations = context_manager.get_citations(session_id)
    return jsonify({'citations': citations})
