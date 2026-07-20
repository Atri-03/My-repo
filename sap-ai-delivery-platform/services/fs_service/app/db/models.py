"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class DocumentTemplate(Base):
    __tablename__ = "document_template"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    type = Column(String(8), nullable=False, default="FS")
    name = Column(String(255), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    schema_ = Column("schema", JSON, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FunctionalSpecification(Base):
    __tablename__ = "functional_specification"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    requirement_set_id = Column(String(36), nullable=False, index=True)
    template_id = Column(String(36), ForeignKey("document_template.id"), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    parent_version_id = Column(String(36), ForeignKey("functional_specification.id"), nullable=True)
    status = Column(String(16), nullable=False, default="DRAFT")
    content = Column(JSON, nullable=False)
    blob_uri = Column(Text, nullable=True)
    regeneration_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

