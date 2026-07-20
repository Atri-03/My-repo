"""Application settings for User Service."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "user_service"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./user_service.db"


@lru_cache
def get_settings() -> "Settings":
    return Settings()
