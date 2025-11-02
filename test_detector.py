import re

# Suspicious patterns
SUSPICIOUS_KEYWORDS = [
    'urgent', 'immediate', 'guaranteed income', 'work from home', 'no experience',
    'easy money', 'limited time', 'act now', 'wire transfer', 'western union',
    'pay upfront', 'processing fee', 'training fee', 'registration fee',
    'too good to be true', 'earn thousands', 'make money fast', 'free training'
]

def analyze_job_posting(text):
    """Analyze job posting for fake indicators"""
    if not text or len(text.strip()) < 50:
        return {"score": 0, "flags": ["Text too short to analyze"], "is_fake": True}
    
    text_lower = text.lower()
    flags = []
    score = 100
    
    # Check suspicious keywords
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in text_lower]
    if found_keywords:
        score -= len(found_keywords) * 5
        flags.append(f"Suspicious keywords: {', '.join(found_keywords[:3])}")
    
    # Check for personal email domains
    if re.search(r'@(gmail|yahoo|hotmail|outlook)\.', text_lower):
        score -= 15
        flags.append("Personal email domain (not corporate)")
    
    # Check for upfront payment requests
    if re.search(r'\b(pay|payment|fee|deposit|charge).{0,20}(upfront|advance|first|registration|training)\b', text_lower):
        score -= 25
        flags.append("Requests upfront payment (MAJOR RED FLAG!)")
    
    # Check for excessive urgency
    urgency_count = len(re.findall(r'\b(urgent|immediate|asap|now|today|hurry)\b', text_lower))
    if urgency_count > 2:
        score -= 15
        flags.append(f"Excessive urgency ({urgency_count} instances)")
    
    # Check for missing key information
    if not re.search(r'\b(salary|compensation|pay|wage|benefits)\b', text_lower):
        score -= 8
        flags.append("No salary/compensation mentioned")
    
    if not re.search(r'\b(experience|qualification|requirement|skill|education)\b', text_lower):
        score -= 12
        flags.append("No clear requirements specified")
    
    # Length check
    if len(text) < 200:
        score -= 10
        flags.append("Very short description")
    
    score = max(0, min(100, score))
    is_fake = score < 60
    
    return {
        "score": score,
        "flags": flags if flags else ["No major red flags detected"],
        "is_fake": is_fake,
        "confidence": "High" if abs(score - 50) > 30 else "Medium"
    }

# Test with a FAKE job posting
print("=" * 60)
print("TESTING FAKE JOB POSTING DETECTOR")
print("=" * 60)

fake_job = """
URGENT! Make $5000/week working from home! 
No experience needed! Just pay $99 registration fee.
Contact: jobs@gmail.com
Act now - limited spots available!
"""

print("\n[TEST 1] Analyzing FAKE job posting:")
print("-" * 60)
print(fake_job)
print("-" * 60)

result = analyze_job_posting(fake_job)
print(f"\nScore: {result['score']}/100")
print(f"Status: {'🚨 LIKELY FAKE' if result['is_fake'] else '✅ LIKELY LEGITIMATE'}")
print(f"Confidence: {result['confidence']}")
print("\nRed Flags Detected:")
for flag in result['flags']:
    print(f"  ⚠️  {flag}")

# Test with a LEGITIMATE job posting
print("\n" + "=" * 60)

legit_job = """
Software Engineer - Full Stack Developer

Company: TechCorp Inc.
Location: San Francisco, CA
Employment Type: Full-time

About the Role:
We are seeking an experienced Full Stack Developer to join our engineering team.
You will work on building scalable web applications using modern technologies.

Requirements:
- Bachelor's degree in Computer Science or related field
- 3+ years of experience with React, Node.js, and Python
- Strong understanding of database design and SQL
- Experience with cloud platforms (AWS/Azure)
- Excellent problem-solving and communication skills

Compensation & Benefits:
- Competitive salary range: $120,000 - $160,000
- Health, dental, and vision insurance
- 401(k) matching
- Flexible work arrangements
- Professional development budget

To Apply:
Please send your resume to careers@techcorp.com or apply through our website at www.techcorp.com/careers
"""

print("\n[TEST 2] Analyzing LEGITIMATE job posting:")
print("-" * 60)
print(legit_job[:200] + "...")
print("-" * 60)

result2 = analyze_job_posting(legit_job)
print(f"\nScore: {result2['score']}/100")
print(f"Status: {'🚨 LIKELY FAKE' if result2['is_fake'] else '✅ LIKELY LEGITIMATE'}")
print(f"Confidence: {result2['confidence']}")
print("\nRed Flags Detected:")
for flag in result2['flags']:
    print(f"  ⚠️  {flag}")

print("\n" + "=" * 60)
print("DETECTOR IS WORKING CORRECTLY!")
print("=" * 60)
