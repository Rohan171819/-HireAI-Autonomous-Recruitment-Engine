from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from app.models.api import JobInput

class JobDescription(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    requirements: List[str] = []
    skills: List[str] = []
    description: str
    raw_text: str

class UserProfile(BaseModel):
    full_name: str
    email: str
    skills: List[str] = []
    experience: List[Dict] = []
    projects: List[Dict] = []
    education: List[Dict] = []
    keywords: List[str] = []
    resume_text: str

class MatchResult(BaseModel):
    ats_score: int = Field(..., ge=0, le=100)
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    gap_analysis: str = ""
    course_suggestions: List[str] = []

class GeneratedDocuments(BaseModel):
    cover_letters: Dict[str, str] = {} # tone -> content
    resume_optimized: Optional[str] = None # base64 or path
    cold_email: Optional[str] = None
    linkedin_dm: Optional[str] = None

class PipelineState(BaseModel):
    job_id: str
    user_id: str
    job_input: Optional[JobInput] = None
    job_description: Optional[JobDescription] = None
    user_profile: Optional[UserProfile] = None
    match_result: Optional[MatchResult] = None
    documents: Optional[GeneratedDocuments] = None
    qa_result: Optional[Dict] = None
    post_apply_intel: Optional[Dict] = None
    status: str = "pending"
    progress: int = 0
