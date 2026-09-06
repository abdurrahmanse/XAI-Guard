import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "XAI-Guard API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"
    
    # Defaults for local dev without env vars
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/xaiguard")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    class Config:
        case_sensitive = True

settings = Settings()
