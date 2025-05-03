"""
Advanced Model Interface for Model Context Protocol (MCP)
This module provides a sophisticated interface for interacting with AI models,
with support for research-focused prompting and response formatting.
"""

import os
import json
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchModelInterface:
    def __init__(self, model_name=None):
        """Initialize the model interface with a specified model."""
        # Get model name from environment or use default
        self.model_name = model_name or os.getenv("DEFAULT_MODEL", "llama3-8b-8192")
        
        # Initialize Groq client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = groq.Client(api_key=api_key)
        
        # Load prompt templates
        self.templates = {
            "research": (
                "You are an AI research assistant helping with {topic}. "
                "Provide detailed, accurate information and cite sources when possible. "
                "If you reference research papers or studies, provide proper citations. "
                "Be thorough and analytical in your responses."
            ),
            "paper_analysis": (
                "Analyze the following research paper:\n\n"
                "Title: {title}\n"
                "Authors: {authors}\n"
                "Abstract: {abstract}\n\n"
                "Provide a summary of the key findings, methodology, and implications. "
                "Evaluate the strengths and limitations of the research."
            ),
            "literature_review": (
                "Based on the research papers and findings in our conversation, "
                "provide a comprehensive literature review on {topic}. "
                "Synthesize the key findings, identify patterns and contradictions, "
                "and highlight gaps in the current research."
            ),
            "default": (
                "You are an AI research assistant using Model Context Protocol to maintain conversation context. "
                "You help users explore research topics, analyze papers, and synthesize information. "
                "Be helpful, accurate, and scientifically rigorous."
            )
        }
    
    def generate_response(self, context, mode="default", parameters=None):
        """Generate a response based on the provided context and mode."""
        if parameters is None:
            parameters = {}
        
        if not context or len(context) == 0:
            return "Hello! I'm your AI research assistant. How can I help with your research today?"
        
        # Format the conversation history for the API
        messages = []
        
        # Add a system message based on the mode
        system_content = self._get_system_prompt(mode, parameters)
        system_message = {
            "role": "system", 
            "content": system_content
        }
        messages.append(system_message)
        
        # Add the conversation history
        for message in context:
            # Skip messages with metadata that indicates they should be excluded
            if message.get("metadata", {}).get("exclude_from_context", False):
                continue
                
            messages.append({
                "role": message["role"],
                "content": message["content"]
            })
        
        try:
            # Call the Groq API with appropriate parameters
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=800,
                temperature=self._get_temperature(mode),
                top_p=0.9,
            )
            
            # Extract the response text
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return f"I'm sorry, I encountered an error while processing your request. Technical details: {str(e)}"
    
    def process_input(self, user_input, context_manager, session_id, mode="default", parameters=None):
        """Process user input using the context manager and generate a response."""
        if parameters is None:
            parameters = {}
            
        # Add the user input to the context
        context_manager.add_to_context(session_id, user_input, role="user")
        
        # Detect if this is a research request
        if self._is_research_request(user_input):
            mode = "research"
            parameters["topic"] = self._extract_topic(user_input)
        
        # Get the formatted context
        formatted_context = context_manager.get_formatted_context(session_id)
        
        # Generate a response
        response = self.generate_response(formatted_context, mode, parameters)
        
        # Add the response to the context
        context_manager.add_to_context(session_id, response, role="assistant")
        
        # Extract potential citations from the response
        self._extract_citations(response, context_manager, session_id)
        
        return response
    
    def analyze_paper(self, context_manager, session_id, title, authors, abstract):
        """Analyze a research paper and add the analysis to the context."""
        # Format the paper analysis request
        parameters = {
            "title": title,
            "authors": ", ".join(authors) if isinstance(authors, list) else authors,
            "abstract": abstract
        }
        
        # Get the formatted context
        formatted_context = context_manager.get_formatted_context(session_id)
        
        # Generate an analysis
        analysis = self.generate_response(formatted_context, mode="paper_analysis", parameters=parameters)
        
        # Add the analysis to the context
        context_manager.add_to_context(
            session_id, 
            f"Analysis of paper '{title}':\n\n{analysis}", 
            role="assistant"
        )
        
        # Add the paper to the research context
        context_manager.add_research_paper(
            session_id,
            title,
            authors if isinstance(authors, list) else [authors],
            abstract,
            relevance=1.0
        )
        
        return analysis
    
    def generate_literature_review(self, context_manager, session_id, topic):
        """Generate a literature review based on the research in the context."""
        # Get the formatted context
        formatted_context = context_manager.get_formatted_context(session_id, include_research=True)
        
        # Generate a literature review
        parameters = {"topic": topic}
        review = self.generate_response(formatted_context, mode="literature_review", parameters=parameters)
        
        # Add the review to the context
        context_manager.add_to_context(
            session_id, 
            f"Literature review on {topic}:\n\n{review}", 
            role="assistant"
        )
        
        return review
    
    def _get_system_prompt(self, mode, parameters):
        """Get the appropriate system prompt based on the mode and parameters."""
        template = self.templates.get(mode, self.templates["default"])
        return template.format(**parameters)
    
    def _get_temperature(self, mode):
        """Get the appropriate temperature based on the mode."""
        # Different modes may benefit from different temperature settings
        temperatures = {
            "research": 0.3,  # More factual and precise
            "paper_analysis": 0.2,  # Very factual and analytical
            "literature_review": 0.4,  # Balanced for synthesis
            "default": 0.5    # Balanced
        }
        return temperatures.get(mode, 0.5)
    
    def _is_research_request(self, text):
        """Detect if the input is a research request."""
        research_keywords = [
            "research", "find information", "look up", "search for",
            "tell me about", "what is", "how does", "explain",
            "analyze", "investigate", "study", "examine"
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in research_keywords)
    
    def _extract_topic(self, text):
        """Extract the main topic from a research request."""
        # In a real implementation, this would use NLP
        # For now, we'll use a simple approach
        text_lower = text.lower()
        
        # Remove research keywords
        research_keywords = [
            "research", "find information about", "look up", "search for",
            "tell me about", "what is", "how does", "explain",
            "analyze", "investigate", "study", "examine"
        ]
        for keyword in research_keywords:
            text_lower = text_lower.replace(keyword, "")
        
        # Clean up and return
        return text_lower.strip().capitalize()
    
    def _extract_citations(self, text, context_manager, session_id):
        """Extract potential citations from the response."""
        # In a real implementation, this would use NLP
        # For now, we'll use a simple approach to detect citation patterns
        
        # Look for patterns like (Author, Year) or (Author et al., Year)
        # This is a very simplified approach
        lines = text.split('\n')
        for line in lines:
            if '(' in line and ')' in line and any(year in line for year in [str(y) for y in range(1900, 2025)]):
                # This is a potential citation
                citation_text = line.strip()
                # Extract a source name (very simplified)
                source = "Unknown Source"
                if ":" in line:
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        source = parts[0].strip()
                
                # Add to context
                context_manager.add_citation(session_id, citation_text, source)
