"""
FAKE JOB POSTING DETECTOR - DEMO
Run this to see the detector in action!
"""
import pickle
import re

print("\n" + "=" * 80)
print(" " * 20 + "FAKE JOB POSTING DETECTOR - LIVE DEMO")
print("=" * 80)

# Load ML model
print("\n[1] Loading ML Model...")
with open('models/fake_job_detector.pkl', 'rb') as f:
    ml_detector = pickle.load(f)
model = ml_detector['model']
vectorizer = ml_detector['vectorizer']
print("    ✓ Model loaded successfully!")

# Suspicious keywords for rule-based detection
SUSPICIOUS_KEYWORDS = [
    'urgent', 'immediate', 'guaranteed income', 'work from home', 'no experience',
    'easy money', 'limited time', 'act now', 'wire transfer', 'western union',
    'pay upfront', 'processing fee', 'training fee', 'registration fee'
]

def analyze_job(text):
    """Analyze job posting"""
    text_lower = text.lower()
    
    # ML Prediction
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    ml_score = int(probability[0] * 100)
    is_fake = prediction == 1
    confidence = max(probability)
    
    # Rule-based checks
    flags = []
    
    # Check keywords
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower]
    if found_keywords:
        flags.append(f"Suspicious keywords: {', '.join(found_keywords[:3])}")
    
    # Check email
    if re.search(r'@(gmail|yahoo|hotmail|outlook)\.', text_lower):
        flags.append("Personal email domain")
    
    # Check payment
    if re.search(r'\b(pay|fee).{0,20}(upfront|registration|training)\b', text_lower):
        flags.append("Requests upfront payment")
    
    # Check urgency
    urgency = len(re.findall(r'\b(urgent|immediate|now|today)\b', text_lower))
    if urgency > 2:
        flags.append(f"Excessive urgency ({urgency} times)")
    
    return {
        'ml_prediction': 'FAKE' if is_fake else 'LEGITIMATE',
        'score': ml_score,
        'confidence': confidence,
        'flags': flags
    }

# Test cases
test_jobs = [
    {
        'name': 'FAKE JOB POSTING',
        'text': """
URGENT! Make $5000/week working from home! 
No experience needed! Just pay $99 registration fee.
Contact: jobs@gmail.com
Act now - limited spots available!
"""
    },
    {
        'name': 'LEGITIMATE JOB POSTING',
        'text': """
Software Engineer - Full Stack Developer

Company: Microsoft Corporation
Location: Seattle, WA
Employment Type: Full-time

Requirements:
- Bachelor's degree in Computer Science
- 5+ years experience with Python, React, Node.js
- Strong understanding of cloud platforms (AWS/Azure)
- Excellent problem-solving skills

Compensation & Benefits:
- Competitive salary: $150,000 - $180,000
- Health, dental, and vision insurance
- 401(k) matching
- Stock options
- Flexible work arrangements

To Apply: careers@microsoft.com
"""
    }
]

# Analyze each test case
print("\n" + "=" * 80)
print("[2] ANALYZING JOB POSTINGS...")
print("=" * 80)

for i, job in enumerate(test_jobs, 1):
    print(f"\n{'─' * 80}")
    print(f"TEST {i}: {job['name']}")
    print('─' * 80)
    print(f"\nJob Posting Text:")
    print(job['text'].strip()[:150] + "...")
    
    result = analyze_job(job['text'])
    
    print(f"\n{'═' * 80}")
    print("DETECTION RESULTS:")
    print('═' * 80)
    
    # Score display
    score = result['score']
    if score >= 70:
        score_emoji = "🟢"
        score_label = "HIGH"
    elif score >= 50:
        score_emoji = "🟡"
        score_label = "MEDIUM"
    else:
        score_emoji = "🔴"
        score_label = "LOW"
    
    print(f"\n  Legitimacy Score:  {score_emoji} {score}/100 ({score_label})")
    print(f"  ML Prediction:     {'🚨 ' + result['ml_prediction'] if result['ml_prediction'] == 'FAKE' else '✅ ' + result['ml_prediction']}")
    print(f"  Confidence:        {result['confidence']:.1%}")
    
    if result['flags']:
        print(f"\n  Red Flags Detected:")
        for flag in result['flags']:
            print(f"    ⚠️  {flag}")
    else:
        print(f"\n  ✅ No major red flags detected")
    
    # Final verdict
    print(f"\n  {'─' * 76}")
    if result['ml_prediction'] == 'FAKE':
        print(f"  🚨 WARNING: This posting shows signs of being FRAUDULENT!")
        print(f"  ⚠️  Do NOT provide personal information or send money")
    else:
        print(f"  ✅ This posting appears LEGITIMATE")
        print(f"  ℹ️  Always verify independently through official channels")
    print(f"  {'─' * 76}")

print("\n" + "=" * 80)
print(" " * 25 + "DETECTION COMPLETE!")
print("=" * 80)

print("\n📌 To use the web interface:")
print("   Run: .\\venv\\Scripts\\streamlit run src\\app.py")
print("   Then open: http://localhost:8501")
print("\n")
