<div align="center">

```
 ____                 _____ _            _  _____ ____  
|  _ \ __ _ ___ ___  |_   _| |__   ___  / \|_   _/ ___| 
| |_) / _` / __/ __|   | | | '_ \ / _ \/ _ \ | | \___ \ 
|  __/ (_| \__ \__ \   | | | | | |  __/ ___ \| |  ___) |
|_|   \__,_|___/___/   |_| |_| |_|\___/_/   \_\_| |____/ 
```

### *Where AI meets your career aspirations*

[![Made with Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)

[Live Demo](https://passtheats.onrender.com) · [Quick Start](#-quick-start) · [Features](#-features) · [Deploy](#-deployment)

<br>

<img src="static/assets/demo.gif" width="90%" alt="PassTheATS Demo" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />

<br>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" />

</div>

## 💭 The Story

You've spent hours perfecting your resume. You hit submit. **Silence.**

Was it the keywords? The format? The ATS? You'll never know—until now.

**PassTheATS** doesn't just scan your resume. It thinks like a recruiter, validates like an ATS, and coaches like a mentor. All powered by AI.

<br>

## 🌟 Features

### ✅ Core Resume Analysis
<table>
<tr>
<td width="33%">

**📄 Smart Upload**
- PDF resume parsing
- Job description input
- Role-based templates
- Real-time processing

</td>
<td width="33%">

**🎯 ATS Scoring**
- Keyword match analysis
- Missing keyword detection
- Compatibility percentage
- Industry benchmarks

</td>
<td width="33%">

**📊 Visual Reports**
- Interactive dashboard
- Progress tracking
- Historical analysis
- Export capabilities

</td>
</tr>
</table>

### 🧠 Skill Proof Verification *(Unique Feature)*

Unlike traditional ATS tools, we verify if skills are actually **proven**:

```
❌ Listed Only   → Skill mentioned but no evidence
✅ Proven        → Backed by projects/experience

Skill Strength:
├─ 🟢 Strong   (Multiple proofs)
├─ 🟡 Medium   (Some proof)
├─ 🟠 Weak     (Minimal proof)
└─ 🔴 Missing  (No mention)
```

**Output:** Proof Score (%), Skill classification, Recommendations

### 🚨 Anti-Cheat Detection

Identifies resume manipulation:

- **Keyword Stuffing** - Excessive repetition without context
- **Fake Skills** - Listed but never used in experience
- **Weak Evidence** - Claims without substantiation

**Risk Levels:** `LOW` | `MEDIUM` | `HIGH`  
**Output:** Detailed reasons, statistics, actionable fixes

### 🎯 Role-Based Rubric Scoring

Weighted evaluation like real companies:

```javascript
const rubric = {
  "Backend Engineer": {
    skills: 35%,      // Technical competency
    experience: 30%,  // Years & relevance
    projects: 20%,    // Practical work
    education: 15%    // Academic background
  }
}
```

**Roles Supported:** Backend, Frontend, Cloud, DevOps, Data Science, Product, and more

### 🤖 AI-Powered Intelligence

Gemini API integration for advanced insights:

| Feature | Description |
|---------|-------------|
| 💡 **Resume Suggestions** | Personalized improvement recommendations |
| 🎤 **Interview Questions** | Role-specific questions based on your resume |
| 🧠 **Recruiter Verdict** | Professional assessment of overall readiness |
| 🎯 **Gap Analysis** | Identifies missing skills for target role |

**Reliability:** Smart fallback logic if API fails

### 🔐 User System

Full authentication & history management:

- ✅ Secure registration & login
- ✅ Password hashing (Werkzeug)
- ✅ Analysis history storage
- ✅ Full report replay
- ✅ Delete saved reports
- ✅ Progress visualization

<br>

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

### AI & Tools
![Google Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### DevOps
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

**Architecture:**
```
Flask (Backend) → Gemini AI → PostgreSQL (Prod) / SQLite (Dev)
         ↓
    Docker Container → Render Cloud → CI/CD
```

<br>

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/raahul-kr/PassTheATS.git
cd PassTheATS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cat > .env << EOF
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///instance/hirelens.db
EOF

# 4. Run application
python app.py

# 5. Open browser
# → http://localhost:5000
```

### 🐳 Docker Setup

```bash
# Build image
docker build -t passtheats .

# Run container
docker run -p 5000:5000 --env-file .env passtheats

# Access at http://localhost:5000
```

### ☁️ Production (Render)

**Live URL:** [https://passtheats.onrender.com](https://passtheats.onrender.com)

**Features:**
- ✅ Docker-based deployment
- ✅ Managed PostgreSQL database
- ✅ Auto-deploy via GitHub Actions
- ✅ Environment variable management
- ✅ SSL/HTTPS enabled

<br>

## 📂 Project Map

```
PassTheATS/
├── 🧠 core/           # Intelligence layer
├── 🎨 templates/      # User interface
├── 💾 db/             # Data models
├── 📁 static/         # Assets & styles
└── 🚀 app.py          # Mission control
```

<details>
<summary>📋 View detailed structure</summary>

```
PassTheATS/
│
├── 📄 .dockerignore               # Docker build exclusions
├── 📄 .env                        # Environment variables (create this)
├── 📄 .gitignore                  # Git ignore rules
├── 🚀 app.py                      # Flask application entry point
├── 🐳 Dockerfile                  # Container configuration
├── 📜 LICENSE                     # MIT License
├── 🔧 list_models.py              # Gemini model utility
├── 📖 README.md                   # This file
├── 📋 requirements.txt            # Python dependencies
│
├── 📁 .github/                    # GitHub configuration
│   └── workflows/
│       └── render-deploy.yml      # CI/CD pipeline
│
├── 🧠 core/                       # Intelligence layer
│   ├── ai_interview_questions.py  # AI question generator
│   ├── ai_suggestions.py          # AI resume tips
│   ├── ai_summary.py              # AI recruiter verdict
│   ├── cheat_detector.py          # ⭐ Keyword stuffing detection
│   ├── interview_questions.py     # Base interview questions
│   ├── jd_parser.py               # Job description parsing
│   ├── jd_templates.py            # Pre-built JD templates
│   ├── keyword_extractor.py       # Keyword identification
│   ├── proof_checker.py           # ⭐ Skill verification
│   ├── resume_parser.py           # PDF text extraction
│   ├── resume_sections.py         # Section identification
│   ├── rubrics.py                 # Role-based scoring
│   ├── scoring_engine.py          # ATS score calculation
│   ├── __init__.py                # Package initializer
│   └── __pycache__/               # Python bytecode cache
│
├── 💾 db/                         # Database layer
│   ├── models.py                  # SQLAlchemy models (User, Report)
│   └── __pycache__/               # Python bytecode cache
│
├── 📂 instance/                   # Runtime data
│   └── hirelens.db                # SQLite database (dev only)
│
├── 🎨 static/                     # Frontend assets
│   ├── style.css                  # ⭐ Minimal glassmorphism design
│   ├── assets/                    # Images, icons
│   ├── css/                       # Additional stylesheets
│   └── js/
│       └── theme.js               # ⭐ Advanced theme engine
│
├── 📄 templates/                  # HTML views
│   ├── demo.html                  # Try without signup
│   ├── history.html               # Analysis history
│   ├── index.html                 # Landing page
│   ├── login.html                 # User authentication
│   ├── register.html              # User registration
│   └── report.html                # Analysis results
│
└── 📤 uploads/                    # File storage
    └── resumes/                   # PDF resume uploads
```

</details>


## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root (never commit this):

```bash
# Required - Get from https://ai.google.dev/
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
# Development (SQLite)
DATABASE_URL=sqlite:///instance/hirelens.db

# Production (PostgreSQL - Render auto-provides this)
# DATABASE_URL=postgresql://user:pass@host:port/dbname

# Optional
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### Customization

**Role-Based Rubrics** (`core/rubrics.py`):
```python
RUBRICS = {
    "Software Engineer": {
        "skills_weight": 0.35,
        "experience_weight": 0.30,
        "projects_weight": 0.20,
        "education_weight": 0.15
    },
    "Your Custom Role": {
        # Add your weights here
    }
}
```

**Job Description Templates** (`core/jd_templates.py`):
```python
TEMPLATES = {
    "Backend Engineer": """
    [Existing template...]
    """,
    "Your Custom Role": """
    [Your custom JD template...]
    """
}
```

<br>

## 🎯 How It Works

```mermaid
graph LR
    A[📄 Upload Resume] --> B[🔍 Parse PDF]
    B --> C[🎯 Extract Keywords]
    C --> D[🧠 Verify Skills]
    D --> E[🚨 Check Stuffing]
    E --> F[📊 Calculate Scores]
    F --> G[🤖 AI Analysis]
    G --> H[💡 Generate Report]
    H --> I[💾 Save History]
    
    style A fill:#e1f5ff,color:#000
    style B fill:#fff3e0,color:#000
    style C fill:#f3e5f5,color:#000
    style D fill:#e8f5e9,color:#000
    style E fill:#fce4ec,color:#000
    style F fill:#e1f5ff,color:#000
    style G fill:#fff3e0,color:#000
    style H fill:#f3e5f5,color:#000
```

<br>

## 💡 What Makes Us Different

| Feature | Traditional ATS | PassTheATS |
|---------|:---------------:|:----------:|
| Keyword Matching | ✅ Basic | ✅ Advanced |
| Skill Proof Verification | ❌ None | ✅ **Unique** |
| Keyword Stuffing Detection | ❌ None | ✅ **Unique** |
| AI Resume Suggestions | ❌ None | ✅ Gemini-powered |
| AI Interview Questions | ❌ None | ✅ Role-aware |
| Role-Based Rubrics | ❌ Generic | ✅ Company-style |
| Recruiter Verdict | ❌ None | ✅ AI summary |
| Progress Tracking | ❌ One-time | ✅ Full history |
| Cloud Deployment | ❌ Local only | ✅ Production-ready |
| Docker Support | ❌ None | ✅ Containerized |
| CI/CD Pipeline | ❌ Manual | ✅ Automated |

<br>

## 🔄 CI/CD Pipeline

Automated deployment via GitHub Actions (`.github/workflows/render-deploy.yml`):

```yaml
GitHub Push → GitHub Actions → Docker Build → Render Deploy
     ↓              ↓                ↓              ↓
   main       Run Tests       Create Image     Live Update
```

**Workflow Features:**
- ✅ Triggers on push to `main` branch
- ✅ Builds Docker container
- ✅ Deploys to Render automatically
- ✅ Zero manual intervention
- ✅ Instant rollback capability

<br>

## 🐳 Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

**.dockerignore:**
```
__pycache__/
*.pyc
*.pyo
.env
.git/
instance/
uploads/
.vscode/
.idea/
*.log
```

**Build & Run:**
```bash
# Local build
docker build -t passtheats .

# Run with environment file
docker run -p 5000:5000 --env-file .env passtheats

# Run with inline env vars
docker run -p 5000:5000 \
  -e GEMINI_API_KEY=your_key \
  -e DATABASE_URL=sqlite:///instance/hirelens.db \
  passtheats
```

<br>

## 🗺️ Roadmap

### ✅ Completed (v1.0)
- [x] Core ATS analysis engine
- [x] PDF resume parsing
- [x] Skill proof verification system
- [x] Keyword stuffing detection
- [x] AI integration (Google Gemini)
- [x] User authentication & sessions
- [x] Analysis history & reports
- [x] Role-based rubric scoring
- [x] Docker containerization
- [x] PostgreSQL production database
- [x] Cloud deployment (Render)
- [x] CI/CD automation (GitHub Actions)
- [x] Dark mode theme support

### 🚧 In Progress (v1.1)
- [ ] PDF report export functionality
- [ ] Email notifications for analysis completion
- [ ] Pre-built resume templates
- [ ] Batch resume analysis
- [ ] Enhanced error handling

### 🌟 Planned (v2.0)
- [ ] **Recruiter Dashboard** - Multi-resume comparison
- [ ] **LinkedIn Integration** - Import profile data
- [ ] **Cover Letter Analyzer** - AI-powered review
- [ ] **ATS Simulation Modes** - Company-specific emulation
- [ ] **REST API** - Third-party integrations
- [ ] **Mobile App** - React Native
- [ ] **Browser Extension** - Chrome/Firefox
- [ ] **Team Collaboration** - Multi-user workspaces
- [ ] **Analytics Dashboard** - Usage insights
- [ ] **White-label Solution** - Custom branding

<br>

## 🎪 Try It Now

### 🎬 Demo Mode
**No signup required** → [Try Demo](https://passtheats.onrender.com/demo)

### 🔥 Full Features
**Create free account** → [Sign Up](https://passtheats.onrender.com/register)

```
┌─────────────────────────────────────┐
│  1. 📂 Upload your resume (PDF)     │
│  2. 📝 Paste job description        │
│  3. ⚡ Click "Analyze Resume"       │
│  4. 🎉 Get comprehensive insights   │
│  5. 📊 Save & track progress        │
│  6. 💡 Iterate and improve          │
└─────────────────────────────────────┘
```

<br>

## 🧠 One-Line Resume Summary

> Built an AI-powered resume analysis platform using Flask and Gemini API that evaluates ATS compatibility, verifies skill proof, detects keyword stuffing, generates AI-driven resume feedback and interview questions, with Docker-based cloud deployment on Render, PostgreSQL persistence, and automated CI/CD via GitHub Actions.

**Tech Stack:** Python · Flask · Gemini AI · PostgreSQL · Docker · GitHub Actions · Render

<br>

## 📌 Project Status

| Component | Status | Details |
|-----------|:------:|---------|
| 🐳 **Dockerization** | ✅ Complete | Multi-platform container support |
| ☁️ **Cloud Deployment** | ✅ Live | https://passtheats.onrender.com |
| 🗄️ **PostgreSQL** | ✅ Production | Managed database on Render |
| 🔄 **CI/CD** | ✅ Automated | GitHub Actions workflow |
| 🚀 **Production Ready** | ✅ Stable | SSL, HTTPS, monitoring |
| 📱 **Mobile Responsive** | ✅ Optimized | Works on all devices |
| 🌙 **Dark Mode** | ✅ Advanced | Smart theme switching |
| 🔐 **Security** | ✅ Secure | Password hashing, SQL injection protection |

<br>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/PassTheATS.git
cd PassTheATS

# 3. Create a feature branch
git checkout -b feature/amazing-feature

# 4. Make your changes and commit
git add .
git commit -m "Add: amazing feature description"

# 5. Push to your fork
git push origin feature/amazing-feature

# 6. Open a Pull Request on GitHub
```

**Contribution Guidelines:**
- Follow PEP 8 Python style guide
- Write clear commit messages
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting
- Include examples in your PR description

<br>

## 📜 License

MIT © 2025 Rahul Kumar  
*Free to use, free to modify, free to share*

<br>

<div align="center">

## 👨‍💻 Creator

**Rahul Kumar**  
*B.Tech CSE · Backend & Cloud Enthusiast*

[![GitHub](https://img.shields.io/badge/raahul--kr-100000?style=flat&logo=github&logoColor=white)](https://github.com/raahul-kr)
[![LinkedIn](https://img.shields.io/badge/Connect-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/raahul-kr)

*Building tools that make a difference* 🚀

<br>

---

<sub>**PassTheATS** · Empowering job seekers with AI-driven insights</sub>

⭐ Star this repo if it helped you land an interview!

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" />

**Made with ❤️ and lots of ☕**

</div>
