"""Application settings for Approval Service."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "approval_service"
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "*"
    database_url: str = "sqlite:///./approval_service.db"
    audit_service_url: str = "http://audit-service:8007"
    request_timeout_seconds: float = 10.0


@lru_cache
def get_settings() -> "Settings":
    return Settings()
