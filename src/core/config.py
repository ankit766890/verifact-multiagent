from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "VeriFact Enterprise"
    APP_VERSION: str = "2.4.0-PROD"
    APP_ENV: str = "production"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    RATE_LIMIT_PER_MINUTE: int = 120
    MAX_CLAIM_LENGTH: int = 2500
    MAX_CLAIMS_PER_ANALYSIS: int = 12
    CORS_ORIGINS: List[str] = ["*"]

    MAX_PARALLEL_RESEARCH_TASKS: int = 8
    AGENT_TIMEOUT_SECONDS: int = 30
    MIN_CONFIDENCE_THRESHOLD: float = 0.60
    STRICT_CITATION_VERIFICATION: bool = True

    # Integrations (Plug-and-play production keys)
    SEARCH_API_KEY: str = ""
    LLM_API_KEY: str = ""
    AUDIT_WEBHOOK_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
