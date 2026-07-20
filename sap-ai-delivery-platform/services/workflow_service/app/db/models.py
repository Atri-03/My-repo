"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class WorkflowRun(Base):
    __tablename__ = "workflow_run"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    transcript_id = Column(String(36), nullable=False, index=True)
    current_state = Column(String(64), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


class WorkflowEvent(Base):
    __tablename__ = "workflow_event"

    id = Column(String(36), primary_key=True, default=_uuid)
    workflow_run_id = Column(String(36), ForeignKey("workflow_run.id"), nullable=False, index=True)
    from_state = Column(String(64), nullable=True)
    to_state = Column(String(64), nullable=False)
    actor = Column(String(64), nullable=False)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())

