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

### Frontend (React)
- User interface for uploading resumes
- Job description input
- Results visualization
- Real-time analysis feedback

### Backend (Flask/Python)
- REST API endpoints
- PDF/Text parsing
- LLM integration
- Database management

### Database (SQLite)
- Resume storage
- Screening results
- Historical analysis

### LLM Integration
- OpenAI GPT-4 (primary)
- Fallback rule-based matching
- Semantic analysis
- Score calculation

## Data Flow
1. User uploads resume(s) + job description
2. Backend parses and extracts structured data
3. LLM analyzes resume against job requirements
4. Results stored in database
5. Frontend displays ranked candidates

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
