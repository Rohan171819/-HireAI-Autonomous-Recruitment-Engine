import json
from app.services.ollama_client import ollama_client
from app.models.state import MatchResult, PipelineState

async def skill_matching_node(state: PipelineState):
    if not state.job_description or not state.user_profile:
        # Fallback to prevent pipeline crash during testing if nodes were skipped
        # In production, these should be mandatory precursors
        raise ValueError("Missing Job Description or User Profile for matching")

    jd_skills = state.job_description.skills
    user_skills = state.user_profile.skills

    prompt = f"""
    Compare the following Job Requirements with the User Profile and provide an ATS-style match analysis.
    Return the result as a JSON object.

    Job Skills: {jd_skills}
    User Skills: {user_skills}

    Required JSON format:
    {{
        "ats_score": (integer 0-100),
        "matched_skills": ["skill1", "skill2"],
        "missing_skills": ["skill3", "skill4"],
        "gap_analysis": "detailed explanation of the gap",
        "course_suggestions": ["Course A for Skill X", "Course B for Skill Y"]
    }}
    """
    
    # Force structured output for ATS matching
    response = await ollama_client.generate(prompt, response_format=MatchResult)
    try:
        clean_json = response.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        match_result = MatchResult(**data)
    except Exception as e:
        print(f"Matching Error: {e} | Response: {response}")
        raise ValueError(f"Failed to calculate ATS match result: {e}")
    
    return {
        "match_result": match_result,
        "progress": 60,
        "status": "skills_matched"
    }
