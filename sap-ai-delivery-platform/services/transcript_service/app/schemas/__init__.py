"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class SourceDocumentCreate(BaseModel):
    tenant_id: str
    project_id: str
    source_type: str
    origin_uri: str
    checksum: str
    blob_uri: str
    ingested_at: Optional[datetime] = None


class SourceDocumentUpdate(BaseModel):
    tenant_id: Optional[str] = None
    project_id: Optional[str] = None
    source_type: Optional[str] = None
    origin_uri: Optional[str] = None
    checksum: Optional[str] = None
    blob_uri: Optional[str] = None
    ingested_at: Optional[datetime] = None


class SourceDocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    project_id: str
    source_type: str
    origin_uri: str
    checksum: str
    blob_uri: str
    ingested_at: Optional[datetime] = None


class TranscriptCreate(BaseModel):
    source_document_id: str
    meeting_date: Optional[datetime] = None
    participants: Optional[list] = Field(default_factory=list)
    parsed_format: str
    raw_text: str
    structured_content: Optional[dict] = None


class TranscriptUpdate(BaseModel):
    source_document_id: Optional[str] = None
    meeting_date: Optional[datetime] = None
    participants: Optional[list] = None
    parsed_format: Optional[str] = None
    raw_text: Optional[str] = None
    structured_content: Optional[dict] = None


class TranscriptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_document_id: str
    meeting_date: Optional[datetime] = None
    participants: Optional[list] = None
    parsed_format: str
    raw_text: str
    structured_content: Optional[dict] = None
    created_at: Optional[datetime] = None


