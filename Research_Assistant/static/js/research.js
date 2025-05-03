/**
 * MCP Research Assistant - Research Page JavaScript
 * This file handles the client-side functionality of the research page.
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const researchSearchInput = document.getElementById('research-search-input');
    const researchSearchBtn = document.getElementById('research-search-btn');
    const researchResults = document.getElementById('research-results');
    const researchFindings = document.getElementById('research-findings');
    const researchSpinner = document.getElementById('research-spinner');
    const literatureReviewInput = document.getElementById('literature-review-input');
    const literatureReviewBtn = document.getElementById('literature-review-btn');
    const literatureReviewResult = document.getElementById('literature-review-result');
    const viewContextBtn = document.getElementById('view-context-btn');
    const getSummaryBtn = document.getElementById('get-summary-btn');
    const topicsList = document.getElementById('topics-list');
    
    // Bootstrap Modals
    const contextModal = new bootstrap.Modal(document.getElementById('contextModal'));
    const summaryModal = new bootstrap.Modal(document.getElementById('summaryModal'));
    const paperModal = new bootstrap.Modal(document.getElementById('paperModal'));
    
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
        
        // Load research findings
        loadResearchFindings();
        
        // Set up event listeners
        setupEventListeners();
    }
    
    /**
     * Set up event listeners
     */
    function setupEventListeners() {
        // Search for papers
        researchSearchBtn.addEventListener('click', function() {
            searchPapers(researchSearchInput.value);
        });
        
        // Search on Enter key
        researchSearchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                searchPapers(researchSearchInput.value);
            }
        });
        
        // Generate literature review
        literatureReviewBtn.addEventListener('click', function() {
            generateLiteratureReview(literatureReviewInput.value);
        });
        
        // View context
        viewContextBtn.addEventListener('click', viewContext);
        
        // Get summary
        getSummaryBtn.addEventListener('click', getSummary);
        
        // Analyze paper button in modal
        document.getElementById('analyze-paper-btn').addEventListener('click', function() {
            if (currentPaper) {
                analyzePaper(currentPaper);
                paperModal.hide();
            }
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
        
        // Show spinner
        researchSpinner.classList.remove('d-none');
        
        // Clear previous results
        researchResults.innerHTML = '';
        
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
            // Hide spinner
            researchSpinner.classList.add('d-none');
            
            if (data.papers && data.papers.length > 0) {
                researchResults.innerHTML = `<h5 class="mb-3">Found ${data.papers.length} papers on "${query}"</h5>`;
                
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
                    
                    researchResults.appendChild(paperElement);
                });
                
                // Update topics
                loadTopics();
                
                // Update research findings
                loadResearchFindings();
            } else {
                researchResults.innerHTML = `<div class="alert alert-info">No papers found for "${query}"</div>`;
            }
        })
        .catch(error => {
            console.error('Error searching papers:', error);
            researchSpinner.classList.add('d-none');
            researchResults.innerHTML = '<div class="alert alert-danger">Error searching for papers</div>';
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
        
        paperModal.show();
    }
    
    /**
     * Analyze a paper
     */
    function analyzePaper(paper) {
        // Show loading
        const loadingElement = document.createElement('div');
        loadingElement.classList.add('alert', 'alert-info');
        loadingElement.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> Analyzing paper...';
        researchResults.prepend(loadingElement);
        
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
            researchResults.prepend(successElement);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                successElement.remove();
            }, 5000);
            
            // Update research findings
            loadResearchFindings();
            
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
            researchResults.prepend(errorElement);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                errorElement.remove();
            }, 5000);
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
        literatureReviewResult.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2">Generating literature review...</p></div>';
        
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
            literatureReviewResult.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h5>Literature Review: ${topic}</h5>
                    </div>
                    <div class="card-body">
                        ${marked.parse(data.review)}
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error generating literature review:', error);
            literatureReviewResult.innerHTML = '<div class="alert alert-danger">Error generating literature review</div>';
        });
    }
    
    /**
     * Load research findings
     */
    function loadResearchFindings() {
        fetch('/api/research-findings')
        .then(response => response.json())
        .then(data => {
            if (data.findings && data.findings.length > 0) {
                // Display findings
                researchFindings.innerHTML = '';
                data.findings.forEach(finding => {
                    const findingElement = document.createElement('div');
                    findingElement.classList.add('research-finding');
                    
                    findingElement.innerHTML = `
                        <div class="research-finding-content">${finding.content}</div>
                        ${finding.source ? `<div class="research-finding-source">Source: ${finding.source}</div>` : ''}
                    `;
                    
                    researchFindings.appendChild(findingElement);
                });
            } else {
                // No findings
                researchFindings.innerHTML = '<div class="placeholder-text">No research findings yet</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching research findings:', error);
            researchFindings.innerHTML = '<div class="alert alert-danger">Error loading research findings</div>';
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
});
