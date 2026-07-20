"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class AuditLogEntry(Base):
    __tablename__ = "audit_log_entry"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False, index=True)
    entity_id = Column(String(36), nullable=False, index=True)
    action = Column(String(32), nullable=False)
    actor = Column(String(64), nullable=False)
    before = Column(JSON, nullable=True)
    after = Column(JSON, nullable=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())

