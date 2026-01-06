from app.config import settings

class OpenAIService:
    def generate(self, event: str, details: str) -> str:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OpenAI API key missing")

        # PLACEHOLDER (real OpenAI code later)
        return f"[OPENAI RESPONSE]\nEvent: {event}\nDetails: {details}"
