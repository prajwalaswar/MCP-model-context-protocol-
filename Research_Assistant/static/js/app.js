/**
 * MCP Research Assistant - Main JavaScript
 * This file handles the client-side functionality of the MCP Research Assistant.
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const clearContextBtn = document.getElementById('clear-context-btn');
    const viewContextBtn = document.getElementById('view-context-btn');
    const getSummaryBtn = document.getElementById('get-summary-btn');
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const literatureReviewBtn = document.getElementById('literature-review-btn');
    const generateReviewBtn = document.getElementById('generate-review-btn');
    const literatureReviewTopic = document.getElementById('literature-review-topic');
    const typingIndicator = document.getElementById('typing-indicator');
    const topicsList = document.getElementById('topics-list');
    
    // Bootstrap Modals
    const contextModal = new bootstrap.Modal(document.getElementById('contextModal'));
    const summaryModal = new bootstrap.Modal(document.getElementById('summaryModal'));
    const literatureReviewModal = new bootstrap.Modal(document.getElementById('literatureReviewModal'));
    const searchResultsModal = new bootstrap.Modal(document.getElementById('searchResultsModal'));
    
    // Initialize
    init();
    
    /**
     * Initialize the application
     */
    function init() {
        // Add welcome message
        addMessage("Hello! I'm your AI research assistant powered by Model Context Protocol (MCP). I can help you research topics, analyze papers, and generate literature reviews. What would you like to research today?", 'assistant');
        
        // Load topics
        loadTopics();
        
        // Set up event listeners
        setupEventListeners();
    }
    
    /**
     * Set up event listeners
     */
    function setupEventListeners() {
        // Send message on button click
        sendBtn.addEventListener('click', sendMessage);
        
        // Send message on Enter key (but allow Shift+Enter for new lines)
        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Clear context
        clearContextBtn.addEventListener('click', clearContext);
        
        // View context
        viewContextBtn.addEventListener('click', viewContext);
        
        // Get summary
        getSummaryBtn.addEventListener('click', getSummary);
        
        // Search papers
        searchBtn.addEventListener('click', function() {
            searchPapers(searchInput.value);
        });
        
        // Open literature review modal
        literatureReviewBtn.addEventListener('click', function() {
            literatureReviewModal.show();
        });
        
        // Generate literature review
        generateReviewBtn.addEventListener('click', function() {
            generateLiteratureReview(literatureReviewTopic.value);
        });
    }
    
    /**
     * Send a message to the server
     */
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add message to chat
        addMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        typingIndicator.style.display = 'flex';
        
        // Disable input while waiting for response
        userInput.disabled = true;
        sendBtn.disabled = true;
        
        // Send message to server
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                mode: 'default'
            })
        })
        .then(response => response.json())
        .then(data => {
            // Hide typing indicator
            typingIndicator.style.display = 'none';
            
            // Add response to chat
            addMessage(data.response, 'assistant');
            
            // Update topics
            loadTopics();
            
            // Re-enable input
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        })
        .catch(error => {
            console.error('Error sending message:', error);
            typingIndicator.style.display = 'none';
            addMessage('Sorry, there was an error processing your request.', 'assistant');
            
            // Re-enable input
            userInput.disabled = false;
            sendBtn.disabled = false;
        });
    }
    
    /**
     * Add a message to the chat
     */
    function addMessage(content, role) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', role);
        
        // Use marked.js to render markdown
        messageElement.innerHTML = marked.parse(content);
        
        // Add timestamp
        const timeElement = document.createElement('div');
        timeElement.classList.add('message-time');
        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageElement.appendChild(timeElement);
        
        // Add to chat
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    /**
     * Clear the context
     */
    function clearContext() {
        if (confirm('Are you sure you want to clear the conversation context? This cannot be undone.')) {
            fetch('/api/clear-context', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                // Clear chat messages
                chatMessages.innerHTML = '';
                
                // Add welcome message
                addMessage("Context cleared. I've forgotten our previous conversation. How can I help you with your research now?", 'assistant');
                
                // Clear topics
                topicsList.innerHTML = '<div class="placeholder-text">No topics yet</div>';
            })
            .catch(error => {
                console.error('Error clearing context:', error);
                addMessage('Sorry, there was an error clearing the context.', 'assistant');
            });
        }
    }
    
    /**
     * View the current context
     */
    function viewContext() {
        fetch('/api/context')
        .then(response => response.json())
        .then(data => {
            // Display context in modal
            document.getElementById('context-content').textContent = JSON.stringify(data, null, 2);
            contextModal.show();
        })
        .catch(error => {
            console.error('Error fetching context:', error);
            alert('Error fetching context');
        });
    }
    
    /**
     * Get a summary of the conversation
     */
    function getSummary() {
        // Show loading in modal
        document.getElementById('summary-content').innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2">Generating summary...</p></div>';
        summaryModal.show();
        
        fetch('/api/summary')
        .then(response => response.json())
        .then(data => {
            // Display summary in modal
            document.getElementById('summary-content').innerHTML = marked.parse(data.summary);
        })
        .catch(error => {
            console.error('Error fetching summary:', error);
            document.getElementById('summary-content').innerHTML = '<div class="alert alert-danger">Error generating summary</div>';
        });
    }
    
    /**
     * Load topics for the current session
     */
    function loadTopics() {
        fetch('/api/topics')
        .then(response => response.json())
        .then(data => {
            if (data.topics && data.topics.length > 0) {
                // Display topics
                topicsList.innerHTML = '';
                data.topics.forEach(topic => {
                    const topicElement = document.createElement('div');
                    topicElement.classList.add('topic-item');
                    topicElement.textContent = topic;
                    topicsList.appendChild(topicElement);
                });
            } else {
                // No topics
                topicsList.innerHTML = '<div class="placeholder-text">No topics yet</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching topics:', error);
        });
    }
    
    /**
     * Search for research papers
     */
    function searchPapers(query) {
        if (!query.trim()) {
            alert('Please enter a search query');
            return;
        }
        
        // Show loading
        document.getElementById('search-results').innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2">Searching for papers...</p></div>';
        searchResultsModal.show();
        
        fetch('/api/search-papers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                max_results: 5
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display search results
            const searchResults = document.getElementById('search-results');
            
            if (data.papers && data.papers.length > 0) {
                searchResults.innerHTML = `<h5>Found ${data.papers.length} papers on "${query}"</h5>`;
                
                // Add papers to results
                data.papers.forEach(paper => {
                    const paperElement = document.createElement('div');
                    paperElement.classList.add('research-paper');
                    
                    const authors = Array.isArray(paper.authors) ? paper.authors.join(', ') : paper.authors;
                    
                    paperElement.innerHTML = `
                        <h4>${paper.title}</h4>
                        <div class="research-paper-authors">${authors}</div>
                        <div class="research-paper-abstract">${paper.abstract}</div>
                        <div class="research-paper-meta">
                            <span>${paper.year || 'N/A'}</span>
                            <span>Relevance: ${(paper.relevance * 100).toFixed(0)}%</span>
                        </div>
                    `;
                    
                    searchResults.appendChild(paperElement);
                });
                
                // Add message to chat
                addMessage(`I found ${data.papers.length} papers on "${query}". The papers have been added to your research context.`, 'assistant');
                
                // Update topics
                loadTopics();
            } else {
                searchResults.innerHTML = `<div class="alert alert-info">No papers found for "${query}"</div>`;
            }
        })
        .catch(error => {
            console.error('Error searching papers:', error);
            document.getElementById('search-results').innerHTML = '<div class="alert alert-danger">Error searching for papers</div>';
        });
    }
    
    /**
     * Generate a literature review
     */
    function generateLiteratureReview(topic) {
        if (!topic.trim()) {
            alert('Please enter a topic for the literature review');
            return;
        }
        
        // Show loading
        document.getElementById('literature-review-content').innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2">Generating literature review...</p></div>';
        
        fetch('/api/literature-review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                topic: topic
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display literature review
            document.getElementById('literature-review-content').innerHTML = marked.parse(data.review);
            
            // Add message to chat
            addMessage(`I've generated a literature review on "${topic}". You can view it in the Literature Review tab.`, 'assistant');
        })
        .catch(error => {
            console.error('Error generating literature review:', error);
            document.getElementById('literature-review-content').innerHTML = '<div class="alert alert-danger">Error generating literature review</div>';
        });
    }
});
