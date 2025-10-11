"""
Configuration settings for CORE-SE Demo Backend
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # App mode
    MODE: str = "demo"
    
    # Database
    DATABASE_URL: str = "sqlite:///./core_demo.db"
    
    # External services
    FDS_BASE_URL: str = "http://localhost:8001"
    OPENAI_API_KEY: Optional[str] = None
    
    # Authentication
    DEMO_AUTH_TOKEN: str = "demo-token-123"
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Feature flags
    FEATURE_EMAIL: bool = True
    FEATURE_WINDCHILL: bool = True
    FEATURE_OUTLOOK: bool = True
    FEATURE_AI_MICROCALLS: bool = True
    FEATURE_TRACE_GRAPH: bool = True
    FEATURE_THEMES: bool = True
    
    # AI settings
    OPENAI_MODEL: str = "gpt-4o-mini"
    AI_TIMEOUT: int = 30
    MODEL: Optional[str] = None  # For backward compatibility
    VITE_MODEL: Optional[str] = None
    VITE_OPENAI_API_KEY: Optional[str] = None
    
    # Embedding settings
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    VECTOR_DIMENSIONS: int = 1536
    
    # Cache settings
    CACHE_TTL_PULSE: int = 300  # 5 minutes
    CACHE_TTL_IMPACT: int = 600  # 10 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
