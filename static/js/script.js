// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const loadingContainer = document.getElementById('loadingContainer');
const resultsContainer = document.getElementById('resultsContainer');
const previewImage = document.getElementById('previewImage');
const generatedCaption = document.getElementById('generatedCaption');
const copyBtn = document.getElementById('copyBtn');
const newImageBtn = document.getElementById('newImageBtn');
const regenerateBtn = document.getElementById('regenerateBtn');
const toast = document.getElementById('toast');
const toastMessage = document.querySelector('.toast-message');

// State management
let currentFilename = null;
let currentImageData = null;

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    checkServerHealth();
});

// Event Listeners
function initializeEventListeners() {
    // File upload events
    browseBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Click to upload (entire upload area)
    uploadArea.addEventListener('click', (e) => {
        if (e.target === uploadArea || uploadArea.contains(e.target)) {
            fileInput.click();
        }
    });
    
    // Action buttons
    copyBtn.addEventListener('click', copyCaption);
    newImageBtn.addEventListener('click', resetUpload);
    regenerateBtn.addEventListener('click', regenerateCaption);
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.addEventListener(eventName, preventDefaults, false);
    });
}

// Prevent default drag behaviors
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// File handling functions
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

// File validation and processing
function processFile(file) {
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
        showToast('Please upload a PNG, JPG, or JPEG image', 'error');
        return;
    }
    
    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showToast('File size must be less than 16MB', 'error');
        return;
    }
    
    // Read and display the image
    const reader = new FileReader();
    reader.onload = function(e) {
        currentImageData = e.target.result;
        uploadImage(file);
    };
    reader.readAsDataURL(file);
}

// Upload image to server
async function uploadImage(file) {
    showLoading();
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            currentFilename = result.filename;
            displayResults(result.caption, currentImageData);
            showToast('Image uploaded and caption generated successfully!', 'success');
        } else {
            throw new Error(result.error || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showToast(`Upload failed: ${error.message}`, 'error');
        hideLoading();
        resetUpload();
    }
}

// Display results
function displayResults(caption, imageData) {
    hideLoading();
    
    // Set image and caption
    previewImage.src = imageData;
    generatedCaption.textContent = caption;
    
    // Show results container
    resultsContainer.style.display = 'block';
    uploadArea.style.display = 'none';
    
    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Loading states
function showLoading() {
    uploadArea.style.display = 'none';
    loadingContainer.style.display = 'block';
    resultsContainer.style.display = 'none';
}

function hideLoading() {
    loadingContainer.style.display = 'none';
}

// Reset upload area
function resetUpload() {
    // Reset state
    currentFilename = null;
    currentImageData = null;
    fileInput.value = '';
    
    // Reset UI
    uploadArea.style.display = 'block';
    loadingContainer.style.display = 'none';
    resultsContainer.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Regenerate caption
async function regenerateCaption() {
    if (!currentFilename) {
        showToast('No image to regenerate caption for', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/caption', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: currentFilename })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            displayResults(result.caption, currentImageData);
            showToast('Caption regenerated successfully!', 'success');
        } else {
            throw new Error(result.error || 'Regeneration failed');
        }
    } catch (error) {
        console.error('Regeneration error:', error);
        showToast(`Regeneration failed: ${error.message}`, 'error');
        hideLoading();
    }
}

// Copy caption to clipboard
async function copyCaption() {
    const caption = generatedCaption.textContent;
    
    try {
        await navigator.clipboard.writeText(caption);
        showToast('Caption copied to clipboard!', 'success');
        
        // Visual feedback
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyBtn.style.background = '#059669';
        
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            copyBtn.style.background = '#10b981';
        }, 2000);
    } catch (error) {
        console.error('Copy error:', error);
        showToast('Failed to copy caption', 'error');
    }
}

// Toast notifications
function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    
    // Update toast appearance based on type
    const toastIcon = toast.querySelector('.toast-icon');
    if (type === 'error') {
        toastIcon.className = 'fas fa-exclamation-circle toast-icon';
        toastIcon.style.color = '#ef4444';
    } else {
        toastIcon.className = 'fas fa-check-circle toast-icon';
        toastIcon.style.color = '#10b981';
    }
    
    // Show toast
    toast.classList.add('show');
    
    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Check server health
async function checkServerHealth() {
    try {
        const response = await fetch('/health');
        const result = await response.json();
        
        if (response.ok && result.status === 'healthy') {
            console.log('Server is healthy');
            updateServerStatus(true);
        } else {
            console.warn('Server health check failed');
            updateServerStatus(false);
        }
    } catch (error) {
        console.error('Health check error:', error);
        updateServerStatus(false);
    }
}

// Update server status indicator
function updateServerStatus(isOnline) {
    const statusIndicator = document.querySelector('.status-indicator');
    if (statusIndicator) {
        if (isOnline) {
            statusIndicator.className = 'status-indicator online';
            statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Model Ready';
        } else {
            statusIndicator.className = 'status-indicator offline';
            statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Model Offline';
        }
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + V to paste image
    if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        // Handle clipboard paste if it contains an image
        navigator.clipboard.read().then(items => {
            for (let item of items) {
                if (item.types.includes('image/png') || item.types.includes('image/jpeg')) {
                    item.getType(item.types[0]).then(blob => {
                        const file = new File([blob], 'pasted-image.png', { type: blob.type });
                        processFile(file);
                    });
                    break;
                }
            }
        }).catch(err => {
            // Clipboard access denied or no image in clipboard
            console.log('No image in clipboard or access denied');
        });
    }
    
    // Escape key to reset
    if (e.key === 'Escape') {
        if (resultsContainer.style.display === 'block') {
            resetUpload();
        }
    }
    
    // Ctrl/Cmd + C to copy caption when results are shown
    if ((e.ctrlKey || e.metaKey) && e.key === 'c' && resultsContainer.style.display === 'block') {
        // Only intercept if no text is selected
        if (window.getSelection().toString() === '') {
            e.preventDefault();
            copyCaption();
        }
    }
});

// Image preview enhancements
previewImage.addEventListener('load', function() {
    // Add a subtle animation when image loads
    this.style.animation = 'fadeIn 0.5s ease';
});

previewImage.addEventListener('error', function() {
    console.error('Failed to load preview image');
    showToast('Failed to display image', 'error');
});

// Auto-save functionality (optional enhancement)
function autoSaveCaption() {
    if (currentFilename && generatedCaption.textContent) {
        const captionData = {
            filename: currentFilename,
            caption: generatedCaption.textContent,
            timestamp: new Date().toISOString()
        };
        
        // Save to localStorage for session persistence
        let savedCaptions = JSON.parse(localStorage.getItem('savedCaptions') || '[]');
        savedCaptions.push(captionData);
        
        // Keep only last 10 captions
        if (savedCaptions.length > 10) {
            savedCaptions = savedCaptions.slice(-10);
        }
        
        localStorage.setItem('savedCaptions', JSON.stringify(savedCaptions));
    }
}

// Call auto-save when caption is generated
const originalDisplayResults = displayResults;
displayResults = function(caption, imageData) {
    originalDisplayResults(caption, imageData);
    autoSaveCaption();
};

// Error boundary for API calls
function handleApiError(error, customMessage = 'An error occurred') {
    console.error('API Error:', error);
    
    let userMessage = customMessage;
    if (error.response) {
        // Server responded with error status
        userMessage = `Server error: ${error.response.status}`;
    } else if (error.request) {
        // Request was made but no response received
        userMessage = 'Network error - please check your connection';
    }
    
    showToast(userMessage, 'error');
}

// Performance monitoring
function logPerformance() {
    // Log performance metrics for debugging
    if (window.performance && window.performance.timing) {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);
    }
}

// Initialize performance monitoring
window.addEventListener('load', logPerformance);

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}
