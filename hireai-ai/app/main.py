from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, Request, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from uuid import uuid4
from typing import Dict, Optional
from app.models.api import PipelineRequest, PipelineResponse
from app.models.state import PipelineState
from app.pipeline.graph import pipeline_app
from app.services.interview_sim import interview_sim
from app.core.config import settings
from app.core.auth import verify_jwt
from app.core.job_store import job_store
from app.core.logging import get_logger
from app.services.parser import parser

logger = get_logger()

app = FastAPI(title="HireAI AI Microservice")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Use Redis job store instead of in-memory dictionary
# jobs: Dict[str, PipelineState] = {}


async def execute_pipeline(job_id: str, request: PipelineRequest):
    state = job_store.get_job(job_id)
    if not state:
        logger.error(f"Job {job_id} not found in store")
        return

    try:
        logger.info(f"Starting pipeline execution for job {job_id}")
        # Initial input for the graph
        initial_state = state.dict()
        initial_state["job_input"] = request.job_input 
        
        # Convert Pydantic models to dicts for LangGraph state update
        initial_state = {k: (v.dict() if hasattr(v, 'dict') else v) for k, v in initial_state.items()}
        
        # Run the LangGraph pipeline using astream to update progress in real-time
        final_output = None
        async for event in pipeline_app.astream(initial_state):
            for node_name, node_state in event.items():
                logger.info(f"Node {node_name} completed for job {job_id}")
                
                # Extract progress and status from the node's output
                progress = node_state.get("progress", 0)
                status = node_state.get("status", state.status)
                
                # Update Redis in real-time
                job_store.update_job(job_id, {
                    "progress": progress,
                    "status": status
                })
                # Capture the latest state as the potential final output
                final_output = node_state

        # FINAL FIX: Ensure we save the absolute final state to Redis
        if final_output:
            # Merge final output with existing state to avoid losing data
            current_state = job_store.get_job(job_id)
            full_final_state = current_state.dict()
            full_final_state.update(final_output)
            
            # Force set the final state as completed
            full_final_state["status"] = "completed"
            full_final_state["progress"] = 100
            
            job_store.set_job(job_id, PipelineState(**full_final_state))
            logger.info(f"Pipeline final state successfully persisted for job {job_id}")
        else:
            # Fallback to ainvoke if stream failed to capture anything
            final_res = await pipeline_app.ainvoke(initial_state)
            job_store.set_job(job_id, PipelineState(**final_res))

    except Exception as e:
        job_store.update_job(job_id, {"status": "failed"})
        logger.exception(f"Pipeline error for job {job_id}: {str(e)}")

@app.get("/")
async def root():
    return {"message": "HireAI AI Service is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/v1/pipeline/run", response_model=PipelineResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def run_pipeline(
    request: Request,
    background_tasks: BackgroundTasks,
    user_profile_id: str = Form(...),
    job_input_type: str = Form(..., description="url|pdf|text"),
    job_input_content: str = Form(...),
    job_description_file: UploadFile = File(None),
    resume_file: UploadFile = File(None),
):
    job_id = str(uuid4())
    
    # 1. Handle Job Description (JD) Upload/Input
    extracted_jd_text = None
    if job_description_file:
        # Save JD file temporarily
        jd_temp_path = f"jd_{job_id}_{job_description_file.filename}"
        with open(jd_temp_path, "wb") as buffer:
            buffer.write(await job_description_file.read())
        
        try:
            extracted_jd_text = parser.parse_pdf(jd_temp_path)
            logger.info(f"Successfully parsed JD PDF for job {job_id}")
        except Exception as e:
            logger.error(f"JD PDF Parsing failed for job {job_id}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"JD PDF parsing failed: {str(e)}")
        finally:
            import os
            if os.path.exists(jd_temp_path):
                os.remove(jd_temp_path)
    
    # Use extracted JD text or the raw content provided
    effective_jd_input = extracted_jd_text if extracted_jd_text else job_input_content

    # 2. Handle Resume Upload
    extracted_resume_text = None
    if resume_file:
        # Save resume file temporarily
        res_temp_path = f"res_{job_id}_{resume_file.filename}"
        with open(res_temp_path, "wb") as buffer:
            buffer.write(await resume_file.read())
        
        try:
            extracted_resume_text = parser.parse_pdf(res_temp_path)
            logger.info(f"Successfully parsed Resume PDF for job {job_id}")
        except Exception as e:
            logger.error(f"Resume PDF Parsing failed for job {job_id}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Resume PDF parsing failed: {str(e)}")
        finally:
            import os
            if os.path.exists(res_temp_path):
                os.remove(res_temp_path)

    # Initialize state
    state = PipelineState(
        job_id=job_id,
        user_id=user_profile_id,
        status="processing",
        progress=0
    )
    
    # We use the JD text as the primary pipeline input
    # If a resume was uploaded, we can store it in the state for later nodes to use
    # For now, we pass the effective JD input to the background task
    
    # Create a dummy PipelineRequest object for the background task
    from app.models.api import PipelineRequest, JobInput
    dummy_payload = PipelineRequest(
        job_input=JobInput(type=job_input_type, content=effective_jd_input),
        user_profile_id=user_profile_id
    )
    
    # If we have extracted resume text, we can add it to the job store state
    # so the pipeline nodes can access it directly from Redis
    updated_state_data = state.dict()
    if extracted_resume_text:
        updated_state_data["resume_text"] = extracted_resume_text
        
    job_store.set_job(job_id, PipelineState(**updated_state_data))
    
    # Integrate with LangGraph pipeline
    background_tasks.add_task(execute_pipeline, job_id, dummy_payload)
    
    return PipelineResponse(job_id=job_id, status="processing")

@app.get("/v1/pipeline/status/{job_id}")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_status(
    request: Request,
    job_id: str, 
):
    state = job_store.get_job(job_id)
    if not state:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "status": state.status,
        "progress": state.progress,
        "result": state if state.status == "completed" else None
    }

@app.post("/v1/interview/start")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def start_interview(
    request: Request, 
    user_id: str, 
    job_description: str, 
):
    return await interview_sim.start_interview(user_id, job_description)

@app.post("/v1/interview/chat")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def chat_interview(
    request: Request, 
    session_id: str, 
    answer: str, 
):
    try:
        return await interview_sim.handle_response(session_id, answer)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

