import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPERSET_BASE_URL = os.getenv("SUPERSET_BASE_URL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SUPERSET_USERNAME = os.getenv("SUPERSET_USERNAME")
    SUPERSET_PASSWORD = os.getenv("SUPERSET_PASSWORD")
    
settings = Settings()