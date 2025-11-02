from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import re

app = Flask(__name__)
CORS(app, origins=['*'])

# Load ML model
def load_ml_model():
    model_path = '../models/fake_job_detector.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

ml_detector = load_ml_model()

# Suspicious patterns (more specific)
SUSPICIOUS_KEYWORDS = [
    'guaranteed income', 'easy money', 'make money fast', 'earn thousands weekly',
    'wire transfer', 'western union', 'pay upfront', 'processing fee', 
    'training fee', 'registration fee', 'too good to be true',
    'no experience required.*high salary', 'work from home.*guaranteed',
    'limited time offer', 'act now or lose', 'send money'
]

def analyze_job_posting(text):
    """Improved job posting analysis with better accuracy"""
    if not text or len(text.strip()) < 50:
        return {"score": 0, "flags": ["Text too short to analyze"], "is_fake": True, "method": "rule-based"}
    
    text_lower = text.lower()
    flags = []
    score = 75  # Start with neutral score
    method = "Enhanced rule-based"
    
    # Positive indicators (increase score)
    positive_score = 0
    
    # Professional company name mentioned
    if re.search(r'\b[A-Z][a-z]+ - [A-Z][A-Z ]+\b', text) or re.search(r'\b[A-Z]{2,}\b', text):
        positive_score += 15
        flags.append("✅ Professional company name format")
    
    # Detailed job requirements
    if re.search(r'(skills?|qualifications?|requirements?|experience).*:', text_lower):
        positive_score += 10
        flags.append("✅ Detailed requirements section")
    
    # Specific technical skills mentioned
    tech_skills = ['google ads', 'meta ads', 'hubspot', 'salesforce', 'analytics', 'seo', 'sem', 'crm', 'adobe']
    found_skills = [skill for skill in tech_skills if skill in text_lower]
    if found_skills:
        positive_score += len(found_skills) * 3
        flags.append(f"✅ Technical skills mentioned: {', '.join(found_skills[:3])}")
    
    # Professional certifications mentioned
    if re.search(r'(certification|certified|degree|bachelor|master)', text_lower):
        positive_score += 8
        flags.append("✅ Educational/certification requirements")
    
    # Specific salary/stipend mentioned
    if re.search(r'(stipend|ctc|salary|₹|rs\.?|lpa)', text_lower):
        positive_score += 10
        flags.append("✅ Clear compensation mentioned")
    
    # Professional structure (sections, bullet points)
    if text.count('###') > 0 or text.count('•') > 2 or text.count('-') > 3:
        positive_score += 8
        flags.append("✅ Well-structured job description")
    
    # Negative indicators (decrease score)
    negative_score = 0
    
    # Major red flags
    if re.search(r'\b(pay|payment|fee|deposit|charge).{0,20}(upfront|advance|first|registration|training)\b', text_lower):
        negative_score += 30
        flags.append("🚨 Requests upfront payment (major red flag!)")
    
    # Personal email domains
    if re.search(r'@(gmail|yahoo|hotmail|outlook)\.', text_lower):
        negative_score += 12
        flags.append("⚠️ Personal email domain")
    
    # Excessive urgency (only if really excessive)
    urgency_count = len(re.findall(r'\b(urgent|immediate|asap|hurry)\b', text_lower))
    if urgency_count > 3:
        negative_score += 15
        flags.append(f"⚠️ Excessive urgency ({urgency_count} instances)")
    
    # Unrealistic promises
    if re.search(r'(guaranteed|easy money|no experience.*high salary|earn thousands)', text_lower):
        negative_score += 20
        flags.append("⚠️ Unrealistic promises")
    
    # Poor grammar (multiple indicators)
    grammar_issues = len(re.findall(r'[a-z]\.[A-Z]|[!]{2,}|\s{2,}', text))
    if grammar_issues > 5:
        negative_score += 8
        flags.append("⚠️ Multiple formatting issues")
    
    # Very vague descriptions
    if re.search(r'\b(various|multiple|several|many)\s+(tasks|duties|responsibilities)\b', text_lower) and len(text) < 300:
        negative_score += 10
        flags.append("⚠️ Vague job description")
    
    # Calculate final score
    final_score = score + positive_score - negative_score
    final_score = max(0, min(100, final_score))
    
    # Determine if fake (more lenient threshold)
    is_fake = final_score < 45  # Lowered threshold
    
    # Add summary flag
    if not flags:
        flags.append("✅ No major red flags detected")
    
    return {
        "score": final_score,
        "flags": flags,
        "is_fake": is_fake,
        "confidence": "High" if abs(final_score - 50) > 25 else "Medium",
        "method": method
    }

# Course recommendations
recommendations = {
    'software': {
        'courses': [
            {'title': 'Complete Python Bootcamp 2024', 'provider': 'Udemy', 'price': '₹799', 'rating': '4.6/5'},
            {'title': 'CS50: Introduction to Computer Science', 'provider': 'Harvard (edX)', 'price': 'Free', 'rating': '4.8/5'},
            {'title': 'Full Stack Web Development', 'provider': 'freeCodeCamp', 'price': 'Free', 'rating': '4.7/5'},
            {'title': 'React Complete Course 2024', 'provider': 'Udemy', 'price': '₹899', 'rating': '4.7/5'},
            {'title': 'JavaScript Algorithms & Data Structures', 'provider': 'freeCodeCamp', 'price': 'Free', 'rating': '4.6/5'},
            {'title': 'Node.js Complete Course', 'provider': 'Udemy', 'price': '₹699', 'rating': '4.6/5'},
            {'title': 'Angular Complete Guide', 'provider': 'Udemy', 'price': '₹799', 'rating': '4.5/5'},
            {'title': 'Vue.js Complete Course', 'provider': 'Udemy', 'price': '₹699', 'rating': '4.6/5'},
            {'title': 'Django for Beginners', 'provider': 'Udemy', 'price': '₹799', 'rating': '4.5/5'},
            {'title': 'Git & GitHub Masterclass', 'provider': 'Udemy', 'price': '₹599', 'rating': '4.7/5'}
        ]
    },
    'data': {
        'courses': [
            {'title': 'Machine Learning Specialization', 'provider': 'Stanford (Coursera)', 'price': 'Free audit', 'rating': '4.9/5'},
            {'title': 'Data Science Complete Bootcamp', 'provider': 'Udemy', 'price': '₹999', 'rating': '4.5/5'},
            {'title': 'Python for Data Science & AI', 'provider': 'IBM (Coursera)', 'price': 'Free audit', 'rating': '4.6/5'},
            {'title': 'SQL for Data Science', 'provider': 'UC Davis (Coursera)', 'price': 'Free audit', 'rating': '4.6/5'},
            {'title': 'Data Analysis with Python', 'provider': 'freeCodeCamp', 'price': 'Free', 'rating': '4.7/5'},
            {'title': 'Tableau Complete Course', 'provider': 'Udemy', 'price': '₹799', 'rating': '4.5/5'},
            {'title': 'Power BI Complete Course', 'provider': 'Udemy', 'price': '₹699', 'rating': '4.4/5'},
            {'title': 'Deep Learning Specialization', 'provider': 'deeplearning.ai (Coursera)', 'price': '₹3999/month', 'rating': '4.8/5'},
            {'title': 'Statistics for Data Science', 'provider': 'Udemy', 'price': '₹799', 'rating': '4.5/5'},
            {'title': 'Excel for Data Analysis', 'provider': 'Udemy', 'price': '₹599', 'rating': '4.6/5'}
        ]
    }
}

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = analyze_job_posting(text)
    result['source'] = 'text'
    
    return jsonify(result)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        message = data.get('message', '').lower()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Programming courses
        if any(word in message for word in ['programming', 'coding', 'software', 'web', 'python', 'javascript', 'react', 'development']):
            courses = recommendations['software']['courses']
            response = "💻 **Top Programming & Development Courses (2024):**\n\n"
            for i, course in enumerate(courses[:10], 1):
                response += f"{i}. **{course['title']}** - {course['provider']} | {course['price']} ⭐ {course['rating']}\n"
            response += "\n💡 **Learning Path:** HTML/CSS → JavaScript → Framework (React/Angular) → Backend (Node.js/Python)"
            return jsonify({'response': response})
        
        # Data science courses
        elif any(word in message for word in ['data science', 'data', 'machine learning', 'ai', 'analytics', 'sql']):
            courses = recommendations['data']['courses']
            response = "📊 **Top Data Science & AI Courses (2024):**\n\n"
            for i, course in enumerate(courses[:10], 1):
                response += f"{i}. **{course['title']}** - {course['provider']} | {course['price']} ⭐ {course['rating']}\n"
            response += "\n💡 **Career Path:** Python/R → Statistics → SQL → Machine Learning → Deep Learning"
            return jsonify({'response': response})
        
        # General courses
        elif any(word in message for word in ['course', 'learn', 'study', 'training', 'skill', 'education']):
            response = "🎓 **Available Course Categories:**\n\n💻 **Programming:** Python, JavaScript, Web Development\n📊 **Data Science:** Machine Learning, AI, Analytics\n\n**Examples:** Ask 'programming courses' or 'data science courses' for detailed recommendations!"
            return jsonify({'response': response})
        
        # Jobs
        elif any(word in message for word in ['job', 'apply', 'position', 'work', 'career', 'opportunity']):
            response = "💼 **Trusted Job Platforms:**\n\n1. **Naukri** - India's largest job portal\n2. **LinkedIn Jobs** - Professional networking\n3. **Indeed** - Global job search\n4. **Glassdoor** - Company reviews & salaries\n\n🛡️ These platforms verify employers and protect job seekers from scams!"
            return jsonify({'response': response})
        
        # Help
        elif any(word in message for word in ['help', 'what', 'how', 'guide', 'tips']):
            response = "🤖 I'm your career assistant! I can help you with:\n\n• 📚 **Course Recommendations** - Programming, Data Science\n• 💼 **Job Opportunities** - Legitimate job platforms\n• 💡 **Career Guidance** - Tips for skill development\n\n**Quick Commands:**\n- Ask 'programming courses' or 'data science courses'\n- Ask 'jobs' for legitimate platforms\n- Say 'tips' for career advice"
            return jsonify({'response': response})
        
        # Default
        else:
            response = "I can help you with courses and career guidance! Try asking:\n• 'programming courses'\n• 'data science courses'\n• 'jobs'\n• 'help'"
            return jsonify({'response': response})
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)