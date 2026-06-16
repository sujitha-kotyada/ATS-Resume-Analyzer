# 📄 ATS Resume Analyzer

An AI-powered Applicant Tracking System (ATS) that analyzes resumes against job descriptions to provide match scores, skill gap analysis, and actionable improvement suggestions — powered by **Google Gemini 2.5 Flash**.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind%20CSS-CDN-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

---

## ✨ Features

- **📤 PDF Resume Upload** — Upload your resume in PDF format via a drag-and-drop interface
- **📝 Job Description Input** — Paste any job description for targeted analysis
- **🎯 ATS Match Score** — Get a percentage-based compatibility score (0–100%) with animated circular gauge
- **✅ Matching Skills Detection** — See which of your skills align with the job requirements
- **❌ Missing Skills Identification** — Discover skills gaps you need to address
- **💪 Strengths Analysis** — Understand what makes your resume stand out
- **💡 Improvement Suggestions** — Get actionable recommendations to boost your ATS score
- **📊 Parsed Data Viewer** — Collapsible section to inspect the raw parsed resume and job description

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Flask                     |
| AI Model   | Google Gemini 2.5 Flash           |
| PDF Parser | PyPDF2                            |
| Frontend   | HTML, Tailwind CSS (CDN), JavaScript |
| Icons      | Font Awesome 6                    |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed
- A **Google Gemini API key** ([Get one here](https://aistudio.google.com/apikey))

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/sujitha-kotyada/ATS-Resume-Analyzer.git
   cd ATS-Resume-Analyzer
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install flask google-genai PyPDF2
   ```

5. **Configure your API key**

   Open `main.py` and replace the API key on line 15 with your own Gemini API key:

   ```python
   client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
   ```

6. **Run the application**

   ```bash
   python main.py
   ```

7. **Open in browser**

   Navigate to [http://localhost:8080](http://localhost:8080)

---

## 📖 Usage

1. **Upload** your resume PDF using the drag-and-drop zone
2. **Paste** the target job description into the text area
3. Click **"Analyze Resume"** and wait for the AI to process
4. Review your results:
   - 🎯 **ATS Match Score** — animated circular progress gauge
   - ✅ **Matching Skills** — green-tagged skills you already have
   - ❌ **Missing Skills** — red-tagged skills to work on
   - 💪 **Strengths** — what's working well in your resume
   - 💡 **Suggestions** — specific improvements to make

---

## 🔌 API Reference

### `POST /analyze`

Analyzes a resume against a job description.

**Request:** `multipart/form-data`

| Field             | Type   | Required | Description                      |
|-------------------|--------|----------|----------------------------------|
| `resume`          | File   | ✅       | PDF resume file                  |
| `job_description` | String | ✅       | Plain text job description       |

**Response:** `application/json`

```json
{
  "parsed_resume": "Bullet-point summary of the resume...",
  "parsed_job_description": "Bullet-point summary of the JD...",
  "ats_result": {
    "match_score": 75,
    "matching_skills": ["Python", "Flask", "REST APIs"],
    "missing_skills": ["Docker", "Kubernetes"],
    "strengths": ["Strong backend experience", "Relevant projects"],
    "improvement_suggestions": ["Add cloud deployment experience", "Include certifications"]
  }
}
```

---

## 📁 Project Structure

```
ATS-Resume-Analyzer/
├── main.py              # Flask backend with Gemini AI integration
├── templates/
│   └── index.html       # Frontend UI (Tailwind CSS + JavaScript)
├── uploads/             # Temporary PDF storage (gitignored)
├── .gitignore
└── README.md
```

---

## ⚠️ Important Notes

- The `uploads/` directory is used for temporary PDF storage and is excluded from version control
- API calls include **exponential backoff retry** logic for handling Gemini 503 (overload) errors
- For production use, store your API key in environment variables instead of hardcoding it

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋‍♀️ Author

**Sujitha Kotyada** — [@sujitha-kotyada](https://github.com/sujitha-kotyada)
