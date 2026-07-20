"""Unit tests for gateway settings."""
from app.core.config import get_settings


def test_settings_defaults():
    settings = get_settings()
    assert settings.service_name == "mcp_gateway_service"
    assert settings.api_v1_prefix == "/api/v1"
    assert settings.rag_service_url.startswith("http")
