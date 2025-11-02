"""
Enhanced ML Model Training with Detailed Metrics Logging
Trains fake job detector and saves comprehensive analytics
"""
import pandas as pd
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve
)
import os
from datetime import datetime
import numpy as np

print("=" * 70)
print("ENHANCED TRAINING: FAKE JOB POSTING DETECTOR")
print("=" * 70)

# Create synthetic training data (expanded dataset)
print("\n[1] Creating training data...")

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
    "Easy money! Work from home! No skills needed! Pay training fee now! Limited spots! urgent@gmail.com",
    "Get rich quick! Multiple income streams! No experience! Pay $200 to start earning thousands!",
    "URGENT: Personal assistant needed! Work from home! Send $50 for background check. jobs@yahoo.com",
    "Guaranteed $10,000 per month! Easy work! Just pay $150 registration. No interview needed!",
    "Make money online! Click ads and earn! Pay $99 activation fee. Start today! money@gmail.com",
    "Work from anywhere! Set your own hours! Guaranteed income! Pay processing fee to begin.",
    "Immediate cash! No experience! Work from home! Send payment to secure your position today!",
    "Limited time! High paying job! No qualifications! Pay small fee! Contact: quickjobs@hotmail.com",
    "Earn $5000 weekly! Simple tasks! No skills required! Pay $120 to get started immediately!",
    "URGENT opportunity! Make money fast! Work from home! Wire $75 to begin earning today!",
    "Easy income! No experience needed! Guaranteed salary! Pay registration fee now! jobs@gmail.com",
]

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
    "Project Manager needed. PMP certification required. 6+ years experience. Salary $110k-$140k. Comprehensive benefits. jobs@enterprise.com",
    "Senior Software Engineer at Microsoft. 5+ years experience. C#, .NET, Azure. Salary $150k-$200k. Full benefits. careers@microsoft.com",
    "Data Analyst position. Bachelor's in Statistics or related field. Python, R, SQL required. Salary $75k-$95k. Apply at analytics@company.com",
    "Frontend Developer at Amazon. React, TypeScript, 3+ years experience. Competitive salary and stock options. Apply through Amazon careers portal.",
    "Machine Learning Engineer. PhD preferred. TensorFlow, PyTorch experience. Salary $160k-$220k. Benefits included. ml@aicompany.com",
    "Cybersecurity Analyst. CISSP certification. 4+ years experience. Salary $110k-$150k. Remote options available. security@techfirm.com",
    "Cloud Architect at Google. 7+ years experience. GCP, AWS expertise. Salary $180k-$250k. Stock grants. Apply at google.com/careers",
    "QA Engineer position. Automation testing experience. Selenium, Python. Salary $85k-$115k. Benefits package. qa@software.com",
    "Technical Writer needed. 3+ years experience. Strong communication skills. Salary $70k-$90k. Remote work. docs@company.com",
    "Database Administrator. Oracle, PostgreSQL experience. 5+ years. Salary $100k-$140k. Full benefits. dba@enterprise.com",
    "Systems Administrator. Linux, Windows Server experience. 4+ years. Salary $90k-$120k. Health benefits. sysadmin@tech.com",
]

# Create DataFrame
data = pd.DataFrame({
    'text': fake_jobs + legit_jobs,
    'fraudulent': [1]*len(fake_jobs) + [0]*len(legit_jobs)
})

print(f"   ✓ Created {len(data)} training samples")
print(f"   ✓ Fake jobs: {sum(data['fraudulent'])} ({sum(data['fraudulent'])/len(data)*100:.1f}%)")
print(f"   ✓ Legit jobs: {len(data) - sum(data['fraudulent'])} ({(len(data)-sum(data['fraudulent']))/len(data)*100:.1f}%)")

# Split data
print("\n[2] Splitting data into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    data['text'], data['fraudulent'], test_size=0.3, random_state=42, stratify=data['fraudulent']
)
print(f"   ✓ Training set: {len(X_train)} samples")
print(f"   ✓ Test set: {len(X_test)} samples")

# Create TF-IDF vectorizer
print("\n[3] Creating TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=500,
    ngram_range=(1, 2),
    stop_words='english',
    min_df=1
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
print(f"   ✓ Feature dimensions: {X_train_tfidf.shape[1]}")
print(f"   ✓ Vocabulary size: {len(vectorizer.vocabulary_)}")

# Train model
print("\n[4] Training Logistic Regression model...")
model = LogisticRegression(
    random_state=42, 
    max_iter=1000,
    C=1.0,
    solver='liblinear'
)
model.fit(X_train_tfidf, y_train)
print("   ✓ Model trained successfully!")

# Evaluate on test set
print("\n[5] Evaluating model performance...")
y_pred = model.predict(X_test_tfidf)
y_pred_proba = model.predict_proba(X_test_tfidf)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

# ROC AUC
roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])

print(f"\n   📊 PERFORMANCE METRICS:")
print(f"   {'='*50}")
print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
print(f"   F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
print(f"   ROC AUC:   {roc_auc:.4f}")
print(f"   {'='*50}")

print(f"\n   📈 CONFUSION MATRIX:")
print(f"   {'='*50}")
print(f"   True Negatives:  {tn}")
print(f"   False Positives: {fp}")
print(f"   False Negatives: {fn}")
print(f"   True Positives:  {tp}")
print(f"   {'='*50}")

print("\n   📋 CLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fake']))

# Save model and vectorizer
print("\n[6] Saving model and vectorizer...")
os.makedirs('models', exist_ok=True)
with open('models/fake_job_detector.pkl', 'wb') as f:
    pickle.dump({'model': model, 'vectorizer': vectorizer}, f)
print("   ✓ Model saved to: models/fake_job_detector.pkl")

# Save comprehensive metrics for dashboard
print("\n[7] Saving training metrics for analytics dashboard...")
metrics = {
    'timestamp': datetime.now().isoformat(),
    'model_type': 'Logistic Regression',
    'vectorizer_type': 'TF-IDF',
    
    # Dataset info
    'total_samples': len(data),
    'train_samples': len(X_train),
    'test_samples': len(X_test),
    'fake_samples': int(sum(data['fraudulent'])),
    'legit_samples': int(len(data) - sum(data['fraudulent'])),
    
    # Performance metrics
    'accuracy': float(accuracy),
    'precision': float(precision),
    'recall': float(recall),
    'f1_score': float(f1),
    'roc_auc': float(roc_auc),
    
    # Confusion matrix
    'true_positives': int(tp),
    'true_negatives': int(tn),
    'false_positives': int(fp),
    'false_negatives': int(fn),
    
    # Feature info
    'num_features': X_train_tfidf.shape[1],
    'vocabulary_size': len(vectorizer.vocabulary_),
    
    # Model parameters
    'max_features': 500,
    'ngram_range': [1, 2],
    'max_iter': 1000,
    'C': 1.0,
    
    # Top features
    'top_fake_indicators': [],
    'top_legit_indicators': []
}

# Extract top features
feature_names = vectorizer.get_feature_names_out()
coefficients = model.coef_[0]

# Top 15 fake indicators (positive coefficients)
top_fake_idx = np.argsort(coefficients)[-15:]
metrics['top_fake_indicators'] = [
    {'feature': feature_names[i], 'coefficient': float(coefficients[i])}
    for i in reversed(top_fake_idx)
]

# Top 15 legitimate indicators (negative coefficients)
top_legit_idx = np.argsort(coefficients)[:15]
metrics['top_legit_indicators'] = [
    {'feature': feature_names[i], 'coefficient': float(coefficients[i])}
    for i in top_legit_idx
]

# Save metrics
with open('models/training_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
print("   ✓ Metrics saved to: models/training_metrics.json")

# Test predictions
print("\n[8] Testing predictions on sample data...")
test_cases = [
    ("URGENT! Easy money from home! Pay fee now!", "Fake"),
    ("Software Engineer at Google. 5 years experience required. Competitive salary.", "Legitimate"),
    ("Make $10000 weekly! No experience! Pay $99 to start!", "Fake"),
    ("Data Scientist position. PhD required. Machine learning experience. Apply at careers@company.com", "Legitimate")
]

print(f"\n   {'='*70}")
for i, (test_text, expected) in enumerate(test_cases, 1):
    test_vec = vectorizer.transform([test_text])
    prediction = model.predict(test_vec)[0]
    probability = model.predict_proba(test_vec)[0]
    
    pred_label = "FAKE" if prediction == 1 else "LEGITIMATE"
    confidence = max(probability)
    
    status = "✓" if pred_label == expected.upper() else "✗"
    
    print(f"\n   Test {i}: {test_text[:60]}...")
    print(f"   Expected: {expected} | Predicted: {pred_label} {status}")
    print(f"   Confidence: {confidence:.1%}")
    print(f"   Probabilities: Legit={probability[0]:.3f}, Fake={probability[1]:.3f}")

print(f"\n   {'='*70}")

# Summary
print("\n" + "=" * 70)
print("✅ MODEL TRAINING COMPLETE!")
print("=" * 70)
print(f"\n📊 Summary:")
print(f"   • Model Accuracy: {accuracy:.2%}")
print(f"   • Total Samples: {len(data)}")
print(f"   • Features: {X_train_tfidf.shape[1]}")
print(f"   • Files Saved:")
print(f"     - models/fake_job_detector.pkl")
print(f"     - models/training_metrics.json")
print(f"\n🚀 Next Steps:")
print(f"   1. Run the main app: streamlit run src/app.py")
print(f"   2. View analytics: streamlit run src/analytics_dashboard.py")
print("\n" + "=" * 70)
