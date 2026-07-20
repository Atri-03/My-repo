"""SQLAlchemy ORM models."""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, func

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class ReviewCycle(Base):
    __tablename__ = "review_cycle"

    id = Column(String(36), primary_key=True, default=_uuid)
    tenant_id = Column(String(64), nullable=False, index=True)
    artefact_type = Column(String(32), nullable=False)
    artefact_id = Column(String(36), nullable=False, index=True)
    gate = Column(String(16), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)


class ReviewComment(Base):
    __tablename__ = "review_comment"

    id = Column(String(36), primary_key=True, default=_uuid)
    review_cycle_id = Column(String(36), ForeignKey("review_cycle.id"), nullable=False, index=True)
    reviewer_id = Column(String(64), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

