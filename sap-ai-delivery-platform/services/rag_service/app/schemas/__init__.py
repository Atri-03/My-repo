"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class KnowledgeSourceCreate(BaseModel):
    tenant_id: str
    source_type: str
    uri: str
    last_indexed_at: Optional[datetime] = None
    is_dead_link: Optional[bool] = False


class KnowledgeSourceUpdate(BaseModel):
    tenant_id: Optional[str] = None
    source_type: Optional[str] = None
    uri: Optional[str] = None
    last_indexed_at: Optional[datetime] = None
    is_dead_link: Optional[bool] = None


class KnowledgeSourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    source_type: str
    uri: str
    last_indexed_at: Optional[datetime] = None
    is_dead_link: Optional[bool] = None


class KnowledgeChunkCreate(BaseModel):
    knowledge_source_id: str
    chunk_index: int
    text: str
    vector_id: str


class KnowledgeChunkUpdate(BaseModel):
    knowledge_source_id: Optional[str] = None
    chunk_index: Optional[int] = None
    text: Optional[str] = None
    vector_id: Optional[str] = None


class KnowledgeChunkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    knowledge_source_id: str
    chunk_index: int
    text: str
    vector_id: str
    created_at: Optional[datetime] = None


