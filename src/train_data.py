"""
train_data.py — Generate a rich labeled dataset for fake job detection.
Produces: data/labeled_jobs.csv  (text, label)  label: 1=fake, 0=legit
"""

import csv, os, random, itertools

random.seed(42)

# ─── FAKE JOB TEMPLATES ───────────────────────────────────────────────────────

FAKE_SCAM_TYPES = [
    # 1. Data entry / typing scams
    lambda: f"""Job Title: {random.choice(['Remote Data Entry Specialist','Online Typing Expert','Home-Based Data Entry Operator','Copy Paste Work From Home','Form Filling Expert'])}
Company: {random.choice(['Zenith Ventures International','Global Opportunities Ltd','OptiWork Solutions','EasyEarn Global','QuickCash Data Services','HomeWork Pro'])}
Location: 100% Work from Home (Anywhere)
Salary: Rs {random.choice(['1,50,000','2,00,000','1,80,000','3,00,000','80,000','1,20,000'])} - Rs {random.choice(['3,00,000','4,00,000','2,50,000','5,00,000'])} per month

We are looking for motivated individuals to join our data entry team. No experience is required! We provide all necessary training.

Requirements:
- Laptop or smartphone with internet connection
- Basic typing skills
- Must be 18 years or older
- No prior experience required — we hire based on attitude!

Why Join Us?
- Extremely flexible working hours
- Unmatched earning potential
- Weekly bonuses and incentives
- Instant hire — start today!

Reply with your resume and bank details to {random.choice(['jobs@gmail.com','apply@yahoo.com','hr@hotmail.com','work@gmail.com'])}.
""",

    # 2. Upfront fee / registration scams
    lambda: f"""URGENT HIRING! {random.choice(['Digital Marketing Executive','Online Customer Support','Virtual Assistant','Social Media Manager','Content Writer'])}

Company: {random.choice(['NetPro Global','DigiReach Services','ClickWork Hub','MegaEarn Corp','GlobalWork Pvt.'])}
Location: Work from Home
Salary: Rs {random.choice(['50,000','75,000','90,000','1,00,000'])} per month — Guaranteed!

Immediate openings! No experience needed.

To confirm your slot, pay a one-time registration fee of Rs {random.choice(['500','1,000','1,500','2,000','999','799'])}.
After registration fee payment, training material will be sent.

Requirements: None! Anyone can apply.
Contact: {random.choice(['register@gmail.com','apply.now@yahoo.com','work@hotmail.com'])}
Limited seats — act now!
""",

    # 3. Guaranteed income / MLM disguised as job
    lambda: f"""Earn Rs {random.choice(['50,000','80,000','1,00,000','30,000','40,000'])} per month from home!

{random.choice(['FastEarnings','QuickMoney Network','HomePay Solutions','EasyIncome Hub','WealthGrow Network'])} is expanding.

No experience required. Guaranteed income every week.
Work part time or full time — you choose!
Easy tasks: refer friends, share links, fill simple forms.

Requirements: Just a smartphone and Wi-Fi. No skills needed.
Training fee: Rs {random.choice(['200','500','1,000','1,500'])} (refundable after 30 days).
Send money via Paytm/Google Pay to activate your account.

Contact: {random.choice(['earnhome@gmail.com','money.work@yahoo.com','fastcash@hotmail.com'])}
Hurry! Last {random.choice(['5','10','20'])} spots left today!
""",

    # 4. Envelope stuffing / form filling
    lambda: f"""Part Time Home Based Work — Earn {random.choice(['Rs 500-1000','Rs 800-1500','Rs 600 to 1200','Rs 15,000-25,000'])} per {random.choice(['day','week','task'])}

Work: {random.choice(['Envelope stuffing','Form filling','SMS sending','Link sharing','Product reviewing','Survey filling'])}
Location: Home
Experience: Not required
Age: 18+

Simple daily tasks. Get paid weekly directly to your bank account.

Registration process: Pay Rs {random.choice(['300','500','700','1,000'])} to get your starter kit.
After payment, tasks will be assigned within {random.choice(['24 hours','2 hours','1 hour'])}.

Send payment proof to {random.choice(['tasks@gmail.com','homejobs@yahoo.com','workfromhome@hotmail.com'])}.
Bank details required for payment processing.
""",

    # 5. Fake HR / recruiter reaching out
    lambda: f"""CONGRATULATIONS! You have been selected for the post of {random.choice(['Customer Support Executive','Back Office Executive','Data Analyst Trainee','HR Coordinator','Accounts Assistant'])} at {random.choice(['Global IT Solutions','TechReach International','OptiServe Global','DataPro Ltd'])}.

Joining is simple. No interview required.
Salary: Rs {random.choice(['25,000','35,000','45,000','60,000'])} per month + incentives.

To confirm your appointment:
- Pay security deposit of Rs {random.choice(['2,000','3,000','5,000','1,500'])} via NEFT/IMPS.
- Provide your Aadhaar, PAN, and bank account number.
- Your joining date is {random.choice(['immediate','this Monday','within 3 days','today'])}.

For confirmation reply to {random.choice(['hr.dept@gmail.com','appointment@yahoo.com','joining@hotmail.com'])}.
This offer expires in {random.choice(['24','48','6','12'])} hours!
""",

    # 6. Work from home package / kit scam
    lambda: f"""Earn Money from Home — {random.choice(['Amazon','Flipkart','Meesho','Myntra'])} Authorized Work

Position: Home Based {random.choice(['Product Reseller','Packing Assistant','Quality Checker','Data Uploader'])}
Salary: Rs {random.choice(['20,000','30,000','40,000','15,000'])} - Rs {random.choice(['50,000','60,000','80,000'])} per month

No experience, no qualification required. Simple tasks done from home.

To get started, purchase your starter kit for Rs {random.choice(['999','1,499','1,999','599'])}.
(Kit includes: product samples, training guide, login ID)

NOTE: We are NOT responsible if you do not purchase the kit.
Send payment to the following UPI ID: {random.choice(['workfromhome@upi','earnhome@paytm','jobs@gpay'])}.
Immediate start after payment. Bank details needed for salary processing.
""",

    # 7. Fake internship with deposit
    lambda: f"""Internship Opportunity: {random.choice(['Digital Marketing','Graphic Design','Business Development','Social Media'])} Intern

Company: {random.choice(['PixelGrow Studios','AdReach Pro','BrandMax Agency','DigiCraft Solutions'])}
Stipend: Rs {random.choice(['10,000','15,000','20,000','25,000'])} per month
Duration: 3 months
Location: Work from Home

No experience or skills required. We train you from scratch!
Guaranteed stipend every month.

Note: A refundable caution deposit of Rs {random.choice(['2,000','3,000','4,000','1,500'])} is required before onboarding.
Deposit will be returned after successful completion.

Apply at: {random.choice(['intern@gmail.com','apply@yahoo.com','jobs@hotmail.com'])}
Only {random.choice(['5','10','3'])} seats left — hurry!
""",

    # 8. Vague remote job with high pay
    lambda: f"""HIRING IMMEDIATELY: {random.choice(['Remote Coordinator','Online Associate','Virtual Employee','Digital Worker','Home Agent'])}

Salary: Rs {random.choice(['1,00,000','1,50,000','2,00,000','80,000'])} per month
Location: Anywhere, fully remote
Experience: Not required

Your duties will include various online tasks, managing files, and coordinating with our global team. Training provided.

You will be paid weekly. No targets, no pressure. Work at your own pace.

To apply: Send your name, age, and bank details to {random.choice(['remote.jobs@gmail.com','work@yahoo.com','online.hire@hotmail.com'])}.
Instant interview — you will be hired today!
""",
]

# ─── LEGITIMATE JOB TEMPLATES ─────────────────────────────────────────────────

LEGIT_JOB_TYPES = [
    # Software Engineering
    lambda: f"""Software Engineer — {random.choice(['Backend','Full Stack','Frontend','Cloud'])}
{random.choice(['Infosys Limited','Wipro Technologies Pvt. Ltd.','HCL Technologies Ltd.','Cognizant Technology Solutions','TCS Tata Consultancy Services'])}
Location: {random.choice(['Bangalore, Karnataka','Hyderabad, Telangana','Pune, Maharashtra','Chennai, Tamil Nadu'])} (Hybrid)

About the Role:
We are hiring a {random.choice(['Backend','Full Stack','Frontend','Cloud'])} Engineer to design, build, and maintain scalable systems.

Requirements:
- B.Tech / B.E. in Computer Science or equivalent
- {random.choice(['2-4','3-5','1-3','4-6'])} years of experience
- Strong proficiency in {random.choice(['Python and Django','Java and Spring Boot','Node.js and React','Go and Kubernetes'])}
- Experience with SQL, {random.choice(['PostgreSQL','MySQL','MongoDB'])}, REST APIs
- Familiarity with {random.choice(['AWS','GCP','Azure'])} and Docker

Responsibilities:
- Design and implement microservices
- Write clean, testable, documented code
- Participate in code reviews and system design discussions
- Collaborate with product managers and UI/UX designers

CTC: {random.choice(['8-12 LPA','10-15 LPA','6-10 LPA','12-18 LPA'])} depending on experience
Apply: careers@{random.choice(['infosys.com','wipro.com','hcl.com','cognizant.com'])}
""",

    # Data Science / ML
    lambda: f"""Data Scientist / ML Engineer
{random.choice(['Flipkart Internet Pvt. Ltd.','Ola Electric Mobility Ltd.','Swiggy (Bundl Technologies)','Freshworks Inc.','Razorpay Software Pvt. Ltd.'])}
Location: {random.choice(['Bangalore','Hyderabad','Gurgaon','Mumbai'])} (Hybrid / Remote)

Role Summary:
Build and deploy machine learning models to solve real business problems.

Required Skills:
- M.Tech / M.Sc / B.Tech in CS, Statistics, or Mathematics
- {random.choice(['2-4','3-6','1-3'])} years of hands-on ML experience
- Proficiency in Python, Pandas, NumPy, Scikit-learn
- Experience with {random.choice(['TensorFlow','PyTorch','Keras'])} and model deployment
- Strong SQL skills; familiarity with Spark / PySpark is a plus
- Knowledge of {random.choice(['NLP','Computer Vision','Time Series Forecasting'])}

What You'll Do:
- Develop predictive models for {random.choice(['recommendation systems','fraud detection','demand forecasting','user churn prediction'])}
- Conduct A/B experiments and interpret results
- Collaborate with data engineers and product teams

Compensation: {random.choice(['12-20 LPA','15-25 LPA','10-18 LPA'])}
Interview Process: Aptitude Test → Technical Round 1 (Coding) → Technical Round 2 (ML Concepts) → HR
Contact: data-hiring@{random.choice(['flipkart.com','ola.com','swiggy.in'])}
""",

    # Marketing / Business
    lambda: f"""Digital Marketing Manager
{random.choice(['Marico Limited','Dabur India Ltd.','Godrej Consumer Products','Asian Paints Ltd.','Hindustan Unilever Limited'])}
Location: {random.choice(['Mumbai, Maharashtra','Delhi NCR','Bangalore, Karnataka'])}

Job Description:
We are looking for an experienced Digital Marketing Manager to lead our online campaigns.

Requirements:
- MBA in Marketing or equivalent; {random.choice(['3-5','4-7','2-4'])} years of experience in digital marketing
- Hands-on expertise with Google Ads, Meta Ads, HubSpot, SEMRush
- Strong understanding of SEO, SEM, email marketing, and analytics
- Proficiency in Google Analytics, Data Studio
- Excellent communication and stakeholder management skills

Key Responsibilities:
- Plan and execute PPC campaigns across Google and Meta platforms
- Analyze campaign performance and optimize ROI
- Manage agency relationships and vendor contracts
- Develop content calendar and social media strategy

CTC: {random.choice(['10-15 LPA','8-13 LPA','12-18 LPA'])}
Apply to: marketing.careers@{random.choice(['marico.com','dabur.com','godrej.com'])}
""",

    # Finance / Accounting
    lambda: f"""Finance Analyst / Senior Accountant
{random.choice(['Deloitte India','KPMG India Pvt. Ltd.','Ernst & Young LLP','PwC India','Grant Thornton Bharat LLP'])}
Location: {random.choice(['Mumbai','Delhi','Bangalore','Hyderabad'])}

Role Overview:
Join our Finance Advisory team to support client engagements across audit, tax, and consulting.

Qualifications:
- CA (Chartered Accountant) / CPA / MBA Finance
- {random.choice(['2-5','3-6','1-4'])} years in finance, accounting, or audit
- Strong knowledge of {random.choice(['IFRS and Ind AS','GST and direct taxation','financial modelling'])}
- Proficiency in SAP, Oracle, or Tally ERP
- Advanced MS Excel skills (VLOOKUP, Pivot Tables, Power Query)

Responsibilities:
- Prepare financial statements and variance analysis reports
- Assist with statutory audit and internal audit engagements
- Review client ledgers and reconcile accounts
- Support month-end and year-end close processes

CTC: {random.choice(['7-12 LPA','10-16 LPA','6-10 LPA'])}
Interview: Online Assessment → Case Study → Partner Interview
Apply: finance.recruitment@{random.choice(['deloitte.com','kpmg.com','ey.com'])}
""",

    # HR / Operations
    lambda: f"""HR Business Partner / Talent Acquisition Specialist
{random.choice(['Zomato Limited','Nykaa (FSN E-Commerce Ventures)','PhonePe Pvt. Ltd.','Meesho Inc.','Dream11 (Sporta Technologies)'])}
Location: {random.choice(['Bangalore','Mumbai','Gurgaon'])} — Hybrid

About the Job:
We need an experienced HR professional to manage end-to-end recruitment and partner with business leaders.

Requirements:
- MBA in HR / Post Graduate Diploma in HRM
- {random.choice(['2-4','3-6','1-3'])} years of talent acquisition or HR BP experience
- Experience with {random.choice(['Workday','SAP SuccessFactors','BambooHR','Darwinbox'])} HRMS
- Strong understanding of labor laws and compliance
- Excellent interpersonal and negotiation skills

Key Responsibilities:
- Partner with hiring managers to define job requirements and sourcing strategy
- Manage end-to-end recruitment for {random.choice(['tech','business','product'])} roles
- Drive employer branding and campus hiring initiatives
- Support performance management and employee engagement programs

CTC: {random.choice(['8-12 LPA','6-10 LPA','10-15 LPA'])}
Selection: HR Screening → Competency Interview → Case Presentation → Offer
hr.careers@{random.choice(['zomato.com','nykaa.com','phonepe.com'])}
""",

    # UI/UX Design
    lambda: f"""UI/UX Designer — Product Design
{random.choice(['Zoho Corporation Pvt. Ltd.','Freshworks Inc.','MakeMyTrip Limited','PolicyBazaar (PB Fintech Ltd.)','Paytm (One97 Communications)'])}
Location: {random.choice(['Chennai','Bangalore','Noida','Gurgaon'])}

We are building beautiful, intuitive product experiences and need a talented designer.

Requirements:
- Bachelor's in Design, Fine Arts, or Human-Computer Interaction
- {random.choice(['2-5','3-6','1-4'])} years of product design experience
- Mastery of Figma and Adobe XD / Illustrator / Photoshop
- Strong portfolio demonstrating UX process (research → wireframe → prototype → test)
- Experience with design systems and accessibility standards (WCAG)

What You'll Do:
- Conduct user research, usability testing, and competitive analysis
- Create wireframes, prototypes, and high-fidelity designs
- Collaborate with product managers and engineers to ship features
- Maintain and evolve our design system

Compensation: {random.choice(['10-18 LPA','8-14 LPA','12-20 LPA'])}
Process: Portfolio Review → Design Challenge → Culture Fit → Offer
Apply: design-team@{random.choice(['zoho.com','freshworks.com','makemytrip.com'])}
""",

    # DevOps / Cloud
    lambda: f"""DevOps / Site Reliability Engineer
{random.choice(['Adobe Systems India Pvt. Ltd.','Microsoft India (R&D) Pvt. Ltd.','Google India Pvt. Ltd.','Amazon India Development Centre','Atlassian Pvt. Ltd.'])}
Location: {random.choice(['Bangalore','Hyderabad','Pune'])} — {random.choice(['Hybrid','On-site'])}

Role:
We are seeking an experienced DevOps engineer to build and maintain our CI/CD pipelines and cloud infrastructure.

Required:
- B.Tech / B.E. in Computer Science or related field
- {random.choice(['3-6','4-8','2-5'])} years of DevOps / SRE experience
- Strong expertise in {random.choice(['AWS (EC2, EKS, Lambda, RDS)','GCP (GKE, Cloud Run, BigQuery)','Azure (AKS, Azure DevOps, Functions)'])}
- Proficiency in Docker, Kubernetes, Terraform, Ansible
- Experience with monitoring tools: Prometheus, Grafana, Datadog, PagerDuty
- Scripting skills in Python, Bash, or Go

Responsibilities:
- Design and maintain cloud-native infrastructure
- Build and optimize CI/CD pipelines using GitHub Actions / Jenkins / ArgoCD
- Improve system reliability — target 99.99% uptime
- Lead incident response and post-mortems

CTC: {random.choice(['15-25 LPA','12-20 LPA','18-30 LPA'])}
Interview: Online Coding → System Design → Infrastructure Round → HR
careers@{random.choice(['adobe.com','microsoft.com','google.com'])}
""",

    # Sales / Business Development
    lambda: f"""Sales Executive / Business Development Manager
{random.choice(['HDFC Bank Limited','ICICI Bank Ltd.','Bajaj Finance Limited','Axis Bank Ltd.','Kotak Mahindra Bank Ltd.'])}
Location: {random.choice(['Pan India (Multiple Locations)','Mumbai','Delhi NCR','Bangalore'])}

We are expanding our {random.choice(['retail banking','insurance','loan products','investment'])} sales team.

Eligibility:
- Graduation in any discipline (MBA preferred)
- {random.choice(['1-3','0-2','2-5'])} years of sales experience (freshers may apply for junior roles)
- Strong communication and negotiation skills
- Willingness to travel within the assigned territory
- Own vehicle preferred

Responsibilities:
- Acquire new customers and achieve monthly sales targets
- Cross-sell banking products — {random.choice(['credit cards, home loans','personal loans, SIPs','life insurance, health insurance'])}
- Maintain CRM records and submit daily sales reports
- Build long-term client relationships

CTC: {random.choice(['3-6 LPA','4-8 LPA','2-4 LPA'])} + performance incentives + allowances
Training: Comprehensive {random.choice(['4-week','2-week','6-week'])} induction program provided
Apply: sales.recruitment@{random.choice(['hdfcbank.com','icicibank.com','bajajfinserv.com'])}
""",

    # Operations / Supply Chain
    lambda: f"""Operations Manager / Supply Chain Analyst
{random.choice(['Amazon India','Myntra Designs Pvt. Ltd.','Delhivery Limited','BlueDart Express Limited','Ekart Logistics Pvt. Ltd.'])}
Location: {random.choice(['Bangalore','Gurgaon','Mumbai','Hyderabad'])}

Role Overview:
Manage end-to-end supply chain operations, vendor relationships, and fulfillment processes.

Required Qualifications:
- B.E. / B.Tech (Industrial / Mechanical) or MBA Operations / Supply Chain
- {random.choice(['3-6','2-5','4-8'])} years of operations management experience
- Expertise in {random.choice(['SAP SCM / WMS','Oracle SCM','Microsoft Dynamics'])}
- Strong analytical skills with Excel / Python / SQL for data-driven decision-making
- Knowledge of lean manufacturing, Six Sigma preferred

Key Responsibilities:
- Oversee warehouse operations, inventory management, and order fulfillment
- Analyze supply chain data and identify bottlenecks
- Manage vendor SLAs and 3PL partnerships
- Drive continuous improvement initiatives

CTC: {random.choice(['9-14 LPA','7-12 LPA','12-18 LPA'])}
Interview: Aptitude Test → Operations Case Study → Technical Interview → HR Discussion
Apply: ops.careers@{random.choice(['amazon.in','myntra.com','delhivery.com'])}
""",

    # Content / Copywriting
    lambda: f"""Content Writer / Senior Copywriter
{random.choice(['Dentsu Webchutney','JWT India','Grey Group India','Ogilvy India','McCann Worldgroup India'])}
Location: {random.choice(['Mumbai','Delhi','Bangalore'])} (Hybrid, {random.choice(['3','2','4'])} days/week in office)

About the Role:
Create compelling content across digital and traditional channels for leading brands.

Requirements:
- Bachelor's in English, Mass Communication, Journalism, or Marketing
- {random.choice(['2-5','3-7','1-4'])} years of copywriting or content writing experience
- Portfolio demonstrating work across digital, social media, print, and video scripts
- Excellent command over English; {random.choice(['Hindi proficiency preferred','Tamil/Telugu is a plus','working knowledge of regional language preferred'])}
- Experience with SEO content strategy is a plus

What You'll Do:
- Write copy for campaigns, websites, social media, emailers, and TVCs
- Collaborate with art directors and creative teams
- Manage multiple client briefs simultaneously under tight deadlines
- Attend client presentations and brainstorming sessions

CTC: {random.choice(['6-12 LPA','5-10 LPA','8-14 LPA'])}
Apply with portfolio: content.careers@{random.choice(['dentsu.com','grey.com','ogilvy.com'])}
""",
]

# ─── Generate dataset ─────────────────────────────────────────────────────────

def generate_dataset(n_fake=300, n_legit=300):
    samples = []

    # Generate fake samples — cycle through all scam types
    fake_cycle = itertools.cycle(FAKE_SCAM_TYPES)
    for _ in range(n_fake):
        gen = next(fake_cycle)
        text = gen()
        # Light random variation: shuffle one sentence
        samples.append({'text': text.strip(), 'label': 1})   # 1 = fake

    # Generate legit samples — cycle through all job types
    legit_cycle = itertools.cycle(LEGIT_JOB_TYPES)
    for _ in range(n_legit):
        gen = next(legit_cycle)
        text = gen()
        samples.append({'text': text.strip(), 'label': 0})   # 0 = legit

    random.shuffle(samples)
    return samples


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    samples = generate_dataset(n_fake=350, n_legit=350)

    out_path = os.path.join('data', 'labeled_jobs.csv')
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'label'])
        writer.writeheader()
        writer.writerows(samples)

    fake_count  = sum(1 for s in samples if s['label'] == 1)
    legit_count = sum(1 for s in samples if s['label'] == 0)
    print(f"Dataset saved to {out_path}")
    print(f"Total: {len(samples)} | Fake: {fake_count} | Legit: {legit_count}")
