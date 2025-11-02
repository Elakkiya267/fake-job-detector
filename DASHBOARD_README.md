# 📊 Analytics Dashboard - Fake Job Detector

## Overview
A comprehensive analytics dashboard for visualizing model performance, detection trends, and dataset insights for the Fake Job Posting Detection system.

## Features

### 📊 Overview Tab
- **Key Metrics**: Total detections, fake jobs detected, average confidence, model accuracy
- **Detection Trends**: 30-day time series visualization
- **Distribution Charts**: Pie chart showing legitimate vs fake job distribution
- **Real-time Insights**: Automated insights based on detection patterns

### 🤖 Model Performance Tab
- **Accuracy Metrics**: Precision, Recall, F1 Score, ROC AUC
- **Confusion Matrix**: Visual representation of model predictions
- **Performance Comparison**: Bar charts comparing different metrics
- **Training Statistics**: Sample counts and model parameters

### 📈 Detection Trends Tab
- **Daily Volume Analysis**: Bar charts showing detection volume over time
- **Fake Job Percentage**: Time series of fraud rate trends
- **Confidence Distribution**: Histogram of prediction confidence scores
- **Weekly Comparison**: Box plots comparing weekly performance

### 🗂️ Data Insights Tab
- **Dataset Statistics**: Total jobs, companies, countries, roles
- **Top Companies**: Bar chart of companies with most postings
- **Geographic Distribution**: Pie chart of job postings by country
- **Work Type Analysis**: Distribution of full-time, part-time, contract, intern positions
- **Data Preview**: Interactive table showing sample job postings

### 🔍 Feature Analysis Tab
- **Top Fake Indicators**: Keywords and phrases that indicate fraudulent postings
- **Top Legitimate Indicators**: Features associated with real job postings
- **Feature Importance Heatmap**: Visual representation of feature weights
- **Model Coefficients**: Detailed analysis of TF-IDF features

## Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `streamlit` - Web framework
- `plotly` - Interactive visualizations
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `scikit-learn` - ML model

### 2. Train the Model (Enhanced Version)
```bash
python src/train_enhanced.py
```

This will:
- Train the ML model
- Save model to `models/fake_job_detector.pkl`
- Generate metrics to `models/training_metrics.json`

### 3. Run the Analytics Dashboard
```bash
streamlit run src/analytics_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Commands Summary

```bash
# Setup (first time)
pip install -r requirements.txt

# Train model with metrics
python src/train_enhanced.py

# Run main detection app
streamlit run src/app.py

# Run analytics dashboard
streamlit run src/analytics_dashboard.py
```

## Dashboard Components

### Sidebar Controls
- **Date Range Filter**: Select time period for analysis
- **Quick Stats**: Model accuracy and training samples
- **Refresh Button**: Reload data
- **Model Status**: Check if model is loaded

### Interactive Features
- **Hover Details**: Hover over charts for detailed information
- **Zoom & Pan**: Interactive chart controls
- **Export**: Download charts as images
- **Responsive Design**: Works on desktop and tablet

## Data Sources

### Model Metrics (`models/training_metrics.json`)
Contains:
- Accuracy, Precision, Recall, F1 Score
- Confusion matrix values
- Feature importance data
- Training parameters
- Top fake/legitimate indicators

### Dataset (`data/job-description-dataset.csv`)
Contains:
- Job titles and descriptions
- Company information
- Location and country data
- Salary ranges
- Work types
- Skills and requirements

### Detection History (Simulated)
- 30 days of detection data
- Daily detection volumes
- Fake job percentages
- Confidence scores

## Customization

### Modify Color Schemes
Edit the CSS in `analytics_dashboard.py`:
```python
# Change gradient colors
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add New Metrics
1. Update `train_enhanced.py` to calculate new metrics
2. Save to `training_metrics.json`
3. Add visualization in `analytics_dashboard.py`

### Change Time Periods
Modify the `generate_detection_history()` function:
```python
dates = pd.date_range(end=datetime.now(), periods=60, freq='D')  # 60 days
```

## Troubleshooting

### Model Not Found
**Error**: "⚠️ Model Not Found"
**Solution**: Run `python src/train_enhanced.py` first

### No Metrics Available
**Error**: "⚠️ No training metrics available"
**Solution**: Use `train_enhanced.py` instead of `train_ml_model.py`

### Dataset Not Found
**Error**: "⚠️ Dataset not found"
**Solution**: Ensure `data/job-description-dataset.csv` exists

### Import Errors
**Error**: "ModuleNotFoundError: No module named 'plotly'"
**Solution**: Run `pip install plotly kaleido`

## Performance Tips

1. **Large Datasets**: The dashboard uses caching (`@st.cache_data`) for performance
2. **Refresh Data**: Click "Refresh Data" button to reload without restarting
3. **Browser Performance**: Close unused tabs for better chart rendering

## Analytics Insights

### Key Metrics to Monitor
- **Accuracy**: Should be > 85% for production use
- **Precision**: Minimize false positives (legitimate jobs marked as fake)
- **Recall**: Minimize false negatives (fake jobs marked as legitimate)
- **F1 Score**: Balance between precision and recall

### Red Flags in Data
- Sudden spike in fake job detections
- Drop in model confidence scores
- Unusual geographic patterns
- High false positive rate

## Future Enhancements

Potential additions:
- [ ] Real-time detection streaming
- [ ] A/B testing different models
- [ ] User feedback integration
- [ ] Automated alerting system
- [ ] Export reports to PDF
- [ ] API endpoint monitoring
- [ ] Multi-model comparison
- [ ] Historical trend analysis

## Screenshots

The dashboard includes:
- 📊 Modern gradient design with purple/blue theme
- 📈 Interactive Plotly charts
- 🎯 Responsive metric cards
- 🔥 Feature importance heatmaps
- 📉 Time series visualizations

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main README.md
3. Ensure all dependencies are installed
4. Verify model training completed successfully

## License

Part of the Fake Job Postings Detection project.
