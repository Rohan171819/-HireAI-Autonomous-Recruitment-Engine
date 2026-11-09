from fastapi import UploadFile, File, Form
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class JobInput(BaseModel):
    type: str = Field(..., description="url|pdf|text")
    content: str = Field(..., description="URL, base64 PDF, or raw text")

class PipelineOptions(BaseModel):
    cover_letter_tones: List[str] = ["formal", "confident", "conversational"]
    include_cold_email: bool = True
    include_interview_prep: bool = True

class PipelineRequest(BaseModel):
    job_input: JobInput
    user_profile_id: str
    options: Optional[PipelineOptions] = Field(default_factory=PipelineOptions)

class PipelineResponse(BaseModel):
    job_id: str
    status: str
