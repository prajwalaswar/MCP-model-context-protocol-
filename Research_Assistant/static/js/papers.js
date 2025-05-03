/**
 * MCP Research Assistant - Papers Page JavaScript
 * This file handles the client-side functionality of the papers page.
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const papersList = document.getElementById('papers-list');
    const papersSpinner = document.getElementById('papers-spinner');
    const addPaperForm = document.getElementById('add-paper-form');
    const citationsList = document.getElementById('citations-list');
    const viewContextBtn = document.getElementById('view-context-btn');
    const getCitationsBtn = document.getElementById('get-citations-btn');
    const topicsList = document.getElementById('topics-list');
    
    // Bootstrap Modals
    const contextModal = new bootstrap.Modal(document.getElementById('contextModal'));
    const paperDetailsModal = new bootstrap.Modal(document.getElementById('paperDetailsModal'));
    const citationsModal = new bootstrap.Modal(document.getElementById('citationsModal'));
    
    // Current paper for analysis
    let currentPaper = null;
    
    // Initialize
    init();
    
    /**
     * Initialize the application
     */
    function init() {
        // Load topics
        loadTopics();
        
        // Load papers
        loadPapers();
        
        // Load citations
        loadCitations();
        
        // Set up event listeners
        setupEventListeners();
    }
    
    /**
     * Set up event listeners
     */
    function setupEventListeners() {
        // Add paper form submission
        addPaperForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addPaper();
        });
        
        // View context
        viewContextBtn.addEventListener('click', viewContext);
        
        // Get citations
        getCitationsBtn.addEventListener('click', function() {
            viewCitations();
        });
        
        // Analyze paper button in modal
        document.getElementById('analyze-paper-btn').addEventListener('click', function() {
            if (currentPaper) {
                analyzePaper(currentPaper);
                paperDetailsModal.hide();
            }
        });
    }
    
    /**
     * Load research papers
     */
    function loadPapers() {
        // Show spinner
        papersSpinner.classList.remove('d-none');
        
        fetch('/api/research-papers')
        .then(response => response.json())
        .then(data => {
            // Hide spinner
            papersSpinner.classList.add('d-none');
            
            if (data.papers && data.papers.length > 0) {
                // Display papers
                papersList.innerHTML = '';
                data.papers.forEach(paper => {
                    const paperElement = document.createElement('div');
                    paperElement.classList.add('research-paper');
                    
                    const authors = Array.isArray(paper.authors) ? paper.authors.join(', ') : paper.authors;
                    
                    paperElement.innerHTML = `
                        <h4>${paper.title}</h4>
                        <div class="research-paper-authors">${authors}</div>
                        <div class="research-paper-abstract">${paper.abstract.substring(0, 200)}${paper.abstract.length > 200 ? '...' : ''}</div>
                        <div class="research-paper-meta">
                            <span>${paper.year || 'N/A'}</span>
                            <span>Relevance: ${(paper.relevance * 100).toFixed(0)}%</span>
                        </div>
                        <div class="mt-2">
                            <button class="btn btn-sm btn-primary view-paper-btn">View Details</button>
                            <button class="btn btn-sm btn-info analyze-paper-btn">Analyze Paper</button>
                        </div>
                    `;
                    
                    // Add event listeners to buttons
                    const viewBtn = paperElement.querySelector('.view-paper-btn');
                    const analyzeBtn = paperElement.querySelector('.analyze-paper-btn');
                    
                    viewBtn.addEventListener('click', function() {
                        viewPaper(paper);
                    });
                    
                    analyzeBtn.addEventListener('click', function() {
                        analyzePaper(paper);
                    });
                    
                    papersList.appendChild(paperElement);
                });
            } else {
                // No papers
                papersList.innerHTML = '<div class="placeholder-text">No papers in your research context yet</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching papers:', error);
            papersSpinner.classList.add('d-none');
            papersList.innerHTML = '<div class="alert alert-danger">Error loading papers</div>';
        });
    }
    
    /**
     * Load citations
     */
    function loadCitations() {
        fetch('/api/citations')
        .then(response => response.json())
        .then(data => {
            if (data.citations && data.citations.length > 0) {
                // Display citations
                citationsList.innerHTML = '';
                data.citations.slice(0, 3).forEach(citation => {
                    const citationElement = document.createElement('div');
                    citationElement.classList.add('citation-item');
                    
                    citationElement.innerHTML = `
                        <div class="citation-text">${citation.text}</div>
                        ${citation.source ? `<div class="citation-source">Source: ${citation.source}</div>` : ''}
                    `;
                    
                    citationsList.appendChild(citationElement);
                });
                
                if (data.citations.length > 3) {
                    const moreElement = document.createElement('div');
                    moreElement.classList.add('text-center', 'mt-2');
                    moreElement.innerHTML = `<button class="btn btn-sm btn-outline-primary view-all-citations-btn">View all ${data.citations.length} citations</button>`;
                    
                    moreElement.querySelector('.view-all-citations-btn').addEventListener('click', function() {
                        viewCitations();
                    });
                    
                    citationsList.appendChild(moreElement);
                }
            } else {
                // No citations
                citationsList.innerHTML = '<div class="placeholder-text">No citations yet</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching citations:', error);
            citationsList.innerHTML = '<div class="alert alert-danger">Error loading citations</div>';
        });
    }
    
    /**
     * View all citations
     */
    function viewCitations() {
        fetch('/api/citations')
        .then(response => response.json())
        .then(data => {
            const citationsContent = document.getElementById('citations-modal-content');
            
            if (data.citations && data.citations.length > 0) {
                // Display citations
                citationsContent.innerHTML = '';
                data.citations.forEach(citation => {
                    const citationElement = document.createElement('div');
                    citationElement.classList.add('citation-item');
                    
                    citationElement.innerHTML = `
                        <div class="citation-text">${citation.text}</div>
                        ${citation.source ? `<div class="citation-source">Source: ${citation.source}</div>` : ''}
                    `;
                    
                    citationsContent.appendChild(citationElement);
                });
            } else {
                // No citations
                citationsContent.innerHTML = '<div class="placeholder-text">No citations yet</div>';
            }
            
            citationsModal.show();
        })
        .catch(error => {
            console.error('Error fetching citations:', error);
            alert('Error fetching citations');
        });
    }
    
    /**
     * View paper details
     */
    function viewPaper(paper) {
        currentPaper = paper;
        
        const paperDetails = document.getElementById('paper-details');
        const authors = Array.isArray(paper.authors) ? paper.authors.join(', ') : paper.authors;
        
        paperDetails.innerHTML = `
            <h4>${paper.title}</h4>
            <div class="paper-details-section">
                <h5>Authors</h5>
                <p>${authors}</p>
            </div>
            <div class="paper-details-section">
                <h5>Abstract</h5>
                <p>${paper.abstract}</p>
            </div>
            <div class="paper-details-section">
                <h5>Publication Year</h5>
                <p>${paper.year || 'Not specified'}</p>
            </div>
            ${paper.url ? `
            <div class="paper-details-section">
                <h5>URL</h5>
                <p><a href="${paper.url}" target="_blank">${paper.url}</a></p>
            </div>
            ` : ''}
            <div class="paper-details-section">
                <h5>Relevance Score</h5>
                <p>${(paper.relevance * 100).toFixed(0)}%</p>
            </div>
        `;
        
        paperDetailsModal.show();
    }
    
    /**
     * Add a paper manually
     */
    function addPaper() {
        const title = document.getElementById('paper-title').value.trim();
        const authorsString = document.getElementById('paper-authors').value.trim();
        const abstract = document.getElementById('paper-abstract').value.trim();
        const year = document.getElementById('paper-year').value.trim();
        const url = document.getElementById('paper-url').value.trim();
        
        if (!title || !authorsString || !abstract) {
            alert('Please fill in the required fields (title, authors, abstract)');
            return;
        }
        
        // Parse authors
        const authors = authorsString.split(',').map(author => author.trim());
        
        // Show loading
        const loadingElement = document.createElement('div');
        loadingElement.classList.add('alert', 'alert-info', 'mt-3');
        loadingElement.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> Adding paper...';
        addPaperForm.appendChild(loadingElement);
        
        fetch('/api/analyze-paper', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                authors: authors,
                abstract: abstract,
                year: year ? parseInt(year) : null,
                url: url || null
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading element
            loadingElement.remove();
            
            // Show success message
            const successElement = document.createElement('div');
            successElement.classList.add('alert', 'alert-success', 'mt-3');
            successElement.textContent = `Paper "${title}" added and analyzed successfully.`;
            addPaperForm.appendChild(successElement);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                successElement.remove();
            }, 5000);
            
            // Reset form
            addPaperForm.reset();
            
            // Reload papers
            loadPapers();
            
            // Update topics
            loadTopics();
        })
        .catch(error => {
            console.error('Error adding paper:', error);
            
            // Remove loading element
            loadingElement.remove();
            
            // Show error message
            const errorElement = document.createElement('div');
            errorElement.classList.add('alert', 'alert-danger', 'mt-3');
            errorElement.textContent = 'Error adding paper.';
            addPaperForm.appendChild(errorElement);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                errorElement.remove();
            }, 5000);
        });
    }
    
    /**
     * Analyze a paper
     */
    function analyzePaper(paper) {
        // Show loading
        const loadingElement = document.createElement('div');
        loadingElement.classList.add('alert', 'alert-info');
        loadingElement.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> Analyzing paper...';
        papersList.prepend(loadingElement);
        
        fetch('/api/analyze-paper', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: paper.title,
                authors: paper.authors,
                abstract: paper.abstract
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading element
            loadingElement.remove();
            
            // Show success message
            const successElement = document.createElement('div');
            successElement.classList.add('alert', 'alert-success');
            successElement.textContent = `Paper "${paper.title}" analyzed successfully.`;
            papersList.prepend(successElement);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                successElement.remove();
            }, 5000);
            
            // Reload citations
            loadCitations();
            
            // Update topics
            loadTopics();
        })
        .catch(error => {
            console.error('Error analyzing paper:', error);
            
            // Remove loading element
            loadingElement.remove();
            
            // Show error message
            const errorElement = document.createElement('div');
            errorElement.classList.add('alert', 'alert-danger');
            errorElement.textContent = 'Error analyzing paper.';
            papersList.prepend(errorElement);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                errorElement.remove();
            }, 5000);
        });
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
});
