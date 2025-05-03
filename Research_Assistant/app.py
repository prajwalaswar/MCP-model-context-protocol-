"""
MCP Research Assistant - Main Application
This is an advanced implementation of Model Context Protocol (MCP) for a research assistant.
"""

from flask import Flask, render_template, session, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API endpoints
from api.endpoints import api, generate_session_id

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    """Render the main page."""
    # Ensure the user has a session ID
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    
    return render_template('index.html')

@app.route('/research')
def research_page():
    """Render the research page."""
    # Ensure the user has a session ID
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    
    return render_template('research.html')

@app.route('/papers')
def papers_page():
    """Render the papers page."""
    # Ensure the user has a session ID
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    
    return render_template('papers.html')

@app.route('/session-id', methods=['GET'])
def get_session_id():
    """Get the current session ID."""
    if 'session_id' not in session:
        session['session_id'] = generate_session_id()
    
    return jsonify({'session_id': session['session_id']})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data/contexts', exist_ok=True)
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    print(f"Starting MCP Research Assistant on port {port}...")
    print(f"Open http://127.0.0.1:{port} in your browser")
    app.run(host='0.0.0.0', port=port, debug=debug)
