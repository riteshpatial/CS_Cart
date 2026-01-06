import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AI_MODE = os.getenv("AI_MODE", "demo")  # demo | prod
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
