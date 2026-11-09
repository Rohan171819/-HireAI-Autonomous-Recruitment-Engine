import ollama
from typing import Any
from app.models.state import JobDescription
from app.core.config import settings

class OllamaClient:
    def __init__(self, model_name: str = "phi3:mini"):
        self.model_name = model_name
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)

    async def generate(self, prompt: str, response_format: Any = None) -> str:
        # If response_format is passed as a Pydantic model, get its JSON schema
        fmt = response_format
        if hasattr(response_format, "model_json_schema"):
            fmt = response_format.model_json_schema()
        elif isinstance(response_format, str) and response_format.lower() == "json":
            fmt = "json"

        response = self.client.generate(
            model=self.model_name,
            prompt=prompt,
            format=fmt,
            options={"temperature": 0, "num_predict": 1024}
        )
        return response['response']

ollama_client = OllamaClient()
