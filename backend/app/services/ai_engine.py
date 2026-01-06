from app.config import settings
from app.services.demo_ai_service import DemoAIService
from app.services.openai_service import OpenAIService

class AIEngine:
    def __init__(self):
        if settings.AI_MODE == "prod":
            self.service = OpenAIService()
        else:
            self.service = DemoAIService()

    def generate(self, event: str, details: str) -> str:
        return self.service.generate(event, details)
