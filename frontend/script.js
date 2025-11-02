// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const analyzeForm = document.getElementById('analyzeForm');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const resultsSection = document.getElementById('resultsSection');
const extractedTextSection = document.getElementById('extractedTextSection');
const extractedTextBox = document.getElementById('extractedTextBox');

// Tab and Image Elements
const tabBtns = document.querySelectorAll('.tab-btn');
const textTab = document.getElementById('textTab');
const imageTab = document.getElementById('imageTab');
const jobImage = document.getElementById('jobImage');
const imageUploadArea = document.getElementById('imageUploadArea');
const uploadPlaceholder = document.getElementById('uploadPlaceholder');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const removeImage = document.getElementById('removeImage');

// Global state
let currentImageData = null;
let activeTab = 'text';
let currentAnalysis = null;

// Tab Switching
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Update active tab button
    tabBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update active tab content
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.getElementById(`${tabName}Tab`).classList.add('active');
    
    activeTab = tabName;
    
    // Clear previous data when switching tabs
    if (tabName === 'text') {
        currentImageData = null;
        if (imagePreview) {
            imagePreview.style.display = 'none';
            uploadPlaceholder.style.display = 'block';
        }
    } else {
        document.getElementById('jobText').value = '';
    }
}

// Image Upload Handling
if (imageUploadArea) {
    imageUploadArea.addEventListener('click', () => {
        jobImage.click();
    });

    imageUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        imageUploadArea.classList.add('dragover');
    });

    imageUploadArea.addEventListener('dragleave', () => {
        imageUploadArea.classList.remove('dragover');
    });

    imageUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        imageUploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageUpload(files[0]);
        }
    });

    jobImage.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageUpload(e.target.files[0]);
        }
    });

    if (removeImage) {
        removeImage.addEventListener('click', (e) => {
            e.stopPropagation();
            clearImage();
        });
    }
}

function handleImageUpload(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Please upload a valid image file.');
        return;
    }
    
    // Validate file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
        alert('Image size must be less than 5MB.');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        currentImageData = e.target.result;
        previewImg.src = currentImageData;
        uploadPlaceholder.style.display = 'none';
        imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    currentImageData = null;
    jobImage.value = '';
    imagePreview.style.display = 'none';
    uploadPlaceholder.style.display = 'block';
}

// Analyze Form Submit
analyzeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const jobText = document.getElementById('jobText').value.trim();
    
    // Validate input based on active tab
    if (activeTab === 'text' && !jobText) {
        alert('Please enter job posting text');
        return;
    }
    
    if (activeTab === 'image' && !currentImageData) {
        alert('Please upload an image of the job posting');
        return;
    }
    
    // Show loading state
    analyzeBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'flex';
    
    try {
        const requestData = {};
        
        if (activeTab === 'text') {
            requestData.text = jobText;
        } else {
            requestData.image = currentImageData;
        }
        
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Analysis failed');
        }
        
        const result = await response.json();
        currentAnalysis = result;
        
        // Save detection to history
        console.log('Saving detection:', result);
        saveDetection(result);
        console.log('Detection saved. Current history:', JSON.parse(localStorage.getItem('jobGuardHistory') || '[]'));
        
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Failed to analyze job posting. Make sure the backend server is running.');
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
});

// Display Results with Modern UI
function displayResults(result) {
    // Show results section with animation
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Animate score circle
    setTimeout(() => {
        updateScoreCircle(result.score);
    }, 300);
    
    // Update status badge
    const statusBadge = document.getElementById('statusBadge');
    const statusValue = document.getElementById('statusValue');
    
    if (result.is_fake) {
        statusValue.textContent = '⚠️ LIKELY FAKE';
        statusBadge.className = 'status-badge fake';
    } else {
        statusValue.textContent = '✅ LEGITIMATE';
        statusBadge.className = 'status-badge legitimate';
    }
    
    // Update confidence
    const confidenceValue = document.getElementById('confidenceValue');
    confidenceValue.textContent = result.confidence;
    
    // Show extracted text if from image
    if (result.source === 'image' && result.extracted_text) {
        extractedTextSection.style.display = 'block';
        extractedTextBox.textContent = result.extracted_text;
    } else {
        extractedTextSection.style.display = 'none';
    }
    
    // Display reasons/analysis breakdown
    displayReasons(result);
    
    // Update final message
    displayFinalMessage(result);
}

function updateScoreCircle(score) {
    const scoreValue = document.getElementById('scoreValue');
    const scoreCircle = document.getElementById('scoreCircle');
    
    // Animate score counting
    let currentScore = 0;
    const increment = score / 50; // 50 steps for smooth animation
    
    const countAnimation = setInterval(() => {
        currentScore += increment;
        if (currentScore >= score) {
            currentScore = score;
            clearInterval(countAnimation);
        }
        scoreValue.textContent = Math.round(currentScore);
    }, 40);
    
    // Update circle gradient based on score
    const percentage = (score / 100) * 360;
    if (score >= 70) {
        scoreCircle.style.background = `conic-gradient(#4facfe ${percentage}deg, #ff9a9e ${percentage}deg)`;
    } else if (score >= 50) {
        scoreCircle.style.background = `conic-gradient(#ffecd2 ${percentage}deg, #ff9a9e ${percentage}deg)`;
    } else {
        scoreCircle.style.background = `conic-gradient(#ff9a9e ${percentage}deg, #4facfe ${percentage}deg)`;
    }
}

function displayReasons(result) {
    const reasonsList = document.getElementById('reasonsList');
    reasonsList.innerHTML = '';
    
    if (result.flags && result.flags.length > 0) {
        result.flags.forEach((flag, index) => {
            const reasonItem = document.createElement('div');
            reasonItem.className = 'reason-item';
            
            // Determine if positive or negative
            if (flag.includes('✅') || flag.includes('No major red flags')) {
                reasonItem.classList.add('positive');
                reasonItem.innerHTML = `
                    <span class="reason-icon">✅</span>
                    <span>${flag}</span>
                `;
            } else {
                reasonItem.classList.add('negative');
                reasonItem.innerHTML = `
                    <span class="reason-icon">⚠️</span>
                    <span>${flag}</span>
                `;
            }
            
            // Animate each reason with delay
            reasonItem.style.animationDelay = `${index * 0.1}s`;
            reasonsList.appendChild(reasonItem);
        });
    }
}

function displayFinalMessage(result) {
    const finalMessage = document.getElementById('finalMessage');
    finalMessage.innerHTML = '';
    
    const messageDiv = document.createElement('div');
    
    if (result.is_fake) {
        messageDiv.className = 'final-message danger';
        messageDiv.innerHTML = `
            <h4>🚨 Warning: Potential Fraud Detected!</h4>
            <p><strong>Recommended Actions:</strong></p>
            <ul>
                <li>🚫 Do NOT provide personal information</li>
                <li>💰 Do NOT send money or pay fees</li>
                <li>🔍 Verify the company independently</li>
                <li>📢 Report to job platform administrators</li>
            </ul>
            <p><strong>Need legitimate opportunities?</strong> Visit our <a href="chatbot.html">Career Assistant</a> for trusted recommendations.</p>
        `;
    } else {
        messageDiv.className = 'final-message success';
        messageDiv.innerHTML = `
            <h4>✅ This posting appears legitimate</h4>
            <p>However, always verify job offers independently through official company websites and trusted sources.</p>
            <p><strong>Want to improve your skills?</strong> Check out our <a href="chatbot.html">Career Assistant</a> for course recommendations.</p>
        `;
    }
    
    finalMessage.appendChild(messageDiv);
}

// Check backend health on load
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected successfully');
        }
    } catch (error) {
        console.warn('⚠️ Backend not available. Please start the Flask server.');
    }
}

// Save detection to history (for dashboard)
function saveDetection(detection) {
    const history = JSON.parse(localStorage.getItem('jobGuardHistory') || '[]');
    const newDetection = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        score: detection.score,
        is_fake: detection.is_fake,
        confidence: detection.confidence,
        source: detection.source || 'text',
        flags: detection.flags || [],
        preview: detection.extracted_text ? 
            detection.extracted_text.substring(0, 100) + '...' : 
            'Job posting analysis'
    };
    
    history.unshift(newDetection);
    
    // Keep only last 100 detections
    if (history.length > 100) {
        history.splice(100);
    }
    
    localStorage.setItem('jobGuardHistory', JSON.stringify(history));
}



// Initialize
checkBackendHealth();