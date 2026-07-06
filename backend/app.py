from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import re
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

app = Flask(__name__)
CORS(app, origins=['*'])

# ── StructuralFeatureExtractor (must be defined here for pickle to find it) ───
class StructuralFeatureExtractor(BaseEstimator, TransformerMixin):
    """Matches the extractor used during training — required for model deserialization."""
    RED_FLAG_PHRASES = [
        r'bank details?', r'bank account', r'account number',
        r'registration fee', r'training fee', r'joining fee', r'security deposit',
        r'pay upfront', r'advance payment', r'western union', r'wire transfer', r'send money',
        r'no experience (is )?required', r'no prior experience',
        r'instant hire', r'start today', r'start immediately',
        r'@gmail\.com', r'@yahoo\.com', r'@hotmail\.com',
        r'guaranteed income', r'earn thousands', r'easy money',
        r'unmatched earning potential',
        r'data entry.{0,30}(per month|monthly|weekly)',
        r'envelope stuffing', r'form filling', r'copy paste work',
        r'100% work from home', r'work from anywhere',
        r'limited seats', r'hurry', r'act now',
        r'reply with.{0,30}(bank|account|details)',
    ]
    LEGIT_PHRASES = [
        r'pvt\.?\s*ltd', r'private limited', r'llp', r'incorporated',
        r'b\.?tech', r'm\.?tech', r'mba', r'bachelor', r'master', r'degree',
        r'\d+.{0,5}years?.{0,10}experience',
        r'lpa\b', r'ctc\b', r'per annum',
        r'interview', r'technical round', r'hr round', r'selection process',
        r'python|java|javascript|react|sql|aws|docker|kubernetes',
        r'figma|photoshop|autocad|tableau|power bi|salesforce|hubspot',
    ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([self._extract(t.lower()) for t in X], dtype=np.float32)

    def _extract(self, tl):
        text   = tl
        words  = text.split()
        red_count   = sum(1 for p in self.RED_FLAG_PHRASES if re.search(p, tl))
        legit_count = sum(1 for p in self.LEGIT_PHRASES  if re.search(p, tl))
        char_len    = len(text)
        word_count  = len(words)
        avg_word    = float(np.mean([len(w) for w in words])) if words else 0.0
        caps_ratio  = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        exclaim     = text.count('!')
        has_personal_email  = int(bool(re.search(r'@(gmail|yahoo|hotmail|outlook|rediffmail)\.', tl)))
        has_corporate_email = int(bool(re.search(r'@(?!(gmail|yahoo|hotmail|outlook|rediffmail))[a-z0-9.\-]+\.(com|in|org|net)', tl)))
        has_monthly_salary  = int(bool(re.search(r'[\d,]+\s*per month', tl)))
        has_lpa_salary      = int(bool(re.search(r'[\d.]+\s*(lpa|ctc|per annum)', tl)))
        no_exp = int(bool(re.search(r'no (prior |previous )?(experience|exp)', tl)))
        high_salary_num = 0
        m = re.search(r'([\d,]+)\s*(per month|/month)', tl)
        if m:
            try: high_salary_num = int(m.group(1).replace(',', ''))
            except ValueError: pass
        scam_salary_flag    = int(no_exp == 1 and high_salary_num >= 50000)
        has_requirements    = int(bool(re.search(r'(requirements?|qualifications?)\s*:', tl)))
        has_responsibilities= int(bool(re.search(r'responsibilities\s*:', tl)))
        has_years_exp       = int(bool(re.search(r'\d+[\+\-]?\s*years? (of\s+)?(experience|exp)', tl)))
        has_interview       = int(bool(re.search(r'(interview|technical round|selection process)', tl)))
        urgency_count       = len(re.findall(r'\b(urgent|immediate|asap|hurry|instant|limited seats|act now)\b', tl))
        is_scam_title       = int(bool(re.search(r'\b(data entry|typing work|copy paste|form fill|envelope stuff)\b', tl)))
        return [
            red_count, legit_count, char_len, word_count, avg_word,
            caps_ratio, exclaim, 0,
            has_personal_email, has_corporate_email,
            has_monthly_salary, has_lpa_salary, scam_salary_flag,
            no_exp, high_salary_num / 100000.0,
            has_requirements, has_responsibilities, has_years_exp, has_interview,
            urgency_count, is_scam_title,
        ]


# ── Load ML model ─────────────────────────────────────────────────────────────
def load_ml_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'fake_job_detector.pkl')
    model_path = os.path.abspath(model_path)
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load ML model: {e}")
    return None

ml_model = load_ml_model()

# ── Rule-based analysis ────────────────────────────────────────────────────────
def rule_based_score(text):
    """
    Balanced rule-based scorer. Returns (score 0-100, flags list).
    Starts neutral at 50 — evidence pushes up or down.
    """
    text_lower = text.lower()
    flags = []
    positive = 0
    negative = 0

    # ─── CRITICAL RED FLAGS (very high penalty) ───────────────────────────────

    # Bank / financial details requested
    if re.search(r'\b(bank details?|bank account|account number|ifsc|routing number|sort code)\b', text_lower):
        negative += 45
        flags.append("FAKE: Asks for bank details — clear financial scam")

    # Upfront payment / fees
    if re.search(r'\b(pay|payment|fee|deposit|charge|send money).{0,40}(upfront|advance|first|registration|training|processing|joining|security)\b', text_lower) or \
       re.search(r'\b(registration|training|processing|security|joining).{0,20}(fee|fees|charge|payment|deposit)\b', text_lower):
        negative += 40
        flags.append("FAKE: Requests upfront payment — major scam indicator")

    # Wire / crypto transfer
    if re.search(r'\b(wire transfer|western union|moneygram|bitcoin|crypto payment|usdt|paypal transfer)\b', text_lower):
        negative += 35
        flags.append("FAKE: Suspicious payment method requested")

    # ─── HIGH RED FLAGS ───────────────────────────────────────────────────────

    # No experience + very high salary (common data-entry / WFH scam pattern)
    no_exp = bool(re.search(r'no (prior |previous )?(experience|exp)([ ,.]| is | required| needed)', text_lower))
    has_high_salary = bool(re.search(r'([\d,]+)\s*(per month|/month|pm\b)', text_lower))
    if no_exp and has_high_salary:
        # Extract salary number to check if it's unrealistically high
        sal_match = re.search(r'([\d,]+)\s*(per month|/month|pm\b)', text_lower)
        if sal_match:
            sal_str = sal_match.group(1).replace(',', '')
            try:
                sal_num = int(sal_str)
                if sal_num >= 50000:  # ≥ ₹50k/month with no experience = red flag
                    negative += 35
                    flags.append("FAKE: No experience required but promises very high monthly salary")
                elif sal_num >= 20000:
                    negative += 15
                    flags.append("WARNING: High pay with no experience required — verify carefully")
            except ValueError:
                pass
    elif no_exp:
        negative += 5  # mild signal alone

    # Unrealistic earnings promises
    if re.search(r'\b(earn|make|income|salary).{0,25}(thousands|lakhs|crores|lakh).{0,20}(week|month|day)\b', text_lower) or \
       re.search(r'\b(guaranteed income|easy money|make money fast|get rich|unlimited earn)\b', text_lower) or \
       re.search(r'\bunmatched earning potential\b', text_lower):
        negative += 30
        flags.append("FAKE: Unrealistic earning promises")

    # Personal email for applications
    if re.search(r'(contact|apply|send|mail|email|reach).{0,40}@(gmail|yahoo|hotmail|outlook|rediffmail|live|aol)\b', text_lower) or \
       re.search(r'@(gmail|yahoo|hotmail|outlook|rediffmail|live|aol)\.(com|in|co)\b', text_lower):
        negative += 25
        flags.append("FAKE: Personal email domain used — not corporate")

    # Work from home guaranteed / any order
    if re.search(r'(100%|fully|completely|100 percent).{0,20}(work from home|remote|wfh)\b', text_lower) or \
       re.search(r'\b(work from home|wfh|remote).{0,30}(guaranteed|assured|100%|fully)\b', text_lower) or \
       re.search(r'\banywhere\b.{0,30}(work from home|remote|wfh)\b', text_lower):
        negative += 20
        flags.append("WARNING: 'Guaranteed work from home anywhere' — common scam claim")

    # Instant hire / immediate start with bank details / urgent
    if re.search(r'\b(instant hire|instant hiring|immediate hire|hired instantly|start immediately|start today|join today)\b', text_lower):
        negative += 20
        flags.append("FAKE: 'Instant hire' claims — no legitimate company does this")

    # Excessive urgency keywords
    urgency_hits = re.findall(r'\b(urgent|immediate|asap|hurry|last chance|limited seats|apply now or|today only|act now|limited time)\b', text_lower)
    if len(urgency_hits) >= 3:
        negative += 20
        flags.append(f"WARNING: Excessive urgency ({len(urgency_hits)} instances)")
    elif len(urgency_hits) >= 1:
        negative += 8

    # Data entry + high salary combo (very common scam pattern)
    if re.search(r'\b(data entry|typing work|copy paste|form fill)\b', text_lower) and has_high_salary:
        sal_match = re.search(r'([\d,]+)\s*(per month|/month|pm\b)', text_lower)
        if sal_match:
            sal_str = sal_match.group(1).replace(',', '')
            try:
                if int(sal_str) >= 30000:
                    negative += 30
                    flags.append("FAKE: Data entry / typing job promising high salary — common scam")
            except ValueError:
                pass

    # "Work from anywhere" vagueness
    if re.search(r'\b(work from anywhere|work anywhere|location.{0,20}anywhere)\b', text_lower):
        negative += 10
        flags.append("WARNING: 'Work from anywhere' — vague location claim")

    # Attitude-based hiring (no skills required)
    if re.search(r'\b(hire.{0,20}attitude|attitude.{0,20}hire|no skill|any background|no qualification)\b', text_lower):
        negative += 15
        flags.append("WARNING: 'Hired based on attitude' — avoids specifying real qualifications")

    # Vague job description
    if len(text.strip()) < 300 and re.search(r'\b(various|multiple|many|etc|and more)\b', text_lower):
        negative += 15
        flags.append("WARNING: Vague job description with minimal details")

    # ─── POSITIVE LEGITIMACY SIGNALS ─────────────────────────────────────────
    # (Only awarded when genuine structural evidence exists)

    # Registered company type
    if re.search(r'\b(pvt\.?\s*ltd|private limited|llp|inc\.|corporation|technologies|solutions|systems|consulting)\b', text_lower):
        positive += 15
        flags.append("LEGIT: Registered company type mentioned")

    # Corporate email
    if re.search(r'@(?!(gmail|yahoo|hotmail|outlook|rediffmail|live|aol))[a-z0-9.\-]+\.(com|in|org|net|co\.in)\b', text_lower):
        positive += 15
        flags.append("LEGIT: Corporate email contact")

    # Specific years of experience required
    if re.search(r'\d+[\+\-–]?\s*(years?|yrs?)\s*(of\s+)?(experience|exp)\b', text_lower):
        positive += 12
        flags.append("LEGIT: Specific experience requirement stated")

    # Educational qualifications required
    if re.search(r'\b(bachelor|master|b\.?tech|m\.?tech|mba|b\.?e|bca|mca|diploma|degree|graduate|post.?graduate)\b', text_lower):
        positive += 10
        flags.append("LEGIT: Educational qualification required")

    # Named technical skills (3+ = strong signal)
    tech_skills = [
        'python', 'javascript', 'java', 'react', 'angular', r'node\.js', 'sql',
        'aws', 'docker', 'kubernetes', 'machine learning', 'deep learning',
        'google ads', 'meta ads', 'hubspot', 'salesforce', 'seo', 'sem',
        'photoshop', 'figma', 'autocad', 'tally', 'power bi', 'tableau',
        r'c\+\+', 'golang', 'rust', 'swift', 'kotlin', 'flutter', 'django',
        'spring boot', 'microservices', r'rest api', 'graphql'
    ]
    found_skills = [s for s in tech_skills if re.search(r'\b' + s + r'\b', text_lower)]
    if len(found_skills) >= 3:
        positive += 14
        flags.append(f"LEGIT: Multiple technical skills specified: {', '.join(found_skills[:3])}")
    elif len(found_skills) >= 1:
        positive += 6
        flags.append(f"LEGIT: Technical skill mentioned: {found_skills[0]}")

    # Specific CTC / LPA salary (annual structured)
    if re.search(r'(\d[\d,.]+\s*(lpa|ctc|per annum|p\.?a\.|annual)|ctc.{0,20}\d)', text_lower):
        positive += 10
        flags.append("LEGIT: Structured annual CTC/salary mentioned")

    # Formal hiring process
    if re.search(r'\b(interview|technical round|hr round|assessment|aptitude test|selection process)\b', text_lower):
        positive += 8
        flags.append("LEGIT: Formal interview/hiring process mentioned")

    # Specific named city location
    if re.search(r'\b(bangalore|bengaluru|mumbai|delhi|hyderabad|chennai|pune|kolkata|noida|gurgaon|gurugram|ahmedabad|new york|london|singapore)\b', text_lower):
        positive += 5
        flags.append("LEGIT: Specific office location mentioned")

    # ─── SCORE CALCULATION ────────────────────────────────────────────────────
    score = 50 + positive - negative
    score = max(5, min(95, score))

    if not flags:
        flags.append("No strong signals detected — verify this posting independently")

    return score, flags


# ── ML-based prediction ────────────────────────────────────────────────────────
def ml_predict(text):
    """Returns ML probability of being FAKE (0-1), or None if unavailable."""
    if ml_model is None:
        return None
    try:
        from scipy.sparse import hstack, csr_matrix
        vectorizer  = ml_model['vectorizer']
        model       = ml_model['model']
        structural  = ml_model.get('structural')   # v2 model has this

        tfidf_feat = vectorizer.transform([text])

        if structural is not None:
            struct_feat = structural.transform([text])
            X = hstack([tfidf_feat, csr_matrix(struct_feat)])
        else:
            X = tfidf_feat

        proba   = model.predict_proba(X)[0]
        classes = list(model.classes_)
        # label 1 = fake, label 0 = legit
        fake_idx = classes.index(1) if 1 in classes else 1
        return float(proba[fake_idx])   # probability of being FAKE
    except Exception as e:
        print(f"ML prediction error: {e}")
        return None


# ── Hybrid analysis ────────────────────────────────────────────────────────────
def analyze_job_posting(text):
    """Hybrid: 60% ML + 40% rule-based. Falls back to rules-only if no ML model."""
    if not text or len(text.strip()) < 50:
        return {
            "score": 10,
            "flags": ["Text too short to analyze properly"],
            "is_fake": True,
            "confidence": "Low",
            "method": "rule-based"
        }

    rule_score, flags = rule_based_score(text)
    ml_fake_prob = ml_predict(text)   # probability text is FAKE (0=legit, 1=fake)

    if ml_fake_prob is not None:
        # Convert fake-probability to a legitimacy score (0-100)
        ml_legit_score = round((1.0 - ml_fake_prob) * 100)
        # Weighted hybrid
        final_score = round(0.60 * ml_legit_score + 0.40 * rule_score)
        method = "ML + Rule-based hybrid"
    else:
        final_score = rule_score
        method = "Rule-based"

    final_score = max(5, min(95, final_score))
    is_fake     = final_score < 50

    distance   = abs(final_score - 50)
    confidence = "High" if distance >= 25 else ("Medium" if distance >= 10 else "Low")

    return {
        "score":      final_score,
        "flags":      flags,
        "is_fake":    is_fake,
        "confidence": confidence,
        "method":     method
    }


# ── Course recommendations ─────────────────────────────────────────────────────
recommendations = {
    'software': {
        'courses': [
            {'title': 'Complete Python Bootcamp 2024',           'provider': 'Udemy',               'price': 'Rs.799',       'rating': '4.6/5'},
            {'title': 'CS50: Introduction to Computer Science',  'provider': 'Harvard (edX)',        'price': 'Free',          'rating': '4.8/5'},
            {'title': 'Full Stack Web Development',              'provider': 'freeCodeCamp',         'price': 'Free',          'rating': '4.7/5'},
            {'title': 'React Complete Course 2024',              'provider': 'Udemy',                'price': 'Rs.899',        'rating': '4.7/5'},
            {'title': 'JavaScript Algorithms & Data Structures', 'provider': 'freeCodeCamp',         'price': 'Free',          'rating': '4.6/5'},
            {'title': 'Node.js Complete Course',                 'provider': 'Udemy',                'price': 'Rs.699',        'rating': '4.6/5'},
            {'title': 'Angular Complete Guide',                  'provider': 'Udemy',                'price': 'Rs.799',        'rating': '4.5/5'},
            {'title': 'Django for Beginners',                    'provider': 'Udemy',                'price': 'Rs.799',        'rating': '4.5/5'},
            {'title': 'Git & GitHub Masterclass',                'provider': 'Udemy',                'price': 'Rs.599',        'rating': '4.7/5'},
        ]
    },
    'data': {
        'courses': [
            {'title': 'Machine Learning Specialization',         'provider': 'Stanford (Coursera)',  'price': 'Free audit',    'rating': '4.9/5'},
            {'title': 'Data Science Complete Bootcamp',          'provider': 'Udemy',                'price': 'Rs.999',        'rating': '4.5/5'},
            {'title': 'Python for Data Science & AI',           'provider': 'IBM (Coursera)',        'price': 'Free audit',    'rating': '4.6/5'},
            {'title': 'SQL for Data Science',                    'provider': 'UC Davis (Coursera)',  'price': 'Free audit',    'rating': '4.6/5'},
            {'title': 'Tableau Complete Course',                 'provider': 'Udemy',                'price': 'Rs.799',        'rating': '4.5/5'},
            {'title': 'Power BI Complete Course',                'provider': 'Udemy',                'price': 'Rs.699',        'rating': '4.4/5'},
            {'title': 'Deep Learning Specialization',            'provider': 'deeplearning.ai',      'price': 'Rs.3999/month', 'rating': '4.8/5'},
        ]
    }
}


# ── Routes ─────────────────────────────────────────────────────────────────────
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

        if any(w in message for w in ['programming','coding','software','web','python','javascript','react','development']):
            courses = recommendations['software']['courses']
            response = "Top Programming & Development Courses (2024):\n\n"
            for i, c in enumerate(courses, 1):
                response += f"{i}. {c['title']} - {c['provider']} | {c['price']} | {c['rating']}\n"
            response += "\nLearning Path: HTML/CSS -> JavaScript -> Framework (React/Angular) -> Backend"
            return jsonify({'response': response})

        elif any(w in message for w in ['data science','data','machine learning','ai','analytics','sql']):
            courses = recommendations['data']['courses']
            response = "Top Data Science & AI Courses (2024):\n\n"
            for i, c in enumerate(courses, 1):
                response += f"{i}. {c['title']} - {c['provider']} | {c['price']} | {c['rating']}\n"
            response += "\nCareer Path: Python -> Statistics -> SQL -> Machine Learning -> Deep Learning"
            return jsonify({'response': response})

        elif any(w in message for w in ['course','learn','study','training','skill','education']):
            return jsonify({'response': "Available categories:\n- Programming: Python, JavaScript, Web Development\n- Data Science: ML, AI, Analytics\n\nAsk 'programming courses' or 'data science courses' for full lists!"})

        elif any(w in message for w in ['job','apply','position','work','career','opportunity']):
            return jsonify({'response': "Trusted Job Platforms:\n1. Naukri - India's largest job portal\n2. LinkedIn Jobs - Professional networking\n3. Indeed - Global job search\n4. Glassdoor - Reviews & salaries\n\nThese platforms verify employers and protect job seekers."})

        elif any(w in message for w in ['help','what','how','guide','tips']):
            return jsonify({'response': "I can help with:\n- Course Recommendations (Programming, Data Science)\n- Legitimate Job Platforms\n- Career Guidance\n\nTry: 'programming courses', 'data science courses', 'jobs', 'help'"})

        else:
            return jsonify({'response': "Try asking:\n- 'programming courses'\n- 'data science courses'\n- 'jobs'\n- 'help'"})

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'ml_model': 'loaded' if ml_model else 'not loaded'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)