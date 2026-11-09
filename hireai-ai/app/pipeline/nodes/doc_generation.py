import json
import asyncio
from app.services.ollama_client import ollama_client
from app.models.state import GeneratedDocuments, PipelineState

async def doc_generation_node(state: PipelineState):
    if not state.job_description or not state.user_profile:
        raise ValueError("Missing Job Description or User Profile for generation")

    # Define tasks for parallel execution
    async def generate_cover_letter(tone):
        prompt = f"""
        Write a {tone} cover letter for the position of {state.job_description.title} at {state.job_description.company}.
        User Profile: {state.user_profile.skills}
        Job Requirements: {state.job_description.requirements}
        
        Return only the cover letter text.
        """
        return tone, await ollama_client.generate(prompt)

    tones = ["formal", "confident", "conversational"]
    
    email_prompt = f"""
    Write a professional cold email to a recruiter for the {state.job_description.title} position at {state.job_description.company}.
    Highlight these skills: {state.user_profile.skills}.
    """
    
    dm_prompt = f"""
    Write a short, punchy LinkedIn DM to the hiring manager for the {state.job_description.title} role at {state.job_description.company}.
    """

    # Execute all LLM calls in parallel
    tasks = [generate_cover_letter(tone) for tone in tones]
    tasks.append(ollama_client.generate(email_prompt))
    tasks.append(ollama_client.generate(dm_prompt))
    
    results = await asyncio.gather(*tasks)

    # Process results
    cover_letters = {}
    for res in results:
        if isinstance(res, tuple):
            tone, text = res
            cover_letters[tone] = text
    
    # The last two results are the email and DM
    # Filter out tuples to find the strings
    texts = [r for r in results if isinstance(r, str)]
    cold_email = texts[0] if len(texts) > 0 else ""
    linkedin_dm = texts[1] if len(texts) > 1 else ""

    documents = GeneratedDocuments(
        cover_letters=cover_letters,
        cold_email=cold_email,
        linkedin_dm=linkedin_dm
    )
    
    return {
        "documents": documents,
        "progress": 80,
        "status": "documents_generated"
    }
