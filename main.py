import os
from flask import Flask, request, jsonify, render_template

from google import genai
import PyPDF2
import time


# ==============================
# CONFIG
# ==============================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client = genai.Client(api_key="AIzaSyDGE8UiKyQE8UFatFFyU8aVnL0rmK8nkPM")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==============================
# RETRY HELPER
# ==============================
def call_gemini_api(prompt, model="gemini-2.5-flash", max_retries=5):
    """Call Gemini API with exponential backoff retry for 503 errors."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            
            # Check for 503 overload error
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # exponential backoff: 1s, 2s, 4s, 8s, 16s
                    print(f"API overloaded (503). Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ValueError(f"Gemini API overloaded (503). Please try again in a few minutes.")
            
            # Other error types
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                raise ValueError("Gemini API quota exceeded. Please try again later or upgrade your API plan.")
            elif "403" in error_msg or "PERMISSION_DENIED" in error_msg:
                raise ValueError("Invalid Gemini API key or insufficient permissions.")
            else:
                raise ValueError(f"Gemini API error: {error_msg}")

# ==============================
# PDF PARSING
# ==============================
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# ==============================
# RESUME PARSER (LLM)
# ==============================
def parse_resume(resume_text):
    prompt = f"""
You are a resume parser.

Extract:
- Skills
- Experience summary
- Education
- Tools & technologies

Resume:
{resume_text}

Return in bullet points.
"""
    return call_gemini_api(prompt)

# ==============================
# JOB DESCRIPTION PARSER
# ==============================
def parse_job_description(jd_text):
    prompt = f"""
Extract:
- Required skills
- Responsibilities
- Preferred qualifications

Job Description:
{jd_text}

Return in bullet points.
"""
    return call_gemini_api(prompt)

# ==============================
# ATS MATCHING
# ==============================
def ats_match(parsed_resume, parsed_jd):
    prompt = f"""
You are an Applicant Tracking System (ATS).

Compare the resume and job description.

Resume:
{parsed_resume}

Job Description:
{parsed_jd}

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT add explanations
- Do NOT wrap in markdown
- Do NOT add text before or after

JSON FORMAT:
{{
  "match_score": number between 0 and 100,
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "strengths": ["point1", "point2"],
  "improvement_suggestions": ["point1", "point2"]
}}
"""
    return call_gemini_api(prompt).strip()



# ==============================
# API ROUTE (PDF UPLOAD)
# ==============================

import json
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

import json
def extract_json(text):
    import re, json
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in Gemini response")
    return json.loads(match.group())

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "Resume PDF is required"}), 400

        resume_file = request.files["resume"]
        jd_text = request.form.get("job_description")

        if not jd_text:
            return jsonify({"error": "Job description is required"}), 400

        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
        resume_file.save(pdf_path)

        resume_text = extract_text_from_pdf(pdf_path)
        print("===== EXTRACTED RESUME TEXT =====")
        print(resume_text[:1000])  # print first 1000 chars
        print("================================")
        
        parsed_resume = parse_resume(resume_text)
        parsed_jd = parse_job_description(jd_text)
        ats_result_text = ats_match(parsed_resume, parsed_jd)

        try:
            ats_result = extract_json(ats_result_text)
        except Exception as e:
            print("RAW ATS RESPONSE:", ats_result_text)
            return jsonify({"error": "Invalid ATS JSON response"}), 500

        return jsonify({
            "parsed_resume": parsed_resume,
            "parsed_job_description": parsed_jd,
            "ats_result": ats_result
        })
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 429
    except Exception as e:
        error_msg = str(e)
        print(f"Unexpected error: {error_msg}")
        return jsonify({"error": "An unexpected error occurred during analysis"}), 500

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(debug=True, port=8080)