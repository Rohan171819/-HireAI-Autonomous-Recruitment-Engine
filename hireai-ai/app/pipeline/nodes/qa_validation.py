import json
from app.services.ollama_client import ollama_client
from app.models.state import PipelineState

async def qa_validation_node(state: PipelineState):
    if not state.documents:
        raise ValueError("No documents to validate")

    # Validate the formal cover letter as a sample
    sample_text = state.documents.cover_letters.get("formal", "")
    
    prompt = f"""
    Act as an expert career coach and ATS validator. 
    Analyze the following cover letter for grammar, tone consistency, and impact.
    Return a JSON object:
    {{
        "quality_score": (float 0-1),
        "suggestions": ["suggestion 1", "suggestion 2"],
        "status": "pass" | "fail"
    }}

    Text: {sample_text}
    """
    
    response = await ollama_client.generate(prompt)
    try:
        clean_json = response.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        qa_result = {
            "quality_score": data.get("quality_score", 0.0),
            "suggestions": data.get("suggestions", []),
            "status": data.get("status", "fail")
        }
    except Exception:
        qa_result = {"quality_score": 0.0, "suggestions": ["Validation failed"], "status": "fail"}
    
    return {
        "qa_result": qa_result,
        "progress": 90,
        "status": "validated"
    }
