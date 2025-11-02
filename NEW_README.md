# Fake Job Posting Detector

A professional web application that uses AI and machine learning to detect fraudulent job postings and provides intelligent recommendations for legitimate opportunities.

## 🌟 Features

### Core Functionality
- **AI-Powered Detection**: Machine learning model trained to identify fake job postings
- **Multi-Factor Analysis**: Analyzes multiple indicators including language patterns, contact information, and red flags
- **Real-Time Results**: Instant analysis with detailed scoring and confidence levels
- **Professional UI**: Clean, formal interface built with HTML/CSS/JavaScript

### Intelligent Chatbot
- **Smart Recommendations**: When a fake posting is detected (score < 60), the chatbot provides:
  - Relevant courses from trusted platforms (Coursera, edX, LinkedIn Learning)
  - Legitimate job opportunities from verified sources (LinkedIn, Indeed, Glassdoor)
  - Career guidance and tips
- **Context-Aware**: Analyzes the job posting content to suggest relevant courses and positions
- **Trusted Sources Only**: All recommendations link to reputable platforms and companies

## 🏗️ Architecture

### Backend (Flask API)
- **Framework**: Flask with CORS support
- **ML Model**: Scikit-learn based classifier
- **Endpoints**:
  - `POST /api/analyze` - Analyze job posting text
  - `POST /api/chat` - Chatbot interactions
  - `GET /health` - Health check

### Frontend (HTML/CSS/JS)
- **Pure Web Technologies**: No frameworks, lightweight and fast
- **Responsive Design**: Works on all devices
- **Modern UI**: Professional, formal design with smooth animations
- **Interactive Chatbot**: Real-time recommendations and guidance

## 📋 Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for external course/job links)

## 🚀 Installation

### 1. Clone or Download the Repository

```bash
cd fake-job-postings-app
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify ML Model

Ensure the trained model exists at:
```
models/fake_job_detector.pkl
```

If not, train the model first using your training script.

## 🎯 Usage

### Step 1: Start the Backend Server

```bash
cd backend
python app.py
```

The Flask server will start at `http://localhost:5000`

### Step 2: Open the Frontend

Open `frontend/index.html` in your web browser, or serve it using a simple HTTP server:

```bash
cd frontend
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

### Step 3: Analyze Job Postings

1. Paste a job posting into the text area
2. Click "Analyze Posting"
3. View the detailed results including:
   - Legitimacy score (0-100)
   - Status (Fake/Legitimate)
   - Confidence level
   - Detected red flags

### Step 4: Get Recommendations (if fake detected)

If the score is below 60:
1. The chatbot will automatically appear
2. Ask about courses or jobs
3. Click quick action buttons for instant recommendations
4. All links open to trusted platforms with apply options

## 🤖 Chatbot Features

### Trigger Conditions
- Automatically appears when legitimacy score < 60
- Provides contextual recommendations based on job posting content

### Capabilities
1. **Course Recommendations**
   - Free and paid courses from top universities
   - Platforms: Coursera, edX, LinkedIn Learning, Udemy
   - Relevant to the detected job category

2. **Job Opportunities**
   - Verified job platforms only
   - Direct links to search results
   - Trusted sources: LinkedIn, Indeed, Glassdoor

3. **Career Guidance**
   - Tips for avoiding scams
   - Job search best practices
   - Skill development advice

### Example Interactions
- "Show me relevant courses" → Lists courses with apply links
- "Show me job opportunities" → Lists trusted job platforms
- "Help me" → Provides guidance and available options

## 📊 Detection Criteria

The system analyzes multiple factors:

### Red Flags
- ⚠️ Requests for upfront payments
- ⚠️ Personal email addresses (Gmail, Yahoo, etc.)
- ⚠️ Excessive urgency or pressure tactics
- ⚠️ Vague job descriptions
- ⚠️ Missing salary/compensation information
- ⚠️ No clear requirements specified
- ⚠️ Poor grammar and formatting
- ⚠️ Generic company references

### Scoring System
- **70-100**: Likely Legitimate
- **50-69**: Suspicious (Medium Risk)
- **0-49**: Likely Fake (High Risk)

## 🔧 Configuration

### Backend Configuration

Edit `backend/app.py` to customize:
- API port (default: 5000)
- Model path
- Recommendation sources
- Detection thresholds

### Frontend Configuration

Edit `frontend/script.js` to customize:
- API base URL
- UI behavior
- Chatbot responses

## 📁 Project Structure

```
fake-job-postings-app/
├── backend/
│   └── app.py                 # Flask API server
├── frontend/
│   ├── index.html            # Main HTML page
│   ├── styles.css            # Professional styling
│   └── script.js             # JavaScript logic & chatbot
├── models/
│   └── fake_job_detector.pkl # Trained ML model
├── requirements.txt          # Python dependencies
└── NEW_README.md            # This file
```

## 🌐 Trusted Recommendation Sources

### Course Platforms
- **Coursera** - University courses and professional certificates
- **edX** - Harvard, MIT, and top university courses
- **LinkedIn Learning** - Professional skill development
- **Udemy** - Practical skill courses
- **Google Career Certificates** - Industry-recognized certifications

### Job Platforms
- **LinkedIn** - Professional networking and jobs
- **Indeed** - Comprehensive job search
- **Glassdoor** - Company reviews and salaries
- **Dribbble** - Design-specific opportunities

All links are verified and lead to legitimate, trusted sources.

## 🛡️ Security & Privacy

- No data is stored or logged
- All analysis happens in real-time
- No personal information required
- External links open in new tabs
- CORS enabled for local development

## 🐛 Troubleshooting

### Backend Not Starting
```bash
# Check if port 5000 is available
# Try a different port in app.py
app.run(debug=True, port=5001)
```

### CORS Errors
- Ensure flask-cors is installed
- Check that backend is running before opening frontend

### Model Not Found
- Verify model path in `backend/app.py`
- Ensure `fake_job_detector.pkl` exists in `models/` directory

### Chatbot Not Appearing
- Chatbot only appears when score < 60
- Check browser console for errors
- Ensure backend is running and accessible

## 🔄 Future Enhancements

- [ ] User authentication and history
- [ ] Save analysis results
- [ ] Email alerts for suspicious postings
- [ ] Browser extension
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Company verification database

## 📝 License

This project is for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- All features are tested
- Documentation is updated

## 📧 Support

For issues or questions:
1. Check troubleshooting section
2. Review console logs
3. Verify all dependencies are installed

## ⚠️ Disclaimer

This tool provides analysis based on patterns and should not be the sole factor in job-seeking decisions. Always verify opportunities through official channels and use your best judgment.

---

**Built with ❤️ to protect job seekers from fraud**
