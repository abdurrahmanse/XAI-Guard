import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "XAI-Guard API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"
    
    # Required for async SQLAlchemy
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:password@localhost:5434/postgres"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6380/0")
    
    class Config:
        case_sensitive = True

settings = Settings()
