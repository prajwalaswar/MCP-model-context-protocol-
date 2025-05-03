"""
Advanced Context Manager for Model Context Protocol (MCP)
This module provides sophisticated context management with topic tracking,
context summarization, and research integration.
"""

import json
import os
import time
from datetime import datetime
import yaml
import numpy as np

class ResearchContextManager:
    def __init__(self, max_context_length=30, storage_path="data/contexts"):
        """Initialize the advanced context manager."""
        self.max_context_length = max_context_length
        self.contexts = {}  # In-memory context storage
        self.storage_path = storage_path
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
    
    def create_context(self, session_id, metadata=None):
        """Create a new context with optional metadata."""
        if metadata is None:
            metadata = {}
        
        now = datetime.now().isoformat()
        
        if session_id not in self.contexts:
            self.contexts[session_id] = {
                "messages": [],
                "metadata": {
                    "created_at": now,
                    "last_updated": now,
                    "topics": [],
                    "summary": "",
                    "user_preferences": {},
                    **metadata
                },
                "research": {
                    "papers": [],
                    "findings": [],
                    "citations": []
                }
            }
        
        return self.contexts[session_id]
    
    def add_to_context(self, session_id, message, role="user", metadata=None):
        """Add a message to the context with optional metadata."""
        if metadata is None:
            metadata = {}
        
        if session_id not in self.contexts:
            self.create_context(session_id)
        
        # Update the context with the new message
        now = datetime.now().isoformat()
        self.contexts[session_id]["messages"].append({
            "role": role,
            "content": message,
            "timestamp": now,
            "metadata": metadata
        })
        
        # Update the last_updated timestamp
        self.contexts[session_id]["metadata"]["last_updated"] = now
        
        # Detect and update topics if this is a user message
        if role == "user":
            self._update_topics(session_id, message)
        
        # Trim context if it exceeds max length
        self._trim_context(session_id)
        
        # Save context to disk
        self._save_context(session_id)
    
    def add_research_paper(self, session_id, title, authors, abstract, url=None, year=None, relevance=1.0):
        """Add a research paper to the context."""
        if session_id not in self.contexts:
            self.create_context(session_id)
        
        now = datetime.now().isoformat()
        
        # Add the research paper
        paper = {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "url": url,
            "year": year,
            "timestamp": now,
            "relevance": relevance
        }
        
        self.contexts[session_id]["research"]["papers"].append(paper)
        
        # Update the last_updated timestamp
        self.contexts[session_id]["metadata"]["last_updated"] = now
        
        # Save context to disk
        self._save_context(session_id)
        
        return paper
    
    def add_research_finding(self, session_id, content, source=None, relevance=1.0):
        """Add a research finding to the context."""
        if session_id not in self.contexts:
            self.create_context(session_id)
        
        now = datetime.now().isoformat()
        
        # Add the research finding
        finding = {
            "content": content,
            "source": source,
            "timestamp": now,
            "relevance": relevance
        }
        
        self.contexts[session_id]["research"]["findings"].append(finding)
        
        # Update the last_updated timestamp
        self.contexts[session_id]["metadata"]["last_updated"] = now
        
        # Save context to disk
        self._save_context(session_id)
        
        return finding
    
    def add_citation(self, session_id, text, source, authors=None, year=None):
        """Add a citation to the context."""
        if session_id not in self.contexts:
            self.create_context(session_id)
        
        now = datetime.now().isoformat()
        
        # Add the citation
        citation = {
            "text": text,
            "source": source,
            "authors": authors,
            "year": year,
            "timestamp": now
        }
        
        self.contexts[session_id]["research"]["citations"].append(citation)
        
        # Update the last_updated timestamp
        self.contexts[session_id]["metadata"]["last_updated"] = now
        
        # Save context to disk
        self._save_context(session_id)
        
        return citation
    
    def get_context(self, session_id):
        """Get the full context for a session."""
        if session_id not in self.contexts:
            # Try to load from disk
            if self._load_context(session_id):
                return self.contexts[session_id]
            return None
        return self.contexts[session_id]
    
    def get_formatted_context(self, session_id, include_research=True, max_research_items=3):
        """Get the context formatted for model input, with optional research items."""
        if session_id not in self.contexts:
            # Try to load from disk
            if not self._load_context(session_id):
                return []
        
        # Format the context as a list of messages
        formatted_context = self.contexts[session_id]["messages"].copy()
        
        # Add relevant research items if requested
        if include_research and self.contexts[session_id]["research"]["findings"]:
            # Sort research findings by relevance
            sorted_findings = sorted(
                self.contexts[session_id]["research"]["findings"],
                key=lambda x: x["relevance"],
                reverse=True
            )[:max_research_items]
            
            # Add research findings as system messages
            for finding in sorted_findings:
                research_msg = {
                    "role": "system",
                    "content": f"Research finding: {finding['content']}",
                    "timestamp": finding["timestamp"]
                }
                formatted_context.append(research_msg)
        
        # Add relevant papers if requested
        if include_research and self.contexts[session_id]["research"]["papers"]:
            # Sort papers by relevance
            sorted_papers = sorted(
                self.contexts[session_id]["research"]["papers"],
                key=lambda x: x["relevance"],
                reverse=True
            )[:max_research_items]
            
            # Add papers as system messages
            for paper in sorted_papers:
                paper_msg = {
                    "role": "system",
                    "content": f"Research paper: {paper['title']}\nAuthors: {', '.join(paper['authors'])}\nAbstract: {paper['abstract']}",
                    "timestamp": paper["timestamp"]
                }
                formatted_context.append(paper_msg)
        
        return formatted_context
    
    def update_user_preferences(self, session_id, preferences):
        """Update user preferences in the context metadata."""
        if session_id not in self.contexts:
            self.create_context(session_id)
        
        # Update preferences
        self.contexts[session_id]["metadata"]["user_preferences"].update(preferences)
        self.contexts[session_id]["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Save context to disk
        self._save_context(session_id)
    
    def get_topics(self, session_id):
        """Get the topics for a session."""
        if session_id not in self.contexts:
            if not self._load_context(session_id):
                return []
        
        return self.contexts[session_id]["metadata"]["topics"]
    
    def add_topic(self, session_id, topic):
        """Add a topic to the context metadata."""
        if session_id not in self.contexts:
            self.create_context(session_id)
        
        if topic not in self.contexts[session_id]["metadata"]["topics"]:
            self.contexts[session_id]["metadata"]["topics"].append(topic)
            self.contexts[session_id]["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Save context to disk
            self._save_context(session_id)
    
    def generate_summary(self, session_id):
        """Generate a summary of the context."""
        if session_id not in self.contexts:
            if not self._load_context(session_id):
                return ""
        
        # In a real implementation, this would use an LLM to generate a summary
        # For now, we'll just use a simple approach
        messages = self.contexts[session_id]["messages"]
        if not messages:
            return ""
        
        # Count topics
        topics = self.contexts[session_id]["metadata"]["topics"]
        topic_str = ", ".join(topics) if topics else "No specific topics"
        
        # Count research items
        papers_count = len(self.contexts[session_id]["research"]["papers"])
        findings_count = len(self.contexts[session_id]["research"]["findings"])
        citations_count = len(self.contexts[session_id]["research"]["citations"])
        
        # Create a simple summary
        user_messages = [m for m in messages if m["role"] == "user"]
        summary = f"Conversation with {len(messages)} messages about {topic_str}. "
        summary += f"User has asked {len(user_messages)} questions. "
        summary += f"Research includes {papers_count} papers, {findings_count} findings, and {citations_count} citations."
        
        # Store the summary
        self.contexts[session_id]["metadata"]["summary"] = summary
        self._save_context(session_id)
        
        return summary
    
    def clear_context(self, session_id):
        """Clear the context for a session."""
        if session_id in self.contexts:
            del self.contexts[session_id]
            
            # Remove from disk if it exists
            context_file = os.path.join(self.storage_path, f"{session_id}.yaml")
            if os.path.exists(context_file):
                os.remove(context_file)
    
    def get_research_papers(self, session_id, max_papers=5):
        """Get research papers for a session."""
        if session_id not in self.contexts:
            if not self._load_context(session_id):
                return []
        
        papers = self.contexts[session_id]["research"]["papers"]
        
        # Sort by relevance and return top N
        return sorted(papers, key=lambda x: x["relevance"], reverse=True)[:max_papers]
    
    def get_research_findings(self, session_id, max_findings=5):
        """Get research findings for a session."""
        if session_id not in self.contexts:
            if not self._load_context(session_id):
                return []
        
        findings = self.contexts[session_id]["research"]["findings"]
        
        # Sort by relevance and return top N
        return sorted(findings, key=lambda x: x["relevance"], reverse=True)[:max_findings]
    
    def get_citations(self, session_id):
        """Get citations for a session."""
        if session_id not in self.contexts:
            if not self._load_context(session_id):
                return []
        
        return self.contexts[session_id]["research"]["citations"]
    
    def _update_topics(self, session_id, message):
        """Update topics based on message content."""
        # In a real implementation, this would use NLP to extract topics
        # For now, we'll use a simple keyword approach
        potential_topics = [
            "research", "science", "technology", "AI", "machine learning",
            "history", "literature", "mathematics", "physics", "chemistry",
            "biology", "medicine", "economics", "politics", "philosophy",
            "computer science", "natural language processing", "deep learning",
            "neural networks", "reinforcement learning", "data science",
            "quantum computing", "blockchain", "cybersecurity", "robotics"
        ]
        
        message_lower = message.lower()
        for topic in potential_topics:
            if topic.lower() in message_lower and topic not in self.contexts[session_id]["metadata"]["topics"]:
                self.contexts[session_id]["metadata"]["topics"].append(topic)
    
    def _trim_context(self, session_id):
        """Trim the context if it exceeds the maximum length."""
        messages = self.contexts[session_id]["messages"]
        if len(messages) > self.max_context_length:
            # Keep the first message (for context) and the most recent messages
            excess = len(messages) - self.max_context_length
            self.contexts[session_id]["messages"] = [messages[0]] + messages[excess+1:]
    
    def _save_context(self, session_id):
        """Save the context to disk."""
        context_file = os.path.join(self.storage_path, f"{session_id}.yaml")
        with open(context_file, 'w') as f:
            yaml.dump(self.contexts[session_id], f, default_flow_style=False)
    
    def _load_context(self, session_id):
        """Load the context from disk."""
        context_file = os.path.join(self.storage_path, f"{session_id}.yaml")
        if os.path.exists(context_file):
            with open(context_file, 'r') as f:
                self.contexts[session_id] = yaml.safe_load(f)
            return True
        return False
