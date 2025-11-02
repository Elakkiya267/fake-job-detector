# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Backend Server
```bash
cd backend
python app.py
```
✅ Backend running at `http://localhost:5000`

### Step 3: Open Frontend
Open `frontend/index.html` in your browser

**OR** use a local server:
```bash
cd frontend
python -m http.server 8000
```
Then visit `http://localhost:8000`

---

## 📝 How to Use

1. **Paste Job Posting** - Copy the entire job description
2. **Click Analyze** - Get instant results
3. **View Score** - See legitimacy rating (0-100)
4. **Check Flags** - Review detected issues

### If Score < 60 (Fake Detected):
🤖 **Chatbot appears automatically!**

**Ask the chatbot:**
- "Show me relevant courses" → Get course recommendations with links
- "Show me job opportunities" → Get trusted job platforms
- Click quick buttons for instant help

---

## 🎯 Example Usage

### Analyzing a Job Posting:
```
Paste this type of content:

Job Title: Software Developer
Company: ABC Tech Corp
Location: Remote

Description:
We are seeking a talented software developer...
[Full job description]

Requirements:
- 3+ years experience
- Python, JavaScript
[etc.]
```

### Chatbot Interaction:
```
You: "Show me relevant courses"
Bot: Lists courses from Coursera, edX with apply links

You: "Show me job opportunities"  
Bot: Lists LinkedIn, Indeed, Glassdoor links
```

---

## ✅ What You Get

### For Legitimate Postings (Score ≥ 60):
- ✅ Green status indicator
- Confidence level
- Any minor warnings
- Verification tips

### For Fake Postings (Score < 60):
- 🚨 Red warning alert
- Detailed red flags
- Safety recommendations
- **Chatbot with alternatives:**
  - Relevant courses (free & paid)
  - Trusted job platforms
  - Career guidance

---

## 🔗 Trusted Sources

All chatbot recommendations link to:
- **Coursera** - University courses
- **edX** - Harvard, MIT courses  
- **LinkedIn** - Professional jobs
- **Indeed** - Job search
- **Glassdoor** - Company reviews
- **Google Certificates** - Career programs

**All links are real and verified!**

---

## ⚡ Quick Troubleshooting

**Backend won't start?**
- Check Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

**Frontend not connecting?**
- Make sure backend is running first
- Check `http://localhost:5000/health` in browser

**Chatbot not showing?**
- It only appears when score < 60 (fake detected)
- This is intentional - legitimate postings don't need alternatives

---

## 💡 Pro Tips

1. **Paste complete job postings** - More text = better analysis
2. **Include all sections** - Title, description, requirements, contact
3. **Check the flags** - Understand why it's flagged
4. **Use chatbot links** - All recommendations are from trusted sources
5. **Verify independently** - Always double-check companies

---

**Ready to protect yourself from job scams? Start analyzing!** 🛡️
