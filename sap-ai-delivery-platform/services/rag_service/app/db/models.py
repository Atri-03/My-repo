"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class KnowledgeSource(Base):
    __tablename__ = "knowledge_source"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_type = Column(String(32), nullable=False)
    uri = Column(Text, nullable=False)
    last_indexed_at = Column(DateTime(timezone=True), nullable=True)
    is_dead_link = Column(Boolean, nullable=False, default=False)


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunk"

    id = Column(String(36), primary_key=True, default=_uuid)
    knowledge_source_id = Column(String(36), ForeignKey("knowledge_source.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    vector_id = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

