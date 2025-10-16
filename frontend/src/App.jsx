import React, { useState } from "react";
import {
  Upload,
  FileText,
  Briefcase,
  Users,
  CheckCircle,
  XCircle,
  Star,
} from "lucide-react";

export default function ResumeScreener() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumes, setResumes] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("upload");

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    const newResumes = files.map((file) => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      file: file,
      status: "pending",
    }));
    setResumes([...resumes, ...newResumes]);
  };

  const mockAnalysis = () => {
    setLoading(true);
    setTimeout(() => {
      const mockResults = resumes.map((resume, idx) => {
        const scores = [8.5, 7.2, 9.1, 6.5, 8.8, 5.9, 7.8];
        const score = scores[idx % scores.length];

        return {
          id: resume.id,
          name: resume.name.replace(".pdf", ""),
          score: score,
          matchedSkills: ["Python", "React", "Node.js", "AWS", "Docker"].slice(
            0,
            Math.floor(Math.random() * 3) + 3
          ),
          missingSkills: ["Kubernetes", "GraphQL", "TypeScript"].slice(
            0,
            Math.floor(Math.random() * 2) + 1
          ),
          experience: `${3 + idx} years`,
          education: ["B.Tech Computer Science", "M.S. Software Engineering"][
            idx % 2
          ],
          justification:
            score >= 7.5
              ? "Strong match with required skills and relevant experience. Candidate demonstrates proficiency in core technologies and has worked on similar projects."
              : score >= 6.5
              ? "Moderate match. Candidate has some relevant skills but lacks experience in key areas mentioned in the job description."
              : "Below threshold. Limited overlap with required qualifications. May need additional training or experience.",
          recommendation:
            score >= 7.5 ? "Shortlist" : score >= 6.5 ? "Maybe" : "Reject",
        };
      });

      setResults(mockResults.sort((a, b) => b.score - a.score));
      setLoading(false);
      setActiveTab("results");
    }, 2000);
  };

  const getScoreColor = (score) => {
    if (score >= 8) return "text-green-600 bg-green-50";
    if (score >= 6.5) return "text-yellow-600 bg-yellow-50";
    return "text-red-600 bg-red-50";
  };

  const getRecommendationBadge = (rec) => {
    const styles = {
      Shortlist: "bg-green-100 text-green-800 border-green-300",
      Maybe: "bg-yellow-100 text-yellow-800 border-yellow-300",
      Reject: "bg-red-100 text-red-800 border-red-300",
    };
    return styles[rec] || "";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Briefcase className="w-10 h-10 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">
              Smart Resume Screener
            </h1>
          </div>
          <p className="text-gray-600 ml-13">
            AI-powered resume matching with job descriptions
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-200">
          <button
            onClick={() => setActiveTab("upload")}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === "upload"
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            <Upload className="w-4 h-4 inline mr-2" />
            Upload & Configure
          </button>
          <button
            onClick={() => setActiveTab("results")}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === "results"
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-gray-500 hover:text-gray-700"
            }`}
            disabled={results.length === 0}
          >
            <Users className="w-4 h-4 inline mr-2" />
            Results ({results.length})
          </button>
        </div>

        {/* Upload Tab */}
        {activeTab === "upload" && (
          <div className="space-y-6">
            {/* Job Description */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5 text-blue-600" />
                Job Description
              </h2>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here...&#10;&#10;Example:&#10;We are looking for a Senior Full Stack Developer with:&#10;- 5+ years of experience in web development&#10;- Proficiency in React, Node.js, and Python&#10;- Experience with AWS and Docker&#10;- Strong problem-solving skills"
                className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              />
            </div>

            {/* Resume Upload */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5 text-blue-600" />
                Upload Resumes
              </h2>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  multiple
                  accept=".pdf,.txt,.doc,.docx"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="resume-upload"
                />
                <label htmlFor="resume-upload" className="cursor-pointer">
                  <Upload className="w-12 h-12 mx-auto text-gray-400 mb-3" />
                  <p className="text-gray-600 font-medium mb-1">
                    Click to upload resumes
                  </p>
                  <p className="text-sm text-gray-500">
                    PDF, TXT, DOC, DOCX (Max 10MB each)
                  </p>
                </label>
              </div>

              {resumes.length > 0 && (
                <div className="mt-4 space-y-2">
                  <h3 className="font-medium text-gray-700 mb-2">
                    Uploaded Files ({resumes.length})
                  </h3>
                  {resumes.map((resume) => (
                    <div
                      key={resume.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center gap-2">
                        <FileText className="w-4 h-4 text-blue-600" />
                        <span className="text-sm text-gray-700">
                          {resume.name}
                        </span>
                      </div>
                      <button
                        onClick={() =>
                          setResumes(resumes.filter((r) => r.id !== resume.id))
                        }
                        className="text-red-600 hover:text-red-700"
                      >
                        <XCircle className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Action Button */}
            <button
              onClick={mockAnalysis}
              disabled={!jobDescription || resumes.length === 0 || loading}
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Analyzing Resumes...
                </>
              ) : (
                <>
                  <Star className="w-5 h-5" />
                  Analyze & Match Candidates
                </>
              )}
            </button>
          </div>
        )}

        {/* Results Tab */}
        {activeTab === "results" && (
          <div className="space-y-4">
            {results.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <Users className="w-16 h-16 mx-auto text-gray-300 mb-4" />
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  No Results Yet
                </h3>
                <p className="text-gray-500">
                  Upload resumes and run analysis to see results
                </p>
              </div>
            ) : (
              <>
                {/* Summary Stats */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="text-2xl font-bold text-green-600">
                      {
                        results.filter((r) => r.recommendation === "Shortlist")
                          .length
                      }
                    </div>
                    <div className="text-sm text-green-700">Shortlisted</div>
                  </div>
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div className="text-2xl font-bold text-yellow-600">
                      {
                        results.filter((r) => r.recommendation === "Maybe")
                          .length
                      }
                    </div>
                    <div className="text-sm text-yellow-700">Maybe</div>
                  </div>
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <div className="text-2xl font-bold text-red-600">
                      {
                        results.filter((r) => r.recommendation === "Reject")
                          .length
                      }
                    </div>
                    <div className="text-sm text-red-700">Below Threshold</div>
                  </div>
                </div>

                {/* Candidate Cards */}
                {results.map((result, idx) => (
                  <div
                    key={result.id}
                    className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <div className="flex items-center gap-3">
                          <h3 className="text-xl font-semibold text-gray-900">
                            {result.name}
                          </h3>
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-semibold border ${getRecommendationBadge(
                              result.recommendation
                            )}`}
                          >
                            {result.recommendation}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">
                          {result.education} • {result.experience}
                        </p>
                      </div>
                      <div
                        className={`text-3xl font-bold ${getScoreColor(
                          result.score
                        )} px-4 py-2 rounded-lg`}
                      >
                        {result.score}/10
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-1">
                          <CheckCircle className="w-4 h-4 text-green-600" />
                          Matched Skills
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {result.matchedSkills.map((skill) => (
                            <span
                              key={skill}
                              className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-1">
                          <XCircle className="w-4 h-4 text-red-600" />
                          Missing Skills
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {result.missingSkills.map((skill) => (
                            <span
                              key={skill}
                              className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
                      <h4 className="text-sm font-semibold text-blue-900 mb-1">
                        AI Analysis
                      </h4>
                      <p className="text-sm text-blue-800">
                        {result.justification}
                      </p>
                    </div>
                  </div>
                ))}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
