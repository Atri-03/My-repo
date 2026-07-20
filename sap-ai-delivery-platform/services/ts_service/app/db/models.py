"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class TechnicalSpecification(Base):
    __tablename__ = "technical_specification"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    functional_specification_id = Column(String(36), nullable=False, index=True)
    template_id = Column(String(36), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    parent_version_id = Column(String(36), ForeignKey("technical_specification.id"), nullable=True)
    status = Column(String(16), nullable=False, default="DRAFT")
    content = Column(JSON, nullable=False)
    blob_uri = Column(Text, nullable=True)
    regeneration_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

