# API Documentation

## Endpoints

### POST /api/upload
Upload and parse a resume

**Request:**
- Content-Type: multipart/form-data
- Body: file (PDF or TXT)

**Response:**
```json
{
  "success": true,
  "resume_id": 1,
  "data": {
    "candidate_name": "John Doe",
    "email": "john@example.com",
    "skills": ["Python", "React"],
    "experience_years": 5
  }
}
```

### POST /api/screen
Screen resumes against job description

**Request:**
```json
{
  "job_description": "Looking for Python developer...",
  "resume_ids": [1, 2, 3]
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "resume_id": 1,
      "candidate_name": "John Doe",
      "match_score": 8.5,
      "matched_skills": ["Python", "React"],
      "missing_skills": ["Docker"],
      "justification": "Strong match...",
      "recommendation": "Shortlist"
    }
  ]
}
```

### GET /api/resumes
Get all stored resumes

### GET /api/results/:resume_id
Get screening results for a specific resume