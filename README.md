# PassTheATS 🚀
**Resume ATS Analyzer + Proof-Based Skill Verification**

PassTheATS is a modern resume screening web application that analyzes a resume against a job description and generates an ATS-style report.  
It goes beyond keyword matching by verifying whether the skills are actually proven in projects/experience and detects keyword stuffing risk.

---

## ✨ Key Features

### ✅ Student Mode (MVP)
- 📄 Upload Resume (PDF)
- 📝 Paste Job Description (JD) OR select a Role Template
- 📊 ATS Match Score (keyword-based)
- 🧾 Skill Proof Score (checks if skills are supported by evidence)
- 🛡️ Anti-Cheat / Keyword Stuffing Risk Detector
- 🎯 Role Fit Score (company-style rubric scoring)
- 🎤 Interview Questions Generator (based on gaps + weak claims)

### 🔐 Login + History (Product Mode)
- 👤 Register / Login / Logout
- 📂 Auto-save analysis reports in History
- 👁️ View full detailed report from History
- 🗑️ Delete saved reports

---

## 🧠 What Makes PassTheATS Different?
Most resume ATS tools only provide **keyword match %**.

PassTheATS adds:
- **Skill Proof Score** → detects skills that are only listed but not proven
- **Keyword Stuffing Risk** → flags suspicious resumes
- **Role Rubric Scoring** → real company-like scoring based on role priorities
- **Interview Questions** → helps candidates prepare smartly

---

## 🛠️ Tech Stack
- **Frontend:** HTML, Bootstrap 5
- **Backend:** Python (Flask)
- **Database:** SQLite (Flask-SQLAlchemy)
- **Resume Parsing:** pdfplumber
- **Auth Security:** Werkzeug Password Hashing

---

## 📂 Project Structure

```bash
PassTheATS/
│   app.py
│   requirements.txt
│   README.md
│
├── core/
│   ├── resume_parser.py
│   ├── keyword_extractor.py
│   ├── scoring_engine.py
│   ├── proof_checker.py
│   ├── cheat_detector.py
│   ├── interview_questions.py
│   ├── rubrics.py
│   ├── jd_templates.py
│   └── jd_parser.py
│
├── db/
│   └── models.py
│
├── templates/
│   ├── index.html
│   ├── demo.html
│   ├── report.html
│   ├── login.html
│   ├── register.html
│   └── history.html
│
├── static/
│   └── style.css
│
└── uploads/
    └── resumes/


## ⚙️ Installation & Run Locally

Follow these steps to get the project up and running on your local machine.

### 1️⃣ Clone the repository
Open your terminal and run the following commands to clone the repo and navigate into the directory:

```bash
git clone [https://github.com/raahul-kr/PassTheATS.git](https://github.com/raahul-kr/PassTheATS.git)
cd PassTheATS

### 2️⃣ Install dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt

### 3️⃣ Run the app
Start the Flask development server:

```bash
python app.py

### 4️⃣ Open in browser
Once the server is running, open your web browser and navigate to:

http://127.0.0.1:5000/