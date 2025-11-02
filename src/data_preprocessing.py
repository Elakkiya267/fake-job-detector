import pandas as pd
import json
import os

# Load dataset
try:
    df = pd.read_csv("data/job-description-dataset.csv")
except FileNotFoundError:
    print("Error: Job_Description_Dataset.csv not found in data/")
    exit(1)

# Basic cleaning
df = df.dropna(subset=['title', 'description', 'company', 'location'])
df = df.drop_duplicates(subset=['title', 'description'])

# Optional: Filter for internships
# df = df[df['title'].str.contains("intern", case=False, na=False)]

# Create prompts
prompts = []
for _, row in df.iterrows():
    prompt = f"Generate a job posting for {row['title']} at {row['company']} in {row['location']}. Description: {row['description']}\nGenerated Posting:"
    prompts.append({"text": prompt})

# Save to JSONL
os.makedirs("data", exist_ok=True)
with open("data/train.jsonl", "w") as f:
    for item in prompts:
        f.write(json.dumps(item) + "\n")

print(f"Preprocessed {len(prompts)} samples to data/train.jsonl")