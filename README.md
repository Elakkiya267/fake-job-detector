# Fake Job & Internship Postings Detection System

A comprehensive ML-powered system to detect fraudulent job postings with an interactive web interface and analytics dashboard.

## Features
- **Fake Job Detection**: AI-powered analysis of job postings
- **Analytics Dashboard**: Real-time metrics and visualizations
- **ML Model**: TF-IDF + Logistic Regression classifier
- **Performance Tracking**: Detailed model metrics and insights
- **Modern UI**: Beautiful, responsive Streamlit interface

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
# Enhanced training with metrics logging
python src/train_enhanced.py

# OR basic training
python src/train_ml_model.py
```

### 3. Run the Applications

**Main Detection App:**
```bash
streamlit run src/app.py
```

**Analytics Dashboard:**
```bash
streamlit run src/analytics_dashboard.py
```

## Project Structure
```
fake-job-postings-app/
├── src/
│   ├── app.py                    # Main detection interface
│   ├── analytics_dashboard.py   # Analytics & metrics dashboard
│   ├── train_enhanced.py         # Enhanced model training
│   ├── train_ml_model.py         # Basic model training
│   └── data_preprocessing.py     # Data preprocessing
├── data/
│   └── job-description-dataset.csv
├── models/
│   ├── fake_job_detector.pkl     # Trained model
│   └── training_metrics.json     # Performance metrics
├── requirements.txt
├── README.md
└── DASHBOARD_README.md           # Dashboard documentation
```

## Usage

### Detection App
1. Paste a job posting into the text area
2. Click "Detect Now"
3. View legitimacy score and red flags
4. Get recommendations

### Analytics Dashboard
- **Overview**: Key metrics and detection trends
- **Model Performance**: Accuracy, precision, recall, confusion matrix
- **Detection trends**: Time series analysis
- **Data Insights**: Dataset statistics and visualizations
- **Feature Analysis**: Top indicators for fake/legitimate jobs

## Dataset
Optional: Use Kaggle job dataset for training
1. Setup Kaggle API: `pip install kaggle`
2. Download: `python src/download_data.py`
3. Preprocess: `python src/data_preprocessing.py`

## Model Performance
- **Accuracy**: ~85-95% (depends on training data)
- **Method**: TF-IDF vectorization + Logistic Regression
- **Features**: 500 TF-IDF features with bigrams
- **Detection**: Rule-based + ML hybrid approach

## Red Flags Detected
- **Upfront payment requests**
- **Personal email domains (Gmail, Yahoo, etc.)**
- **Excessive urgency**
- **Vague job descriptions**
- **Missing salary/requirements**
- **Poor grammar and formatting**

## Notes
- Training on CPU: ~1-2 mins for synthetic data
- Dashboard uses simulated detection history for demo
- Model works with rule-based fallback if not trained
- See `DASHBOARD_README.md` for detailed dashboard documentation

## Future Enhancements
- Real-time detection API
- User feedback integration
- Multi-language support
- Deep learning models
- Browser extension