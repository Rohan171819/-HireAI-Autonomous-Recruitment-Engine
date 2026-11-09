# HireAI - Project Specification & Build Plan

## Project Overview
**HireAI** - AI-Powered Job Application Assistant
- End-to-end AI assistant that reads job descriptions, matches skills, and generates tailored applications in under 60 seconds
- 6-phase intelligent pipeline + Interactive Interview Simulator: JD Ingestion → Portfolio Analysis → AI Skill Matching → Doc Generation → QA Validation → Post-Apply Intel → Mock Interview Mode
- Target: 1.5B+ global job seekers, $2.4B AI recruitment tools market

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO FRONTEND (Teammate)               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ User Auth   │  │ Dashboard   │  │ Application Tracker │  │
│  │ Profile Mgmt│  │ Results UI  │  │ History/Analytics   │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          ▼                                   │
│              ┌─────────────────────┐                         │
│              │   Django REST API   │                         │
│              │   (Internal Bridge) │                         │
│              └──────────┬──────────┘                         │
└─────────────────────────┼────────────────────────────────────┘
                          │ HTTP/JSON (async via Celery)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  FASTAPI AI MICROSERVICE (You)              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              LANGGRAPH 6-PHASE PIPELINE             │   │
│  │  JD Ingest → Portfolio → Match → Generate → QA →   │   │
│  │  Post-Apply                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            INTERACTIVE INTERVIEW SIMULATOR           │   │
│  │      (Stateful Chat: Recruit AI ↔ User Response)     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────┐  │
│  │   OLLAMA     │ │  PyMuPDF/    │ │  PostgreSQL/       │  │
│  │  (Gemma 4 31B) │ │  Playwright  │ │  Supabase (Vector) │  │
│  └──────────────┘ └──────────────┘ └────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack Decisions

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Frontend Framework** | Django + HTMX/Tailwind | Teammate knows Django |
| **AI Backend** | FastAPI + LangGraph | Clean separation, async, OpenAPI |
| **LLM** | Ollama Cloud (Gemma 4 31B + nomic-embed-text) | High reasoning, cloud-powered, precise |
| **Parsing** | PyMuPDF (PDF), Playwright (URL/LinkedIn) | Robust extraction |
| **Vector DB** | Supabase (pgvector) | Managed, scales, free tier |
| **Task Queue** | Celery + Redis | Reliable, Django-native |
| **PDF Gen** | WeasyPrint (HTML→PDF) | Template-based, CSS support |
| **Deploy** | Railway / Render / Fly.io | Simple Docker deploy |
| **Monitoring** | Sentry + Structured Logs | Free tier sufficient |

---

## Monorepo Structure

```
hireai/
├── docker-compose.yml          # Full stack local dev
├── .github/workflows/          # CI/CD
├── hireai-ai/                  # YOUR FastAPI microservice
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py             # FastAPI entry
│   │   ├── pipeline/           # LangGraph nodes
│   │   │   ├── nodes/
│   │   │   ├── state.py
│   │   │   └── graph.py
│   │   ├── services/
│   │   │   ├── ollama_client.py
│   │   │   ├── parser.py       # PDF, URL, LinkedIn
│   │   │   ├── ats_scorer.py
│   │   │   ├── doc_generator.py
│   │   │   └── interview_sim.py # Mock Interview Logic
│   │   ├── models/             # Pydantic schemas
│   │   └── api/v1/             # REST endpoints
│   └── tests/
└── hireai-web/                 # TEAMMATE Django project
    ├── pyproject.toml
    ├── Dockerfile
    ├── hireai_web/             # Project settings
    ├── core/                   # Home, dashboard
    ├── accounts/               # Auth, profiles
    ├── applications/           # Job apps, results
    ├── ai_client/              # FastAPI communication
    └── templates/              # HTML templates
```

---

## 6-Phase Pipeline Specification

### Phase 1: JD Ingestion
- **Inputs**: LinkedIn URL, Indeed/Naukri URL, PDF upload, raw text paste
- **Output**: Structured `JobDescription` (title, company, requirements, skills, description)
- **Tools**: Playwright (scraping), PyMuPDF (PDF), LLM (normalization)

### Phase 2: Portfolio Analysis
- **Inputs**: User resume (PDF), GitHub URL, LinkedIn URL, manual skills entry
- **Output**: `UserProfile` (skills, experience, projects, education, keywords)
- **Tools**: PyMuPDF, LLM extraction, embedding generation

### Phase 3: AI Skill Matching
- **Process**: Embedding similarity (semantic) + Keyword overlap (lexical) + LLM reasoning
- **Output**: `MatchResult` (ATS score 0-100, matched skills, missing skills, gap analysis, course suggestions)

### Phase 4: Document Generation
- **Outputs**:
  - Cover Letter (3 tones: Formal, Confident, Conversational)
  - Tailored Resume (keyword-optimized)
  - Cold Outreach Email (recruiter/hiring manager)
  - LinkedIn DM template
- **Tools**: Jinja2 templates + LLM prompts

### Phase 5: QA Validation
- **Checks**: Grammar (LanguageTool), ATS re-score, readability, tone consistency
- **Output**: Quality score, specific suggestions, pass/fail

### Phase 6: Post-Apply Intel
- **Outputs**: Follow-up email sequence (3 emails), Interview prep kit (5 Q&As behavioral + technical)
- **Timing**: Immediate + 3 days + 7 days + 14 days

### Phase 7: AI Interview Simulator (Interactive)
- **Process**: Stateful chat session where LLM acts as a recruiter
- **Flow**: Ask Question → User Answers → Analyze & Score → Suggest Better Answer → Next Question
- **Tools**: Gemma 4 (Recruiter Persona), Redis/DB for session state, FastAPI WebSocket/REST

---

## 4-6 Week Timeline

### WEEK 1: Foundation & AI Core
| Day | You (AI Backend) | Teammate (Django) |
|-----|------------------|-------------------|
| 1-2 | Monorepo, FastAPI, Poetry, Docker | Django project, apps structure |
| 2-3 | Ollama setup, model pull | Auth (allauth), profile models |
| 3-4 | LangGraph skeleton (6 nodes) | Application model, dashboard UI |
| 4-5 | JD Ingestion node | FastAPI client service |
| 5-6 | Portfolio Analysis node | Results display templates |
| 6-7 | Skill Matching node (ATS score) | Tailwind/Bootstrap styling |

### WEEK 2: Generation & Integration
| Day | You (AI Backend) | Teammate (Django) |
|-----|------------------|-------------------|
| 8-9 | Document Generation node | Celery integration, async jobs |
| 9-10 | QA Validation node | Real-time progress (HTMX/WS) |
| 10-11 | Post-Apply node | PDF/DOCX download |
| 11-12 | Pipeline integration testing | Application tracker, history |
| 12-13 | OpenAPI docs, versioning | Error handling, notifications |
| 13-14 | Caching, SSE streaming | Mobile responsive polish |

### WEEK 3: Advanced Features
- LinkedIn scraping (Playwright stealth)
- Multi-tone cover letters (prompt engineering)
- Cold email + LinkedIn DM generator
- Skills gap + course recommendations (vector search)
- Interview prep kit (JD-specific Q&As)
- AI Interview Simulator (Dynamic Mock Interview mode)
- Analytics dashboard (Chart.js)

### WEEK 4: Production Hardening
- Security: JWT inter-service, rate limiting, CORS
- Observability: Structured logs, Prometheus, Sentry
- Testing: Unit (80%+), integration, E2E (Playwright), load (Locust)
- CI/CD: GitHub Actions → Docker → Railway/Render
- Documentation: API docs, ADRs, runbooks

---

## Key Deliverables (MVP)

1. **Paste JD URL/text → Get in 60s**:
   - ATS match score (0-100)
   - 3 cover letter variants
   - Tailored resume (PDF/DOCX)
   - Cold email + LinkedIn DM
   - Missing skills + course links
   - Interactive Mock Interview access

2. **User Features**:
   - Auth + profile management
   - Application history & tracking
   - Re-run with different tones
   - Download all documents
   - Follow-up reminders

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Ollama Cloud latency | Use async streaming, optimize prompt tokens |
| LinkedIn blocks scraping | Manual paste fallback, stealth plugin, rate limits |
| Pipeline > 60s | SSE streaming, embedding cache, async phases |
| Teammate blocked | API contract first (OpenAPI), mock server |
| Scope creep | Strict MVP: JD → 3 docs + ATS only |

---

## Immediate Next Steps (Today)

1. Create monorepo with structure above
2. Set up `hireai-ai/` with FastAPI + Poetry + Docker
3. Install Ollama, pull `llama3.2` + `nomic-embed-text`
4. Define Pydantic schemas for pipeline state (share with teammate)
5. Build JD Ingestion node first (unblocks everything)

---

## API Contract (Share with Teammate)

```python
# POST /v1/pipeline/run
{
  "job_input": {
    "type": "url|pdf|text",
    "content": "https://linkedin.com/jobs/... or base64 PDF or raw text"
  },
  "user_profile_id": "uuid",
  "options": {
    "cover_letter_tones": ["formal", "confident", "conversational"],
    "include_cold_email": true,
    "include_interview_prep": true
  }
}

# Response: Job ID for polling
{"job_id": "uuid", "status": "processing"}

# GET /v1/pipeline/status/{job_id}
{"status": "completed", "progress": 100, "result": {...}}

# Result Schema
{
  "ats_score": 87,
  "matched_skills": ["Python", "FastAPI", "PostgreSQL"],
  "missing_skills": ["Kubernetes", "AWS"],
  "gap_analysis": "...",
  "course_suggestions": [...],
  "documents": {
    "cover_letters": {"formal": "...", "confident": "...", "conversational": "..."},
    "resume": "base64_pdf",
    "cold_email": "...",
    "linkedin_dm": "..."
  },
  "interview_prep": [{"question": "...", "answer": "..."}, ...],
  "follow_up_sequence": [...]
}
```

---

## Success Metrics

- Pipeline latency: < 60s (P95)
- ATS score accuracy: > 85% correlation with real ATS
- Document quality: < 3 grammar issues per doc
- User success: > 20% interview callback rate (track post-launch)