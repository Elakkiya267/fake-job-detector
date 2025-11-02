"""
Train ML model for fake job detection
Uses TF-IDF + Logistic Regression for text classification
"""
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import os

print("=" * 60)
print("TRAINING FAKE JOB POSTING DETECTOR")
print("=" * 60)

# Since we don't have labeled data, create synthetic training data
# In production, you'd use a real dataset like the Employment Scam Aegean Dataset
print("\n[1] Creating synthetic training data...")

# Fake job postings (fraudulent=1)
fake_jobs = [
    "URGENT! Make $5000/week working from home! No experience needed! Pay $99 registration fee. Contact: jobs@gmail.com",
    "Earn thousands weekly! Easy money from home! Just pay training fee of $150. Email: opportunity@yahoo.com",
    "Immediate hire! Work from anywhere! Guaranteed income $3000+! Wire transfer $50 processing fee to start.",
    "Limited time offer! No experience required! Make money fast! Pay upfront fee. Contact: hiring@hotmail.com",
    "Act now! Easy work from home! Earn big money! Send $75 registration fee. Email us at jobs123@gmail.com",
    "URGENT HIRING! No qualifications needed! Guaranteed salary! Pay small fee to begin. jobs@outlook.com",
    "Make money immediately! Work from home! Just $100 startup fee! Contact fastcash@yahoo.com today!",
    "Too good to be true opportunity! Earn while you sleep! Pay processing fee $80. Email: money@gmail.com",
    "Immediate start! No interview! Guaranteed income! Western Union payment required. jobs@hotmail.com",
    "Easy money! Work from home! No skills needed! Pay training fee now! Limited spots! urgent@gmail.com"
]

# Legitimate job postings (fraudulent=0)
legit_jobs = [
    "Software Engineer at TechCorp Inc. Requirements: 3+ years experience with Python, React. Salary: $120k-$160k. Benefits: health insurance, 401k. Apply at careers@techcorp.com",
    "Marketing Manager needed. Bachelor's degree required. 5 years experience in digital marketing. Competitive salary and benefits. Send resume to hr@company.com",
    "Data Scientist position. PhD in Computer Science preferred. Experience with machine learning, Python, SQL. Salary range $140k-$180k. Apply through our website.",
    "Full Stack Developer role. Requirements: JavaScript, Node.js, React, 2+ years experience. Salary $100k-$130k. Health benefits, remote work options. careers@startup.com",
    "Product Manager at FinTech company. MBA preferred. 4+ years product management experience. Competitive compensation package. Apply at jobs@fintech.com",
    "Senior Accountant position. CPA required. 5+ years experience. Salary $80k-$100k. Full benefits package. Send resume to accounting@firm.com",
    "UX Designer needed. Portfolio required. 3+ years experience. Proficient in Figma, Adobe XD. Salary $90k-$120k. Apply at design@agency.com",
    "DevOps Engineer role. AWS/Azure certification preferred. 4+ years experience. Salary $130k-$170k. Stock options available. careers@tech.com",
    "Business Analyst position. Bachelor's degree in Business. SQL, Excel proficiency. 2+ years experience. Salary $70k-$90k. hr@consulting.com",
    "Project Manager needed. PMP certification required. 6+ years experience. Salary $110k-$140k. Comprehensive benefits. jobs@enterprise.com"
]

# Create DataFrame
data = pd.DataFrame({
    'text': fake_jobs + legit_jobs,
    'fraudulent': [1]*len(fake_jobs) + [0]*len(legit_jobs)
})

print(f"   Created {len(data)} training samples")
print(f"   Fake jobs: {sum(data['fraudulent'])} | Legit jobs: {len(data) - sum(data['fraudulent'])}")

# Split data
print("\n[2] Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    data['text'], data['fraudulent'], test_size=0.3, random_state=42
)
print(f"   Train: {len(X_train)} | Test: {len(X_test)}")

# Create TF-IDF vectorizer
print("\n[3] Creating TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=500,
    ngram_range=(1, 2),
    stop_words='english'
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
print(f"   Feature dimensions: {X_train_tfidf.shape[1]}")

# Train model
print("\n[4] Training Logistic Regression model...")
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_tfidf, y_train)
print("   Model trained successfully!")

# Evaluate
print("\n[5] Evaluating model...")
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"   Accuracy: {accuracy:.2%}")
print("\n   Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fake']))

# Save model and vectorizer
print("\n[6] Saving model...")
os.makedirs('models', exist_ok=True)
with open('models/fake_job_detector.pkl', 'wb') as f:
    pickle.dump({'model': model, 'vectorizer': vectorizer}, f)
print("   Model saved to: models/fake_job_detector.pkl")

# Test predictions
print("\n[7] Testing predictions...")
test_cases = [
    "URGENT! Easy money from home! Pay fee now!",
    "Software Engineer at Google. 5 years experience required. Competitive salary."
]
for i, test_text in enumerate(test_cases, 1):
    test_vec = vectorizer.transform([test_text])
    prediction = model.predict(test_vec)[0]
    probability = model.predict_proba(test_vec)[0]
    print(f"\n   Test {i}: {test_text[:50]}...")
    print(f"   Prediction: {'FAKE' if prediction == 1 else 'LEGITIMATE'}")
    print(f"   Confidence: {max(probability):.1%}")

print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETE!")
print("=" * 60)
