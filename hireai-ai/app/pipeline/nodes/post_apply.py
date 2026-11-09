import json
import asyncio
from app.services.ollama_client import ollama_client
from app.models.state import PipelineState

async def post_apply_node(state: PipelineState):
    if not state.job_description:
        raise ValueError("Missing Job Description for intel generation")

    # Generate Interview Prep Kit
    prompt = f"""
    Create a comprehensive interview prep kit for the {state.job_description.title} role at {state.job_description.company}.
    
    CONTEXT:
    - Job Requirements: {state.job_description.requirements}
    - User Skills: {state.user_profile.skills if state.user_profile else "Not provided"}
    
    REQUIREMENTS:
    1. Provide 5 behavioral questions (using STAR method) tailored to this company and role.
    2. Provide 5 technical questions focusing on the gaps between the user's skills and job requirements.
    3. For each question, provide an "Ideal Answer" and a "Personalized Tip" based on the user's profile.
    
    Return ONLY a valid JSON list of objects: 
    [{{ "category": "behavioral|technical", "question": "...", "ideal_answer": "...", "personalized_tip": "..." }}]
    """
    
    # Generate Follow-up Sequence
    follow_up_prompt = f"""
    Create a high-conversion 3-email follow-up sequence for the {state.job_description.title} role at {state.job_description.company}.
    
    CONTEXT:
    - Company: {state.job_description.company}
    - User Name: {state.user_profile.full_name if state.user_profile else "the candidate"}
    
    SEQUENCE:
    1. Immediate Thank You: Focus on a specific point discussed (leave a placeholder [Mention Specific Topic]).
    2. 3-Day Check-in: Professional nudge, reiterating value proposition.
    3. 14-Day Final Follow-up: "Closing the loop" email, remaining open for future opportunities.
    
    Return ONLY a valid JSON list of objects: 
    [{{ "day": 0, "subject": "...", "body": "..." }}]
    """

    # Execute LLM calls in parallel
    results = await asyncio.gather(
        ollama_client.generate(prompt),
        ollama_client.generate(follow_up_prompt)
    )
    
    # Parse Prep Kit
    try:
        prep_kit = json.loads(results[0])
    except Exception:
        prep_kit = []
        
    # Parse Follow-up
    try:
        follow_up_sequence = json.loads(results[1])
    except Exception:
        follow_up_sequence = []

    return {
        "post_apply_intel": {
            "interview_prep": prep_kit,
            "follow_up_sequence": follow_up_sequence
        },
        "progress": 100,
        "status": "completed"
    }
