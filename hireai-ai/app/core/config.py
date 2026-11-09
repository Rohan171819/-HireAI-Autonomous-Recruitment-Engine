from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "super-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    CORS_ORIGINS: list[str] = ["*"]
    RATE_LIMIT_PER_MINUTE: int = 60
    SENTRY_DSN: str = ""
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_API_KEY: Optional[str] = None
    REDIS_URL: str = "redis://redis:6379/0"


    class Config:
        env_file = ".env"

settings = Settings()
