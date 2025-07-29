// Main JavaScript for Fake News Detection System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Setup form handlers
    setupAnalysisForm();
    setupClearForm();
    setupExampleButtons();
    
    // Setup UI enhancements
    setupTooltips();
    setupAnimations();
    
    console.log('✅ Fake News Detection App initialized');
}

// Analysis Form Handler
function setupAnalysisForm() {
    const form = document.getElementById('analysisForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeNews();
    });
}

// Clear Form Handler
function setupClearForm() {
    const clearBtn = document.getElementById('clearForm');
    if (!clearBtn) return;
    
    clearBtn.addEventListener('click', function() {
        clearForm();
    });
}

// Example Buttons Handler
function setupExampleButtons() {
    const exampleButtons = document.querySelectorAll('.example-btn');
    exampleButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            loadExample(this.dataset.type);
        });
    });
}

// Main Analysis Function
async function analyzeNews() {
    const title = document.getElementById('newsTitle').value.trim();
    const content = document.getElementById('newsContent').value.trim();
    
    // Validation
    if (!title || !content) {
        showAlert('Please fill in both title and content fields', 'warning');
        return;
    }
    
    if (title.length < 5) {
        showAlert('Title must be at least 5 characters long', 'warning');
        return;
    }
    
    if (content.length < 20) {
        showAlert('Content must be at least 20 characters long', 'warning');
        return;
    }
    
    try {
        // Show loading state
        showLoadingModal();
        
        // Prepare data
        const data = {
            title: title,
            content: content
        };
        
        // Make API request
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        // Hide loading modal
        hideLoadingModal();
        
        if (result.success) {
            displayResults(result.result);
            showAlert('Analysis completed successfully!', 'success');
        } else {
            showAlert(result.message || 'Analysis failed', 'danger');
        }
        
    } catch (error) {
        hideLoadingModal();
        console.error('Analysis error:', error);
        showAlert('Network error. Please check your connection and try again.', 'danger');
    }
}

// Display Results Function
function displayResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    if (!resultsSection || !resultsContent) return;
    
    const prediction = result.prediction;
    const confidence = result.confidence;
    const fakeProb = result.fake_probability;
    const realProb = result.real_probability;
    const analysis = result.analysis;
    
    // Determine styling based on prediction
    const isReal = prediction === 'Real';
    const cardClass = isReal ? 'result-real' : 'result-fake';
    const iconClass = isReal ? 'fa-check-circle' : 'fa-exclamation-triangle';
    const iconColor = isReal ? 'text-success' : 'text-danger';
    const predictionColor = isReal ? 'success' : 'danger';
    
    // Generate confidence level description
    const confidenceLevel = getConfidenceLevel(confidence);
    
    const html = `
        <div class="analysis-result ${cardClass} fade-in">
            <div class="row">
                <div class="col-md-4 text-center mb-3">
                    <div class="prediction-display">
                        <i class="fas ${iconClass} fa-4x ${iconColor} mb-3"></i>
                        <h3 class="fw-bold text-${predictionColor}">${prediction}</h3>
                        <span class="badge bg-${predictionColor} prediction-badge">
                            ${prediction.toUpperCase()} NEWS
                        </span>
                    </div>
                </div>
                
                <div class="col-md-8">
                    <div class="confidence-display mb-3">
                        <h5 class="mb-2">
                            <i class="fas fa-chart-bar"></i> Confidence Analysis
                        </h5>
                        <div class="row">
                            <div class="col-sm-6">
                                <div class="mb-2">
                                    <strong>Overall Confidence:</strong>
                                    <div class="confidence-meter mt-1">
                                        <div class="confidence-fill" style="width: ${confidence * 100}%"></div>
                                    </div>
                                    <small class="text-muted">${(confidence * 100).toFixed(1)}% - ${confidenceLevel}</small>
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <div class="mb-2">
                                    <strong>Probability Scores:</strong>
                                    <div class="mt-1">
                                        <span class="badge bg-success me-2">Real: ${(realProb * 100).toFixed(1)}%</span>
                                        <span class="badge bg-danger">Fake: ${(fakeProb * 100).toFixed(1)}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="detailed-analysis">
                        <h6><i class="fas fa-microscope"></i> Detailed Analysis</h6>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="analysis-metric">
                                    <strong>Pattern Analysis:</strong><br>
                                    <div class="progress mb-1" style="height: 20px;">
                                        <div class="progress-bar bg-warning" 
                                             style="width: ${analysis.suspicion_patterns * 100}%">
                                            ${(analysis.suspicion_patterns * 100).toFixed(1)}%
                                        </div>
                                    </div>
                                    <small class="text-muted">Suspicious pattern detection</small>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="analysis-metric">
                                    <strong>Pipeline Score:</strong><br>
                                    <div class="progress mb-1" style="height: 20px;">
                                        <div class="progress-bar bg-info" 
                                             style="width: ${analysis.pipeline_score * 100}%">
                                            ${(analysis.pipeline_score * 100).toFixed(1)}%
                                        </div>
                                    </div>
                                    <small class="text-muted">AI classification result</small>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="analysis-metric">
                                    <strong>BERT Features:</strong><br>
                                    ${analysis.bert_features ? `
                                        <div class="small">
                                            <div>Diversity: ${(analysis.bert_features.token_diversity * 100).toFixed(1)}%</div>
                                            <div>Length: ${analysis.bert_features.text_length} tokens</div>
                                        </div>
                                    ` : `
                                        <small class="text-muted">Basic analysis</small>
                                    `}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-3">
                        <small class="text-muted">
                            <i class="fas fa-info-circle"></i> 
                            Analysis method: ${result.method || 'BERT-based Detection'}
                        </small>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mt-3 text-center">
            <button class="btn btn-outline-primary me-2" onclick="clearForm()">
                <i class="fas fa-plus"></i> Analyze Another Article
            </button>
            <a href="/history" class="btn btn-outline-info">
                <i class="fas fa-history"></i> View History
            </a>
        </div>
    `;
    
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Animate confidence bars
    setTimeout(() => {
        animateProgressBars();
    }, 500);
}

// Helper Functions
function getConfidenceLevel(confidence) {
    if (confidence >= 0.8) return 'Very High';
    if (confidence >= 0.6) return 'High';
    if (confidence >= 0.4) return 'Medium';
    if (confidence >= 0.2) return 'Low';
    return 'Very Low';
}

function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}

function clearForm() {
    document.getElementById('newsTitle').value = '';
    document.getElementById('newsContent').value = '';
    
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
    
    // Scroll to top of form
    const form = document.getElementById('analysisForm');
    if (form) {
        form.scrollIntoView({ behavior: 'smooth' });
    }
    
    showAlert('Form cleared successfully', 'info');
}

function loadExample(type) {
    const examples = {
        real: {
            title: "Climate Change Research Shows Alarming Trends in Arctic Ice Loss",
            content: "A comprehensive study published in the journal Nature Climate Change reveals that Arctic sea ice is disappearing at an unprecedented rate. The research, conducted by an international team of scientists from 15 institutions, analyzed satellite data spanning four decades. The findings indicate that summer Arctic sea ice extent has declined by 13% per decade since 1979. Dr. Sarah Mitchell, lead researcher at the National Ice Center, stated that the current rate of ice loss is far exceeding previous climate model predictions. The study utilized advanced satellite imagery and temperature measurements to track changes in ice thickness and coverage. The implications for global sea levels and weather patterns are significant, with potential impacts on coastal communities worldwide."
        },
        fake: {
            title: "SHOCKING: Scientists Discover Miracle Cure That Big Pharma Doesn't Want You to Know!",
            content: "URGENT UPDATE: A secret government study has revealed an AMAZING natural cure that can heal EVERY disease known to mankind! Doctors are FURIOUS about this incredible discovery because it threatens their billion-dollar industry! This ONE simple trick, discovered by ancient civilizations, can cure cancer, diabetes, heart disease, and even aging itself! The pharmaceutical companies have been hiding this information for DECADES, but we've obtained EXCLUSIVE access to this life-changing secret! Order now for just $19.99 and receive FREE shipping! WARNING: This offer may be removed at any time due to pressure from Big Pharma! Don't let them silence the TRUTH! Act NOW before it's too late!"
        }
    };
    
    const example = examples[type];
    if (example) {
        document.getElementById('newsTitle').value = example.title;
        document.getElementById('newsContent').value = example.content;
        
        showAlert(`${type === 'real' ? 'Real' : 'Fake'} news example loaded`, 'info');
        
        // Scroll to form
        document.getElementById('analysisForm').scrollIntoView({ behavior: 'smooth' });
    }
}

// UI Enhancement Functions
function setupTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

function setupAnimations() {
    // Add intersection observer for fade-in animations
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        });
        
        document.querySelectorAll('.card').forEach(card => {
            observer.observe(card);
        });
    }
}

// Modal Functions
function showLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal && typeof bootstrap !== 'undefined') {
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }
}

function hideLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal && typeof bootstrap !== 'undefined') {
        const bootstrapModal = bootstrap.Modal.getInstance(modal);
        if (bootstrapModal) {
            bootstrapModal.hide();
        }
    }
}

// Alert Function
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Find container and insert alert
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// API Functions for other pages
async function loadApiStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        return stats;
    } catch (error) {
        console.error('Error loading stats:', error);
        return null;
    }
}

async function loadApiHistory(page = 1, perPage = 10) {
    try {
        const response = await fetch(`/api/history?page=${page}&per_page=${perPage}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading history:', error);
        return null;
    }
}

// Utility Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function truncateText(text, maxLength = 100) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showAlert('Copied to clipboard!', 'success');
        } catch (err) {
            showAlert('Failed to copy to clipboard', 'warning');
        }
        document.body.removeChild(textArea);
    }
}

// Performance monitoring
function logPerformance(startTime, operation) {
    const endTime = performance.now();
    const duration = endTime - startTime;
    console.log(`${operation} took ${duration.toFixed(2)} milliseconds`);
}

// Export functions for global use
window.analyzeNews = analyzeNews;
window.clearForm = clearForm;
window.loadExample = loadExample;
window.showAlert = showAlert;
window.loadApiStats = loadApiStats;
window.loadApiHistory = loadApiHistory;
