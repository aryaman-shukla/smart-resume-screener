from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import re
import json
from datetime import datetime
import sqlite3
import openai
import os

app = Flask(__name__)
CORS(app)

# Configure OpenAI (or any LLM API)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database setup
def init_db():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            candidate_name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            experience_years REAL,
            education TEXT,
            raw_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS screening_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            job_description TEXT,
            match_score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            justification TEXT,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# PDF parsing
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

# Resume parsing
def parse_resume(text):
    """Extract structured data from resume text"""
    data = {
        'candidate_name': '',
        'email': '',
        'phone': '',
        'skills': [],
        'experience_years': 0,
        'education': '',
        'raw_text': text
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        data['email'] = emails[0]
    
    # Extract phone
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    if phones:
        data['phone'] = phones[0]
    
    # Extract name (first line often contains name)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        data['candidate_name'] = lines[0]
    
    # Common skills to look for
    common_skills = [
        'python', 'java', 'javascript', 'react', 'node.js', 'angular', 'vue',
        'sql', 'mongodb', 'postgresql', 'aws', 'azure', 'gcp', 'docker', 
        'kubernetes', 'git', 'ci/cd', 'machine learning', 'deep learning',
        'tensorflow', 'pytorch', 'rest api', 'graphql', 'typescript', 'go',
        'rust', 'c++', 'html', 'css', 'tailwind', 'bootstrap', 'flask',
        'django', 'spring boot', 'express', 'fastapi', 'redis', 'elasticsearch'
    ]
    
    text_lower = text.lower()
    for skill in common_skills:
        if skill in text_lower:
            data['skills'].append(skill.title())
    
    # Extract experience (rough estimate)
    exp_patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience[:\s]+(\d+)\+?\s*years?',
    ]
    for pattern in exp_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            data['experience_years'] = int(matches[0])
            break
    
    # Extract education
    education_keywords = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'b.s', 'm.s', 'mba']
    for keyword in education_keywords:
        if keyword in text_lower:
            # Get surrounding context
            idx = text_lower.find(keyword)
            edu_section = text[max(0, idx-20):min(len(text), idx+100)]
            data['education'] = edu_section.strip()
            break
    
    return data

# Store resume in database
def store_resume(resume_data):
    """Store parsed resume in database"""
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO resumes (filename, candidate_name, email, phone, skills, 
                           experience_years, education, raw_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        resume_data.get('filename', ''),
        resume_data.get('candidate_name', ''),
        resume_data.get('email', ''),
        resume_data.get('phone', ''),
        json.dumps(resume_data.get('skills', [])),
        resume_data.get('experience_years', 0),
        resume_data.get('education', ''),
        resume_data.get('raw_text', '')
    ))
    resume_id = c.lastrowid
    conn.commit()
    conn.close()
    return resume_id

# LLM-based matching
def llm_match_resume(resume_text, job_description):
    """Use LLM to match resume with job description"""
    
    prompt = f"""You are an expert HR recruiter. Compare the following resume with the job description and provide a detailed analysis.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Please provide your analysis in the following JSON format:
{{
    "match_score": <float between 1-10>,
    "matched_skills": [<list of skills from resume that match job requirements>],
    "missing_skills": [<list of important skills from job description not in resume>],
    "justification": "<2-3 sentence explanation of the match score>",
    "recommendation": "<one of: 'Shortlist', 'Maybe', 'Reject'>"
}}

Consider:
1. Technical skills match
2. Experience level alignment
3. Educational qualifications
4. Relevant project experience
5. Cultural fit indicators

Be objective and provide specific reasoning."""

    try:
        # Using OpenAI GPT (you can replace with any LLM)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert HR recruiter with years of experience in technical hiring."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        # Fallback to rule-based matching if LLM fails
        print(f"LLM Error: {str(e)}")
        return rule_based_matching(resume_text, job_description)

def rule_based_matching(resume_text, job_description):
    """Fallback rule-based matching"""
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Extract skills from job description
    common_skills = [
        'python', 'java', 'javascript', 'react', 'node.js', 'angular', 
        'sql', 'mongodb', 'aws', 'docker', 'kubernetes'
    ]
    
    matched = []
    missing = []
    
    for skill in common_skills:
        if skill in job_lower:
            if skill in resume_lower:
                matched.append(skill.title())
            else:
                missing.append(skill.title())
    
    match_score = (len(matched) / max(len(matched) + len(missing), 1)) * 10
    
    if match_score >= 7.5:
        recommendation = "Shortlist"
        justification = "Strong alignment with job requirements based on technical skills."
    elif match_score >= 5:
        recommendation = "Maybe"
        justification = "Partial match with some relevant skills but gaps in key areas."
    else:
        recommendation = "Reject"
        justification = "Limited match with job requirements."
    
    return {
        "match_score": round(match_score, 1),
        "matched_skills": matched,
        "missing_skills": missing,
        "justification": justification,
        "recommendation": recommendation
    }

# Store screening results
def store_screening_result(resume_id, job_description, result):
    """Store screening analysis results"""
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO screening_results 
        (resume_id, job_description, match_score, matched_skills, 
         missing_skills, justification, recommendation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        resume_id,
        job_description,
        result['match_score'],
        json.dumps(result['matched_skills']),
        json.dumps(result['missing_skills']),
        result['justification'],
        result['recommendation']
    ))
    conn.commit()
    conn.close()

# API Routes
@app.route('/api/upload', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Extract text
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
        
        # Parse resume
        resume_data = parse_resume(text)
        resume_data['filename'] = file.filename
        
        # Store in database
        resume_id = store_resume(resume_data)
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'data': resume_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/screen', methods=['POST'])
def screen_resumes():
    """Screen multiple resumes against job description"""
    data = request.json
    job_description = data.get('job_description', '')
    resume_ids = data.get('resume_ids', [])
    
    if not job_description or not resume_ids:
        return jsonify({'error': 'Job description and resume IDs required'}), 400
    
    results = []
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    
    for resume_id in resume_ids:
        # Get resume from database
        c.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        resume = c.fetchone()
        
        if not resume:
            continue
        
        # Perform matching
        match_result = llm_match_resume(resume[8], job_description)  # raw_text is at index 8
        
        # Store results
        store_screening_result(resume_id, job_description, match_result)
        
        results.append({
            'resume_id': resume_id,
            'candidate_name': resume[2],
            'email': resume[3],
            'match_score': match_result['match_score'],
            'matched_skills': match_result['matched_skills'],
            'missing_skills': match_result['missing_skills'],
            'justification': match_result['justification'],
            'recommendation': match_result['recommendation'],
            'experience_years': resume[6],
            'education': resume[7]
        })
    
    conn.close()
    
    # Sort by match score
    results.sort(key=lambda x: x['match_score'], reverse=True)
    
    return jsonify({
        'success': True,
        'results': results
    }), 200

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    """Get all stored resumes"""
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT id, filename, candidate_name, email, skills, experience_years, education FROM resumes')
    resumes = c.fetchall()
    conn.close()
    
    return jsonify({
        'resumes': [
            {
                'id': r[0],
                'filename': r[1],
                'candidate_name': r[2],
                'email': r[3],
                'skills': json.loads(r[4]) if r[4] else [],
                'experience_years': r[5],
                'education': r[6]
            }
            for r in resumes
        ]
    }), 200

@app.route('/api/results/<int:resume_id>', methods=['GET'])
def get_screening_results(resume_id):
    """Get screening results for a specific resume"""
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM screening_results WHERE resume_id = ? ORDER BY created_at DESC', (resume_id,))
    results = c.fetchall()
    conn.close()
    
    return jsonify({
        'results': [
            {
                'id': r[0],
                'job_description': r[2],
                'match_score': r[3],
                'matched_skills': json.loads(r[4]),
                'missing_skills': json.loads(r[5]),
                'justification': r[6],
                'recommendation': r[7],
                'created_at': r[8]
            }
            for r in results
        ]
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
