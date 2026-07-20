"""Application settings for MCP Gateway Service."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "mcp_gateway_service"
    api_v1_prefix: str = "/api/v1"
    transcript_service_url: str = "http://transcript-service:8001"
    document_extraction_service_url: str = "http://document-extraction-service:8002"
    fs_service_url: str = "http://fs-service:8003"
    ts_service_url: str = "http://ts-service:8004"
    review_service_url: str = "http://review-service:8005"
    approval_service_url: str = "http://approval-service:8006"
    audit_service_url: str = "http://audit-service:8007"
    rag_service_url: str = "http://rag-service:8008"
    user_service_url: str = "http://user-service:8009"
    workflow_service_url: str = "http://workflow-service:8010"
    request_timeout_seconds: float = 10.0


@lru_cache
def get_settings() -> "Settings":
    return Settings()
