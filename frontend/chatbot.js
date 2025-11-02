// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const chatInput = document.getElementById('chatInput');
const sendChatBtn = document.getElementById('sendChatBtn');
const quickActionBtns = document.querySelectorAll('.quick-action-btn');

// Global state
let currentAnalysis = null;

// Send Chat Message
async function sendMessage(message) {
    if (!message.trim()) return;
    
    // Add user message
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                context: currentAnalysis || {}
            })
        });
        
        if (!response.ok) {
            throw new Error('Chat failed');
        }
        
        const result = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add bot response
        addBotResponse(result.response);
        
    } catch (error) {
        console.error('Chat Error:', error);
        removeTypingIndicator(typingId);
        addChatMessage('Connection error. Please check if the backend server is running on port 5000.', 'bot');
    }
}

// Add Chat Message
function addChatMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message`;
    
    const avatar = sender === 'user' ? '👤' : '🤖';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${message}</p>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Add Bot Response with Rich Formatting
function addBotResponse(response) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message bot-message';
    
    // Convert markdown-like formatting to HTML
    let formattedResponse = response
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>')
        .replace(/(\d+\.\s)/g, '<br>$1');
    
    // Convert URLs to clickable links
    formattedResponse = formattedResponse.replace(
        /(https?:\/\/[^\s]+)/g, 
        '<a href="$1" target="_blank">🔗 View Course</a>'
    );
    
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            ${formattedResponse}
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Typing Indicator
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot-message typing-indicator';
    typingDiv.id = 'typing-' + Date.now();
    
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <p>Typing...</p>
        </div>
    `;
    
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return typingDiv.id;
}

function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Event Listeners
sendChatBtn.addEventListener('click', () => {
    sendMessage(chatInput.value);
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage(chatInput.value);
    }
});

quickActionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const message = btn.getAttribute('data-message');
        sendMessage(message);
    });
});

// Check backend health on load
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected successfully');
        } else {
            throw new Error('Backend not responding');
        }
    } catch (error) {
        console.warn('⚠️ Backend not available:', error);
        addChatMessage('⚠️ Backend server is not running. Please start: python backend/app.py', 'bot');
    }
}

// Initialize
checkBackendHealth();