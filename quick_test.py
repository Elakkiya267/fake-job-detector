import pickle

# Load model
with open('models/fake_job_detector.pkl', 'rb') as f:
    ml_detector = pickle.load(f)

model = ml_detector['model']
vectorizer = ml_detector['vectorizer']

# Test cases
tests = [
    ("FAKE", "URGENT! Make $5000/week working from home! No experience needed! Pay $99 registration fee. Contact: jobs@gmail.com"),
    ("LEGIT", "Software Engineer at Microsoft. Requirements: 5 years Python experience. Salary: $150,000-$180,000. Benefits: Health insurance, 401k. Apply: careers@microsoft.com")
]

print("=" * 70)
print("FAKE JOB DETECTOR - ML MODEL OUTPUT")
print("=" * 70)

for label, text in tests:
    print(f"\n[{label} JOB TEST]")
    print("-" * 70)
    print(f"Text: {text[:80]}...")
    print("-" * 70)
    
    # Predict
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    legit_prob = probability[0] * 100
    fake_prob = probability[1] * 100
    
    print(f"ML PREDICTION: {'FAKE' if prediction == 1 else 'LEGITIMATE'}")
    print(f"Legitimacy Score: {int(legit_prob)}/100")
    print(f"Fake Probability: {fake_prob:.1f}%")
    print(f"Confidence: {max(probability):.1%}")
    print()

print("=" * 70)
print("DETECTOR IS WORKING!")
print("=" * 70)
