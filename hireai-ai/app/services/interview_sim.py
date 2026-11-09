import json
from app.services.ollama_client import ollama_client
from app.models.state import PipelineState

class InterviewSimulator:
    def __init__(self):
        self.sessions = {} # session_id -> chat_history

    async def start_interview(self, user_id: str, job_description: str):
        session_id = f"int_{user_id}_{id(job_description)}"
        
        prompt = f"""
        Act as a professional technical recruiter. Start a mock interview for the following job:
        {job_description}
        
        Introduce yourself briefly and ask the first behavioral or technical question.
        Keep it professional and engaging.
        """
        
        first_question = await ollama_client.generate(prompt)
        self.sessions[session_id] = [
            {"role": "assistant", "content": first_question}
        ]
        
        return {
            "session_id": session_id,
            "question": first_question
        }

    async def handle_response(self, session_id: str, user_answer: str):
        if session_id not in self.sessions:
            raise ValueError("Session not found")
            
        history = self.sessions[session_id]
        history.append({"role": "user", "content": user_answer})
        
        # Analyze answer and generate next question
        prompt = f"""
        You are a recruiter. The user is in a mock interview.
        History: {json.dumps(history)}
        
        Analyze the user's last answer. 
        Provide:
        1. A brief critique/score (0-10).
        2. A suggestion for a better answer.
        3. The next interview question.
        
        Return ONLY a JSON object:
        {{
            "score": int,
            "critique": "string",
            "suggestion": "string",
            "next_question": "string"
        }}
        """
        
        response = await ollama_client.generate(prompt)
        try:
            clean_json = response.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            # Store the recruiter's next question in history
            history.append({"role": "assistant", "content": data["next_question"]})
            return data
        except Exception:
            return {
                "score": 0,
                "critique": "Could not analyze answer",
                "suggestion": "Try being more specific",
                "next_question": "Can you tell me more about your experience?"
            }

interview_sim = InterviewSimulator()
