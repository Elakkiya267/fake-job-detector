import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize Kaggle API
api = KaggleApi()
try:
    api.authenticate()
except Exception as e:
    print(f"Authentication failed. Ensure kaggle.json is in ~/.kaggle/: {e}")
    exit(1)

# Download dataset
dataset_slug = "ravindrasinghrana/job-description-dataset"
download_path = f"data/{dataset_slug.split('/')[-1]}.zip"

os.makedirs("data", exist_ok=True)
try:
    api.dataset_download_files(dataset_slug, path="data", unzip=False)
    print(f"Downloaded dataset to {download_path}")
except Exception as e:
    print(f"Download failed: {e}")
    exit(1)

# Unzip
try:
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall("data")
    os.remove(download_path)  # Clean up ZIP file
    print("Unzipped dataset to data/Job_Description_Dataset.csv")
except Exception as e:
    print(f"Unzipping failed: {e}")
    exit(1)