"""
Application configuration management using Pydantic Settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = "Medical Research Agent API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # AI Model Configuration
    google_api_key: str
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    max_tokens: int = 2048
    
    # Search APIs
    tavily_api_key: Optional[str] = None
    
    # PubMed Configuration
    pubmed_email: str = "wondem5060@gmail.com"
    pubmed_tool: str = "MedicalResearchAgent"
    pubmed_max_results: int = 10
    
    # Agent Configuration
    agent_max_iterations: int = 10
    agent_timeout: int = 300  # 5 minutes
    
    # Rate Limiting
    rate_limit_calls: int = 100
    rate_limit_period: int = 60  # seconds
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
