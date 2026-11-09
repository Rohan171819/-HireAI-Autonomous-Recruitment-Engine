import json
from app.services.ollama_client import ollama_client
from app.services.parser import parser
from app.models.state import JobDescription, PipelineState

async def jd_ingestion_node(state: PipelineState):
    # In a real flow, raw input would be passed via the state or an initial config
    # Handle case where state.job_description is a string (unstructured input) or a JobDescription object
    if isinstance(state.job_description, JobDescription):
        return {
            "job_description": state.job_description,
            "progress": 20,
            "status": "ingested"
        }

    raw_input = state.job_description if isinstance(state.job_description, str) else state.job_input.content if state.job_input else "No job description provided"
    
    if raw_input == "No job description provided":
        raise ValueError("No job description provided in input")
        raw_text = await parser.scrape_url(raw_input)
    elif raw_input.endswith(".pdf"):
        raw_text = parser.parse_pdf(raw_input)
    else:
        raw_text = raw_input

    prompt = f"""
    Extract structured job details from the following text. 
    Return ONLY a JSON object matching this schema:
    {{
        "title": "string",
        "company": "string",
        "location": "string",
        "requirements": ["string"],
        "skills": ["string"],
        "description": "string"
    }}

    Text: {raw_text}
    """
    
    # Use Pydantic schema to force structured output from Ollama
    response = await ollama_client.generate(prompt, response_format=JobDescription)
    try:
        clean_json = response.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        # Remove raw_text from data if present to avoid duplicate argument error
        data.pop("raw_text", None)
        job_desc = JobDescription(**data, raw_text=raw_text)
    except Exception as e:
        # Log error and fail fast instead of returning "Unknown"
        print(f"JD Parsing Error: {e} | Response: {response}")
        raise ValueError(f"Failed to extract structured job details: {e}")
    
    return {
        "job_description": job_desc,
        "progress": 20,
        "status": "ingested"
    }
