# 🛡️ Enhanced Fake Job Postings Detection System

A comprehensive ML-powered system to detect fraudulent job postings with **image upload capability** and an **intelligent career chatbot**.

## ✨ New Features

### 📸 Image Upload & OCR
- **Upload job posting images** (JPG, PNG, GIF up to 5MB)
- **Automatic text extraction** using Tesseract OCR
- **Drag & drop support** for easy image uploads
- **Image preview** with text extraction display

### 🤖 Enhanced Career Chatbot
- **Intelligent responses** based on job analysis
- **Personalized course recommendations** from trusted platforms
- **Legitimate job platform suggestions**
- **Career safety tips** and scam prevention advice
- **Interactive quick actions** for common queries

### 🎨 Modern UI Improvements
- **Tabbed interface** for text/image input
- **Enhanced visual feedback** for analysis results
- **Responsive design** for all devices
- **Improved chat interface** with rich formatting

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup OCR (Required for Image Upload)
```bash
# Run the setup script
python install_ocr.py

# Follow the instructions for your operating system
```

**Windows Users:**
- Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Or use: `winget install UB-Mannheim.TesseractOCR`

**macOS Users:**
```bash
brew install tesseract
```

**Linux Users:**
```bash
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
sudo yum install tesseract          # CentOS/RHEL
```

### 3. Train the Model (Optional)
```bash
python src/train_enhanced.py
```

### 4. Start the Backend
```bash
cd backend
python app.py
```

### 5. Open the Frontend
Open `frontend/index.html` in your browser or serve it locally:
```bash
# Using Python's built-in server
cd frontend
python -m http.server 8080
# Then visit: http://localhost:8080
```

## 📋 How to Use

### Method 1: Text Input
1. Click **"📝 Paste Text"** tab
2. Paste the job posting content
3. Click **"Analyze Posting"**

### Method 2: Image Upload
1. Click **"📷 Upload Image"** tab
2. Upload or drag & drop job posting image
3. Click **"Analyze Posting"**
4. View extracted text and analysis results

### Chatbot Interaction
When a potentially fake job is detected:
1. **Ask about courses**: "Show me relevant courses"
2. **Ask about jobs**: "Find legitimate job opportunities"
3. **Get safety tips**: "How to avoid job scams"
4. **General help**: "Help me with career advice"

## 🎯 Detection Capabilities

### Red Flags Detected
- ⚠️ **Upfront payment requests**
- 📧 **Personal email domains** (Gmail, Yahoo, etc.)
- ⏰ **Excessive urgency** language
- 📝 **Vague job descriptions**
- 💰 **Missing salary information**
- 📋 **No clear requirements**
- ✍️ **Poor grammar and formatting**

### Analysis Methods
- 🤖 **Machine Learning Model** (TF-IDF + Logistic Regression)
- 📊 **Rule-based Detection** for known patterns
- 🔍 **Multi-factor Analysis** combining various indicators

## 🎓 Chatbot Knowledge Base

### Course Recommendations
- **Free Courses**: Harvard CS50, freeCodeCamp, Coursera (audit mode)
- **Paid Courses**: Udemy, GUVI, LinkedIn Learning
- **Categories**: Software Development, Data Science, Design, Marketing, Business

### Job Platforms
- **Trusted Sources**: Naukri, LinkedIn Jobs, Indeed, Glassdoor
- **Verified Employers**: Platforms with company verification
- **Safety Features**: Scam protection and reporting systems

### Career Guidance
- **Interview Preparation** tips
- **Resume Building** advice
- **Skill Development** roadmaps
- **Industry Insights** and trends

## 🛠️ Technical Architecture

```
fake-job-postings-app/
├── backend/
│   └── app.py                 # Flask API with OCR support
├── frontend/
│   ├── index.html            # Enhanced UI with image upload
│   ├── script.js             # JavaScript with OCR handling
│   └── styles.css            # Modern responsive design
├── models/
│   ├── fake_job_detector.pkl # Trained ML model
│   └── training_metrics.json # Performance metrics
├── src/                      # Training scripts
├── data/                     # Dataset files
├── install_ocr.py           # OCR setup script
└── requirements.txt         # Updated dependencies
```

## 🔧 API Endpoints

### POST /api/analyze
Analyze job posting from text or image:
```json
{
  "text": "job posting content",     // For text input
  "image": "base64_image_data"    // For image input
}
```

Response:
```json
{
  "score": 85,
  "is_fake": false,
  "confidence": "High",
  "method": "ML + rules",
  "source": "image",              // "text" or "image"
  "extracted_text": "...",       // Only for image input
  "flags": ["✅ No major red flags detected"],
  "recommendations": {            // Only if score < 60
    "courses": [...],
    "jobs": [...]
  }
}
```

### POST /api/chat
Interact with career chatbot:
```json
{
  "message": "Show me courses",
  "context": { /* analysis result */ }
}
```

## 📊 Performance Metrics

- **Accuracy**: 85-95% (depends on training data)
- **OCR Accuracy**: 90%+ for clear images
- **Response Time**: <2 seconds for analysis
- **Image Processing**: <5 seconds for OCR extraction

## 🔒 Security & Privacy

- **No data storage**: Images and text are processed in memory only
- **Local processing**: OCR runs on your machine
- **Secure recommendations**: Only trusted educational and job platforms
- **Privacy-first**: No personal information required

## 🐛 Troubleshooting

### OCR Issues
```bash
# Check Tesseract installation
tesseract --version

# Run setup script
python install_ocr.py

# Manual configuration (Windows)
# Add to backend/app.py:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Backend Issues
```bash
# Check if Flask is running
curl http://localhost:5000/health

# Install missing dependencies
pip install -r requirements.txt

# Check Python version (3.7+ required)
python --version
```

### Frontend Issues
- **CORS errors**: Make sure backend is running on port 5000
- **Image upload fails**: Check file size (<5MB) and format (JPG/PNG/GIF)
- **Chatbot not responding**: Verify backend connection

## 🚀 Future Enhancements

- 🌐 **Multi-language support** for global job markets
- 🔗 **Browser extension** for real-time protection
- 📱 **Mobile app** for on-the-go scanning
- 🧠 **Deep learning models** for better accuracy
- 📈 **Analytics dashboard** for detection trends
- 🔔 **Real-time alerts** for new scam patterns

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Run `python install_ocr.py` for OCR setup help
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Verify backend is running: `python backend/app.py`

## 📄 License

This project is open source and available under the MIT License.

---

**Stay Safe! 🛡️** Always verify job opportunities through official company websites and trusted platforms.