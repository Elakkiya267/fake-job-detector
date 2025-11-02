// Dashboard functionality with local storage and Chart.js

// Get detection history from localStorage
function getDetectionHistory() {
    const history = localStorage.getItem('jobGuardHistory');
    return history ? JSON.parse(history) : [];
}

// Save detection to history
function saveDetection(detection) {
    const history = getDetectionHistory();
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

// Calculate statistics
function calculateStats() {
    const history = getDetectionHistory();
    
    const stats = {
        total: history.length,
        legitimate: history.filter(d => !d.is_fake).length,
        fake: history.filter(d => d.is_fake).length,
        avgScore: history.length > 0 ? 
            Math.round(history.reduce((sum, d) => sum + d.score, 0) / history.length) : 0
    };
    
    return stats;
}

// Update statistics display
function updateStats() {
    const stats = calculateStats();
    
    document.getElementById('totalScans').textContent = stats.total;
    document.getElementById('legitimateCount').textContent = stats.legitimate;
    document.getElementById('fakeCount').textContent = stats.fake;
    document.getElementById('avgScore').textContent = stats.avgScore;
}

// Create trend chart
function createTrendChart() {
    const history = getDetectionHistory();
    const last7Days = [];
    const today = new Date();
    
    // Generate last 7 days data
    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];
        
        const dayDetections = history.filter(d => 
            d.timestamp.split('T')[0] === dateStr
        );
        
        last7Days.push({
            date: date.toLocaleDateString('en-US', { weekday: 'short' }),
            total: dayDetections.length,
            fake: dayDetections.filter(d => d.is_fake).length,
            legitimate: dayDetections.filter(d => !d.is_fake).length
        });
    }
    
    const ctx = document.getElementById('trendChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: last7Days.map(d => d.date),
            datasets: [{
                label: 'Total Scans',
                data: last7Days.map(d => d.total),
                borderColor: '#4facfe',
                backgroundColor: 'rgba(79, 172, 254, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Fake Detected',
                data: last7Days.map(d => d.fake),
                borderColor: '#ff9a9e',
                backgroundColor: 'rgba(255, 154, 158, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#ffffff' } }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    ticks: { color: '#b8b8d1' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: { 
                    ticks: { color: '#b8b8d1' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Create score distribution chart
function createScoreChart() {
    const history = getDetectionHistory();
    const scoreRanges = {
        '0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0
    };
    
    history.forEach(d => {
        if (d.score <= 20) scoreRanges['0-20']++;
        else if (d.score <= 40) scoreRanges['21-40']++;
        else if (d.score <= 60) scoreRanges['41-60']++;
        else if (d.score <= 80) scoreRanges['61-80']++;
        else scoreRanges['81-100']++;
    });
    
    const ctx = document.getElementById('scoreChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(scoreRanges),
            datasets: [{
                label: 'Number of Detections',
                data: Object.values(scoreRanges),
                backgroundColor: [
                    'rgba(255, 154, 158, 0.8)',
                    'rgba(255, 206, 84, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(79, 172, 254, 0.8)'
                ],
                borderColor: [
                    '#ff9a9e', '#ffce54', '#ff9f40', '#4bc0c0', '#4facfe'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#ffffff' } }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    ticks: { color: '#b8b8d1' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: { 
                    ticks: { color: '#b8b8d1' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Create detection methods chart
function createMethodChart() {
    const history = getDetectionHistory();
    const methods = { text: 0, image: 0 };
    
    history.forEach(d => {
        methods[d.source] = (methods[d.source] || 0) + 1;
    });
    
    const ctx = document.getElementById('methodChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Text Analysis', 'Image Analysis'],
            datasets: [{
                data: [methods.text, methods.image],
                backgroundColor: ['#4facfe', '#ff9a9e'],
                borderColor: ['#4facfe', '#ff9a9e'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#ffffff' } }
            }
        }
    });
}

// Create risk categories chart
function createRiskChart() {
    const history = getDetectionHistory();
    const riskCategories = {
        'Upfront Payment': 0,
        'Personal Email': 0,
        'Excessive Urgency': 0,
        'Vague Description': 0,
        'Poor Grammar': 0,
        'No Salary Info': 0
    };
    
    history.forEach(d => {
        if (d.flags) {
            d.flags.forEach(flag => {
                if (flag.includes('upfront') || flag.includes('payment')) riskCategories['Upfront Payment']++;
                else if (flag.includes('email') || flag.includes('gmail')) riskCategories['Personal Email']++;
                else if (flag.includes('urgency') || flag.includes('urgent')) riskCategories['Excessive Urgency']++;
                else if (flag.includes('vague') || flag.includes('description')) riskCategories['Vague Description']++;
                else if (flag.includes('grammar') || flag.includes('formatting')) riskCategories['Poor Grammar']++;
                else if (flag.includes('salary') || flag.includes('compensation')) riskCategories['No Salary Info']++;
            });
        }
    });
    
    const ctx = document.getElementById('riskChart').getContext('2d');
    new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: Object.keys(riskCategories),
            datasets: [{
                label: 'Occurrences',
                data: Object.values(riskCategories),
                backgroundColor: 'rgba(255, 154, 158, 0.8)',
                borderColor: '#ff9a9e',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#ffffff' } }
            },
            scales: {
                y: { 
                    ticks: { color: '#b8b8d1' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: { 
                    beginAtZero: true,
                    ticks: { color: '#b8b8d1' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Display recent detections
function displayRecentDetections() {
    const history = getDetectionHistory();
    const recentList = document.getElementById('recentList');
    
    if (history.length === 0) {
        recentList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <p>No detections yet. Start analyzing job postings to see your history here.</p>
                <a href="index.html" class="btn btn-primary">Start Analyzing</a>
            </div>
        `;
        return;
    }
    
    recentList.innerHTML = '';
    
    history.slice(0, 10).forEach(detection => {
        const timeAgo = getTimeAgo(new Date(detection.timestamp));
        const statusClass = detection.is_fake ? 'fake' : 'legitimate';
        const statusIcon = detection.is_fake ? '⚠️' : '✅';
        const statusText = detection.is_fake ? 'Fake Detected' : 'Legitimate';
        
        const item = document.createElement('div');
        item.className = `recent-item ${statusClass}`;
        item.innerHTML = `
            <div class="recent-icon">${statusIcon}</div>
            <div class="recent-content">
                <div class="recent-title">${statusText}</div>
                <div class="recent-details">${detection.preview}</div>
            </div>
            <div class="recent-score">${detection.score}</div>
            <div class="recent-time">${timeAgo}</div>
        `;
        
        recentList.appendChild(item);
    });
}

// Helper function to get time ago
function getTimeAgo(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
}

// Clear history function
function clearHistory() {
    if (confirm('Are you sure you want to clear all detection history? This cannot be undone.')) {
        localStorage.removeItem('jobGuardHistory');
        location.reload();
    }
}

// Initialize dashboard
function initDashboard() {
    console.log('Initializing dashboard...');
    const history = getDetectionHistory();
    console.log('Detection history:', history);
    
    updateStats();
    displayRecentDetections();
    
    // Only create charts if we have data
    if (history.length > 0) {
        createTrendChart();
        createScoreChart();
        createMethodChart();
        createRiskChart();
    }
    
    // Add clear history event listener
    const clearBtn = document.getElementById('clearHistoryBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearHistory);
    }
}



// Initialize when page loads
document.addEventListener('DOMContentLoaded', initDashboard);