# Hire-AI Web Implementation Roadmap

## Project Overview
**Goal:** An AI-powered recruitment platform to automate screening and matching.
**Core Value:** Reducing time-to-hire using AI.
**Target Users:** Job Seekers (Candidates) & HR Managers (Recruiters).

---

## Tech Stack (The Foundation)
- **Frontend:** React.js / Next.js, Tailwind CSS.
- **Backend:** Node.js / Python (FastAPI or Django).
- **Database:** MongoDB or PostgreSQL.
- **AI Engine:** OpenAI API / LangChain / PyTorch.

---

## Implementation Steps

### Phase 1: User Authentication & Roles
- Implement JWT-based Auth (Login/Signup).
- **Candidate Role:** Resume upload, Job search, Application tracking.
- **Recruiter Role:** Job posting, Candidate filtering, Dashboard.

### Phase 2: Candidate Experience
- **Profile Builder:** Personal details, experience, skills.
- **Smart Resume Upload:** PDF upload feature.
- **Job Board:** Search and filter jobs based on skills.

### Phase 3: Recruiter Dashboard
- **Job Creator:** Form to add Job Title, Description, and Required Skills.
- **Applicant Management:** List of all people who applied for a specific job.
- **Status Update:** Change status (e.g., Applied -> Shortlisted -> Rejected).

### Phase 4: AI Integration (Core Feature)
- **Resume Parsing:** Extracting skills and experience from PDF using AI.
- **AI Scoring:** Matching Resume vs. Job Description (Match % score).
- **Automated Screening:** AI generates custom questions based on the resume.

### Phase 5: Workflow & Integration
- **Email Notifications:** Notify candidates upon shortlisting.
- **Interview Scheduler:** Integration with Google Calendar/Calendly.
- **Testing:** Unit tests for AI logic and UI responsiveness.

---

## Execution Plan
- **Week 1:** UI Design & Database Schema.
- **Week 2:** Authentication & Basic Profiles.
- **Week 3:** Job Posting & Application Flow.
- **Week 4:** AI Engine Integration & Final Polishing.
