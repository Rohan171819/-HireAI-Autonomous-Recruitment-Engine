import redis
import json
from app.core.config import settings
from app.models.state import PipelineState

class JobStore:
    def __init__(self):
        # Using REDIS_URL from settings
        self.client = redis.from_url(settings.REDIS_URL or "redis://redis:6379/0")

    def set_job(self, job_id: str, state: PipelineState):
        # Store as JSON string
        self.client.set(f"job:{job_id}", state.json())

    def get_job(self, job_id: str) -> PipelineState:
        data = self.client.get(f"job:{job_id}")
        if not data:
            return None
        return PipelineState.parse_raw(data)

    def update_job(self, job_id: str, updates: dict):
        state = self.get_job(job_id)
        if state:
            updated_data = state.dict()
            updated_data.update(updates)
            self.set_job(job_id, PipelineState(**updated_data))
            return True
        return False

job_store = JobStore()
