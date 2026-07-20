"""Application settings for SAP Execution Service."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "sap_execution_service"
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "*"
    database_url: str = "sqlite:///./sap_execution_service.db"


@lru_cache
def get_settings() -> "Settings":
    return Settings()
