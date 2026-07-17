"""Centralized application configuration loaded from environment variables.

Copy .env.example to .env and fill in real credentials before running.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Azure OpenAI
    azure_openai_api_key: str = "CHANGEME"
    azure_openai_endpoint: str = "https://your-resource.openai.azure.com/"
    azure_openai_api_version: str = "2024-05-01-preview"
    azure_openai_deployment: str = "gpt-4o"

    # ChromaDB
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection_name: str = "fs_ts_examples"

    # SAP ADT
    adt_base_url: str = "https://your-sap-host:44300"
    adt_sap_client: str = "100"
    adt_auth_mode: str = "basic"
    adt_username: str = "CHANGEME"
    adt_password: str = "CHANGEME"
    adt_target_package: str = "ZRAG_POC"

    # Teams Graph API (not implemented, placeholders only)
    graph_tenant_id: str = ""
    graph_client_id: str = ""
    graph_client_secret: str = ""

    # App
    tracker_db_path: str = "./data/tracker/tracker.json"
    output_dir: str = "./data/output"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
