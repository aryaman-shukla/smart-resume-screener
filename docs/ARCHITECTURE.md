# System Architecture

## Overview
Smart Resume Screener uses a client-server architecture with the following components:

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