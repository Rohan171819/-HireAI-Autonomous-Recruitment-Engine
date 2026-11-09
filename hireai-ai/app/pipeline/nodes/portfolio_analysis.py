import json
from app.services.ollama_client import ollama_client
from app.services.parser import parser
from app.models.state import UserProfile, PipelineState

async def portfolio_analysis_node(state: PipelineState):
    # In a real flow, we'd fetch the user's resume path/content using state.user_id
    # For MVP, we use a sample text or mock path. 
    # If state.user_profile is already provided, skip analysis.
    if state.user_profile:
        return {
            "user_profile": state.user_profile,
            "progress": 40,
            "status": "profile_analyzed"
        }

    resume_input = "John Doe. Experienced Python Developer. Skills: FastAPI, Docker, PostgreSQL. Projects: AI Chatbot, E-commerce API."
    
    if resume_input.endswith(".pdf"):
        resume_text = parser.parse_pdf(resume_input)
    else:
        resume_text = resume_input

    prompt = f"""
    Extract structured professional profile details from the following resume text. 
    Return ONLY a JSON object matching this schema:
    {{
        "full_name": "string",
        "email": "string",
        "skills": ["string"],
        "experience": [{{ "role": "string", "company": "string", "duration": "string", "description": "string" }}],
        "projects": [{{ "name": "string", "description": "string", "tech_stack": ["string"] }}],
        "education": [{{ "degree": "string", "institution": "string", "year": "string" }}],
        "keywords": ["string"]
    }}

    Text: {resume_text}
    """
    
    response = await ollama_client.generate(prompt)
    try:
        clean_json = response.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        user_profile = UserProfile(**data, resume_text=resume_text)
    except Exception:
        user_profile = UserProfile(
            full_name="Unknown",
            email="unknown@example.com",
            resume_text=resume_text
        )
    
    return {
        "user_profile": user_profile,
        "progress": 40,
        "status": "profile_analyzed"
    }
