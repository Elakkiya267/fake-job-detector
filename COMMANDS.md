# 🚀 Quick Command Reference

## Setup Commands

### First Time Setup
```bash
# Install all dependencies
pip install -r requirements.txt
```

## Training Commands

### Train Model (Recommended - with Analytics)
```bash
# Enhanced training that generates metrics for dashboard
python src/train_enhanced.py
```

### Train Model (Basic)
```bash
# Basic training without detailed metrics
python src/train_ml_model.py
```

## Running the Applications

### Main Detection App
```bash
# Run the fake job detector interface
streamlit run src/app.py
```
- Opens at: `http://localhost:8501`
- Features: Job posting analysis, detection, recommendations

### Analytics Dashboard
```bash
# Run the analytics and metrics dashboard
streamlit run src/analytics_dashboard.py
```
- Opens at: `http://localhost:8501`
- Features: Model metrics, trends, data insights, feature analysis

### Run Both (Different Ports)
```bash
# Terminal 1 - Main app on port 8501
streamlit run src/app.py

# Terminal 2 - Dashboard on port 8502
streamlit run src/analytics_dashboard.py --server.port 8502
```

## Optional: Kaggle Dataset Commands

### Setup Kaggle API
```bash
# Install Kaggle
pip install kaggle

# Place kaggle.json in:
# Windows: C:\Users\<username>\.kaggle\kaggle.json
# Linux/Mac: ~/.kaggle/kaggle.json
```

### Download and Process Data
```bash
# Download dataset from Kaggle
python src/download_data.py

# Preprocess the data
python src/data_preprocessing.py
```

## Testing Commands

### Test the Detector
```bash
# Run test script
python test_detector.py
```

### Quick Test
```bash
# Run quick validation
python quick_test.py
```

### Demo
```bash
# Run demo script
python demo.py
```

## Troubleshooting Commands

### Check Python Version
```bash
python --version
# Should be Python 3.8+
```

### Check Installed Packages
```bash
pip list
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Clear Streamlit Cache
```bash
streamlit cache clear
```

## Development Commands

### Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Freeze Dependencies
```bash
pip freeze > requirements.txt
```

## Port Configuration

### Change Streamlit Port
```bash
# Run on custom port
streamlit run src/app.py --server.port 8080
```

### Run in Browser
```bash
# Auto-open browser
streamlit run src/app.py --server.headless false
```

### Run Without Browser
```bash
# Don't open browser
streamlit run src/app.py --server.headless true
```

## Common Workflows

### Complete Setup & Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train model
python src/train_enhanced.py

# 3. Run main app
streamlit run src/app.py
```

### View Analytics
```bash
# 1. Ensure model is trained
python src/train_enhanced.py

# 2. Run dashboard
streamlit run src/analytics_dashboard.py
```

### Update and Retrain
```bash
# 1. Update code
git pull  # if using git

# 2. Update dependencies
pip install -r requirements.txt --upgrade

# 3. Retrain model
python src/train_enhanced.py

# 4. Restart apps
streamlit run src/app.py
```

## File Locations

### Model Files
- `models/fake_job_detector.pkl` - Trained model
- `models/training_metrics.json` - Performance metrics

### Data Files
- `data/job-description-dataset.csv` - Job dataset
- `data/train.jsonl` - Preprocessed training data

### Source Files
- `src/app.py` - Main detection app
- `src/analytics_dashboard.py` - Analytics dashboard
- `src/train_enhanced.py` - Enhanced training script

## Quick Tips

### Stop Running App
- Press `Ctrl + C` in terminal

### Refresh App
- Press `R` in browser or `Ctrl + R`

### Clear Cache
- Press `C` in browser while app is running

### View Logs
- Check terminal output for errors and warnings

### Multiple Instances
- Use different ports for multiple apps:
  ```bash
  streamlit run src/app.py --server.port 8501
  streamlit run src/analytics_dashboard.py --server.port 8502
  ```

## Environment Variables (Optional)

```bash
# Set Streamlit theme
export STREAMLIT_THEME=dark

# Set max upload size (MB)
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
```

## Production Deployment

### Streamlit Cloud
```bash
# Push to GitHub
git add .
git commit -m "Deploy to Streamlit Cloud"
git push

# Deploy via streamlit.io
```

### Docker (if needed)
```bash
# Build image
docker build -t fake-job-detector .

# Run container
docker run -p 8501:8501 fake-job-detector
```

## Help Commands

### Streamlit Help
```bash
streamlit --help
```

### Python Help
```bash
python --help
```

### Pip Help
```bash
pip --help
```
