"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class SourceDocument(Base):
    __tablename__ = "source_document"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), nullable=False, index=True)
    source_type = Column(String(32), nullable=False)
    origin_uri = Column(Text, nullable=False)
    checksum = Column(String(128), nullable=False)
    blob_uri = Column(Text, nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())


class Transcript(Base):
    __tablename__ = "transcript"

    id = Column(String(36), primary_key=True, default=_uuid)
    source_document_id = Column(String(36), ForeignKey("source_document.id"), nullable=False, index=True)
    meeting_date = Column(DateTime(timezone=True), nullable=True)
    participants = Column(JSON, nullable=False, default=list)
    parsed_format = Column(String(32), nullable=False)
    raw_text = Column(Text, nullable=False)
    structured_content = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

