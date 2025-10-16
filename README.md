# Smart Resume Screener 🎯

An intelligent AI-powered resume screening system that matches candidates with job descriptions using Large Language Models (LLMs) for semantic analysis and scoring.

## 📋 Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [LLM Prompts](#llm-prompts)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)

---

## ✨ Features

- **Intelligent Resume Parsing** – Extract structured data from PDF/Text resumes  
- **Semantic Matching** – LLM-powered comparison between resumes and job descriptions  
- **Scoring System** – 1–10 match score with detailed justification  
- **Skill Analysis** – Identify matched and missing skills  
- **Candidate Ranking** – Automatic sorting by relevance  
- **REST API** – Full-featured backend API  
- **Interactive Dashboard** – Modern React-based frontend  
- **Persistent Storage** – SQL-based storage for resumes and match results  

---

## 🏗️ Architecture

The **Smart Resume Screener** follows a modular, service-oriented architecture:

### **1. Input Layer**
- **Resume Upload Service:** Accepts PDF/Text resumes via REST API or dashboard.  
- **Job Description Input:** Accepts text or file upload for analysis.

### **2. Parsing & Extraction Layer**
- **Resume Parser:**
  - Uses NLP tools (spaCy / PyPDF2 / pdfplumber) to extract *skills, education, experience,* and *achievements*.
  - Converts unstructured resumes into structured JSON.

### **3. LLM Semantic Matching Layer**
- **Purpose:** Uses an LLM (GPT-4 / Claude / Gemini) to perform **semantic similarity**, **fit scoring**, and **contextual matching**.
- **Functions:**
  - Compare resumes and job descriptions.
  - Generate a **match score (1–10)**.
  - Provide a **textual justification**.
  - Identify **matched** and **missing skills**.
- Implemented using LangChain or a custom LLM wrapper.

### **4. Scoring & Ranking Layer**
- Aggregates results from the LLM:
  - `match_score`
  - `matched_skills`
  - `missing_skills`
  - `fit_summary`
- Stores structured results in a SQL database.
- Automatically ranks candidates by match score.

### **5. Storage Layer**
- **Database:** PostgreSQL / MySQL  
- **Core Tables:**
  - `resumes`
  - `job_descriptions`
  - `matches`
  - `skills`
- Stores parsed resume data, job descriptions, and computed match results.

### **6. API Layer**
- **Backend Framework:** FastAPI / Flask / Express.js  
- **Key Endpoints:**
  - `POST /upload_resume`
  - `POST /upload_job_description`
  - `GET /get_matches`
- Handles file parsing, LLM calls, and database interactions.

### **7. Frontend Layer (Optional)**
- **Framework:** React.js + Tailwind CSS  
- **Features:**
  - Resume and JD upload interface  
  - Visualization of scores and skill matches  
  - Candidate ranking table with justifications  

### **8. Deployment**
- **Containerization:** Docker  
- **Hosting:** Render / AWS / Railway  
- **Environment Variables:**  
  - `OPENAI_API_KEY`  
  - `DB_URL`  
  - `MODEL_NAME`  

---

## 🧠 LLM Prompts

Below are example prompt templates used for semantic matching and skill extraction.  
They can be customized or orchestrated using LangChain or custom prompt templates.

### **Prompt 1 — Resume-to-JD Matching**
```text
You are an AI recruitment assistant. 
Compare the following RESUME and JOB DESCRIPTION and provide:
1. A match score between 1–10 (10 = perfect fit)
2. A brief justification for your score
3. A list of matched skills
4. A list of missing skills

RESUME:
{{resume_text}}

JOB DESCRIPTION:
{{job_description}}

Respond in JSON:
{
  "match_score": <number>,
  "justification": "<text>",
  "matched_skills": [ ... ],
  "missing_skills": [ ... ]
}
